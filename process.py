#!/usr/bin/env python3

import datetime
import json
import os
import stat
import struct
import sys
import time
import random

from libcitizenwatt import database
from libcitizenwatt import tools
from Crypto.Cipher import AES
from libcitizenwatt.config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

filename = "/tmp/sensor.log"

#valeurs seuil et top, je ne sais pas à quoi exactement elles correspondent en terme de grandeur, juste que la valeur (en Watts) dans l'appli CW sera "environ" 10x moins grande
valeur_seuil = 300
valeur_top = 3000

#duree interval en mode seuil (ms)
interval_seuil = 30000
#duree interval en mode top (ms)
interval_top = 30000


def get_rate_type(db):
    """Returns "day" or "night" according to current time
    """
    user = db.query(database.User).filter_by(is_admin=1).first()
    now = datetime.datetime.now()
    now = 3600 * now.hour + 60 * now.minute
    if user is None:
        return -1
    elif user.end_night_rate > user.start_night_rate:
        if now > user.start_night_rate and now < user.end_night_rate:
            return 1
        else:
            return 0
    else:
        if now > user.start_night_rate or now < user.end_night_rate:
            return 1
        else:
            return 0


def get_cw_sensor():
    """Returns the citizenwatt sensor object or None"""
    db = create_session()
    sensor = (db.query(database.Sensor)
              .filter_by(name="CitizenWatt")
              .first())
    db.close()
    return sensor


# Configuration
config = Config()

# DB initialization
database_url = (config.get("database_type") + "://" + config.get("username") +
                ":" + config.get("password") + "@" + config.get("host") + "/" +
                config.get("database"))
engine = create_engine(database_url, echo=config.get("debug"))
create_session = sessionmaker(bind=engine)
database.Base.metadata.create_all(engine)

sensor = get_cw_sensor()
sensor.last_timer = 1475314330
while not sensor or not sensor.aes_key:
    tools.warning("Install is not complete ! " +
                  "Visit http://citizenwatt.local first.")
    time.sleep(1)
    sensor = get_cw_sensor()
    sensor.last_timer = 1475314330

key = json.loads(sensor.aes_key)
key = struct.pack("<16B", *key)

seuil = -1
timer_start = 0
interval_start = 0


#0 en seuil, 1 en top
null_top = 0;




try:
    with open(filename):
        pass
except FileNotFoundError:
    sys.exit("Unable to open file " + filename + ".")

try:
    with open(config.get(filename), 'rb'):
        while True:
        
            FileTemp = open(filename, 'rb')
            measure = FileTemp.read(16)
            print("New encrypted packet:" + str(measure))

            decryptor = AES.new(key, AES.MODE_ECB)
            measure = decryptor.decrypt(measure)
            measure = struct.unpack("<HHHLlH", measure)
            print("New incoming measure:" + str(measure))

            voltage = measure[1]
            battery = measure[2]
            timer = measure[3]
            power = measure[0]
            


            if timer_start == 0:
                timer_start = measure[3]
                interval_start = measure[3]

                            
            if(null_top == 0 and measure[3] - interval_start < interval_seuil):
                power = valeur_seuil + valeur_seuil * 0.1 * random.random()
                print("niveau=" + str(null_top) + " time=" + str(timer) + "  power=" + str(power))
            
            if(null_top == 0 and measure[3] - interval_start >= interval_seuil):
                null_top = 1
                interval_start = measure[3]
                power = valeur_top + valeur_top * 0.1 * random.random()
                print("niveau=" + str(null_top) + " time=" + str(timer) + " power=" + str(power))
                
            if(null_top == 1 and measure[3] - interval_start < interval_top):
                power = valeur_top + valeur_top * 0.1 * random.random()
                print("niveau=" + str(null_top) + " time=" + str(timer) + " power=" + str(power))
                
            if(null_top == 1 and measure[3] - interval_start >= interval_top):
                null_top =0
                interval_start = measure[3]
                power = valeur_top + valeur_top * 0.1 * random.random()
                print("niveau=" + str(null_top) + " time=" + str(timer) + " power=" + str(power))
            
            interval_start = interval_start - 1000

            try:
                db = create_session()
                measure_db = database.Measures(sensor_id=sensor.id,
                                           value=power,
                                           timestamp=datetime.datetime.now().timestamp(),
                                           night_rate=get_rate_type(db))
                db.add(measure_db)
                sensor.last_timer = timer
                (db.query(database.Sensor)
                 .filter_by(name="CitizenWatt")
                 .update({"last_timer": datetime.datetime.now().timestamp()}))
                db.commit()
            except Exception as e:
                print("DB commit failed : " + str(e))
            else:
                print("Saved successfully.")
except KeyboardInterrupt:
    pass
