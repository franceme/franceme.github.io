title: submissions

### Submissions

<p>
    <div class="container submissions-container">
        <h5><i>This material is presented to ensure timely dissemination of scholarly and technical work. Copyright and all rights therein are retained by authors or by other copyright holders. All persons copying this information are expected to adhere to the terms and constraints invoked by each author's copyright. In most cases, these works may not be reposted without the explicit permission of the copyright holder.</i></h5>
        {%
            set sub = [
                {
                    "SHORT_NAME":"Secure Java Tutorial",
                    "SELF_FILE_URL":"https://secdev.ieee.org/2020/accepted/",
                    "CONF_NAME":"SecDev20",
                    "CONF_URL":"https://secdev.ieee.org/2020/accepted/",
                    "RAW_NAME":"Tutorial",
                    "RAW_URL":"https://secdev.ieee.org/2020/accepted/",
                    "DATE":"September 2020",
                    "FULL_NAME":"Tutorial: Principles and Practices of Secure Cryptographic Coding in Java",
                },{
                    "SHORT_NAME":"Enhancing CryptoGuard",
                    "SELF_FILE_URL":"https://rebrand.ly/frantzme_cryptoguard_ccs",
                    "CONF_NAME":"ACM CCS",
                    "CONF_URL":"https://sigsac.org/ccs/CCS2019/",
                    "RAW_NAME":"Conference",
                    "RAW_URL":"https://dl.acm.org/doi/10.1145/3319535.3345659",
                    "DATE":"November 2019",
                    "FULL_NAME":"CryptoGuard: High Precision Detection of Cryptographic Vulnerabilities in Massive-sized Java Projects",
                },{
                    "SHORT_NAME":"Cryptoguard",
                    "SELF_FILE_URL":"https://rebrand.ly/frantzme_ms_thesis",
                    "CONF_NAME":"VT ETDs",
                    "CONF_URL":"https://vtechworks.lib.vt.edu/handle/10919/5534",
                    "RAW_NAME":"Thesis",
                    "RAW_URL":"https://vtechworks.lib.vt.edu/handle/10919/98521",
                    "DATE":"May 2020",
                    "FULL_NAME":"Enhancing CryptoGuard’s Deployability for Continuous Software Security Scanning",
                },{
                    "SHORT_NAME":"Cryptoguard Poster",
                    "SELF_FILE_URL":"https://rebrand.ly/frantzme_cryptoguard_poster",
                    "CONF_NAME":"ACM SIGSAC",
                    "CONF_URL":"https://sigsac.org/ccs.html",
                    "RAW_NAME":"Poster",
                    "RAW_URL":"https://people.cs.vt.edu/nm8247/publications/security-2019-poster.pdf",
                    "DATE":"November 2019",
                    "FULL_NAME":"Deployment-quality and Accessible Solutions for Cryptography Code Development",
                },
            ]
        %}
        {% for paper in sub %}
        <div class="row clearfix layout layout-left">
            <div class="col-xs-12 col-sm-4 col-md-3 col-print-12 details">
                <h4>{{paper['SHORT_NAME']}}</h4>
                <h4>
                    <a target="_blank" href="{{paper['SELF_FILE_URL']}}">
                    <i class="fas fa-file-pdf" title="{{paper['SHORT_NAME']}}" style="font-size:125%;"></i>
                    </a>
                </h4>
                <p><b>
                    <a href="{{paper['CONF_URL']}}" target="_blank" class="link">{{paper['CONF_NAME']}}</a></b>
                </p>
                <p><a href="{{paper['RAW_URL']}}">{{paper['RAW_NAME']}}</a></p>
                <p>{{paper['DATE']}}</p>
                <p class="no-print">
                </p>
            </div>
            <div class="col-xs-12 col-sm-8 col-md-9 col-print-12">
                <p>{{paper['FULL_NAME']}}</p>
            </div>
        </div>
        {% endfor %}
    </div>
</p>
