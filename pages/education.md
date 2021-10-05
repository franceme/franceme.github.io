title: education

### Education

<p>
    {%
        set edu = [
            {
                "NAME":"Virginia Polytechnic Institute and State University",
                "DEPT_URL":"https://cs.vt.edu",
                "DEPT_NAME":"cs.vt.edu",
                "TITLE":"Ph.D. Computer Science",
                "FROM":"May 2020",
                "TO":"May 2023",
                "QUOTE":"Ut Prosim, That I May Serve.",
                "TEXT-DESC":[
                    'I have been working under [http://people.cs.vt.edu/danfeng/](Dr. Danfeng Yao) on [https://github.com/franceme/cryptoguard](Cryptoguard) related projects and other static analysis projects.',
                    'I have also been joining various groups (located at the bottom) as well as taking more security oriented courses and enjoying the mountains.',
                ]
            },{
                "NAME":"Virginia Polytechnic Institute and State University",
                "DEPT_URL":"https://cs.vt.edu",
                "DEPT_NAME":"cs.vt.edu",
                "TITLE":"M.S. Computer Science",
                "FROM":"August 2018",
                "TO":"May 2020",
                "QUOTE":"Ut Prosim, That I May Serve.",
                "TEXT-DESC":[
                    'I have been working under [http://people.cs.vt.edu/danfeng/](Dr. Danfeng Yao) on [https://github.com/franceme/cryptoguard](Cryptoguard) related projects and other static analysis projects.',
                    'I have also been joining various groups (located at the bottom) as well as taking more security oriented courses and enjoying the mountains.',
                ]
            },{
                "NAME":"University of Cincinnati",
                "DEPT_URL":"https://ceas.uc.edu",
                "DEPT_NAME":"ceas.uc.edu",
                "TITLE":"B.S. Computer Engineering",
                "FROM":"August 2013",
                "TO":"April 2018",
                "QUOTE":"We Engineer Better.",
                "TEXT-DESC":[
                    'During my Undergraduate I learned alot throughout the classes I took and the Co-Ops I was a part of.',
                    'The Co-Ops were some of the best part of the degree, as it gave me real-world experience, and a chance for practical application.',
                ]
            }
        ]
    %}
    {% for ed in edu %}
    <div class="container education-container">
        <div class="row clearfix layout layout-left">
            <div class="col-xs-12 col-sm-4 col-md-3 col-print-12 details">
                <h4>{{ed['NAME']}}</h4>
                <a href="{{ed['DEPT_URL']}}" target="_blank" class="link">{{ed['DEPT_NAME']}}</a>
                <p><b>{{ed['TITLE']}}</b></p>
                <p>{{ed['FROM']}} - {{ed['TO']}}</p>
                <p class="no-print">
                </p>
            </div>
            <div class="col-xs-12 col-sm-8 col-md-9 col-print-12">
                {% if 'QUOTE' in ed %}
                <p class="quote">{{ed['QUOTE']}}</p>
                {% endif %}
                {% for text in ed['TEXT-DESC'] %}
                    <p>{{text|fix_url|safe}}</p>
                {% endfor %}
            </div>
        </div>
    {% endfor %}
</p>
