title: mentees

### Mentees

<p>
    <div class="container mentors-container">
        {%
            set mentees = [
                {
                    "NAME":"UNLISTED",
                    "TITLE":"UNLISTED",
                    "FROM":"08/29/2020",
                    "TO":"01/01/2021",
                    "TEXT-DESC":[
                        "Instructed about assistance on the CryptoGuard Project.",
                        "Helping instruct them on creating an IDE plugin."
                    ]
                },{
                    "NAME":"Jason",
                    "TITLE":"Bachelor in Computer Science",
                    "FROM":"06/08/2020",
                    "TO":"08/22/2020",
                    "TEXT-DESC":[
                        "Instructed about assistance on the CryptoGuard Project.",
                        "Read the proper review [https://docs.google.com/document/d/18Xa6M5ymDyZ-zvPFqN5tAlQuIPqd27nWBdp2pevpytU/edit?usp=sharing](here)."
                    ]
                },{
                    "NAME":"UNLISTED",
                    "TITLE":"UNLISTED",
                    "FROM":"01/22/2020",
                    "TO":"05/30/2020",
                    "TEXT-DESC":[
                        "Help lead them on the Cryptoguard project.",
                        "Help to instruct them on current Java research.",
                    ]
                },{
                    "NAME":"UNLISTED",
                    "TITLE":"UNLISTED",
                    "FROM":"01/09/2017",
                    "TO":"08/12/2017",
                    "TEXT-DESC":[
                        "Instructed them on current project workflows.",
                        "Helped them to build up them Java API skills.",
                    ]
                },{
                    "NAME":"UNLISTED",
                    "TITLE":"UNLISTED",
                    "FROM":"01/09/2017",
                    "TO":"08/12/2017",
                    "TEXT-DESC":[
                        "Instructed them on current project workflows.",
                        "Helped to teach them about the projects within the teams.",
                    ]
                }
            ]
        %}
        {% for mentee in mentees %}
        <div class="row clearfix layout layout-left">
            <div class="col-xs-12 col-sm-4 col-md-3 col-print-12 details">
                <h4>{{mentee['NAME']}}</h4>
                <p><b>{{mentee['TITLE']}}</b></p>
                <p>{{mentee['FROM']}} to {{mentee['TO']}}</p>
                <p class="no-print">
                </p>
            </div>
            <div class="col-xs-12 col-sm-8 col-md-9 col-print-12">
                <ul>
                    {% for item in mentee['TEXT-DESC'] %}
                    <li>{{item|fix_url|safe}}</li>
                    {% endfor %}
                </ul>
            </div>
        </div>
        {% endfor %}
    </div>
</p>