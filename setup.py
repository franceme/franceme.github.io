#!/usr/bin/env python3
from setuptools import find_packages, setup
import sys,os, base64

try:
    from flask import Flask, render_template_string, make_response
    from mystring import string as str
    from flask_frozen import Freezer
    from flask_flatpages import (
        FlatPages, pygmented_markdown)
    from feedgen.feed import FeedGenerator
except:
    for x in [
            'requests',
            'flask==3.0.1',
            'flask_flatpages==0.7.3',
            'frozen_flask==1.0.1',
            'pygments==2.10.0',
            'feedgen==0.9.0',
            'elsa==0.1.6',
            'werkzeug==3.0.0'
        ]:
        os.system(str(sys.executable) + " -m pip install " + str(x))
    from flask import Flask, render_template_string, make_response
    from flask_frozen import Freezer
    from flask_flatpages import (FlatPages, pygmented_markdown)
    from feedgen.feed import FeedGenerator


base_info = {
    'name':"Miles Frantz",
    'title':"Cyber Security Ph.D. Student",
    'NAME':"Miles Frantz",
    'EMAIL':"codeanalysis@vt.edu",
    'GITHUB':"franceme",
    'DOCKER':"frantzme",
    'RESUME':'https://drive.google.com/file/d/1wq_hU272QvwmW1Cj1on7MaufEvGxzA7C/view?usp=drive_link',
    'CV':'https://drive.google.com/file/d/18qCa6lW4718-tTrpE5_H5Nr0s6ssG5Na/view?usp=drive_link',
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
    "show_skills":True,
    "show_docker":True,
    "show_consult":True,
    "show_path":True,
    "show_utils":True
}

#https://stackoverflow.com/questions/20646822/how-to-serve-static-files-in-flask
def get_file(filename, base=None):  # pragma: no cover
    try:
        if base:
            src = os.path.join(base,filename)
        else:
            src = filename
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

#https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types
def easy_add_page(contents, contenttype='text/html',pullcontent=False):
    if not pullcontent or not os.path.exists(contents):
        return contents, 200, {'Content-Type':contenttype}

    raw_contents = None
    with open(contents,'r') as reader:
        raw_contents = reader.readlines()

    if contents.endswith(".csv"): #Hard Test
        output = make_response(raw_contents)
        output.headers["Content-Disposition"] = "attachment; filename=export.csv"
        output.headers["Content-type"] = "text/csv"
        return output

    return '\n'.join(raw_contents), 200, {'Content-Type':contenttype}

def easy_add_file(file):
    return easy_add_page(open(file).read())

def add_secure_pages(pagepaths):
    from fileinput import FileInput as finput
    with finput(__file__, inplace=True, backup=False) as file:
        for line in file:
            if line.startswith("#Add Secure Pages Here"):
                print(line)
                for pagepath in pagepaths:
                    if pagepath.endswith('.html') or pagepath.endswith('.htm'):
                        secure_page_name = str(pagepath.split("/")[-1]).replace('.html','').replace("*","")
                        print(f"""
@app.route('/secure_{secure_page_name}.html')
def secure_get_{secure_page_name}():
    return easy_add_file('{pagepath}')
""")
                    else:
                        secure_page_name = str(pagepath.split("/")[-1])#.split('.')[0]
                        pull_content=any([secure_page_name.endswith("."+str(x)) for x in [
                            'py','java','rs','csv','json','xml',
                        ]])
                        print(f"""
@app.route('/secure_{secure_page_name.split('.')[0]}.html')
def secure_get_{secure_page_name.split('.')[0]}():
    return easy_add_page('{pagepath}','text/plain',pullcontent={pull_content})
""")
            else:
                print(line, end='')

# === URL Routes === #

@app.route('/')
@app.route('/index.html')
def index():
    for x in base_info.keys():
        if x.startswith('show_'):
            base_info[x] = True

    for x in ['show_skills','show_ment']:
        base_info[x] = False
    return rendre('index.html')

@app.route('/research.html')
def research():
    for x in base_info.keys():
        if x.startswith('show_'):
            base_info[x] = True

    for x in ['show_skills','show_exp','show_grp','show_docker']:
        base_info[x] = False
    return rendre('index.html')

@app.route('/industry.html')
def industry():
    for x in base_info.keys():
        if x.startswith('show_'):
            base_info[x] = True

    for x in ['show_edu','show_talks','show_sub',"show_utils"]:
        base_info[x] = False
    return rendre('index.html')

@app.route('/uful')
def redirect_uful():
    return page_redirect('https://franceme.github.io/secure_useful.html#staticrypt_pwd=9befb4c4a149223bca56d9db353cd4fecf576f24105dd10ee3f929942f06ad35')

@app.route('/frac.html')
def fracpage():
    return rendre('frac.html')

@app.route('/frac')
def fracpage_one():
    return fracpage()

@app.route('/full.html')
def full():
    for x in base_info.keys():
        if x.startswith('show_'):
            base_info[x] = True
    return rendre('index.html')

@app.route('/full')
def full_one():
    return full()

@app.route('/resume.html')
def resume_grab():
    return page_redirect(base_info["RESUME"])

@app.route('/resume')
def resume_grab_one():
    return resume_grab()

@app.route('/cv.html')
def cv_grab():
    return page_redirect(base_info["CV"])

@app.route('/cv')
def cv_grab_one():
    return cv_grab()

@app.route('/sok.html')
def sok_grab():
    return page_redirect('https://oaklandsok.github.io')

@app.route('/sok')
def sok_grab_one():
    return sok_grab()

@app.route('/365')
def vt_microsoft_redirect():
    return page_redirect('https://login.microsoftonline.com/?whr=virginiatech.onmicrosoft.com')

@app.route('/scheduling')
def vt_schedule():
    return page_redirect('https://outlook.office.com/findtime/dashboard')

@app.route('/paperss')
def paperRss():
    """
    # https://www.reddit.com/r/flask/comments/evjcc5/question_on_how_to_generate_a_rss_feed/
    # https://github.com/lkiesow/python-feedgen
    """
    fg = FeedGenerator()
    fg.title('Faper rss feed')
    fg.description('A feed of paper news pulled from the email')
    fg.link(href="https://franceme.github.io/paperss")

    foil = 'paperss.jsonl'
    if os.path.exists(foil):

        import json
        content = []
        with open(foil, 'r') as reader:
            for line in reader.readlines():
                try:
                    content += [json.loads(line)]
                except:
                    pass

        for article in content:
            fe = fg.add_entry()
            fe.title(article['Title'])
            link = article['Link'].replace('https://franceme.github.io/','').replace('<','').replace('>','')
            fe.link(href=link)
            fe.description(article['Content'].replace('Twitter] ;LinkedIn] Facebook]','').replace('"',"'"))
            fe.guid(link, permalink=True)
            fe.author(name=article['AuthorName'], email=article['AuthorEmail'])
            if article['PubDate'] != "":
                fe.pubDate(article['PubDate'])

    response = make_response(fg.rss_str())
    response.headers.set('Content-Type', 'application/rss+xml')
    return response

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
    svg = open('static/images/VCard.svg').read()
    return svg, 200, {'Content-Type':'image/svg+xml'}

#Add Redirect Pages Here

@app.route('/mtimeline')
def redirect_mtimeline():
    return page_redirect('https://franceme.github.io/secure_timeline.html#staticrypt_pwd=fbeb482b15be779fdafecdb47d48313870b7b6f5610ed0b87dd1176fbb430ad6')

@app.route('/dtimeline')
def redirect_dtimeline():
    return page_redirect('https://franceme.github.io/secure_timeline.html#staticrypt_pwd=b29f188f689c4cee0e1de17286305e0bea933d1e02177ae6db16a006654d4b8c')

@app.route('/2m31fhi')
def redirect_2m31fhi():
    return page_redirect('https://franceme.github.io/secure_timeline.html')

@app.route('/mioi0d8')
def redirect_mioi0d8():
    return page_redirect('https://franceme.github.io/secure_timeline.html')

@app.route('/1feo9lx')
def redirect_1feo9lx():
    return page_redirect('https://franceme.github.io/secure_timeline.html')

@app.route('/qscala2')
def redirect_qscala2():
    return page_redirect('https://notebooks.gesis.org/binder/jupyter/user/almond-sh-examples-tc0zflur/lab')

@app.route('/qscala')
def redirect_qscala():
    return page_redirect('https://www.tutorialspoint.com/scala/scala_quick_guide.htm')

@app.route('/vmale')
def redirect_vmale():
    return page_redirect('https://outlook.office.com/mail/')

@app.route('/pyprep')
def redirect_pyprep():
    return page_redirect('https://raw.githubusercontent.com/franceme/staticpy/master/prep.py')

@app.route('/mstack')
def redirect_mstack():
    return page_redirect('https://docs.google.com/document/d/1bt9hEam01J51zpytdwCZs0VWcjfs0UZk/edit')

@app.route('/peratonlabs')
def redirect_peratonlabs():
    return page_redirect('https://www.google.com/maps/place/Peraton Labs/@40.6949202,-74.5729342,19.33z/data=!4m14!1m7!3m6!1s0x89c3bd6b0abcaa13:0x81d4713a9198a366!2s150 Mt Airy Rd RM. 2S-115, Basking Ridge, NJ 07920!3b1!8m2!3d40.6949992!4d-74.5726182!3m5!1s0x89c3bd6bc4408817:0x569dc120652bd12!8m2!3d40.6948905!4d-74.57275!16s/g/11x9btjyk?entry=ttu')

@app.route('/pyup')
def redirect_pyup():
    return page_redirect('https://raw.githubusercontent.com/franceme/staticpy/master/up.py')

@app.route('/pyfollow')
def redirect_pyfollow():
    return page_redirect('https://raw.githubusercontent.com/franceme/staticpy/master/follow.py')

@app.route('/pymux')
def redirect_pymux():
    return page_redirect('https://raw.githubusercontent.com/franceme/staticpy/master/mux.py')

@app.route('/balget')
def redirect_balget():
    return page_redirect('https://raw.githubusercontent.com/franceme/staticpy/master/bal_install.sh')

@app.route('/qaONE')
def redirect_qaONE():
    return page_redirect('https://www.plantuml.com/plantuml/svg/LO_13S8m34NldiBolGSMG9s07LBNg16DKnndVumg89mIlo__9y_DatalEt0jHrLHnoNfOnmjAM-GsAiXz-QrY45ivNimz8XRV79Lu6oy2rBN_Eo2cehG5wPrDMdj1uuj1AYzB684yDOYNGYdwOfqeuyOplV4O_CG3EqZ_3VCecjS-W80')

@app.route('/pptr')
def redirect_pptr():
    return page_redirect('https://www.plantuml.com/plantuml/svg/RL9DQzj04BtdL-obeSLCDawB71TC7QWRScdT3mWb137MZgHDjJloxifo_dqdaWMbxKKypS3xUBFhc30aPxrns9xDr3Pm5T2ftgRQUdKl2-xLw-tsXxenXlsRizdiD8q2P-hXeKwfZU-rxll-ufcxrEteec2dUqn5_U6m-fpTtbV7pS7kDkhdk5UR8xgseSV7Cm1rPmYZ052VcYub2YyO_c0MZyKlFb0e6-u7xdr7CLdsKMVBj_EhnMMcQ-uXCP3RaG4w2et7HW11QHkAO3qWbAC0j86Vg4XGSe1-JAE-tWns0FxAL35NpHWf4WR9j5-TU5vTNOREotVI4zYE3GeQEnGmAfnRMdMfXEjpda3HMF9fLTf09HzX1tDmwlRxeFAl6KV6TcumidvYB6hhN8lUu78nfM-myqKDneQNTEWvrP8MsnRAm0xaF67gO9YQkK5ybrqlIihKtPTHKtt4aFxNH21ZR1eC16qmf0PzfUNNIOgeutwVFI-rDEAjh_Afa_pKICojpyLFlfDhLe4xR_A3HQs-3RIYlIPlJa_nDm00')

@app.route('/pycmtr')
def redirect_pycmtr():
    return page_redirect('https://raw.githubusercontent.com/franceme/staticpy/master/cmt.py')

@app.route('/GTAhours')
def redirect_GTAhours():
    return page_redirect('https://calendar.google.com/calendar/u/0?cid=Y19lODBmZDlkMmE2NGQ0YjNkZTkyNGIxM2I2MDI5NmRjNGQzYjIwNDk3YTgwMjVjNTNhMmQxYTg3M2NhYWRhNGRhQGdyb3VwLmNhbGVuZGFyLmdvb2dsZS5jb20')

@app.route('/pyscriptBadge')
def redirect_pyscriptBadge():
    return page_redirect('https://github.com/franceme/py_scripts/actions/workflows/builder.yml/badge.svg')

@app.route('/confs')
def redirect_confs():
    return page_redirect('https://www.plantuml.com/plantuml/svg/VPHVQzim5CNV-oak3FOGiDLaBsLFzTnq69eiJ1aRb59K-SOMioIZApVrjv_yPwiRPys3aQFpE_SSsVYQl71UAvDhKLyi8BNcW0wDHBfOBE3-llI-_ipOGSYcycqiAVP2Dp7c3IiQUq352EMZ3DXZiF9nwJLmb8rJldru21uBs2jqi0pBgU7nU8mL8aOqYcFh2hPF6Tz5cSdnfNEgW7_S1PSvIgeW8Nj6IXgqQShVQcaKDuH6lGpYrtxigJL28rjUNi4FljvclyxJ9YUAgDMr9TNetWMsDvnFswtEH1JoRq98KfxEQjJeJrntwpt_NrjfzQ32PpIUcD8oUYq3sMOouDqZJldjpoC-CGYBiS9NDEX4TQvyhlIp6DBTTClv4TMjVJeq9EEGC5HeVMaDVEl_4Xvpa3R7S34UoVSqS7lmH-4GrgPG1j4fKroyDPqyfiwtRZowFeMI5APaATy4hoaphIl5S5Iho-KL-r0xMpYXWQV97Ee6nGu9XPFbC8BGAIIcYBo0ZFDzCgCQYXnXhsueh5QV67pdww2B8aYoS8rWSmS7wy1XRRlxQ88hMRbOob3ZhaF2x_r4fTN8DBbeTRbQmeQxWJfvqf8mcfvR84FyT4WrdM1KJTtuRRRZu-Ru1fncwNo546fuSLwzMP8a6UjtwhA6xcvUH4bT3IqtOqsu4Lvmz7GgDTYu8TIRALrTbeggkhMkGocWNy9MgONxJR0Tg7-kymYrin8nLwQWU39Z93lW6aq-Vlt-0000')

@app.route('/xpiz')
def redirect_xpiz():
    return page_redirect('https://raw.githubusercontent.com/franceme/staticpy/master/xpizr.py')

@app.route('/drumpf')
def redirect_drumpf():
    return page_redirect('https://www.politico.com/interactives/2023/trump-criminal-investigations-cases-tracker-list/')

@app.route('/cryptograde')
def redirect_cryptograde():
    return page_redirect('https://drive.google.com/file/d/1X8MSjJmc7qQ_kd4d3U_CogYw81nzFY3_/view?usp=sharing')

@app.route('/farsi')
def redirect_farsi():
    return page_redirect('https://www.plantuml.com/plantuml/svg/ZPFHRzem4CRV-rVugIyeyRfAAvl4McZfDgaCHYkaKLN8n9VuEiVsx2CP--iNd81Q7gO--hlxVT_bJhaA93oLQ6Gft4cFtGeVaDs1y0PDSTBhiGSlJD22q9hGl7liyL4HkV29S-fAa1RM5XhIp9RyCkW1c5FIWroSMZSuDB6nAJG6nPBFRSpJqv7Vipmxl-Yd1PBQh5Eqt47J9an2Dd7OqhnbeqadlV9fRC9ML2AeE8spdeJcU_fzleDvPaq5dgoF7lyVQWtAG8KXse7XRq0aPhjr2RzDOruQCcMjvkpcK8WCkzcjvJeE4nhzoAQkwvH4eIeiOtWtDNZE7bhvE3aYw8N9b2ZNu5jCQ31I-1VyhWM5MUrBgqCfTShj3zMkDadO77BmO388pIjv-Q4UgrV7pr43b_oCzAG_lBl8t7Iaho_Mj3AabeZrkr7oS_jdrESLGdsv2MuGBOBynHRWrsnY9UO8FkQ-AMdYxFrORrOBkPmz3_zEFsRBBrytszlptxCFkFenZKbi14JWsKnPicpHACSHtUuyI8aK0poVZUVttuRVEPj7jG6kmCZkN_a7')

@app.route('/ondock')
def redirect_ondock():
    return page_redirect('https://www.plantuml.com/plantuml/svg/SoWkIImgoStCIybDBE3IKd39JyvEBUBIqbA8ZiueAIaejjBNpqbCAjOho4cir2tFBCdGJG4hqKlEpzLNyC_BoSnBZOr5rL2UcPsfbvXJ09G2IfTMwEKNfOC5zI76ApY2vHHA2r8IIq2w7LBpKg1k0000')

@app.route('/myne')
def redirect_myne():
    return page_redirect('https://github.com/franceme/cryptoguard4py/tree/reorg')

@app.route('/pyez')
def redirect_pyez():
    return page_redirect('https://raw.githubusercontent.com/franceme/staticpy/master/ezgit.py')

@app.route('/pyshark')
def redirect_pyshark():
    return page_redirect('https://raw.githubusercontent.com/franceme/staticpy/master/shark.py')

@app.route('/pydockinstall')
def redirect_pydockinstall():
    return page_redirect('https://raw.githubusercontent.com/franceme/staticpy/master/in_docker.py')

@app.route('/gsync')
def redirect_gsync():
    return page_redirect('https://raw.githubusercontent.com/franceme/staticpy/master/gsync.py')

@app.route('/toturkey')
def redirect_toturkey():
    return page_redirect('https://virginiatech-my.sharepoint.com/personal/frantzme_vt_edu/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Ffrantzme%5Fvt%5Fedu%2FDocuments%2FPersonal%2FTurkey%2FFlightItenerary%2Epdf&parent=%2Fpersonal%2Ffrantzme%5Fvt%5Fedu%2FDocuments%2FPersonal%2FTurkey')

@app.route('/vscod')
def redirect_vscod():
    return page_redirect('https://www.plantuml.com/plantuml/svg/jPJ1Qjmm48RlUGf1ZujMXD8IUWejf9SKbhhq4a8PIsElch56QCRR-kqhkuRWDe4KjXTZQUJl_tuCkXQ5eaDCOO1yiJDV6_E10ve3ZNrC5xkTQM38L3SAVqUlKhTsvkxkg9hbdNDzrEFOxZqFReY-i72dxYI-CcoUA2PrMX3T036vTao1C3Xb9dEORklq_hu2pqDq9FcRO3bXsUV9R5OrvkKfBO5_i1sN0LInF5VW_Nni1f-9VFuYKRYeQudR9_INuOpxHzx_bku87l3gEUkRPJe3pqJSUh-wlNnpzPUyjUOpTbWmUPIwigR9w9St-xG3Pqm4FoYs1ShayjIJcCFqyRQfkErdZxxx5H3P4QH-X1xjRmsR2olxQYirE7RHWqPEibtQr_RohLlSQiesf60rIM5Fqr9OfunYlipFzUYdvaylpm7tfoWZaEWO8Y_D84S7uGJ9Ox3AENgfzVHOu_6dOf9PH77818gLQXg5eclh5_wmHv101LNJcv5elObcuMjCORspVW40')

@app.route('/dulles')
def redirect_dulles():
    return page_redirect('https://www.google.com/maps/place/Dulles+International+Airport/@38.9522806,-77.4604559,17z/data=!3m1!4b1!4m6!3m5!1s0x89b64740174eb057:0x8e01cb201080601d!8m2!3d38.9522765!4d-77.457881!16zL20vMDg0MmI')

@app.route('/to_qr')
def redirect_to_qr():
    return page_redirect('https://demos.hankruiger.com/kuu_er/')

@app.route('/on_qr')
def redirect_on_qr():
    return page_redirect('https://faizrktm.github.io/barcode-reader-wasm/')

@app.route('/pyvb')
def redirect_pyvb():
    return page_redirect('https://raw.githubusercontent.com/franceme/staticpy/master/vb.py')

@app.route('/userstudy')
def redirect_userstudy():
    return page_redirect('https://www.plantuml.com/plantuml/uml/XP31JeOm48JlVOhrv15-C9vv10BnH3YiC16qrAQxbV3s8h69DIPUUfcPxsks4UMWB-nKpPqks40RbAtnONKg4rlG3hpPmxJX_HMJqhKGgiggBig7ubQReGtm741FWa2znlaOKutrtoRS_AFtMDnACtJHPHtBeaBrzHV9urpsb-5UlXpd2XyhTkeWqQeaQ9MWUPn1V_aIi8_FswhKiaSOQM7luRu76IiDclEvRlq9')

@app.route('/rechrome')
def redirect_rechrome():
    return page_redirect('https://remotedesktop.google.com/access')

@app.route('/lsp_types')
def redirect_lsp_types():
    return page_redirect('https://github.com/microsoft/lsprotocol/blob/main/packages/python/lsprotocol/types.py#L11420')

@app.route('/sshak')
def redirect_sshak():
    return page_redirect('https://virginiatech-my.sharepoint.com/:p:/g/personal/sdavari_vt_edu/ET0-rkKaKlNMtVny5heNQJwBXMbYp-yPH2WcNNeBxRUozA?rtime=rTAN8SE820g')

@app.route('/gtan')
def redirect_gtan():
    return page_redirect('https://www.plantuml.com/plantuml/svg/ZP9DYy8m48Rl_ehSIvj-rBhkoKL13tjpOGyYCcr2EslpGIQrVtzRrose5oyP23pFl7d9YZmuhr0B1NOMiEtNnom8sEvxECUHZ3DWXqFZlQLtpYlG5w3euYCfEbwPpf4adXJp-JpdG8IrLbBxuMgH5yaYOUihS3m-Ylg-Zse7Gb9bh8mgeoPRlYpYkBYpfSLRbiLBxkG5PN_w0zbs7FkHV_RNw9kkl7gXRx0w4r_lmsmHv-4-pNZPcf8hGCrFBPJynqASH4gmBVfTLxBD4CkXzMZqe0x35nkulPPzeZvFt7EWAOXrgEimZTFiV_6w1I9dZ7h4bMYYQbehW9hIW1DiWuCOMhO3BIRcrOxl6rn9BMvVuHS0')

@app.route('/progression')
def redirect_progression():
    return page_redirect('https://www.plantuml.com/plantuml/svg/dPN1Sjem48RlVehjgIUmC2GbjoGbwUJ038LsSc1os845gmZ9bUHG-lILFIprU6GVSk72_t-VTj68U-VH-ZrgxvDFFgSZGOwR0zcai59xjq55yBiC6RBgd2oi-KKR3tNBGIP6qrJSfcAK30Om7ww6C1WawrUqnx80R-2hFHVUV0lzxHkNWgLHx4oJtZQpqogRh9zqZdeZzJwAHWyTkC-k0hRwKLacKZ59HoB8NhIdlKKlZGQf0t7r-Z1Vj0UvknokCnw5Xtqjyk7iiZ1Z3s3qvKogHhGqcM1DDDoItANPD0omf7VfA8v53r4KhuhB4Gtwof9LesIJe7cM6fNysorYLjJ3xMxJE1NZDBi9faVfNOwM73oJKkRaSbcq5nNIDs5HyN2BozTgOQa8IVZfoCBAbzjp-CJDeJa47pG-HWz2eGk4MpWH7LnSzh9y_B2A0IoQNaKFHM7DEohO6TjdY_DOruTXvoYxIfUbxdF5VXGsSJSYc32_lafqQiPcwB7fw3qmg-8Orl4u_szd8zbqTN5O4wlppjXnVGhcKf7pHfEhNuNwFVsHavCEPhGZxUWDSYmAqhMxyPoilvT1ivF1yVG7Z-tOA1LPAhxKDqV9ezHepz7WkEQDatM7Rr9zFnP9SX-cg_yr_W40')

@app.route('/rnoqw')
def redirect_rnoqw():
    return page_redirect('https://www.plantuml.com/plantuml/svg/lLPhRzku4lsUNq7W0XSf2bdlXme4QUmaJjAaUJX9hriKneWSsMmaKI7fX_lhBosvXTURPDD5T-KF4gcPSsRc34T-hpH8NVAAbL3ll2LVlaoqhjKxsuQwxb2eWNBDKNMui6aARfXvkUNw3AmWPDI2nAKMHUf3xD0mS78R88wzE0ChZyFC2cWIMwcNefLI6liiIE88Ot8bnJUaMdtzklFst-F4Wfj4GIuRsarU9gZgZ8KO5zYXehHhYGeh3PgBocQswuJgw7BIlviVw-x7WxJ7lY_ge3wOtVFIxsQ3lesCQp8eECCs9uD-j82oBb2PrQ-HtVpF6oPNnmj8rR5t6iq_NqQFf_YO3J-d9PyuYs-ztb2DZeV7tM7BsvLO2KFxgqJN4sjvVNsNf9Ruc1xCBxHtDOJn-StHX_lb6IruYpw41leVATW4f55aBSSLr2XtjeXG6Hu9R0eQ5Pq8KNHckeDiQjSmHcNVSvolAjsf9pNf6qCoQApMSZSg_53au9ISO56JNQucR_wKqdm-xzIh42p63R9kycg38eDfMOBatr4QhASSwGHqpVBMfsSMPCxrX00nYCyxYQf2gf4rHchj_6EpfVxPJeFdkado6MvAaVC26ma61-Fvuq9F-GtSLLQ_-wat6ushIQHcXui5hUsPATt-LDLxoiY0eu9N3qRiTU4CxQkPkcT7paqlIwAnJEV3q-LrOOLduzcYlZpl7vsFt2UPrjh_3Rg-o0vExigRWiwoiJgJLVVZSN7HlNku5OFFxWVhERe7dcrbHxgezNBD_4botVJVLXnZNeqV1DHr4uIv_oSAl2ZqVG-2X4Q9u-SU1cw04Rb5fOrr0sNk3SiJkeiPoWAXxPQw7OLsv7leW0z9H1saMKHTweQOKtAvjduARMoQR9fr6CxiN495iKHxOywHFjSdqumSucpRspYxNjnnpCzzbwHkQE_dec0ezsorh2Yv7_pq63tb4gM-OnUGxMlnWDKUynClTrcGnq2J27mdYDoKPcuQfe4NOnP6PZU1A6IfusHvJ2phR5elDSfpo2phf_ndgBiIUAN88MXu8UJONFkLq0EaKucVG5Qcu7iv50h9rR9dX6z4VY7d98dtIv7n0l_x3Cv5y_R5oiK6PgCChXlwAOlzD8JOOn66kSz27ptqGl0ZOuk96_kOvDJnl31YP5q4W_1YkPjqJStMcJK5iomptBI47nzJSeDAJ2L5PLvP6qqIPHqiSAedA3l0pKWJ6YlDeI0NqqBpfcjHxZUGctvr0JeNiko86YlWJRUkvhvT2eQ58fTcUpLJBvfbwxuzJtcD1Q-mvLqlZ4z3jcaiCPDGiKwnjEiIwlNi8reGoZMsrfS5M-ytJ3svhBKeca_EQiDwrIbpc8DXx6H-24dk1qcGf16wG5oNxDuEZioapqgkbC5yqx2Qwo_Ec-kEDaCPdHaHAYZ-UFPU7P_BQ1I1au2NErdYWXDu43W1SIAoUoLMGcs5-FhCFS_nVJHp9ainJ1A4rC3dn83ldbPy6_QryMPnIccAZXjbOU36YKSZ1Z6v693TjYpzAKZMGZQ7Mg5MP7VmM72DRxPuMBOgBnSsEUoUD4-jtotI2JdW31lx0Ufcp6wMdLoWbfogxNfCfkFL0C-1eWdSPki06ldqToFVLFD2sLaXChi4NjbNIpqHrUfzYID5eIfRu4wz91jB4zTlPMfXLoJjq-_6DwPKI5mHhEu6VkSzLcpzn___')

@app.route('/pmap')
def redirect_pmap():
    return page_redirect('https://www.mindmeister.com/map/2667079025')


@app.route('/audible')
def redirect_audible():
    return page_redirect('https://www.audible.com/webplayer?asin=B06X3QQTFH&contentDeliveryType=MultiPartBook&ref_=a_minerva_cloudplayer_B06X3QQTFH&overrideLph=false&initialCPLaunch=true')

@app.route('/motivate')
def redirect_motivate():
    return page_redirect('https://homeforfiction.com/apps/locked/quoteJux/')

@app.route('/dcap')
def redirect_dcap():
    return page_redirect('https://app.capacities.io/c9a15b2f-13da-45dc-a81c-cec3a70c540f/154e5043-6462-48f6-b49f-b133bec368b6')

@app.route('/frantzme_frac_hashsha_example_00')
def redirect_frantzme_frac_hashsha_example_00():
    return page_redirect('https://franceme.github.io/frac.html?code=from%20hashlib%20import%20sha1%0Ainsecure_value%20=%20sha1(%22My%20Password%22).hexdigest()%0Aprint(insecure_value)')

@app.route('/cchef')
def redirect_cchef():
    return page_redirect('https://gchq.github.io/CyberChef/')

@app.route('/frantzme_frac')
def redirect_frantzme_frac():
    return page_redirect('https://franceme.github.io/frac.html')

@app.route('/wordle')
def redirect_wordle():
    return page_redirect('https://www.nytimes.com/games/wordle/index.html')

@app.route('/rsch_defense')
def rsch_defense():
    return page_redirect('https://virginiatech.zoom.us/j/87373440937?pwd=MGppYWNxanNiZXdRanc1TUZMdXdIdz09')

@app.route('/final_defense')
def final_defense():
    return page_redirect('https://virginiatech.zoom.us/j/83512572602?pwd=OHY1MysxNVB6eWV0dTJqcDRjM0xFUT09')

@app.route('/final')
def final():
    return page_redirect('https://github.com/codespaces/cuddly-yodel-44vvjrvjqxfj595?editor=web')

@app.route('/audio')
def redirect_audio():
    return page_redirect('https://noises.online/player.php?g=ca5fa5')


@app.route('/gordle')
def redirect_gordle():
    return page_redirect('https://gist.github.com/ikuamike/c2611b171d64b823c1c1956129cbc055')

@app.route('/chef')
def redirect_chef():
    return page_redirect("""

https://gchq.github.io/CyberChef/#recipe=Find_/_Replace(%7B'option':'Regex','string':'b64:'%7D,'',true,false,true,false)From_Base64('A-Za-z0-9%2B/%3D',true,false)Find_/_Replace(%7B'option':'Simple%20string','string':'As%20a%20security%20scanner,%20review%20the%20source%20code;%20identify%20if%20it%20has%20a%20vulnerability%20as%20$HASVULN$,%20identify%20the%20insecure%20code%20as%20$INSECURE$,%20identify%20the%20CWE%20code%20as%20$CWE$.%20Also%20correct%20the%20source%20code%20and%20return%20it%20as%20$SECURE$.Return%20the%20output%20exactly%20as%20%3CRESP%3E%7B%22CWE%22:$CWE$,%22INSECURE%22:$INSECURE$,%22SECURE%22:$SECURE$,%22HASVULN%22:$HASVULN$%7D%3C/RESP%3E.SOURCE%3D'%7D,'',true,false,true,false)&oeol=NEL

""".strip())

@app.route('/tele')
def redirect_telegram():
    return page_redirect('https://web.telegram.org/z/')

@app.route('/getab')
def redirect_getab():
    return page_redirect('http://www.unicode-symbol.com/u/0009.html')

@app.route('/bov')
def redirect_bov():
    return page_redirect('https://www.youtube.com/watch?v=PQUzc1-IU3c')

@app.route('/rnow')
def redirect_rnow():
    link = """
https://www.plantuml.com/plantuml/svg/tLTjJ-D84lu-lwAb4tn1xNV7Db8qa-24dH5a6SWo0tkhgEskn4rijxUxan1-_PMJW0ntUs8rqaatmSHDTRtKKrLFg_ca3LEc4ZMlMFFXP4P-_xqmfj6djhqMQY5gmGpa1QssbYwOWaQAsbYvhEm6b9OrA-svOhLvgc2sDZFWAtjMigrS6MsxeIrhu4gimMAwUVmeUF_86pyRulBPz2WShmr-eJbAKvclAgYDnlMvOXnVqmAqqCTh0Pk-GrAXDIZ3Z90rkIfPNOjwySSV7qvEY1iJIWRqukAItf1JCb10SAs9Xdob03LEo3LKqe1kroSTk6edvg2NHZRMGif52JkWBCz1QvkS5KfMS30dwLuHetRye1lNYom7VzpJ63zsoRAFHYwXxhCuXCm9U9Gb6VY97qGzpkA4GSJ0ZSB4YTpOo-80V2TqGpycNrRDre2wODa-o8oS2_FBAYCNebxkq--sQo5CiShQZ7SToQ42surdgBrkasuaUdbhywne7Oo5H1CREwoaLPYg_8TkYvohRMDcpORtBtnpwRlruVEf4bfNR2l85Lk0tldlECSPAALSMd8-5_c-b3aheUPCsS90PG--NYu7wHTnwNtsxfw6rSLquVwQtfb9UXVS2rTCfdVknRVRvVrqwTzDxwl9b1Ttc-7vO81MctbqTVQv6Inln5deLIohn6AH3pmvhO-yuPNtzKzdwwxphmyJe_Ep1TeiHXFy_ckDD3dBpxrDgtFaf_XWrJGmbHVOx3dK6fxxa383f-IVjHFQRcHxZXTCtV3KSV11wUtjcwrelzNQ_WMzh2SfAskbxGh0u2pRSUH7VX0uYH-HUzmZepKI0kE_myT3r_fZsxRBywQv-pPvPFL4t7_drzXqT_hR_IN_pZ_p9oVPXsZ7wjyYL2hJ5kELgArSMsjZjGnlQJZ3VDJMQehcuuwLd6sFjy1KlyLyNCdQ5Ftm6ALzDpfc2bZVyuu5xyT16FHmaiiCb261xqHjp9ziSCuEwNRRDYCJ04wC97g5CGtXpyTSApC540IASWD0iYtv_jt6fotc1qh_duk3qleckXXqoZCMDIixfAAKTaZLipttm1o_GwhELeTlQFkgFA2rjL2Chz2RpWifo-UX9JTvWUyIwKMcXPAhHK7EKRELengcySOLQnfjmSlGQvtPnPDUBjYSMrUpLEWcXSMWQGZ-bbiobegWGC41qRkfxeUk5qPUp_4wL7-VZuUkzOxgl_vovrvkzUFaTjY3RxSEdtxvCq-l7owTn_5lqoxLkn5-dEgz7TKzzotLmnUgNsFWPxxJdswazum7rUaUkGOjLoe7tUBz6pUhqysfhTvtlqfblhzQxIDncVUFek78ILpFTrFguv86OoUWmy0Tqa4w6iUZU1Gbe-5Hb1xFHGdzqJIrqExncENjVQhFOSvMfS6-PhYjW0i5kUaRjO9N5o_4-3TXDJy8gpTm_BDmFAHUqXlJ8C1Ld2O-3U8uSWTZpn-T-I-m3gUBrJJc1HfY-S-uhXHeg3ku_gVjIfBCyvpCfp40el71fOpDWIQEmnF6a3CyG5olK6pu5JBCRVcrF-swL-43XFzEiRcekH4Ls9pf8fDCSN8box9ZVWrpK53l1_YrFyxMGZ-mgdDnP1a6iSaNLWay0Schiwkjt4QgfRPAaRqSgA3Me6pM23kN2knC66qKi4hReJ-777gSHdFVeq4MnfHv2QFUF9cxJX9ceGTeL1ke3S41nepVPhZPR2pDdfwmE6g7bzomtHy_d5lWH4aISigTEAO1TnFAeWYe7xhSptqdp3t_7RdbsX9C6sPW5x01sPGOHq4jAMUrOPhcQlL4XgtaHtFc4Pk7KJwdCSIS1YntAKkSY6QGEK4GGgyNlytv4zJyy6_Xlm00
    """

    link = """
https://www.plantuml.com/plantuml/svg/lPLVRzey5CRl-oailMflglm1mXygeQqKwDgkQxVIZZ5DaR5Fi269NTi9b4__dj3Ijtjxmsuc0N4Ipkzvpl4J-6WTDIwJES-eFZWcJX6k3ewFO_Bpft1EsvCWAAMPornI1qnusPDl1JMWbSoTprGMQ31MvJGD4aDpjyaWBbqCl0ZYb3wfmjcWrWnK3jp84dngzVg3vBt3-cXNYCjTwM5pL3hym7AyEb2io21t5jVdXd8yZ0LOQOzA2QjUI0RIMZ2EEgdoNx_Gzf_uFbcT16O_zsZasRXLXM705UiTjlkdhQWpQWy7NclOx7fHlnvvdTRWr3kjzyEmNhr6jSFsu2YHAVHkbNM7zV2jOppry7tX89CRuBZy1bQht8AF2kiZogflzJWaj4ZTKQPc23B0fG7cUiuKSBJY5jaXgUY_JOFig6J7tCrdk6PWBKbblhHuvU-EhDkTrUlXhE5r01fUr82QHsa2NZSCUPVIg17o24UsQnrxTTZZBUQb5ZL9ezN4Blxl6T7MdoirJs5hah-a9k11RJAvRtyVNwscvpVjhzDD61ViubwAYuL-uE7jt0MLmWVZj4gs0oNdWogbpofxQbnkVgZDT5tUZzUpKIFPVBRVnPa-4_cgmyHmMcmro0ZILAsia9hiOlswDSGZbqNwH9fEl5DUhLQ-Ai6aG9Ejj3Pg0Sm5hIPbxLgKr6WIDXky6pKJoZaBoGWtq0fIQ7BpKlUg-4ue9jLpHUwOK2ebdtUPU6k0Qcrzi7xf_6gFhPq5OcENSvPA_pR6p66hm9Qfn0H-Kai9TvgIrqieioUF9lo5Du3vgTR_mV04FO-K8NZ70BndWiNTmKOAwi1kUzdXgzRmY6cVax4mgfYBjorlKUHEqCVVdfu3pul9jIgn2fVUda6mfdDfdwAbYB_COZPXuwjb-HZoXzamj_hcCTu6uHy1b2Et9_nQ9rfahJLNdVOQio2pMM4iL3IqjR_iGrVhSD9Vdrr_6ZdpvVvnKdoTTHTfMPl4YoaVFkUlRzGIyZy2jxnmiVeHqL4ydLnr1eFcnQbcdNhxBhq6VYQMp-2nwXTFxxXLRFC5aiiWArcm_UqtJcd9R91Xdft2ky9bc3a6kONWDgKEC3SqdyCBxHlw06F9HMuBGtC61nyXvo__LVy2
"""
    return page_redirect(link.strip())

@app.route('/8cxpy7u')
def redirect_8cxpy7u():
    return page_redirect('https://mail.google.com/mail/u/0/')

@app.route('/ssec2024')
def redirect_ssec2024():
    return page_redirect('https://www.google.com/')

@app.route('/testsamplebbterminal')
def redirect_testsamplebbterminal():
    return page_redirect('https://github.com/OpenBB-finance/OpenBBTerminal')

@app.route('/myexcelreview')
def redirect_myexcelreview():
    return page_redirect('https://www.plantuml.com/plantuml/svg/SoWkIImgoStCIybDBE3IKd2jI4xDKV2j34ejoqmjLt0gIatCJialp-FIqb8mKB2oLV3BXqY110n10hw9UQM9EGX18v1WG55-Ub5YRcvYIMPoOavE9KBQ6A57mJ4l1KEb0bIfGsfU2jHP0000')

@app.route('/rustgameengines')
def redirect_rustgameengines():
    return page_redirect('https://arewegameyet.rs/ecosystem/engines/')

@app.route('/my_remotework')
def redirect_my_remotework():
    return page_redirect('https://www.plantuml.com/plantuml/svg/lP9FQy904CNlVeezjiYQFza_6q4KzT3sL11w4IcJsLbC6vCqkrBoxRkAb4BlifV7Cc_URuPP-G13EDMjFK4_cRBz_XX2x-T90dq_G-W1wr2JdzLTWYLaiieTpmeBN4YB74o670aBq2bAaRe4GEjSLy2TbXKNQ3Glyv9uYQWBAunMfDdhq7qG1dyuJARtowIcZeF2C5vZfsnD8OnH_I94WYpNipI-RAvAaIPBrpMMXaNYnnRPs-xYlDN_CsXZJD90jGpT9xKBKYGLvIAN6WKA8rIQAfi9S624Su9SAQqo1P0gXAISlPpxCT0GEznpBPbytsoUsUxOVIDuYj6Sios4g8Dd3xklfWxq63_v7o1R7S_LXODjrqzN5NqhQktja7u0')

@app.route('/remotework')
def redirect_remotework():
    return page_redirect('https://www.plantuml.com/plantuml/svg/lP9FQy904CNlVeezjiYQFza_6q4KzT3sL11w4IcJsLbC6vCqkrBoxRkAb4BlifV7Cc_URuPP-G13EDMjFK4_cRBz_XX2x-T90dq_G-W1wr2JdzLTWYLaiieTpmeBN4YB74o670aBq2bAaRe4GEjSLy2TbXKNQ3Glyv9uYQWBAunMfDdhq7qG1dyuJARtowIcZeF2C5vZfsnD8OnH_I94WYpNipI-RAvAaIPBrpMMXaNYnnRPs-xYlDN_CsXZJD90jGpT9xKBKYGLvIAN6WKA8rIQAfi9S624Su9SAQqo1P0gXAISlPpxCT0GEznpBPbytsoUsUxOVIDuYj6Sios4g8Dd3xklfWxq63_v7o1R7S_LXODjrqzN5NqhQktja7u0')

@app.route('/capz')
def redirect_capz():
    return page_redirect('https://app.capacities.io/')

@app.route('/corers')
def redirect_corers():
    return page_redirect('https://raw.githubusercontent.com/franceme/staticpy/master/sample.rs')

@app.route('/finaldefense')
def redirect_finaldefense():
    return page_redirect('https://drive.google.com/drive/u/0/folders/12WQsEcgXg6Lzd9ILQ-NIuBBgrSrN328l')

@app.route('/researchdefense')
def redirect_researchdefense():
    return page_redirect('https://www.mindmeister.com/map/2611141209')

@app.route('/vt_hardener')
def redirect_vt_hardener():
    return page_redirect('https://raw.githubusercontent.com/franceme/staticpy/master/hardener.sh')

@app.route('/pypyg')
def redirect_pypyg():
    return page_redirect('https://github.com/Kanaries/pygwalker')

@app.route('/hermy')
def redirect_hermy():
    return page_redirect('https://web.telegram.org/k/#@HermesFeetBot')

@app.route('/projectbreakdown')
def redirect_projectbreakdown():
    return page_redirect('https://www.plantuml.com/plantuml/png/VP11IyD048Nl_HNlvXge9AaLSslHivIWU9JLZ6HrCnjs9zNyUuUjI27WQHQ-xprukqjYemoEky6Egm9LMTx2j6Jz-Zb4t-4GmmUzoUMgA5vm0_COHhIMF-aF9MKvMEjLQLl3F0J1_cYTjw-UiETv297KKx7Pbdfpst-UyWhctdLy8UZjaM1vnc6MFZ3UdQTqfbNd05zEtvD0UiBLE8E-XJYvmAS4ckiQTrECn8AMqkGbASXTcpnmlHnu2cuQc2TUuXrnz_k7Fm00')

@app.route('/veedly')
def redirect_veedly():
    return page_redirect('https://www.veed.io/workspaces/34d68d13-42c8-4c30-b56c-91893f5181fa/home')

@app.route('/plann')
def redirect_plann():
    return page_redirect('https://mermaid.ink/svg/pako:eNp1VE1z2jAQ_SsandqpIf6QgfiWQtLpgSkTDpl0uCjWYqvYkkeWaUkm_70r2QEn02o4SOi9fW9Xu36huRZAM1pwZe1OEVxW2grI-kR-qEJLVZBNxRXZa0NsCWQLNbQWTI8V3MKdNjW3hDzimqzXk9XqLU5--K4QeuQViQQ_7VR_0UJupVbkGygweHd7BGXb_m7bGCf51QA_kMvKeBSQOIyTSYg_FmC8Hp9XqEJ4REoDe7KjpbVNm11d1YCmpPjVTgtpy-5pKvXVjn50sDSnxuqKu0N_cyeVbEuy5UraE1mWkB-cnyw3-uwgnoS4T8SZwSv57FDLkhvbenAcEL7H3MlAHMA3QpB7aLsKYZ--5B7_2ROSESG-EG4xi4rkesI7W2rTEq4EMXCU8NvT2IiWXEyhjoG2dY5UAb2ldARlF-i2e6pl27py3AMXJ4-d_du-x1qy4Q1eOdx8hEv7V3lf4Y2BStYDG9A7-IRcN_Ej7viTrFylM6EVvC_wfBDdGF34ZDCc60Cju6IkwqCw8yAtekCxI9IbAx9fKRQjcavJykzJI9fewVsdkXZ-rz5ExAbaUisrVQcD1vcCQpL_wL3KSuddjS3t5HJdY8UsgKexES25NHFMHgAO5IFL6-cNjNTCE9IRgY10bsa1c6k0vs6eMxtx0jcODegwEjjsLy7IjmIxa9jRDLeCm4Mbj1fEYafp7UnlNNvzqoWAdo0b85XkheH1-d-Gq59a49marj_S7IX-odmEMTZdpLNoHs5SFl_PrgN6otl8Nl3EKQujJJxFaZyw14A--wDxNGJJurhmaRim0SJhAQUhrTbr_tvkP1GvfwF8kXXc')

@app.route('/prelim')
def redirect_prelim():
    return page_redirect('https://virginiatech.zoom.us/j/85652239554?pwd=VlZTRGIzNlZqaWh6NmxpZldoNDVYUT09')

@app.route('/auroa')
def redirect_auroa():
    return page_redirect('https://www.authorea.com/users/579829-miles-frantz')

@app.route('/pyhook')
def redirect_pyhook():
    return page_redirect('https://raw.githubusercontent.com/franceme/staticpy/master/hook.py')

@app.route('/txtpad')
def redirect_txtpad():
    return page_redirect('https://www.onlinetexteditor.com/')

@app.route('/installgh')
def redirect_installgh():
    return page_redirect('https://raw.githubusercontent.com/franceme/staticpy/master/install_gh.sh')

@app.route('/office_hour')
def redirect_office_hour():
    return page_redirect('https://virginiatech.zoom.us/j/81604121297?pwd=eGE5T2RlSU14ZTFUUzg0eWRWSlkrQT09')

@app.route('/mdh')
def redirect_mdh():
    return page_redirect('https://mdh.cs.vt.edu/dashboard')

@app.route('/gpss_elections')
def redirect_gpss_elections():
    return page_redirect('https://docs.google.com/document/d/15qd7Bh_2KTj_OZWWsOqWSaPjnp8JfcrY/edit?usp=share_link&ouid=103289071436703194896&rtpof=true&sd=true')

@app.route('/gpss_initiatives')
def redirect_gpss_initiatives():
    return page_redirect('https://docs.google.com/forms/d/e/1FAIpQLSdaJJcwfVjZInEOojruAjYgRqATtlUKUbPs--zxiSM-Bw8FSA/viewform')

@app.route('/sulis')
def redirect_sulis():
    return page_redirect('https://github.com/Grokmoo/sulis/releases/download/0.6.0/sulis-0.6.0-linux64.zip')

@app.route('/chat3')
def redirect_chat3():
    return page_redirect('https://chat.openai.com/chat/')

@app.route('/ovabox')
def redirect_ovabox():
    return page_redirect('https://www.huestones.co.uk/2015/08/creating-a-windows-10-base-box-for-vagrant-with-virtualbox/')

@app.route('/staruml_python')
def redirect_staruml_python():
    return page_redirect('https://raw.githubusercontent.com/niklauslee/staruml-python/master/unittest-files/generate/CodeGenTestModel.mdj')

@app.route('/mmail')
def redirect_mmail():
    return page_redirect('https://dropmail.me/en/')

@app.route('/r_shell')
def redirect_r_shell():
    return page_redirect('https://raw.githubusercontent.com/franceme/staticpy/master/rshell.sh')

@app.route('/ou701g1')
def redirect_ou701g1():
    return page_redirect('https://stackoverflow.com/questions/38987/how-do-i-merge-two-dictionaries-in-a-single-expression')

@app.route('/gift_rents')
def redirect_gift_rents():
    return page_redirect('https://docs.google.com/document/d/14CYdx3o_15LrhV9wCYv0X-MJv5fqhgPI/edit?usp=sharing&ouid=103289071436703194896&rtpof=true&sd=true')

@app.route('/gift_rent')
def redirect_gift_rent():
    return page_redirect('http://google.com')

@app.route('/gift_shak')
def redirect_gift_shak():
    return page_redirect('https://docs.google.com/document/d/1Hock_q21oJto4zHtZilbDIMDRT0HX7n-/edit?usp=sharing&ouid=103289071436703194896&rtpof=true&sd=true')

@app.route('/gift_self')
def redirect_gift_self():
    return page_redirect('https://docs.google.com/document/d/1eI4C3MiRPDO-VElCZF2_NBaV2-z8LxYp/edit?usp=sharing&ouid=103289071436703194896&rtpof=true&sd=true')

@app.route('/gift_selfshak')
def redirect_gift_selfshak():
    return page_redirect('https://docs.google.com/document/d/1D68CY8765mevTuMtAKJEenK8rUKf5oEE/edit?usp=sharing&ouid=103289071436703194896&rtpof=true&sd=true')

@app.route('/gift_browns')
def redirect_gift_browns():
    return page_redirect('https://docs.google.com/document/d/1HfcsVm-3YY19MCmoI-v3EISh6mfc_43J/edit?usp=sharing&ouid=103289071436703194896&rtpof=true&sd=true')

@app.route('/gpsss')
def redirect_gpsss():
    return page_redirect('https://share.1password.com/s#2lHGv5Ad6eD85ocX0OXFM8Q35QaQ-w-PkFO-rbmUcYQ')

@app.route('/ghspace')
def redirect_ghspace():
    return page_redirect('https://raw.githubusercontent.com/franceme/staticpy/master/ghspace.py')

@app.route('/gpss')
def redirect_gpss():
    return page_redirect('https://virginiatech.zoom.us/w/81971442237?tk=UOgQTIJl6yDiKJk5OIx0PCqdmlEDaCweFf0HDbUA1zw.DQMAAAATFeDyPRY2c1A1X01SMlQtMk9BS2RrbS0zLW5nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA&uuid=tZUkcOisqjkoGdOt1nGOGEOeEa2WQkaJCOrX#success')

@app.route('/full_research_redirect_link')
def redirect_full_research_redirect_link():
    return page_redirect('https://www.plantuml.com/plantuml/svg/JO_13e8m38RlUugUT_45a9089qGIYSPhaQbDM4TOf_BsEgB9JltQhsdp5rvm5aiyM9oKXjBqXAoqXbCVMCANDEo9mniQObdREYGguRgiu60SgpXloYhMpetBSAbN58EsxI8UqK_n3xn87e3mDFC2e-CxC5gp7ijy7hTiVyqsFeTj3ctNx5ArtEYlpcuCbfmg30-_B1y0')

@app.route('/myn')
def redirect_myn():
    return page_redirect('https://share.1password.com/s#6ZbzIk_ey0tIf5-S33djZ-yvskQWzcqG9j3QbV6TyGo')

@app.route('/vt4iran')
def redirect_vt4iran():
    return page_redirect('https://google.com/rerer')

@app.route('/opiran')
def redirect_opiran():
    return page_redirect('https://google.com/based')

@app.route('/irantoo')
def redirect_irantoo():
    return page_redirect('https://google.com/rawr')

@app.route('/mahsa_amini')
def redirect_mahsa_amini():
    return page_redirect('https://google.com/eat')

@app.route('/mahsaamini')
def redirect_mahsaamini():
    return page_redirect('https://google.com/base')

@app.route('/spacy')
def redirect_spacy():
    return page_redirect('https://github.com/codespaces/franceme-spaces-pvwwj6pv6v36x7')

@app.route('/mmap2')
def redirect_mmap2():
    return page_redirect('https://www.mindomo.com')

@app.route('/11_Naming')
def redirect_11_Naming():
    return page_redirect('https://viewer.diagrams.net/?tags=%7B%7D&highlight=0000ff&edit=_blank&layers=1&nav=1#RzZjLcpswFIafhmVmuAeWtZO26YzbTGnqtQoqUiIQI4QxffoegjAXOTPppmJl8R9drE%2B%2F0BGWty%2FOnwSqyIFnmFmunZ0t785yXdcOQ%2FjplW5QHCd2BiUXNFPaJCT0D1airdSGZrheVJScM0mrpZjyssSpXGhICN4uq%2F3mbDlqhXKsCUmKmK4eaSbJoEaBPemfMc3JOLJjq0iBxspKqAnKeDuTvHvL2wvO5VAqznvMenojl6Hdxzeilz8mcCnf0yBpfn09PrMvsnKj6iBZdHh6ulG9nBBr1IQtN2TQ3y6jJyjmfTGRSNJ0DMAIs5iam%2BxGYDAorA087FpCJU4qlPaRFvwBGpEFgyfn0vKEhcTnN6fkXECBxTAvsBQdVBkbRIqtclcwuqadlsoZ%2BZPZMo3tkHJHful6AggFxfAfeLoaz0fBn8GYtVlQt0tQvmsalKeB%2BkEEb3JilFPorDjZpjn5GqdvFS5BSXgjAIRJWv7WTBVosD6UmVFE3tpQxhmFGqO96CrJ8%2F4A79%2FyJmm5S1qe8e13q9H6iRjN4Dwsc6OoVqQi476Kruw9xLqamj351pYKjIOKNVBXUq7vGLEjF5CsbjDripdIIeU1zXR8y86g7nCZkgKJF7NH5DrxMo%2FqXSn%2FYycJL7dovmhrR4Sj5%2FxXgB5o3QCi7QH1o2BrQPW7wXZSFH%2Flvzg2jku%2FIlzx3x2WcAt9zVq2Z8HNbWn9IvFQSixu4DKf4qwRiBkF5m0tp3H0PPlIJaGlUUxh%2BP%2BMBY%2FTp7zX2OyLqHf%2FFw%3D%3D')

@app.route('/semgrep_rules_cut')
def redirect_semgrep_rules_cut():
    return page_redirect('https://drive.google.com/file/d/1J4OBlhfJZvuXP7Sb54tru31L-eRFM9Ly/view?usp=sharing')

@app.route('/pyzz')
def redirect_pyzz():
    return page_redirect('https://raw.githubusercontent.com/franceme/staticpy/master/zz.py')

@app.route('/usb_wifi')
def redirect_usb_wifi():
    return page_redirect('https://gist.githubusercontent.com/franceme/db2f4f3e7bd27ed0e873063b56bc97cf/raw/9b965fff3130ab4bdbb60e9f48b215c919fb1421/install.sh')

@app.route('/bashrc')
def redirect_bashrc():
    return page_redirect('https://raw.githubusercontent.com/franceme/Scripts/master/bashrc.txt')

@app.route('/rrun')
def redirect_rrun():
    return page_redirect('https://franceme-11-cryptolation-journal-66559p46p9frw57.github.dev/')

@app.route('/my_time')
def redirect_my_time():
    return page_redirect('https://wakatime.com/dashboard')

@app.route('/time')
def redirect_time():
    return page_redirect('https://wakatime.com/dashboard')

@app.route('/frantzme_qr')
def redirect_frantzme_qr():
    return page_redirect('https://franceme.github.io/qr.html')

@app.route('/piper')
def redirect_piper():
    return page_redirect('https://pipedream.com/@frantzme')

@app.route('/mmap')
def redirect_mmap():
    return page_redirect('https://accounts.meister.co/login?locale=en&product=mindmeister&r=140672&return_to=https%3A%2F%2Fwww.mindmeister.com%2Fmap%2F2373355898')

@app.route('/hugface')
def redirect_hugface():
    return page_redirect('https://www.plantuml.com/plantuml/svg/fPDTgzD048RlpwyOwEKXk_QWWbvLYRL2rM8jNfIoR3QJP37xmUx4sd_lcezI46dBkSlxPERPpGnPH9A1ZBQbaVxX4VRxXiZ7jvmtNLrhMrTI8LCELaDSfXWFXuV7_vVoqgcOMC6J5N_3DwoxLeR90Bq2tcq-zPfhdbAIZ4YH_vgp-Pozc828552QLCuQCYrifmYv97cd-eczJ6Qqt4lrKzOe0bOOq2hahPDbQXG6gN5bd4rDxEyBCIPO3rMG3_ckuwyVUjP_7lBzWtkTFg_pbrVkfpORM5O5Pp9_eiPPsFK8bWd1Pa0Pv5-_V8VTziDjcpypqNG5l4SYlBx-csIySSUCNDRvOVtZRNklRZ4-nrcwensjUNhyrtkXhJMbJgQSuLMGLg51lbL1UugyQ5t1ZOo4WLUTBR1DK0XjDGd1_6csVlNc2JvgMgNX_0ZIUmp9lq1RZl_X7m00')

@app.route('/sioyek')
def redirect_sioyek():
    return page_redirect('https://github.com/ahrm/sioyek/blob/main/tutorial.pdf')

@app.route('/my_dock')
def redirect_my_dock():
    return page_redirect('https://www.plantuml.com/plantuml/svg/hPT1RzCm5CVl-nG-WggHEwTH2cYeWufkuZ1DaMERrio9BTiPoxV7oKlSOlMG5tEoNwJ_x_tqQZdDZVFK-beslARcQaKscZqBUrlJWt1NgnLvV3nwRzpxeZX8VsohTqpNnIzB6oPgKUoPbSOxCgvFJo4oCrDGvgLk7Fa0wwoiwKetjjnrPqqnoRJnl7n5dIZvC1oo3dkO4sGnuRGxdb2signQgVW_9W-tQtW6mAN4L6ykZOkNG26Ri3p8FeH8vVKiTUN6lkNt2iAuT6P_mPGqJamEdw0429gIwQAwrybZsxr269NExCyjVTRDfB0PAa1W6PaY1ysrdpo-z0K0a8HCYrhhqy6uwmi080dvTyQ52oFZklWFTuMIVXWCsOOD1179fPrDvu-wYVrtGucsY9JBBdYC5ywVPEv3bGZXK4kdyvk-q3YRhw70JIOXBBNuOqFOWiJFOOznYFdyOzAFKZQ7ywDo3u-Y49wMvLKhaBdR3WRapJVjoUTMgOxih316yBU0cidAKB6jy_6i_0W5xgmaXDG21J7ToMBNHGaq84e023iHnwYYayiUYYY38sJyBXLLIbZPKF1OJsKqmLEYIqB3_tyUtnkJMl8ccXIlho-ZcER26Sg48n_3Tjzl--Otek7ZzyjV')

@app.route('/dock')
def redirect_dock():
    return page_redirect('https://www.plantuml.com/plantuml/svg/hPT1RzCm5CVl-nG-WggHEwTH2cYeWufkuZ1DaMERrio9BTiPoxV7oKlSOlMG5tEoNwJ_x_tqQZdDZVFK-beslARcQaKscZqBUrlJWt1NgnLvV3nwRzpxeZX8VsohTqpNnIzB6oPgKUoPbSOxCgvFJo4oCrDGvgLk7Fa0wwoiwKetjjnrPqqnoRJnl7n5dIZvC1oo3dkO4sGnuRGxdb2signQgVW_9W-tQtW6mAN4L6ykZOkNG26Ri3p8FeH8vVKiTUN6lkNt2iAuT6P_mPGqJamEdw0429gIwQAwrybZsxr269NExCyjVTRDfB0PAa1W6PaY1ysrdpo-z0K0a8HCYrhhqy6uwmi080dvTyQ52oFZklWFTuMIVXWCsOOD1179fPrDvu-wYVrtGucsY9JBBdYC5ywVPEv3bGZXK4kdyvk-q3YRhw70JIOXBBNuOqFOWiJFOOznYFdyOzAFKZQ7ywDo3u-Y49wMvLKhaBdR3WRapJVjoUTMgOxih316yBU0cidAKB6jy_6i_0W5xgmaXDG21J7ToMBNHGaq84e023iHnwYYayiUYYY38sJyBXLLIbZPKF1OJsKqmLEYIqB3_tyUtnkJMl8ccXIlho-ZcER26Sg48n_3Tjzl--Otek7ZzyjV')

@app.route('/7rqpa54')
def redirect_7rqpa54():
    return page_redirect('https://drive.google.com/file/d/1HIp0_b3JLSJclPZ0Wl-EbA2k2-mNlGmZ/view?usp=drivesdk')

@app.route('/temails')
def redirect_temails():
    return page_redirect('https://dropmail.me/en/')

@app.route('/mathpix')
def redirect_mathpix():
    return page_redirect('https://snip.mathpix.com')

@app.route('/url2bib')
def redirect_url2bib():
    return page_redirect('https://karlosos.github.io/url_to_bibtex/')

@app.route('/mlconf')
def redirect_mlconf():
    return page_redirect('https://aideadlin.es/?sub=ML,CV,CG,NLP,RO,SP,DM')

@app.route('/secconf')
def redirect_secconf():
    return page_redirect('https://sec-deadlines.github.io/')

@app.route('/vscode_fixtodo')
def redirect_vscode_fixtodo():
    return page_redirect('https://github.com/Gruntfuggly/todo-tree/issues/129#issuecomment-465482314')

@app.route('/pry')
def redirect_pry():
    return page_redirect('https://www.dignitymemorial.com/obituaries/dayton-oh/robert-pry-10835211#')

@app.route('/pydock')
def redirect_pydock():
    return page_redirect('https://raw.githubusercontent.com/franceme/staticpy/master/pydock.py')

@app.route('/my_cloud')
def redirect_my_cloud():
    return page_redirect('https://rebrand.ly/frantzme_adobe')

@app.route('/vegas_hotels')
def redirect_vegas_hotels():
    return page_redirect('https://www.google.com/travel/hotels/Las%20Vegas%2C%20NV?q=las%20vegas%20hotels&g2lb=2502548%2C2503771%2C2503781%2C2503998%2C4258168%2C4270442%2C4284970%2C4291517%2C4306835%2C4515404%2C4597339%2C4649665%2C4703207%2C4722900%2C4723331%2C4738544%2C4741664%2C4757164%2C4758493%2C4762561%2C4777462%2C4786153%2C4786958%2C4787395%2C4790639%2C4790928%2C4794648%2C4800879&hl=en-US&gl=us&cs=1&ssta=1&ts=CAESCgoCCAMKAggDEAAaMQoTEg86DUxhcyBWZWdhcywgTlYaABIaEhQKBwjmDxAIGBESBwjmDxAIGBUYBDICCAEqDwoLEgIEBSgBOgNVU0QaAA&rp=ogENTGFzIFZlZ2FzLCBOVjgBQABIAg&ap=MAFamAMKBQivARAAIgNVU0QqFgoHCOYPEAYYFxIHCOYPEAYYGBgBKAA4BDgFsAEAWAFoAXIECAIYAJoBDxINTGFzIFZlZ2FzLCBOVqIBFQoIL20vMGN2M3cSCUxhcyBWZWdhc6oBDwoCCBISAwibARICCGgYAaoBDgoCCBQSAgg_EgIIGxgBqgEHCgMInAEYAKoBBwoDCKECGACqATgKAggcEgIIBxIDCJcBEgIIURICCFgSAghzEgIIRxICCF8SAgg2EgIIJBICCE0SAwieAhICCCkYAaoBCgoCCCUSAgh5GAGqARoKAggREgIINBICCEASAgg4EgIIAhICCCsYAaoBMAoCCC4SAghWEgMIhgESAgg6EgIIGhICCD0SAwiDARICCEsSAghTEgIIKBICCCcYAaoBBgoCCCwYAKoBCwoDCOECEgIIYxgBqgEKCgIIUBICCEwYAaoBBgoCCAoYAKoBBwoDCLgCGACqAQYKAggzGACqASIKAgg1EgIIHhICCBMSAggiEgIIJhICCAsSAghdEgIIEBgBkgECIAFoAA&ictx=1&sa=X&ved=0CAAQ5JsGahcKEwiY1aGhkcD4AhUAAAAAHQAAAAAQBA&utm_campaign=sharing&utm_medium=link&utm_source=htls')

@app.route('/py_task')
def redirect_py_task():
    return page_redirect('https://raw.githubusercontent.com/franceme/Scripts/master/tasks.py')

@app.route('/my_conf')
def redirect_my_conf():
    return page_redirect('https://www.plantuml.com/plantuml/svg/ZP5FQm8n4CNlVeevBsmYdafFsbMAi5B1taHap8vkQFw4pInRltqJfIZLGq-PWVT-UO-PHiQEhNQDnJ0gu9qSTMYWrkuhZee2Ak-Er95JbDS2DgJoMy1sspA7-2fbOmGgAtntakgcXbcrskqUj0SJiZ8D5x6CGSByhLu_IeTX4FRSzlg0JYXlx-1oyWBBLVNSeudeRnYP2jAtQDaQM2uMY-JyJmaPJADXNS-NLmEiwcS_iWy7p_4ICiqbasgTLcXAr2MwfhIcl0jJJiQJiOJFZtNYmUpAXihRW1sDRlX4FwBg3P-5YeBHzeAQNfvwVoGj8wbzXkuZ8-Tc-JImIKjCm2cvvlUgFm00')

@app.route('/conf')
def redirect_conf():
    return page_redirect('https://www.plantuml.com/plantuml/svg/ZP5FQm8n4CNlVeevBsmYdafFsbMAi5B1taHap8vkQFw4pInRltqJfIZLGq-PWVT-UO-PHiQEhNQDnJ0gu9qSTMYWrkuhZee2Ak-Er95JbDS2DgJoMy1sspA7-2fbOmGgAtntakgcXbcrskqUj0SJiZ8D5x6CGSByhLu_IeTX4FRSzlg0JYXlx-1oyWBBLVNSeudeRnYP2jAtQDaQM2uMY-JyJmaPJADXNS-NLmEiwcS_iWy7p_4ICiqbasgTLcXAr2MwfhIcl0jJJiQJiOJFZtNYmUpAXihRW1sDRlX4FwBg3P-5YeBHzeAQNfvwVoGj8wbzXkuZ8-Tc-JImIKjCm2cvvlUgFm00')

@app.route('/csgc_website')
def redirect_csgc_website():
    return page_redirect('https://www.plantuml.com/plantuml/svg/nLHHRzCm47xlhpZj2T0QjzacMFUoRe9DGa9eBPjWweFZt1Apn8xiSwE2-E-SanPMfasW8SX3LITttttttNS-zYGTXReQJ3vuT53BM_GWGPNI50ZMmFLrITJuYH25fZ9aYRArE9sTEPa7INXgWr6w6bvgLsYZvHnLAPGlrB35p6j2EDDq7hB5ucWm-MjOa0LTvHweHDXyMshvPB8YgsmcQka9dKXw3D5QTtjJsTQB2wnGUanMTRMc0bD5sXeVspEM49mkIXe0m8ixP1WzaKwLUec9TKKyYtIKfgE3SShFuIWL_upt5MRJdifYyIlF9W9asdJbhqRB2tcmjm_luziJRJWUJHwx74p-ez3WqQn7_qKtSACh1BBn_FJnkxwkXysV-tETbxZv2kVJMInToYLszLLm3Wq1wHfviUec9doq0PGqZ0AXgQpCjrpRCj7kXPSrWk6VcFF6Ef21x90RQBZ1NOw7u1-eqeDuL9Q5-J6ZHZhIKJFOURr4ju9tiGKuYPkp0rzZcSbyIpIMWfLAb4-Mb60Un8ObYwvPas20qOXpBkSmGyUe4v3D-6V6KOSwipLQ4-yHfLXoYfbyUCXeRr-bQZoVVWBbh24Prti8ptvtU_PUfeVYSLoslDnO_daaOxGf03jHJ1IbexqrPduuBSQ2fhkXuBLH64LmoAAiGus5Lguw6p92WIu6z9TKZ5YFP2FvGqACf4iFJlHdo96DiWAld6xep-JO7uz6ud7qRJbosvheIW-L9FPJpteN77EG2lsMvUwvrc3R9nmDlWsEkSzGLzy1')

@app.route('/my_task')
def redirect_my_task():
    return page_redirect('https://app.asana.com/0/1202250158074124/list')

@app.route('/task')
def redirect_task():
    return page_redirect('https://app.asana.com/0/1202250158074124/list')

@app.route('/frantzme_latex')
def redirect_frantzme_latex():
    return page_redirect('https://drive.google.com/uc?export=download&id=1EjUCp54i4KXiXbroPvrGqiZEvdWkF2Lu')

@app.route('/frantzme_adobe')
def redirect_frantzme_adobe():
    return page_redirect('https://acrobat.adobe.com/link/home/?locale=en-US')

@app.route('/frantzme_linkedin')
def redirect_frantzme_linkedin():
    return page_redirect('https://www.linkedin.com/in/frantzme/')

@app.route('/biblelove')
def redirect_biblelove():
    return page_redirect('https://ffrf.org/component/k2/item/25602-abortion-rights')

@app.route('/frantzme_contact')
def redirect_frantzme_contact():
    return page_redirect('https://franceme.github.io/vcard/')

@app.route('/ndss')
def redirect_ndss():
    return page_redirect('https://calendar.google.com/calendar/u/0?cid=Y19hOTFzMGUzMjdpYmxjN2htMjZwY2l0czQ3NEBncm91cC5jYWxlbmRhci5nb29nbGUuY29t')

@app.route('/rsc_gen')
def redirect_rsc_gen():
    return page_redirect('https://www.plantuml.com/plantuml/svg/RT7FIiD040RmUvzYm6D95pnwgWJffNYeMW-bbEdks2pidxWxIUhRknqN3E9nvfllHyYkCsDYRuFns2-M9zXGe8GETfJZa3JbnR9iMtGK3AOoBE5mw9Zx1wMcQLfrxDszrUXMEdfL7Bgk-gw7nu6ZHxubxWjq8cG215qX-4ZHmzjkUppEp5nGiJocmKGM4ref_rPffC1PYYVObkWASwD-cBi53UFPKHRdhjw-oghMt-dyRBLbI_aVupCrEXfgBl9JE2Q1SdG3snYo6ZKcqzGh1VksZ1L-sM_WoTZI-GldyK8InE1i825_5chMAioQWgalymq0')

@app.route('/vt_funding')
def redirect_vt_funding():
    return page_redirect('https://www.plantuml.com/plantuml/svg/ZT1VIp9150RmUp_5tCixmnk854IQuc99g5j2Y2pZpDdPjPq_dZExbf--hRn8wgAxWJdydeTdG55YjANJLePEDsEJskdIcKwtVQ_NHOo1heGmWOWtaOEkMJ9FqyscFUZ-VY02UeFIaeXvu4Mq5Nj4sK3rQRFvr-_V18FwH2GeTIqZi2KGI5G56qDh-c31nJFqUs-4BKgdUVKc51d5Hcao-f6ilI9kl3SLSEMjo3ssqLg0-3yPJiDYbgfUEbxD3692jyVTHSzceqBD3jEdUrWzz_V5STZ_fovx_Tts8NzrTmlHb73uO6vg2jUKPrNfNivMMCA-1efjbm4uVTh_7G00')

@app.route('/vt_etd_rsc')
def redirect_vt_etd_rsc():
    return page_redirect('https://vtechworks.lib.vt.edu/handle/10919/73192')

@app.route('/vt_etd_docs')
def redirect_vt_etd_docs():
    return page_redirect('https://guides.lib.vt.edu/c.php?g=547528&p=3756998')

@app.route('/VT_ETD')
def redirect_VT_ETD():
    return page_redirect('https://www.overleaf.com/latex/templates/virginia-tech-etd-template/cpqhbscstfrx#.WusPwtMvxBw')

@app.route('/vt_stages')
def redirect_vt_stages():
    return page_redirect('https://secure.graduateschool.vt.edu/graduate_catalog/policies.htm?policy=002d14432c654287012c6542e3630013')

@app.route('/vt_exams')
def redirect_vt_exams():
    return page_redirect('https://secure.graduateschool.vt.edu/graduate_catalog/policies.htm?policy=002d14432c654287012c6542e3630013')

@app.route('/better_shell')
def redirect_better_shell():
    return page_redirect('https://raw.githubusercontent.com/franceme/Scripts/master/better_shell.sh')

@app.route('/csgc_rules')
def redirect_csgc_rules():
    return page_redirect('https://docs.google.com/document/d/1YrcqQCxML7jFIrtPRbh80wkqDbkA-7syDoGd6AdtGpQ/edit#heading=h.8p56zfsqdojw')

@app.route('/ohjohnny')
def redirect_ohjohnny():
    return page_redirect('https://docs.google.com/presentation/d/1amVrGpFoJZq4zCBPsTn4DEab9wdN548n/edit?usp=sharing&ouid=103289071436703194896&rtpof=true&sd=true')

@app.route('/python_save')
def redirect_python_save():
    return page_redirect('https://raw.githubusercontent.com/franceme/staticpy/master/ipython_save.py')

@app.route('/cybers')
def redirect_cybers():
    return page_redirect('https://gchq.github.io/CyberChef/')

@app.route('/graphz')
def redirect_graphz():
    return page_redirect('https://www.plantuml.com/plantuml/svg/ZLPlRzis4t_VJq7W0Hwq22GbJLUqUzKqQRUbpkfDtJgiA8oJT9Lfapo2FCLMF_qeKau2oyxsmk4T-RiVxyyTepUUmR6Mfj5Wdvmin1KmFCcoXRZkRC_enA_4M16jnKokCPo4exUEDXxTe6JYovSbi_K_5aLD2ghSeKTmzJ9lYLg5UKsw43z5MLmEYAzVfuOrg7f01iHb4ASGtLV1HtGvkROGD_tRg4rnPlJMv_2zS-Fj5uCunJR0e2Y091NYQbIciCrcaw-GAmVI-4ZeK1DZrk0jAh8Q3HSjC6wW3v4c8T4in6m8xH2Zjtq889CDff3Ag4zlNwKo9D2k9hCnYwbSOYujAcd6wboIjk2a9-FtoLh9owwACTn8qtU-cFUy9BEOGxs65ltY6xd5ZcxncTpwcwADIAY7pE8iE72StJQIIMlmLC06FMdCxCYwOnb8dYUIQKTD6Icq57hUhU9ZMX_DCvDKkKDeU8aDrJwN93w5lMXq_2QBPjEe8lp4vwlP51ph5v2Qp4R5mdGUtQBjP8E5kFmycwRcEzeOVGuMwkLOyeieYx_3MJYQ6bMAshpg7PcLry6_w1r3M-nIwVCbQoLA0slKuJUbM6FZQ2y51Ph2CrGAYzEpXJJigEbgbcJszKJ_OU2OKazxQUVMzguX_peyJQZ0inm6lbZB2WmKuaDS_nKktaKvlJ0FHw1aSj2E4_2Ud0OUkx_yRIOPatpjoIJfilmp2Jz3GsJthoLZjZd8GWp2NO_9oe6J68YJ3gODSbBIY4Gjgc0Qy4zEJeAeY5cQDYX1-qIaXlru0h8HJpSXaOAT1EMVnOEJlVYrh1rv-iOnsMYoaEkxlUpyvGy5RcjKujtmDpXxY4DMEWrcAgullFK-ymmiXznwKSxBCjf6r_Qi8vWxfkXb98fRDWQTLU03HR5x9dunZAs3eOEEU1Ex3xf893ubvT3b4p1Kr74SZEBvwTdhuaMXy1Q7ocUMDkYo4Po1QNRUMOU-TjAolCMm3weV0ixEJb-yFdtvttqc9rjf5CIM5n-ZTWIwqdOirIAKQaaQqoHTtyoFM6XfP73zGO75JTeQ3K9JEyI9RRq4nvddhf6KMqMi-iXHEmJ6ud-X9d7pmBMDWz0M9Ax2Akc8NrQ1uKwh6FDyKFxGwbZKeEbMZl-eedm0k09lOzlv4NXH7ij9w6wuRz0OLaobNLfHVdn_4StYLCPvkXl1FIeD71CZg-56SQy6-pseHwZ8cTps3J0a1yUzAVX1jbEZxUNwy5EfvHeRt80hcdFRYwlpB7ezvK-jxtejcU87oaqGoYKYJw4Lw8feYF3LwQjJ1LNAbdWxx8VyFEgHwhPPY7HOnQpRFefT1I0kBTrzPbsNzz-7GNuwJjF_Gs3F4jCYzC8jb740zvcRyrLgWm3VeN_l_1H7eVxEnvGp1a41e-TxNSn7QSSo2u1jV5ZyeRoguJYz5IbLoI1B5e7a3Pfc_2Z-1m00')


@app.route('/diagrams')
def diagrams_one():
    return redirect_graphz()

@app.route('/rshstmt')
def redirect_rshstmt():
    return page_redirect('https://www.overleaf.com/7678327114txpgtbjcqswn')

@app.route('/dashes')
def redirect_dashes():
    return page_redirect('https://www.cyberciti.biz/faq/unix-linux-remove-strange-names-files/')

@app.route('/python_split')
def redirect_python_split():
    return page_redirect('https://raw.githubusercontent.com/franceme/Scripts/master/jupyter_split.py')

@app.route('/preview_planning')
def redirect_preview_planning():
    return page_redirect('https://docs.google.com/document/d/1kYioS4KSfYTMmStAq9yTs95Enn_80CFQjLWxs6B1fvI/edit#')

@app.route('/python_shell_root')
def redirect_python_shell_root():
    return page_redirect('https://raw.githubusercontent.com/franceme/Scripts/master/python_shell_root.sh')

@app.route('/my_adobe')
def redirect_my_adobe():
    return page_redirect('https://acrobat.adobe.com/link/documents/agreements/?locale=en-US#agreement_type=all')

@app.route('/splyt')
def redirect_splyt():
    return page_redirect('https://raw.githubusercontent.com/franceme/Scripts/master/split.py')

@app.route('/climbers')
def redirect_climbers():
    return page_redirect('https://portal.rockgympro.com/portal/public/4a70c60d7428aa6e2ae64baef2665766/occupancy')

@app.route('/os_defcon')
def redirect_os_defcon():
    return page_redirect('https://www.defconlevel.com/current-level.php')

@app.route('/acm_latex')
def redirect_acm_latex():
    return page_redirect('https://www.acm.org/publications/taps/accepted-latex-packages')

@app.route('/vt_preview')
def redirect_vt_preview():
    return page_redirect('https://app.slack.com/client/T0354KNE2AU/D034FAMSCAF')

@app.route('/verizon_colors')
def redirect_verizon_colors():
    return page_redirect('https://www.verizon.com/business/small-business-essentials/resources/truth-best-worst-call-action-button-colors-website-212506540/')

@app.route('/signup_previewweekend')
def redirect_signup_previewweekend():
    return page_redirect('https://docs.google.com/spreadsheets/d/1JRcB5vZFhJhlYfSFHs_PDS6ieOJXmmtDlKRdRP0Ov4o/edit?usp=sharing')

@app.route('/vt_graduate')
def redirect_vt_graduate():
    return page_redirect('https://ess.graduateschool.vt.edu/')

@app.route('/vt_weekend')
def redirect_vt_weekend():
    return page_redirect('https://join.slack.com/t/slack-anm6806/shared_invite/zt-144gcog52-xb_TUoSSB90QfgmRutmhyQ')

@app.route('/python_get')
def redirect_python_get():
    return page_redirect('https://raw.githubusercontent.com/franceme/staticpy/master/python.sh')

@app.route('/python_shell')
def redirect_python_shell():
    return page_redirect('https://raw.githubusercontent.com/franceme/Scripts/master/python_shell.sh')

@app.route('/good_guy_with_gun')
def redirect_good_guy_with_gun():
    return page_redirect('https://www.nbcnews.com/news/us-news/father-arrested-ordering-son-4-shoot-officers-mcdonalds-drive-thru-pol-rcna17130')

@app.route('/my_sok')
def redirect_my_sok():
    return page_redirect('https://oaklandsok.github.io/')

@app.route('/sok')
def redirect_sok():
    return page_redirect('https://oaklandsok.github.io/')

@app.route('/mendeley')
def redirect_mendeley():
    return page_redirect('https://www.mendeley.com/reference-manager/library/all-references')

@app.route('/my_mendeley')
def redirect_my_mendeley():
    return page_redirect('https://www.mendeley.com/reference-manager/library/all-references')

@app.route('/roa_hookah')
def redirect_roa_hookah():
    return page_redirect('https://www.google.com/maps/place/Shishka+Mediterranean+Grill+and+Hookah+Bar/@37.2715551,-79.9403762,17z/data=!3m1!5s0x884d0d94e23c50ff:0x2fc8c19f220c8bb7!4m9!1m2!2m1!1shookah+bar+roanoke!3m5!1s0x884d0d94e29880f3:0xd7bf3d1c517b8608!8m2!3d37.2719034!4d-79.9384901!15sChJob29rYWggYmFyIHJvYW5va2VaFCISaG9va2FoIGJhciByb2Fub2tlkgEKaG9va2FoX2JhcpoBJENoZERTVWhOTUc5blMwVkpRMEZuU1VOQmVVbEVVVEZuUlJBQg')

@app.route('/zoom_meet')
def redirect_zoom_meet():
    return page_redirect('https://virginiatech.zoom.us/j/81615358434?pwd=b2hiUi82M3BpR2hxVUdYeVkxUEdadz09')

@app.route('/g_tasks')
def redirect_g_tasks():
    return page_redirect('https://script.google.com/a/macros/vt.edu/s/AKfycbxd5gSRyM9Z0AYLfMWFOZqDT8Kfw6WNYhO5ooYgC4y_oXzn3zdwBfXnnhbQwGtGkPxxjg/exec')

@app.route('/frantzme_webresume')
def redirect_frantzme_webresume():
    return page_redirect('https://sway.office.com/Jj48pkUIdjvnStcP?ref=Link')

@app.route('/my_grad')
def redirect_my_grad():
    return page_redirect('https://virginiatech-my.sharepoint.com/:w:/r/personal/frantzme_vt_edu/_layouts/15/Doc.aspx?sourcedoc=%7B99B220B3-8EE3-43E1-AAFE-900D9AA430D4%7D&file=Graduation_Plan.docx&action=default&mobileredirect=true')

@app.route('/grad')
def redirect_grad():
    return page_redirect('https://virginiatech-my.sharepoint.com/:w:/r/personal/frantzme_vt_edu/_layouts/15/Doc.aspx?sourcedoc=%7B99B220B3-8EE3-43E1-AAFE-900D9AA430D4%7D&file=Graduation_Plan.docx&action=default&mobileredirect=true')

@app.route('/fun_rt')
def redirect_fun_rt():
    return page_redirect('https://forum.xda-developers.com/t/desktop-apps-ported-to-windows-rt.2092348/')

@app.route('/thenticate')
def redirect_thenticate():
    return page_redirect('https://shibboleth.turnitin.com/shibboleth/ithenticate')

@app.route('/ithenticate')
def redirect_ithenticate():
    return page_redirect('https://shibboleth.turnitin.com/shibboleth/ithenticate')

@app.route('/mythenticate')
def redirect_mythenticate():
    return page_redirect('https://shibboleth.turnitin.com/shibboleth/ithenticate')

@app.route('/my_feedly')
def redirect_my_feedly():
    return page_redirect('https://feedly.com/i/collection/content/user/420bc1de-a3e3-4023-84fa-752509fde431/category/global.all')

@app.route('/feedly')
def redirect_feedly():
    return redirect_my_feedly()

@app.route('/vt_linkedin')
def redirect_vt_linkedin():
    return page_redirect('https://www.linkedin.com/learning-login/?redirect=https%3A%2F%2Fwww.linkedin.com%2Flearning%2Fsearch%3Fkeywords%3D%26trk%3Dhomepage-basic_guest_nav_menu_learning&fromSignIn=true&trk=learning-serp_nav-header-signin&upsellOrderOrigin=homepage-basic_guest_nav_menu_learning')

@app.route('/vt_year')
def redirect_vt_year():
    return page_redirect('https://www.registrar.vt.edu/dates-deadlines/academic-calendar/2021-2022.html')

@app.route('/_live')
def redirect__live():
    return page_redirect('https://mybinder.org/v2/gh/franceme/Esorics\_Conference/HEAD')

@app.route('/g_task')
def redirect_g_task():
    return page_redirect('https://tasks.google.com/embed/?origin=https://calendar.google.com&fullWidth=1')

@app.route('/spresso4')
def redirect_spresso4():
    return page_redirect('https://tracking.narvar.com/nespresso/tracking/fedex?t=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiIsImlzc3VlciI6Im1lc3NhZ2luZyIsImtpZCI6ImtleTEifQ.eyJvcmRlcl9udW1iZXIiOiIxMDQxMTMxNjQiLCJ0cmFja2luZ19udW1iZXJzIjoiNTYwNjQ2MzUwMDMzIn0.bI1Tnmbb4SXyxTvGYF9sW-Iv6RrxGP3BC73UJFvqNv4&bzip=24060&src=email&locale=en_us&customer_id=e5826fe0-dadf-35b4-a97e-b1bc5e7e302a&campaign_id=delivery_anticipation_standard&nrfid=f060acba-55d9-473d-9fe5-4c87a8314d8c&ncid=0c83f57c786a0b4a39efab23731c7ebc')

@app.route('/g_out')
def redirect_g_out():
    return page_redirect('https://accounts.google.com/Logout')

@app.route('/vt_training')
def redirect_vt_training():
    return page_redirect('https://www.citiprogram.org/Shibboleth.sso/Login?target=https://www.citiprogram.org/Secure/Welcome.cfm?inst=1684&entityID=urn:mace:incommon:vt.edu')

@app.route('/vt_irb')
def redirect_vt_irb():
    return page_redirect('https://secure.research.vt.edu/irb/')

@app.route('/cryptolation_paper')
def redirect_cryptolation_paper():
    return page_redirect('https://www.overleaf.com/8484473529hrpfwmbkpbdb')

@app.route('/overleaf')
def redirect_overleaf():
    return page_redirect('https://www.overleaf.com/')

@app.route('/vt_writing')
def redirect_vt_writing():
    return page_redirect('https://vt.mywconline.com/')

@app.route('/signin_issue')
def redirect_signin_issue():
    return page_redirect('https://drive.google.com/file/d/1DohU5wM4IreDmOBTCXhn8MPvm-lqE-SS/view?usp=sharing')

@app.route('/spresso3')
def redirect_spresso3():
    return page_redirect('https://nespresso.narvar.com/nespresso/tracking/lasership?tracking_numbers=1LSCY8X000L0Z2B&service=ST&ozip=33702&dzip=24060-2095&order_number=102017362')

@app.route('/spresso2')
def redirect_spresso2():
    return page_redirect('https://nespresso.narvar.com/nespresso/tracking/fedex?tracking_numbers=948810876101&service=&ozip=45069&dzip=24060-2095&order_number=101667647')

@app.route('/spresso')
def redirect_spresso():
    return page_redirect('https://tracking.narvar.com/nespresso/tracking/lasership?t=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiIsImlzc3VlciI6Im1lc3NhZ2luZyIsImtpZCI6ImtleTEifQ.eyJvcmRlcl9udW1iZXIiOiIxMDExMzE1ODIiLCJ0cmFja2luZ19udW1iZXJzIjoiMUxTQ1k4WDAwMEpTUU9RIn0.lwvSq-Z2pznAlY8z6B48rvPl5EXmaIu1zhTKcEcPB_w&bzip=24060&src=email&locale=en_us&customer_id=9125f2e7-c3b2-3b81-8a03-f81a829230a7&campaign_id=delivery_anticipation_standard&nrfid=c600d909-c965-4e20-b71a-a8b2a686d7eb&ncid=0c83f57c786a0b4a39efab23731c7ebc')

@app.route('/dimension202')
def redirect_dimension202():
    return page_redirect('https://www.reddit.com/user/pineappleretrograde/comments/orb0i3/sharing_is_caring/?utm_source=share&utm_medium=web2x&context=3')

@app.route('/dimension20')
def redirect_dimension20():
    return page_redirect('https://www.reddit.com/r/Piracy/comments/nztzku/dropouttv_content_is_impossible_to_find/')

@app.route('/resolution_2021E')
def redirect_resolution_2021E():
    return page_redirect('https://gpss.vt.edu/content/gpss_vt_edu/en/the-senate/resolutions/_jcr_content/content/vtmultitab/vt-items_2/download_2110540057/file.res/(7)%20GPSS%20Resolution%202021-22E%20(Change%20transition%20of%20power).pdf')

@app.route('/resolution_2021B')
def redirect_resolution_2021B():
    return page_redirect('https://gpss.vt.edu/content/gpss_vt_edu/en/the-senate/resolutions/_jcr_content/content/vtmultitab/vt-items_2/download_1407676851/file.res/(3)%20GPSS%20Resolution%202021-22B%20(Assistantship%20extension%20from%209%20to%2012%20months%20by%20default).pdf')

@app.route('/resolution_2021A')
def redirect_resolution_2021A():
    return page_redirect('https://gpss.vt.edu/content/gpss_vt_edu/en/the-senate/resolutions/_jcr_content/content/vtmultitab/vt-items_2/download_999411592/file.res/(1_2)%20GPSS%20resolution%202021-22A%20(Task%20force%20policy).pdf')

@app.route('/NREL_Slides')
def redirect_NREL_Slides():
    return page_redirect('https://virginiatech-my.sharepoint.com/:p:/g/personal/frantzme_vt_edu/EX8-SBr5E8hGlUgwNEMggH4BGHlItf1ESxWlejbjLOdxFA?e=HPTdu6')

@app.route('/frantzme_cryptolation')
def redirect_frantzme_cryptolation():
    return page_redirect('https://docs.google.com/document/d/1U1ozi2FteI86Rb-OkGRJ8VqK2kJ22JYi/edit#heading=h.gjdgxs')

@app.route('/JavaVis')
def redirect_JavaVis():
    return page_redirect('https://pythontutor.com/java.html#mode=edit')

@app.route('/frantzme_contacts')
def redirect_frantzme_contacts():
    return page_redirect('https://docs.google.com/document/d/1HhZwyFzxgQVdL8iPMkvOrSdZmSY3iaNv/edit#bookmark=id.bg057vnr5q8w')

@app.route('/csgc_cscompact')
def redirect_csgc_cscompact():
    return page_redirect('https://drive.google.com/file/d/1ind38gD_62ctcKn8I83IIe3gH_oCjffI/view?usp=sharing')

@app.route('/frantzme_transcript_grad')
def redirect_frantzme_transcript_grad():
    return page_redirect('https://drive.google.com/file/d/192BTnc1YdIkmdMpnTAWJ-cvM3cjbcz8o/view?usp=sharing')

@app.route('/frantzme_transcript_undergrad')
def redirect_frantzme_transcript_undergrad():
    return page_redirect('https://drive.google.com/file/d/1FfpMv0saG-SMEBpmogmt-y4OwGM3YNAU/view?usp=sharing')

@app.route('/frantzme_references')
def redirect_frantzme_references():
    return page_redirect('https://docs.google.com/document/d/1HhZwyFzxgQVdL8iPMkvOrSdZmSY3iaNv/edit#bookmark=id.ssksbd1dnsbb')

@app.route('/frantzme_transcript')
def redirect_frantzme_transcript():
    return page_redirect('https://drive.google.com/file/d/192BTnc1YdIkmdMpnTAWJ-cvM3cjbcz8o/view?usp=sharing')

@app.route('/ridebt')
def redirect_ridebt():
    return page_redirect('https://ridebt.org/routes-schedules?route=CRC')

@app.route('/frantzme_ms_thesis')
def redirect_frantzme_ms_thesis():
    return page_redirect('https://drive.google.com/file/d/1ZnKPDYF_rlFeS6pGdcfLIeaqs_-bTZ3I/view?usp=sharing')

@app.route('/frantzme_cryptoguard_poster')
def redirect_frantzme_cryptoguard_poster():
    return page_redirect('https://drive.google.com/file/d/12MPEaDSBt_d73jlRaeoy2-RIzGQPX2MR/view?usp=sharing')

@app.route('/frantzme_cryptoguard_ccs')
def redirect_frantzme_cryptoguard_ccs():
    return page_redirect('https://drive.google.com/file/d/1ltQnGlsAeLQAnpWOQHpH-X5qhJ0VHL1h/view?usp=sharing')

@app.route('/frantzme_cv')
def redirect_frantzme_cv():
    return page_redirect('https://drive.google.com/file/d/18qCa6lW4718-tTrpE5_H5Nr0s6ssG5Na/view?usp=sharing')

@app.route('/secdev')
def redirect_secdev():
    return page_redirect('https://mybinder.org/v2/gh/franceme/cryptoguard/2020_SecDev_Tutorial?filepath=SecDev_Tutorial.ipynb')

@app.route('/mac_dockersock')
def redirect_mac_dockersock():
    return page_redirect('https://forums.docker.com/t/how-is-var-run-docker-sock-created-on-mac-if-docker-daemon-runs-in-hyperkit-vm-on-linux/29090')

@app.route('/frantzme_resume')
def redirect_frantzme_resume():
    return page_redirect('https://drive.google.com/file/d/1wq_hU272QvwmW1Cj1on7MaufEvGxzA7C/view?usp=sharing')

@app.route('/win_vm')
def redirect_win_vm():
    return page_redirect('https://developer.microsoft.com/en-us/windows/downloads/virtual-machines/')

@app.route('/OrderMyCoffvffeeGio')
def redirect_OrderMyCoffvffeeGio():
    return page_redirect('https://docs.google.com/spreadsheets/d/1vGKLvXUXAskXRrwGfjVRgsYpGMYWQkXUWsroRIDCyRo/edit#gid=0')

@app.route('/esorics_rsc')
def redirect_esorics_rsc():
    return page_redirect('https://github.com/franceme/Esorics_Conference')

@app.route('/esorics')
def redirect_esorics():
    return page_redirect('https://mybinder.org/v2/gh/franceme/Esorics_Conference/HEAD')

@app.route('/racist')
def redirect_racist():
    return page_redirect('https://gobblerconnect.vt.edu/organization/turning-point-usa')

@app.route('/cs4264')
def redirect_cs4264():
    return page_redirect('https://docs.google.com/document/d/1sEyssZ3D7n0bri_gi-JLdxzN5X3BP9pQ/edit?usp=sharing&ouid=103289071436703194896&rtpof=true&sd=true')

@app.route('/docker_noroot')
def redirect_docker_noroot():
    return page_redirect('https://askubuntu.com/questions/477551/how-can-i-use-docker-without-sudo')

@app.route('/remote_python')
def redirect_remote_python():
    return page_redirect('https://www.jetbrains.com/help/idea/configuring-remote-python-sdks.html')

@app.route('/dev_docker')
def redirect_dev_docker():
    return page_redirect('https://www.codemag.com/article/1811021/Docker-for-Developers')

@app.route('/where_multiplayer')
def redirect_where_multiplayer():
    return page_redirect('https://www.co-optimus.com/games.php')

@app.route('/noelectron')
def redirect_noelectron():
    return page_redirect('https://medium.com/how-to-electron/how-to-get-source-code-of-any-electron-application-cbb5c7726c37')

@app.route('/python_mergeexcel')
def redirect_python_mergeexcel():
    return page_redirect('https://stackoverflow.com/questions/66531396/export-pandas-dataframe-to-xlsx-dealing-with-the-openpyxl-issue-on-python-3-9')

@app.route('/cryptolation')
def redirect_cryptolation():
    return page_redirect('https://www.overleaf.com/project/60d0e570b35a8f3484896e1a')

@app.route('/my_img')
def redirect_my_img():
    return page_redirect('https://pixlr.com/e')

@app.route('/my_ocr')
def redirect_my_ocr():
    return page_redirect('https://brandfolder.com/workbench/extract-text-from-image')

@app.route('/vt_parking')
def redirect_vt_parking():
    return page_redirect('https://parking.vt.edu/permits.html')

@app.route('/my_pdf')
def redirect_my_pdf():
    return page_redirect('https://localpdf.tech/')

@app.route('/humes')
def redirect_humes():
    return page_redirect('https://hume.vt.edu/education-outreach/graduate-research-assistantships/deloitte-graduate-student-research-program.html')

@app.route('/Takex')
def redirect_Takex():
    return page_redirect('https://news.ycombinator.com/item?id=27325431')

@app.route('/TekaPoint')
def redirect_TekaPoint():
    return page_redirect('https://news.ycombinator.com/item?id=27768680')

@app.route('/sazzadur')
def redirect_sazzadur():
    return page_redirect('https://www.overleaf.com/project/5d782318e69fb10001d91878')

@app.route('/kriminal')
def redirect_kriminal():
    return page_redirect('https://www.salon.com/2021/07/14/gop-rep-on-cyber-committee-dumped-msft-stock-shortly-before-10b-pentagon-contract-was-scrapped/')

@app.route('/sexist')
def redirect_sexist():
    return page_redirect('https://boingboing.net/2021/07/13/people-who-turn-in-women-seeking-abortions-are-eligible-for-a-10000-reward-in-texas.html')

@app.route('/KWII_Printer')
def redirect_KWII_Printer():
    return page_redirect('http://adder.cs.vt.edu/wcd/print.xml')

@app.route('/docker_env')
def redirect_docker_env():
    return page_redirect('https://levelup.gitconnected.com/a-great-local-development-environment-is-not-a-nice-to-have-but-a-must-have-ed678ba4c8ed')

@app.route('/vt_vaccine')
def redirect_vt_vaccine():
    return page_redirect('https://ready.vt.edu/?utm_source=cmpgn_news&utm_medium=email&utm_campaign=vtUnirelNewsDailyCMP_070121-fs')

@app.route('/conferences')
def redirect_conferences():
    return page_redirect('http://www.plantuml.com/plantuml/svg/XPD1Yzim48Nl-olcr4D0rYQdqjCQDIs6JGWefOLbMRJZIIomPAEHcys_hnsvnFMcxCL8wBqtxnlm0qSJehE-TAQzMu1g_842UII-MopWwQcAiVqYvS5WLyTpXfn5uxgCoauUk-P0LZBX2_Qs5uucPbLqe0cxOEFv-RdFMC3UKe3bS9m4dawdp1AHu56SDU4ezqhgdIXyIMz3KWtwqowbpAniZspmua7af5LA_wlbKTmnUVkMn5S--Nhsnf5Std-67tgzBNxTTlkIMV3PjGtRpbrIOFjLwodTwaP5WtyRGgwqUeVHKfobxjPx_JzQR5nIqM_oaQLrAAumK6pIW8zNhFItdoTwbT0VUeiGa1VzLy3c4GvDW41jCzp5P0qMwv0XGg4UUyliSMYH1M8o0QjmcL4rZgJZ85RtgoLiT4YkMJLacY3mu8H2gtKIJoPus_8mVblizFZudJm5Ky-wfBqROnFfDLlcULx8oqjRjJ3SteDOT7MYt0oO3-JBySVu0m00')

@app.route('/scolar')
def redirect_scolar():
    return page_redirect('https://scholar.google.com/citations?user=RKKj9VgAAAAJ')

@app.route('/ssok')
def redirect_ssok():
    return page_redirect('https://oaklandsok.github.io')

@app.route('/muzic')
def redirect_muzic():
    return page_redirect('https://open.spotify.com/playlist/3Zzn4YJ0PHe4OpSfD5E0U2?si=0769860a7f6445f0&nd=1')

@app.route('/graduateme')
def redirect_graduateme():
    return page_redirect('https://docs.google.com/document/d/1cx7iiqP4c33yA-Yh2jNklh_ZLLMDJEtj/edit#')

@app.route('/BestBreakfast')
def redirect_BestBreakfast():
    return page_redirect('https://youtu.be/k1BneeJTDcU?t=86')

@app.route('/PipelineZeroMultifactorOne')
def redirect_PipelineZeroMultifactorOne():
    return page_redirect('https://beta.darkreading.com/attacks-breaches/colonial-pipeline-ceo-ransomware-attack-started-via-pilfered-legacy-vpn-account')

@app.route('/bigdick')
def redirect_bigdick():
    return page_redirect('https://franceme.github.io')

@app.route('/programmingpatterns')
def redirect_programmingpatterns():
    return page_redirect('https://docs.google.com/presentation/d/17mrn7T3GHAeFIE5LXJIqxldbGF6WffrXRxAw6AVS09k/edit#slide=id.gcec2ece6a6_0_48')

@app.route('/csgc')
def redirect_csgc():
    return page_redirect('https://csgrad.cs.vt.edu/')

@app.route('/smartware')
def redirect_smartware():
    return page_redirect('https://github.com/Malware-Research/Resources')

@app.route('/telatex')
def redirect_telatex():
    return page_redirect('https://www.latex-tables.com/#')

@app.route('/xelatex')
def redirect_xelatex():
    return page_redirect('https://www.latex-tables.com/#')

@app.route('/31ph985')
def redirect_31ph985():
    return page_redirect('https://fifty.user-interface.io/50_ui_tips.pdf')

@app.route('/latex_table')
def redirect_latex_table():
    return page_redirect('https://texblog.org/2012/07/30/single-column-figuretable-in-a-two-multi-column-environment/')

@app.route('/ml_metrics')
def redirect_ml_metrics():
    return page_redirect('https://en.wikipedia.org/wiki/Precision_and_recall')

@app.route('/delatex')
def redirect_delatex():
    return page_redirect('https://detexify.kirelabs.org/classify.html')

@app.route('/cryptoguard')
def redirect_cryptoguard():
    return page_redirect('https://github.com/franceme/cryptoguard')

@app.route('/DarkSideAttack')
def redirect_DarkSideAttack():
    return page_redirect('https://docs.google.com/document/d/1JFj4P7S4XKGE-xGusa1lMnQKloKB3dP7/preview')

@app.route('/vt_contract')
def redirect_vt_contract():
    return page_redirect('https://apps.es.vt.edu/gradcontract/home/contract/index')

@app.route('/apt')
def redirect_apartment_finding():
    return page_redirect('https://www.google.com/maps/d/edit?mid=1rGzYJrLlP7jXkLxEG1uGb2yIiy8YbCY')

@app.route('/iceberg')
def redirect_vt_contracticeburg():
    return page_redirect('https://suricrasia.online/iceberg/')

@app.route('/md_folder')
def redirect_md_folder():
    return page_redirect('https://www.w3schools.io/file/markdown-folder-tree/')

@app.route('/HokieSpa')
def redirect_HokieSpa():
    return page_redirect('https://banweb.banner.vt.edu/ssb/prod/twbkwbis.P_GenMenu?name=bmenu.P_StuMainMnu')

@app.route('/vt_365')
def redirect_vt_365():
    return page_redirect('https://login.microsoftonline.com/?whr=virginiatech.onmicrosoft.com')

@app.route('/365')
def redirect_365():
    return redirect_vt_365()

@app.route('/odrive')
def redirect_odrive():
    return redirect_vt_365()

@app.route('/gdrive')
def redirect_gdrive():
    return page_redirect('https://drive.google.com')

@app.route('/idrive')
def redirect_idrive():
    return page_redirect('https://www.icloud.com/iclouddrive/')

@app.route('/myvt')
def redirect_myvt():
    return page_redirect('https://onecampus.vt.edu/')

@app.route('/frantzme')
def redirect_frantzme():
    return page_redirect('https://franceme.github.io/')

@app.route('/cryptoguard4py')
def redirect_cryptoguard4py():
    return page_redirect('https://github.com/franceme/CryptoGuard4Py')

#Add Secure Pages Here


@app.route('/secure_timeline.html')
def secure_get_timeline():
    return easy_add_file('secure/timeline.html')


@app.route('/secure_useful.html')
def secure_get_useful():
    return easy_add_file('secure/useful.html')


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

def get_base(title, co_name, _from, _to, desc, is_info=True, color=None, html_id=None):
    base_color = "timeline-card-info" if is_info else "timeline-card-success"

    if color is not None:
        color = f"timeline-card-{color}"

    stripi = lambda x:None if x.strip() == '' else x.strip()
    _from = stripi(_from)
    _to = stripi(_to)

    if _from is not None and _to is not None:
        date_string = _from + " - " + _to
    elif _from is None and _to is not None:
        date_string = _to
    elif _from is not None and _to is None:
        date_string = _from
    else:
        date_string = ""

    if co_name is not None and co_name.strip() != "":
        co_name = f" at {co_name}"

    if html_id is not None:
        html_id = f"id='{html_id}'"

    return render_template_string(f"""
<div class="timeline-card {color or base_color}" data-aos="fade-in" data-aos-delay="0" {color} {html_id}>
    <div class="timeline-head px-4 pt-3">
    <div class="h5">{title} <span class="text-muted h6">{co_name}</span></div>
    </div>
    <div class="timeline-body px-4 pb-4">
    <div class="text-muted text-small mb-3">{date_string}</div>
    <div>{desc}</div>
    </div>
</div>
""")

app.jinja_env.filters['get_base'] = get_base

def get_ref(name, title, desc,left_side=True):

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

def get_main_url(page_name, extra_info=''):
    page_name = str(page_name)
    return render_template_string(f""" <a href="/{page_name.lower()}.html">{page_name.title()}_{extra_info}</a> """)

app.jinja_env.filters['get_main_url'] = get_main_url

def arg(string):
    return __name__ == "__main__" and len(
        sys.argv) > 1 and sys.argv[0].endswith('setup.py') and str(sys.argv[1]).upper().replace("--",'') == str(string).upper()

if arg('build'):
    freezer.freeze()
    sys.exit(0)
elif arg('addsecurepages'):
    add_secure_pages(sys.argv[2:])
    sys.exit(0)
elif arg('run'):
    port = int(sys.argv[2]) if len(sys.argv) >= 3 else 8899
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
            'flask==3.0.1',
            'flask_flatpages==0.7.3',
            'frozen_flask==1.0.1',
            'pygments==2.10.0',
            'elsa==0.1.6',
            'feedgen==0.9.0',
            'werkzeug==3.0.0' #https://stackoverflow.com/questions/71661851/typeerror-init-got-an-unexpected-keyword-argument-as-tuple#answer-71662972
        ]
)
