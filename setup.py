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

prerender_jinja = lambda text: pygmented_markdown(render_template_string(text))

base_info = {
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
}

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

# === URL Routes === #

@app.route('/')
def index():
    page = pages.get_or_404('index')
    print('Index', flush=True)
    return Response(get_file('index.html'),mimetype="text/html")
    #return Response(get_file('index.html'),mimetype="text/html") #render_template('pages/index.html', page=page, base_info=base_info)

@app.route('/css/')
def get_css():
    print(f"css ", flush=True)
    page = pages.get_or_404(path)
    return Response(get_file(page,'css'),mimetype="text/css") #render_template('pages/page.html', page=page, base_info=base_info)

@app.route('/path:str/')
def test_route(path):
    print('Hi', flush=True)
    return Response(get_file('index.html'),mimetype="text/html")


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


# === Main function  === #

def arg(string):
    return __name__ == "__main__" and len(
        sys.argv) > 1 and sys.argv[0].endswith('setup.py') and str(sys.argv[1]).upper() == str(string).upper()

if arg('build'):
    freezer.freeze()
    sys.exit(0)
elif arg('run'):
    port = int(sys.argv[2]) if len(sys.argv) >= 2 else 8
    899
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
