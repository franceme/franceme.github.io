title: groups

### Groups

<p>
    <div class="container group-container">
        {%
            set groups = [
                {
                    "NAME":"Graduate Student Council",
                    "WHEN":"2021 to Present",
                    "TITLE":"President",
                    "LINK":"https://csgrad.cs.vt.edu",
                    "NICE_LINK":"csgrad.cs.vt.edu",
                    "TEXT-DESC":[
                        "This group represents the interests of the graduate student body at Virginia Tech and assists within any meetings for the department.",
                        "It also creates events to help enhance the graduate student climate such as fun activities and welcome back meetings."
                    ]
                },{
                    "NAME":"iMentor",
                    "WHEN":"2020",
                    "TITLE":"Slack Admin",
                    "LINK":"https://sites.google.com/vt.edu/imentor/people/staff",
                    "NICE_LINK":"sites.google.com/vt.edu/imentor/people/staff",
                    "TEXT-DESC":[
                        "From the [https://sites.google.com/vt.edu/imentor/home](homepage).",
                        "iMentor focuses squarely on attracting, mentoring, and career advising early-stage graduate students from underrepresented communities who want to pursue a career in computer security.",
                        "Being virtually co-located with the ACM Conference on Computer and Communications Security (ACM CCS) 2020, the workshop provides an opportunity for attendees to also participate in the main conference and benefit from it.",
                        "ACM CCS is a top-tier venue for the quick and wide dissemination of cutting-edge research results in computer and communications security.",
                    ]
                },{
                    "NAME":"Graduate Student Council",
                    "WHEN":"2020 to 2021",
                    "TITLE":"Vice President",
                    "LINK":"https://csgrad.cs.vt.edu",
                    "NICE_LINK":"csgrad.cs.vt.edu",
                    "TEXT-DESC":[
                        "This group represents the interests of the graduate student body at Virginia Tech and assists within any meetings for the department.",
                        "It also creates events to help enhance the graduate student climate such as fun activities and welcome back meetings.",
                        "I have setup the GitHub Organization and the website to autobuild using GitHub Actions."
                    ]
                },{
                    "NAME":"Order of The Engineer",
                    "WHEN":"2018 - Now",
                    "TITLE":"Member",
                    "LINK":"https://order-of-the-engineer.org",
                    "NICE_LINK":"order-of-the-engineer.org",
                    "TEXT-DESC":[
                        "Upholding Devotion to the Standards and Dignity of the Engineering Profession",
                        "This group is a ceremonious group acknowledging members commitments to uphold high qualities and their duty as an engineer."
                    ]
                },
            ]
        %}
        {% for group in groups %}
        <div class="row clearfix layout layout-left">
            <div class="col-xs-12 col-sm-4 col-md-3 col-print-12 details">
                <h4>{{group['NAME']}}</h4>
                <a href="{{group['LINK']}}" target="_blank" class="link">{{group['NICE_LINK']}}</a>
                <p><b>{{group['TITLE']}}</b></p>
                <p>{{group['WHEN']}}</p>
                <p class="no-print">
                </p>
            </div>
            <div class="col-xs-12 col-sm-8 col-md-9 col-print-12">
                {% for text in group['TEXT-DESC'] %}
                    <p>{{text|fix_url|safe}}</p>
                {% endfor %}
            </div>
        </div>
        {% endfor %}
    </div>
</p>
