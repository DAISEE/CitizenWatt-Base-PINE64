% include('_begin.tpl', title='Accueil', page='home')

            <main>
                <div class="left-column">
                    <div class="menu">
                        <h1><img alt="" src="{{ get_url('static', filename='img/data.svg') }}" />Consommation</h1>
                        <a href="{{ get_url('conso') }}">
                            <img alt="" src="{{ get_url('static', filename='img/small-data.svg') }}" />En cours
                        </a>
                        <a href=""><img alt="" src="{{ get_url('static', filename='img/month.svg') }}" />Par mois</a>
                        <a href=""><img alt="More" src="{{ get_url('static', filename='img/more.svg') }}" /></a>
                    </div>

                    <div class="menu">
                        <h1><img alt="" src="{{ get_url('static', filename='img/target.svg') }}" />Objectifs</h1>
                        <a href=""><img alt="" src="{{ get_url('static', filename='img/tick.svg') }}" />Atteints</a>
                        <a href=""><img alt="" src="{{ get_url('static', filename='img/loading.svg') }}" />En cours</a>
                        <a href=""><img alt="More" src="{{ get_url('static', filename='img/more.svg') }}" /></a>
                    </div>
                </div>

                <div class="right-column">
                    <div class="menu">
                        <h1><img alt="" src="{{ get_url('static', filename='img/help.svg') }}" />Guide</h1>
                        <a href="http://wiki.citizenwatt.paris"><img alt="" src="{{ get_url('static', filename='img/wiki.svg') }}" />Wiki</a>
                        <a href=""><img alt="" src="{{ get_url('static', filename='img/contact.svg') }}" />Contact</a>
                        <a href=""><img alt="More" src="{{ get_url('static', filename='img/more.svg') }}" /></a>
                    </div>

                    <div class="menu">
                        <h1><img alt="" src="{{ get_url('static', filename='img/results.svg') }}" />Bilan</h1>
                        <a href=""><img alt="" src="{{ get_url('static', filename='img/bill.svg') }}" />Estimation de facture</a>
                        <a href=""><img alt="" src="{{ get_url('static', filename='img/progress.svg') }}" />Progrès</a>
                        <a href=""><img alt="More" src="{{ get_url('static', filename='img/more.svg') }}" /></a>
                    </div>
                </div>
            </main>

% include('_end.tpl')
