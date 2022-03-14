#!/usr/bin/env python3

from setuptools import find_packages, setup
import sys,os,re
from datetime import datetime
import urllib.parse
from flask import Flask, render_template, render_template_string
from flask_frozen import Freezer
from flask_flatpages import (
    FlatPages, pygmented_markdown, pygments_style_defs)



def prerender_jinja(text):
    """ Pre-renders Jinja templates before markdown. """
    return pygmented_markdown(render_template_string(text))


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

app = Flask(__name__)
app.config.from_object(__name__)
pages = FlatPages(app)
freezer = Freezer(app)

def fix_url(line):
    for url in list(re.compile(r'\[([^\]]+)\]\(([^)]+)\)').findall(line)):
        link,name = url[0],url[1]
        md,tex = f"[{link}]({name})",f"<a href=\"{link}\">{name}</a>"
        line = line.replace(md,tex)
    return line

def setup_latex_url(name, url):
    return f"\href{{{url}}}{{{name}}}"

def setup_google(name):
    return f"https://google.com/search?q={urllib.parse.quote(name)}"

def nice_divide(num):
    return -(int(num) // -2)

def nice_times(num):
    return int(num) * 2

def returnRange(val):
    return list(range(1,int(val)))

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

app.jinja_env.filters['fix_url'] = fix_url
app.jinja_env.filters['setup_latex_url'] = setup_latex_url
app.jinja_env.filters['setup_google'] = setup_google
app.jinja_env.filters['nice_divide'] = nice_divide
app.jinja_env.filters['nice_times'] = nice_times
app.jinja_env.filters['returnRange'] = returnRange

# === URL Routes === #

@app.route('/')
def index():
    page = pages.get_or_404('index')
    return render_template('pages/index.html', page=page, base_info=base_info)


@app.route('/<path:path>/')
def page(path):
    page = pages.get_or_404(path)
    return render_template('pages/page.html', page=page, base_info=base_info)

@app.route('/diagrams')
def diagrams():
    return page_redirect('https://rebrand.ly/graphz')

@app.route('/resume')
def resume_grab():
    return page_redirect('https://rebrand.ly/frantzme_resume')

@app.route('/cv')
def cv_grab():
    return page_redirect('https://rebrand.ly/frantzme_cv')


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

@app.route('/pygments.css')
def pygments_css():
    return pygments_style_defs('tango'), 200, {'Content-Type': 'text/css'}


# === Main function  === #

def arg(string):
    return __name__ == "__main__" and len(
        sys.argv) > 1 and sys.argv[0].endswith('setup.py') and str(sys.argv[1]).upper() == str(string).upper()

if arg('build'):
    freezer.freeze()
    sys.exit(0)
elif arg('run'):
    port = int(sys.argv[2]) if len(sys.argv) >= 2 else 49849
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
