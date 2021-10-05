title: projects

### Projects

<p>
    <div class="container projects-container">
    {%
        set projects = [
            {
                "NAME":"franceme.github.io",
                "FROM":"2019",
                "TO":"Present",
                "URL":"https://github.com/franceme/franceme.github.io",
                "RELEASES_RSS":True,
                "ACTIONS_URL":True,
                "GITUB_PAGE":False,
                "TEXT-DESC":[
                    "This is my ‘now and again’ public website.",
                    "I’ve used the same framework to generate the static website, and I have migrated the build to GitHub actions to ensure public transparency.",
                    "I only made it public after hiding some of the web content since the build for the website is activated AFTER the Resume repo is complete.",
                    "This was a neat trick that allows the Website to automatically download and host the most recent documents, as well as load the most recent web content (since this website used yml files that were created from the Resume Repo)."
                ],
            },{
                "NAME":"WaveNetExploration",
                "FROM":"2019",
                "TO":"2019",
                "URL":"https://github.com/franceme/WaveNetExploration",
                "RELEASES_RSS":True,
                "ACTIONS_URL":False,
                "GITUB_PAGE":True,
                "TEXT-DESC":[
                    "This was a class project created for an Advanced Machine Learning class.",
                    "The purpose of this project was to replicate an existing papers work and to add onto it.",
                    "For this my group chose to replicate the paper [https://arxiv.org/pdf/1609.03499.pdf](WaveNet) and to enhance the results by running it on music samples.",
                    "Unfortunately we were unable to create any sound samples that mimic actual music, however from the website there is a clear improvement in the music generation from the models."
                ],
            },{
                "NAME":"GradleGuard",
                "FROM":"2019",
                "TO":"2020",
                "URL":"https://github.com/franceme/gradleguard",
                "RELEASES_RSS":True,
                "ACTIONS_URL":False,
                "GITUB_PAGE":False,
                "TEXT-DESC":[
                    "This is the gradle plugin for my thesis project Cryptoguard.",
                    "This was created to help ease the access and use for developers to be able to use Cryptoguard.",
                ],
            },{
                "NAME":"MavenGuard",
                "FROM":"BASE",
                "TO":"BASE",
                "URL":"https://github.com/franceme/mavenguard",
                "RELEASES_RSS":True,
                "ACTIONS_URL":True,
                "GITUB_PAGE":False,
                "TEXT-DESC":[
                    "This is the maven plugin for my thesis project Cryptoguard.",
                    "This was created to help ease the access and use for developers to be able to use Cryptoguard.",
                ],
            },{
                "NAME":"CryptoGuard",
                "FROM":"2019",
                "TO":"Now",
                "URL":"https://github.com/franceme/cryptoguard",
                "RELEASES_RSS":True,
                "ACTIONS_URL":False,
                "GITUB_PAGE":True,
                "TEXT-DESC":[
                    "This is a static and compiled code analyzer, serving as my current thesis project.",
                    "This project will scan cryptographic misuse in Java Projects (Maven/Gradle based) and Android Projects.",
                    "Recent works with this project have included making an enhanced interface for this to work with other programs and tools.",
                ],
            }
        ]
    %}
        {% for proj in projects %}
        <div class="row clearfix layout layout-left">
            <div class="col-xs-12 col-sm-4 col-md-3 col-print-12 details">
                <h4>{{proj['NAME']}}</h4>
                <p>{{proj['FROM']}} to {{proj['TO']}}</p>
                <p class="no-print">
                    <a href="{{proj['URL']}}" target="_blank">
                    <i class="fa fa-github" style="font-size:225%;" title="{{proj['NAME']}} Github Link"></i>
                    </a>
                    {% if proj['GITUB_PAGE'] %}
                    <a href="https://franceme.github.io/{{proj['NAME']}}/" target="_blank">
                    <i class="fab fa-internet-explorer" style="font-size:225%;" title="{{proj['NAME']}} Github Page link"></i>
                    </a>
                    {% endif %}
                    {% if proj['RELEASES_RSS'] %}
                    <a href="{{proj['URL']}}/releases.atom" target="_blank">
                    <i class="fas fa-rss" style="font-size:225%;" title="{{proj['NAME']}} RSS Link"></i>
                    </a>
                    {% endif %}
                    {% if proj['ACTIONS_URL'] %}
                    <a href="{{proj['URL']}}/actions" target="_blank">
                    <i class="fas fa-wrench" style="font-size:225%;" title="{{proj['NAME']}} GitHub Actions"></i>
                    {% endif %}
                    </a>
                </p>
            </div>
            <div class="col-xs-12 col-sm-8 col-md-9 col-print-12">
                {% for text in proj['TEXT-DESC'] %}
                <p>{{text|fix_url|safe}}</p>
                {% endfor %}
            </div>
        </div>
        {% endfor %}
    </div>
</p>