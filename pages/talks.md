title: talks

### Talks

<p>
    <div class="container group-container">
        {%
            set talks = [
                {
                    "NAME":"Esorics 2021 Demo",
                    "URL":"https://esorics2021.athene-center.de/tutorial-09-08.php",
		    "NOTEBOOK_URL":"https://mybinder.org/v2/gh/franceme/Esorics_Conference/HEAD",
                },{
                    "NAME":"Course SQL Injection Demo",
                    "YOUTUBE_URL":"rLY2skQTeJE"
                },{
                    "NAME":"Course Project Demo",
                    "YOUTUBE_URL":"wU5VFDHc11s"
                },{
                    "NAME":"SecDev 2020 Tutorial",
                    "YOUTUBE_URL":"42Qw06OrjwM",
		    "NOTEBOOK_URL":"https://mybinder.org/v2/gh/franceme/cryptoguard/2020_SecDev_Tutorial?filepath=SecDev_Tutorial.ipynb"
                },
            ]
        %}
        {% for talk in talks %}
        <div style="padding-left:25%;" class="row clearfix layout">
            <div class="col-xs-12 col-sm-4 col-md-3 col-print-12 details">
                <h4>{{talk['NAME']}}</h4>{%- if 'NOTEBOOK_URL' in talk %}
		<h4>
                    <a target="_blank" href="{{talk['NOTEBOOK_URL']}}">
                    <i class="fas fa-book" title="Live Jupyter Notebook" style="font-size:125%;"></i>
                    </a>
                </h4>
		{% endif %}
                {% if 'YOUTUBE_URL' in talk %}
                <iframe width="420" height="315" src="https://www.youtube-nocookie.com/embed/{{talk['YOUTUBE_URL']}}"
                    frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
                {% endif %}
                {% if 'URL' in talk %}
                <a href="{{talk['URL']}}" target="_blank" class="link">{{talk['URL']}}</a>
                {% endif %}
                <p class="no-print">
                </p>
            </div>
        </div>
        {% endfor %}
    </div>
</p>
