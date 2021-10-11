title:skills

### Skills

<p>
    <div class="container skills-container">
        {%
            set skills = [
                {
                        "NAME":"Java EE",
                        "NUMPROJ":14,
                        "LINK":"openjdk.java.net",
                        "FROM":"2015",
                        "TO":"Now",
                        "PERCENT":90,
                        "TYPE":"lang"
                },
                {
                        "NAME":"Soap Webservices",
                        "NUMPROJ":8,
                        "LINK":null,
                        "FROM":"2015",
                        "TO":"Now",
                        "PERCENT":75,
                        "TYPE":"projectType"
                },
                {
                        "NAME":"Rest Webservices",
                        "NUMPROJ":3,
                        "LINK":null,
                        "FROM":"2017",
                        "TO":"Now",
                        "PERCENT":65,
                        "TYPE":"projectType"
                },
                {
                        "NAME":"Machine Learning",
                        "NUMPROJ":2,
                        "LINK":null,
                        "FROM":"2019",
                        "TO":"Now",
                        "PERCENT":40,
                        "TYPE":"projectType"
                },
                {
                        "NAME":"Maven",
                        "NUMPROJ":10,
                        "LINK":"maven.apache.org",
                        "FROM":"2015",
                        "TO":"Now",
                        "PERCENT":85,
                        "TYPE":"framework"
                },
                {
                        "NAME":"Gradle",
                        "NUMPROJ":2,
                        "LINK":"gradle.org",
                        "FROM":"2019",
                        "TO":"Now",
                        "PERCENT":65,
                        "TYPE":"framework"
                },
                {
                        "NAME":"Python3",
                        "NUMPROJ":13,
                        "LINK":"python.org",
                        "FROM":"2016",
                        "TO":"Now",
                        "PERCENT":95,
                        "TYPE":"lang"
                },
                {
                        "NAME":"Rust",
                        "NUMPROJ":1,
                        "LINK":"rust-lang.org",
                        "FROM":"2021",
                        "TO":"Now",
                        "PERCENT":20,
                        "TYPE":"lang"
                },
                {
                        "NAME":"Bash Scripts",
                        "NUMPROJ":7,
                        "LINK":null,
                        "FROM":"2017",
                        "TO":"Now",
                        "PERCENT":50,
                        "TYPE":"lang"
                },
                {
                        "NAME":"Tasktop Integrations",
                        "NUMPROJ":3,
                        "LINK":"tasktop.com",
                        "FROM":"2019",
                        "TO":"2019",
                        "PERCENT":85,
                        "TYPE":"lang"
                },
                {
                        "NAME":"Linux",
                        "NUMPROJ":null,
                        "LINK":null,
                        "FROM":"2017",
                        "TO":"Now",
                        "PERCENT":60,
                        "TYPE":"OS"
                },
                {
                        "NAME":"Spring",
                        "NUMPROJ":3,
                        "LINK":"spring.io",
                        "FROM":"2015",
                        "TO":"Now",
                        "PERCENT":50,
                        "TYPE":"framework"
                },
                {
                        "NAME":"C#",
                        "NUMPROJ":3,
                        "LINK":"docs.microsoft.com/en-us/dotnet/csharp",
                        "FROM":"2017",
                        "TO":"Now",
                        "PERCENT":25,
                        "TYPE":"lang"
                },
                {
                        "NAME":"Flask",
                        "NUMPROJ":2,
                        "LINK":"fullstackpython.com/flask.html",
                        "FROM":"2017",
                        "TO":"Now",
                        "PERCENT":25,
                        "TYPE":"framework"
                },
                {
                        "NAME":"Jenkins",
                        "NUMPROJ":3,
                        "LINK":"jenkins.io",
                        "FROM":"2017",
                        "TO":"Now",
                        "PERCENT":50,
                        "TYPE":"framework"
                },
                {
                        "NAME":"Mako",
                        "NUMPROJ":1,
                        "LINK":"makotemplates.org",
                        "FROM":"2018",
                        "TO":"Now",
                        "PERCENT":40,
                        "TYPE":"framework"
                },
                {
                        "NAME":"Tensorflow",
                        "NUMPROJ":2,
                        "LINK":"tensorflow.org",
                        "FROM":"2019",
                        "TO":"Now",
                        "PERCENT":30,
                        "TYPE":"framework"
                },
                {
                        "NAME":"HTML",
                        "NUMPROJ":3,
                        "LINK":null,
                        "FROM":"2015",
                        "TO":"Now",
                        "PERCENT":50,
                        "TYPE":"lang"
                },
                {
                        "NAME":"SQL",
                        "NUMPROJ":6,
                        "LINK":null,
                        "FROM":"2015",
                        "TO":"Now",
                        "PERCENT":65,
                        "TYPE":"lang"
                },
                {
                        "NAME":".NET",
                        "NUMPROJ":1,
                        "LINK":"microsoft.com/net",
                        "FROM":"2018",
                        "TO":"Now",
                        "PERCENT":25,
                        "TYPE":"lang"
                },
                {
                        "NAME":"GO",
                        "NUMPROJ":1,
                        "LINK":"golang.org",
                        "FROM":"2019",
                        "TO":"Now",
                        "PERCENT":40,
                        "TYPE":"lang"
                },
                {
                        "NAME":"Scala",
                        "NUMPROJ":2,
                        "LINK":"scala-lang.org",
                        "FROM":"2018",
                        "TO":"Now",
                        "PERCENT":65,
                        "TYPE":"lang"
                },
                {
                        "NAME":"Agile/SAFE",
                        "NUMPROJ":null,
                        "LINK":null,
                        "FROM":"2015",
                        "TO":"Now",
                        "PERCENT":70,
                        "TYPE":"Methodology"
                },
                {
                        "NAME":"Scrum",
                        "NUMPROJ":null,
                        "LINK":null,
                        "FROM":"2015",
                        "TO":"Now",
                        "PERCENT":60,
                        "TYPE":"Methodology"
                },
                {
                        "NAME":"C++",
                        "NUMPROJ":1,
                        "LINK":"isocpp.org",
                        "FROM":"2014",
                        "TO":"2015",
                        "PERCENT":1,
                        "TYPE":"lang"
                },
                {
                        "NAME":"JavaScript",
                        "NUMPROJ":2,
                        "LINK":null,
                        "FROM":"2017",
                        "TO":"Now",
                        "PERCENT":15,
                        "TYPE":"lang"
                }
            ]
        %}
    <div style="width:100%;display:inline-block;">
        {% for skill in skills %}
            {% if loop.index | int % 2 == 0 %}
                <div style="width:50%;float:left;" class="progress-container">
                    {% if skill['LINK'] == null %}
                        <h4>{{ skill['NAME'] }} ~ {{ skill['PERCENT'] }}% Mastery</h4>
                    {% else %}
                        <h4><a href="https://{{ skill['LINK'] }}">{{ skill['NAME'] }} ~ {{ skill['PERCENT'] }}% Mastery</a></h4>
                    {% endif %}
                    <br>
                    <p>
                    {% if skill['PROEJCTS'] != null and skill['PROJECTS'] != "None" and skill['PROJECTS'] != "" %}
                        <b>Number of Projects:{{ skill['PROJECTS'] }}</b>
                    {% else %}
                        <b></b>
                    {% endif %}
                    <br>
                    </p>
                   <p>{{ skill['FROM'] }} to {{skill['TO']}}</p>
                    <div class="progress">
                        <progress style="background:rgba(0, 0, 179, .45);color:rgba(0, 0, 179, .45);width:100%;height:100%;" value="{{ skill['PERCENT'] }}" max="100"></progress>
                    </div>
                </div>
            {% else %}
                <div style="display:inline-block;width:50%;" class="progress-container">
                    {% if skill['LINK'] == null %}
                        <h4>{{ skill['NAME'] }} ~ {{ skill['PERCENT'] }}% Mastery</h4>
                    {% else %}
                        <h4><a href="https://{{ skill['LINK'] }}">{{ skill['NAME'] }} ~ {{ skill['PERCENT'] }}% Mastery</a></h4>
                    {% endif %}
                    <br>
                    <p>
                    {% if skill['PROJECTS'] != null and skill['PROJECTS'] != "None" and skill['PROJECTS'] != "" %}
                        <b>Number of Projects:{{ skill['PROJECTS'] }}</b>
                    {% else %}
                        <b></b>
                    {% endif %}
                    <br>
                    </p>
                    <p>{{ skill['FROM'] }} to {{skill['TO']}}</p>
                    <div class="progress">
                        <progress style="background:rgba(0, 0, 179, .45);color:rgba(0, 0, 179, .45);width:100%;height:100%;" value="{{ skill['PERCENT'] }}" max="100"></progress>
                    </div>
                </div>
            {% endif %}
        {% endfor %}
        <div style="clear:both;"></div>
    </div>
    </div>
</p>
