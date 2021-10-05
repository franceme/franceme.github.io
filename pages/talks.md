title: talks

### Talks

<p>
    <div class="container group-container">
        {%
            set talks = [
                {
                    "NAME":"Esorics 2021 Demo",
                    "URL":"https://esorics2021.athene-center.de/tutorial-09-08.php"
                },{
                    "NAME":"Course SQL Injection Demo",
                    "YOUTUBE_URL":"rLY2skQTeJE"
                },{
                    "NAME":"Course Project Demo",
                    "YOUTUBE_URL":"wU5VFDHc11s"
                },{
                    "NAME":"SecDev 202 Tutorial",
                    "YOUTUBE_URL":"42Qw06OrjwM"
                },
            ]
        %}
        {% for talk in talks %}
        <div class="row clearfix layout layout-left">
            <div class="col-xs-12 col-sm-4 col-md-3 col-print-12 details">
                <h4>{{talk['NAME']}}</h4>
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