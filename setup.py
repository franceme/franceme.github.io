#!/usr/bin/env python3

from setuptools import find_packages, setup
import sys,os,re
from datetime import datetime
import urllib.parse

try:
    from flask import Flask, render_template, render_template_string,Response
    from flask_frozen import Freezer
    from flask_flatpages import (
        FlatPages, pygmented_markdown, pygments_style_defs)
except:
    for x in [
            'flask==2.0.1',
            'flask_flatpages==0.7.3',
            'frozen_flask==0.18',
            'pygments==2.10.0',
            'elsa==0.1.6'
        ]:
        os.system(str(sys.executable) + " -m pip install " + str(x))

    from flask import Flask, render_template, render_template_string,Response
    from flask_frozen import Freezer
    from flask_flatpages import (
        FlatPages, pygmented_markdown, pygments_style_defs)


base_info = {
    'name':"Miles Frantz",
    'title':"Cyber Security Ph.D. Student",
    'NAME':"Miles Frantz",
    'EMAIL':"g00qhtdbp@relay.firefox.com",#"frantzme@vt.edu",
    'GITHUB':"franceme",
    'DOCKER':"frantzme",
    'RESUME':'https://rebrand.ly/frantzme_resume',
    'CV':'https://rebrand.ly/frantzme_cv',
    'GITHUB_USERNAME': 'franceme',
    'LINKEDIN_USERNAME': 'franceme',
    'SCHOLAR_USERNAME': 'RKKj9VgAAAAJ',
    #'MENDELEY_USERNAME': 'myles-f',
    #'ieee': 'MilesFrantz662182',
    #'acm': 'here',
    #'MEDIUM': 'frantzme',
    'ORCID': '0000-0002-7329-6979',
    'ZENODO': '3701552',
    'WEBSITE': 'franceme.github.io',
    'LINKEDIN': 'frantzme',
    # 'phone': '513-480-3169',
    "show_edu":True,
    "show_exp":True,
    "show_proj":True,
    "show_grp":True,
    "show_ment":True,
    "show_sub":True,
    "show_talks":True,
    "show_skills":True
}

#https://stackoverflow.com/questions/20646822/how-to-serve-static-files-in-flask
def get_file(filename, base=None):  # pragma: no cover
    try:
        if base:
            src = os.path.join(base,filename)
        else:
            src = filename
        # Figure out how flask returns static files
        # Tried:
        # - render_template
        # - send_file
        # This should not be so non-obvious
        return open(src).read()
    except IOError as exc:
        return str(exc)

prerender_jinja = lambda text: pygmented_markdown(render_template_string(text))
rendre = lambda page:render_template_string(get_file(page),mimetype="text/html",dyct=base_info)
rendre_string = lambda page:render_template_string(page,mimetype="text/html",dyct=base_info)

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'
FLATPAGES_HTML_RENDERER = prerender_jinja
FLATPAGES_MARKDOWN_EXTENSIONS = ['codehilite']
FREEZER_IGNORE_MIMETYPE_WARNINGS = True

app = Flask(
    __name__,
    static_url_path='',
    static_folder='static',
)
app.config.from_object(__name__)
pages = FlatPages(app)
freezer = Freezer(app)

def page_redirect(url):
    return f"""<!DOCTYPE HTML>
<html lang="en-US">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="refresh" content="0; url={url}">
        <script type="text/javascript">
             window.location.href = "{url}"
        </script>
        <title>Page Redirection</title>
    </head>
    <body>
        If you are not redirected automatically, follow this <a href='{url}'>link to example</a>.
    </body>
</html>
""", 200, {'Content-Type':'text/html'}


# === URL Routes === #

@app.route('/')
def index():
    for x in ['show_skills','show_ment']:
        base_info[x] = False
    return rendre('index.html')

@app.route('/research')
def research():
    for x in ['show_skills','show_exp','show_grp']:
        base_info[x] = False
    return rendre('index.html')

@app.route('/industry')
def industry():
    for x in ['show_edu','show_talks','show_sub']:
        base_info[x] = False
    return rendre('index.html')

@app.route('/full')
def full():
    for x in ["show_edu",    "show_exp",    "show_proj",    "show_grp",    "show_ment",    "show_sub",    "show_talks",    "show_skills"]:
        base_info[x] = True
    return rendre('index.html')

"""
@app.route('/css/<page>')
def get_css(page):
    print(f"css ", flush=True)
    return Response(get_file(page,'css'),mimetype="text/css") #render_template('pages/page.html', page=page, base_info=base_info)

@app.route('/path:str/')
def test_route(path):
    print('Hi', flush=True)
    return Response(get_file('index.html'),mimetype="text/html")
"""


@app.route('/diagrams.html')
def diagrams():
    return page_redirect('https://rebrand.ly/graphz')

@app.route('/resume.html')
def resume_grab():
    return page_redirect('https://rebrand.ly/frantzme_resume')

@app.route('/cv.html')
def cv_grab():
    return page_redirect('https://rebrand.ly/frantzme_cv')

@app.route('/sok.html')
def sok_grab():
    return page_redirect('https://oaklandsok.github.io')

@app.route('/security.txt')
def security():
    return f"""
# Miles Frantz Website
Contact: mailto:{base_info['EMAIL']}
Preferred-Languages: en
Expires: 2025-12-31T18:00:00.000Z
""", 200, {'Content-Type':'text/plain'}


@app.route('/robots.txt')
def robots():
    return f"""
# robots.txt - for Miles Frantz Website

User-agent: *
Disallow: /
""", 200, {'Content-Type':'text/plain'}

@app.route('/qr.html')
def qr_grab():
    return rendre_string("""
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" shape-rendering="crispEdges" viewBox="0 0 100 100"><rect x="0" y="0" height="10" width="10" fill="#FFF"/><rect x="0" y="0" height="1" width="7" fill="#000"/><rect x="11" y="0" height="3" width="1" fill="#000"/><rect x="16" y="0" height="1" width="2" fill="#000"/><rect x="19" y="0" height="1" width="4" fill="#000"/><rect x="24" y="0" height="4" width="1" fill="#000"/><rect x="26" y="0" height="1" width="7" fill="#000"/><rect x="0" y="1" height="6" width="1" fill="#000"/><rect x="6" y="1" height="6" width="1" fill="#000"/><rect x="10" y="1" height="3" width="1" fill="#000"/><rect x="13" y="1" height="3" width="1" fill="#000"/><rect x="15" y="1" height="1" width="2" fill="#000"/><rect x="18" y="1" height="4" width="1" fill="#000"/><rect x="20" y="1" height="1" width="1" fill="#000"/><rect x="22" y="1" height="3" width="1" fill="#000"/><rect x="26" y="1" height="6" width="1" fill="#000"/><rect x="32" y="1" height="6" width="1" fill="#000"/><rect x="2" y="2" height="3" width="3" fill="#000"/><rect x="8" y="2" height="2" width="2" fill="#000"/><rect x="12" y="2" height="1" width="1" fill="#000"/><rect x="15" y="2" height="2" width="1" fill="#000"/><rect x="17" y="2" height="2" width="1" fill="#000"/><rect x="19" y="2" height="1" width="1" fill="#000"/><rect x="21" y="2" height="3" width="1" fill="#000"/><rect x="23" y="2" height="3" width="1" fill="#000"/><rect x="28" y="2" height="3" width="3" fill="#000"/><rect x="14" y="3" height="4" width="1" fill="#000"/><rect x="16" y="3" height="2" width="1" fill="#000"/><rect x="12" y="4" height="1" width="1" fill="#000"/><rect x="19" y="4" height="2" width="1" fill="#000"/><rect x="9" y="5" height="1" width="2" fill="#000"/><rect x="13" y="5" height="1" width="1" fill="#000"/><rect x="15" y="5" height="1" width="1" fill="#000"/><rect x="17" y="5" height="1" width="1" fill="#000"/><rect x="20" y="5" height="2" width="1" fill="#000"/><rect x="24" y="5" height="2" width="1" fill="#000"/><rect x="1" y="6" height="1" width="5" fill="#000"/><rect x="8" y="6" height="1" width="1" fill="#000"/><rect x="10" y="6" height="1" width="1" fill="#000"/><rect x="12" y="6" height="2" width="1" fill="#000"/><rect x="16" y="6" height="1" width="1" fill="#000"/><rect x="18" y="6" height="1" width="1" fill="#000"/><rect x="22" y="6" height="1" width="1" fill="#000"/><rect x="27" y="6" height="1" width="5" fill="#000"/><rect x="11" y="7" height="4" width="1" fill="#000"/><rect x="19" y="7" height="4" width="1" fill="#000"/><rect x="23" y="7" height="4" width="1" fill="#000"/><rect x="3" y="8" height="4" width="2" fill="#000"/><rect x="6" y="8" height="1" width="2" fill="#000"/><rect x="10" y="8" height="2" width="1" fill="#000"/><rect x="29" y="8" height="1" width="2" fill="#000"/><rect x="1" y="9" height="1" width="1" fill="#000"/><rect x="5" y="9" height="1" width="1" fill="#000"/><rect x="8" y="9" height="2" width="1" fill="#000"/><rect x="12" y="9" height="1" width="2" fill="#000"/><rect x="15" y="9" height="1" width="2" fill="#000"/><rect x="25" y="9" height="1" width="1" fill="#000"/><rect x="27" y="9" height="1" width="2" fill="#000"/><rect x="6" y="10" height="1" width="1" fill="#000"/><rect x="9" y="10" height="4" width="1" fill="#000"/><rect x="12" y="10" height="1" width="1" fill="#000"/><rect x="15" y="10" height="1" width="1" fill="#000"/><rect x="17" y="10" height="1" width="1" fill="#000"/><rect x="21" y="10" height="1" width="1" fill="#000"/><rect x="24" y="10" height="1" width="1" fill="#000"/><rect x="26" y="10" height="2" width="2" fill="#000"/><rect x="30" y="10" height="1" width="3" fill="#000"/><rect x="0" y="11" height="7" width="1" fill="#000"/><rect x="2" y="11" height="1" width="1" fill="#000"/><rect x="5" y="11" height="1" width="1" fill="#000"/><rect x="13" y="11" height="1" width="1" fill="#000"/><rect x="18" y="11" height="1" width="1" fill="#000"/><rect x="28" y="11" height="1" width="3" fill="#000"/><rect x="32" y="11" height="2" width="1" fill="#000"/><rect x="1" y="12" height="3" width="1" fill="#000"/><rect x="3" y="12" height="1" width="1" fill="#000"/><rect x="6" y="12" height="1" width="1" fill="#000"/><rect x="11" y="12" height="1" width="2" fill="#000"/><rect x="16" y="12" height="1" width="1" fill="#000"/><rect x="19" y="12" height="1" width="4" fill="#000"/><rect x="24" y="12" height="1" width="1" fill="#000"/><rect x="26" y="12" height="1" width="1" fill="#000"/><rect x="28" y="12" height="1" width="2" fill="#000"/><rect x="31" y="12" height="2" width="1" fill="#000"/><rect x="4" y="13" height="3" width="1" fill="#000"/><rect x="7" y="13" height="1" width="2" fill="#000"/><rect x="12" y="13" height="1" width="3" fill="#000"/><rect x="19" y="13" height="1" width="1" fill="#000"/><rect x="21" y="13" height="1" width="3" fill="#000"/><rect x="25" y="13" height="2" width="1" fill="#000"/><rect x="29" y="13" height="2" width="2" fill="#000"/><rect x="5" y="14" height="1" width="3" fill="#000"/><rect x="10" y="14" height="1" width="1" fill="#000"/><rect x="13" y="14" height="1" width="2" fill="#000"/><rect x="16" y="14" height="2" width="1" fill="#000"/><rect x="18" y="14" height="2" width="1" fill="#000"/><rect x="24" y="14" height="1" width="1" fill="#000"/><rect x="28" y="14" height="4" width="1" fill="#000"/><rect x="7" y="15" height="1" width="3" fill="#000"/><rect x="15" y="15" height="2" width="1" fill="#000"/><rect x="17" y="15" height="1" width="1" fill="#000"/><rect x="23" y="15" height="1" width="1" fill="#000"/><rect x="30" y="15" height="1" width="2" fill="#000"/><rect x="1" y="16" height="1" width="3" fill="#000"/><rect x="6" y="16" height="1" width="1" fill="#000"/><rect x="9" y="16" height="2" width="2" fill="#000"/><rect x="12" y="16" height="2" width="1" fill="#000"/><rect x="25" y="16" height="1" width="2" fill="#000"/><rect x="29" y="16" height="1" width="2" fill="#000"/><rect x="2" y="17" height="1" width="4" fill="#000"/><rect x="14" y="17" height="1" width="1" fill="#000"/><rect x="16" y="17" height="1" width="1" fill="#000"/><rect x="18" y="17" height="1" width="1" fill="#000"/><rect x="20" y="17" height="1" width="3" fill="#000"/><rect x="24" y="17" height="1" width="1" fill="#000"/><rect x="26" y="17" height="1" width="2" fill="#000"/><rect x="29" y="17" height="5" width="1" fill="#000"/><rect x="32" y="17" height="4" width="1" fill="#000"/><rect x="1" y="18" height="1" width="1" fill="#000"/><rect x="3" y="18" height="3" width="2" fill="#000"/><rect x="6" y="18" height="1" width="1" fill="#000"/><rect x="9" y="18" height="2" width="1" fill="#000"/><rect x="15" y="18" height="1" width="1" fill="#000"/><rect x="23" y="18" height="2" width="1" fill="#000"/><rect x="27" y="18" height="2" width="1" fill="#000"/><rect x="30" y="18" height="2" width="1" fill="#000"/><rect x="0" y="19" height="6" width="1" fill="#000"/><rect x="2" y="19" height="1" width="1" fill="#000"/><rect x="5" y="19" height="1" width="1" fill="#000"/><rect x="7" y="19" height="2" width="1" fill="#000"/><rect x="12" y="19" height="1" width="3" fill="#000"/><rect x="16" y="19" height="1" width="1" fill="#000"/><rect x="18" y="19" height="1" width="3" fill="#000"/><rect x="24" y="19" height="1" width="2" fill="#000"/><rect x="6" y="20" height="1" width="1" fill="#000"/><rect x="8" y="20" height="1" width="1" fill="#000"/><rect x="10" y="20" height="1" width="1" fill="#000"/><rect x="12" y="20" height="2" width="1" fill="#000"/><rect x="14" y="20" height="3" width="2" fill="#000"/><rect x="26" y="20" height="3" width="1" fill="#000"/><rect x="1" y="21" height="1" width="2" fill="#000"/><rect x="9" y="21" height="1" width="1" fill="#000"/><rect x="13" y="21" height="2" width="1" fill="#000"/><rect x="18" y="21" height="1" width="5" fill="#000"/><rect x="24" y="21" height="1" width="1" fill="#000"/><rect x="27" y="21" height="2" width="2" fill="#000"/><rect x="30" y="21" height="2" width="2" fill="#000"/><rect x="2" y="22" height="1" width="2" fill="#000"/><rect x="5" y="22" height="1" width="2" fill="#000"/><rect x="8" y="22" height="1" width="1" fill="#000"/><rect x="11" y="22" height="1" width="1" fill="#000"/><rect x="16" y="22" height="4" width="1" fill="#000"/><rect x="18" y="22" height="1" width="2" fill="#000"/><rect x="23" y="22" height="3" width="1" fill="#000"/><rect x="32" y="22" height="1" width="1" fill="#000"/><rect x="4" y="23" height="1" width="1" fill="#000"/><rect x="10" y="23" height="1" width="1" fill="#000"/><rect x="12" y="23" height="1" width="1" fill="#000"/><rect x="17" y="23" height="2" width="1" fill="#000"/><rect x="20" y="23" height="4" width="1" fill="#000"/><rect x="22" y="23" height="1" width="1" fill="#000"/><rect x="24" y="23" height="8" width="1" fill="#000"/><rect x="28" y="23" height="6" width="1" fill="#000"/><rect x="30" y="23" height="1" width="1" fill="#000"/><rect x="1" y="24" height="1" width="2" fill="#000"/><rect x="5" y="24" height="1" width="5" fill="#000"/><rect x="13" y="24" height="1" width="1" fill="#000"/><rect x="19" y="24" height="1" width="1" fill="#000"/><rect x="25" y="24" height="1" width="3" fill="#000"/><rect x="29" y="24" height="5" width="1" fill="#000"/><rect x="8" y="25" height="2" width="4" fill="#000"/><rect x="15" y="25" height="3" width="1" fill="#000"/><rect x="18" y="25" height="1" width="1" fill="#000"/><rect x="21" y="25" height="1" width="1" fill="#000"/><rect x="0" y="26" height="1" width="7" fill="#000"/><rect x="12" y="26" height="2" width="1" fill="#000"/><rect x="23" y="26" height="3" width="1" fill="#000"/><rect x="26" y="26" height="1" width="1" fill="#000"/><rect x="0" y="27" height="6" width="1" fill="#000"/><rect x="6" y="27" height="6" width="1" fill="#000"/><rect x="11" y="27" height="4" width="1" fill="#000"/><rect x="13" y="27" height="2" width="2" fill="#000"/><rect x="17" y="27" height="1" width="3" fill="#000"/><rect x="21" y="27" height="3" width="2" fill="#000"/><rect x="30" y="27" height="1" width="2" fill="#000"/><rect x="2" y="28" height="3" width="3" fill="#000"/><rect x="8" y="28" height="1" width="3" fill="#000"/><rect x="16" y="28" height="1" width="2" fill="#000"/><rect x="20" y="28" height="1" width="1" fill="#000"/><rect x="25" y="28" height="1" width="3" fill="#000"/><rect x="31" y="28" height="4" width="1" fill="#000"/><rect x="8" y="29" height="1" width="2" fill="#000"/><rect x="12" y="29" height="2" width="1" fill="#000"/><rect x="17" y="29" height="1" width="3" fill="#000"/><rect x="25" y="29" height="1" width="1" fill="#000"/><rect x="27" y="29" height="1" width="1" fill="#000"/><rect x="10" y="30" height="1" width="1" fill="#000"/><rect x="14" y="30" height="1" width="4" fill="#000"/><rect x="19" y="30" height="1" width="2" fill="#000"/><rect x="23" y="30" height="1" width="1" fill="#000"/><rect x="28" y="30" height="1" width="2" fill="#000"/><rect x="32" y="30" height="2" width="1" fill="#000"/><rect x="9" y="31" height="2" width="1" fill="#000"/><rect x="13" y="31" height="2" width="2" fill="#000"/><rect x="17" y="31" height="1" width="2" fill="#000"/><rect x="20" y="31" height="2" width="1" fill="#000"/><rect x="22" y="31" height="1" width="1" fill="#000"/><rect x="25" y="31" height="1" width="2" fill="#000"/><rect x="29" y="31" height="1" width="1" fill="#000"/><rect x="1" y="32" height="1" width="5" fill="#000"/><rect x="10" y="32" height="1" width="1" fill="#000"/><rect x="12" y="32" height="1" width="1" fill="#000"/><rect x="15" y="32" height="1" width="1" fill="#000"/><rect x="23" y="32" height="1" width="2" fill="#000"/><rect x="28" y="32" height="1" width="1" fill="#000"/><rect x="30" y="32" height="1" width="1" fill="#000"/></svg>
""".strip())


# === Main function  === #
def get_skill(name,amount, isLeft=True):
    ranking = "No Experience"
    if amount == 0:
        ranking = "No Experience"
    if amount >= 25:
        ranking = "Beginner"
    if amount >= 50:
        ranking = "Journeyman"
    if amount >= 75:
        ranking = "Expert"
    if amount >= 100:
        ranking = "Master"

    klass = "bg-info" if isLeft else "bg-secondary"

    return render_template_string(f"""
<div class="mb-3"><span class="fw-bolder">{name}</span>
    <div class="progress my-2 rounded" style="height: 20px">
        <div class="progress-bar {klass}" role="progressbar" data-aos="zoom-in-right" data-aos-delay="100" data-aos-anchor=".skills-section" style="width: {amount}%;" aria-valuenow="{amount}" aria-valuemin="0" aria-valuemax="100">{ranking}</div>
    </div>
</div>
""")

app.jinja_env.filters['get_skill'] = get_skill

def get_base(title,co_name, _from,_to,desc, is_info=True,color=None):

    base_color = "timeline-card-info" if is_info else "timeline-card-success"

    if color is not None:
        color = "timeline-card-" + color

    return render_template_string(f"""
<div class="timeline-card {color or base_color}" data-aos="fade-in" data-aos-delay="0" {color}>
    <div class="timeline-head px-4 pt-3">
    <div class="h5">{title} <span class="text-muted h6">at {co_name}</span></div>
    </div>
    <div class="timeline-body px-4 pb-4">
    <div class="text-muted text-small mb-3">{_from} - {_to}</div>
    <div>{desc}</div>
    </div>
</div>
""")

app.jinja_env.filters['get_base'] = get_base

def get_ref(name, title, desc,left_side=True):

    side = "timeline-card-info" if left_side else "timeline-card-success"

    return render_template_string(f"""
          <div class="d-flex mb-2">
            <div class="avatar"><img src="images/reference-image-1.jpg" width="60" height="60"/></div>
            <div class="header-bio m-3 mb-0">
              <h3 class="h6 mb-1" data-aos="fade-left" data-aos-delay="0">{name}</h3>
              <p class="text-muted text-small" data-aos="fade-left" data-aos-delay="100">{title}</p>
            </div>
          </div>
          <div class="d-flex"><i class="text-secondary fas fa-quote-left"></i>
            <p class="lead mx-2" data-aos="fade-left" data-aos-delay="100">{desc}</p>
          </div>
""")

app.jinja_env.filters['get_ref'] = get_ref

def get_main_url(page_name):
    page_name = str(page_name)
    return render_template_string(f""" <a href="/{page_name.lower()}">{page_name.title()}</a> """)

app.jinja_env.filters['get_main_url'] = get_main_url

def arg(string):
    return __name__ == "__main__" and len(
        sys.argv) > 1 and sys.argv[0].endswith('setup.py') and str(sys.argv[1]).upper() == str(string).upper()

if arg('build'):
    freezer.freeze()
    sys.exit(0)
elif arg('run'):
    port = int(sys.argv[2]) if len(sys.argv) >= 2 else 8899
    app.run(host='0.0.0.0', port=port)
    sys.exit(0)
elif arg('install'):
    sys.exit(os.system('python3 -m pip install -e .'))
elif __name__ == '__main__':
    from elsa import cli
    sys.exit(cli(app, base_url='https://franceme.github.io'))


setup(name='My Website',
        version='0.0.0',
        description='Python Website',
        author='Miles Frantz',
        author_email='frantzme@vt.edu',
        url='',
        packages=find_packages(),
        install_requires=[
            'flask==2.0.1',
            'flask_flatpages==0.7.3',
            'frozen_flask==0.18',
            'pygments==2.10.0',
            'elsa==0.1.6'
        ]
)
