#!/usr/bin/env python3
#region Imports
import setuptools
import sys
import os
import base64
import mystring

import flask
import flask_frozen
import flask_flatpages
from feedgen.feed import FeedGenerator

#endregion
#region Core Imports
base_info = {
    'name':"Dr. Miles Frantz",
    'title':"Ph.D. Lead Associate at Peraton Labs",
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
    """
    Reads the content of a file.

    Args:
        filename (str): The name of the file to read.
        base (str, optional): The base directory to prepend to the filename. Defaults to None.

    Returns:
        str: The content of the file if it is successfully read.
        str: An error message if an IOError occurs.
    """
    try:
        if base:
            src = os.path.join(base,filename)
        else:
            src = filename
        return open(src).read()
    except IOError as exc:
        return mystring.string.str(exc)

rendre = lambda page:flask.render_template_string(get_file(page),mimetype="text/html",dyct=base_info)

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'
FLATPAGES_HTML_RENDERER = lambda text: flask_flatpages.pygmented_markdown(flask.render_template_string(text))
FLATPAGES_MARKDOWN_EXTENSIONS = ['codehilite']
FREEZER_IGNORE_MIMETYPE_WARNINGS = True

app = flask.Flask(
    __name__,
    static_url_path='',
    static_folder='static',
)
app._current_rules = lambda: [x.endpoint for x in app.url_map.iter_rules()]

app.config.from_object(__name__)
pages = flask_flatpages.FlatPages(app)
freezer = flask_frozen.Freezer(app)

#endregion
#region API URLs
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
    """
    Processes and returns the contents of a file or a string, with optional content type and file handling.

    Args:
        contents (str): The content to be processed. This can be a string or a file path.
        contenttype (str, optional): The MIME type of the content. Defaults to 'text/html'.
        pullcontent (bool, optional): If True, the function will attempt to read the contents from a file. Defaults to False.

    Returns:
        tuple: A tuple containing the processed content, HTTP status code, and a dictionary of headers.
    """
    if not pullcontent or not os.path.exists(contents):
        return contents, 200, {'Content-Type':contenttype}

    raw_contents = None
    with open(contents,'r') as reader:
        raw_contents = reader.readlines()

    if contents.endswith(".csv"): #Hard Test
        output = flask.make_response(raw_contents)
        output.headers["Content-Disposition"] = "attachment; filename=export.csv"
        output.headers["Content-type"] = "text/csv"
        return output
    elif contents.endswith(".json"): #Hard Test
        output = flask.make_response(raw_contents)
        output.headers["Content-Disposition"] = "attachment; filename=export.json"
        output.headers["Content-type"] = "text/json"
        return output

    return '\n'.join(raw_contents), 200, {'Content-Type':contenttype}

def easy_add_file(file):
    return easy_add_page(open(file).read())

def add_secure_pages(pagepaths):
    """
    Adds secure routes for the given list of page paths to the Flask application.

    This function reads the current file and inserts Flask route definitions for each
    page path provided in the `pagepaths` list. The routes are added at the location
    marked by the comment "#Add Secure Pages Here".

    Args:
        pagepaths (list): A list of file paths to be added as secure pages. The paths
                          can be for HTML files or other file types such as Python,
                          Java, Rust, CSV, JSON, and XML.

    The function distinguishes between HTML files and other file types. For HTML files,
    it creates a route that serves the file directly. For other file types, it creates
    a route that serves the file with a 'text/plain' content type and determines whether
    to pull the content based on the file extension.

    Example:
        add_secure_pages(['path/to/page1.html', 'path/to/script.py'])

    Note:
        This function modifies the current file in place.
    """
    from fileinput import FileInput as finput
    with finput(__file__, inplace=True, backup=False) as file:
        for line in file:
            if line.startswith("#Add Secure Pages Here"):
                print(line)
                for pagepath in pagepaths:
                    if pagepath.endswith('.html') or pagepath.endswith('.htm'):
                        secure_page_name = mystring.string.str(pagepath.split("/")[-1]).replace('.html','').replace("*","")
                        print(f"""
@app.route('/secure_{secure_page_name}.html')
def secure_get_{secure_page_name}():
    return easy_add_file('{pagepath}')
""")
                    else:
                        secure_page_name = mystring.string.str(pagepath.split("/")[-1])#.split('.')[0]
                        pull_content=any([secure_page_name.endswith("."+mystring.string.str(x)) for x in [
                            'py','java','rs','csv','json','xml',
                        ]])
                        print(f"""
@app.route('/secure_{secure_page_name.split('.')[0]}.html')
def secure_get_{secure_page_name.split('.')[0]}():
    return easy_add_page('{pagepath}','text/plain',pullcontent={pull_content})
""")
            else:
                print(line, end='')
#endregion
#region EZ Routes

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

def create_dynamic_function(name, code):
    """
    Creates a new function dynamically.

    Args:
        name (str): The name of the function.
        code (str): The code of the function as a string.

    Returns:
        function: The dynamically created function.
    """
    exec(code)
    return locals()[name]

for route, url in {
    #Python Packages
    '/pyprep':'https://raw.githubusercontent.com/franceme/staticpy/master/prep.py',
    '/xpiz':'https://raw.githubusercontent.com/franceme/staticpy/master/xpizr.py',
    '/pyup':'https://raw.githubusercontent.com/franceme/staticpy/master/up.py',
    '/pyfollow':'https://raw.githubusercontent.com/franceme/staticpy/master/follow.py',
    '/pymux':'https://raw.githubusercontent.com/franceme/staticpy/master/mux.py',
    '/pycmtr':'https://raw.githubusercontent.com/franceme/staticpy/master/cmt.py',
    '/pyez':'https://raw.githubusercontent.com/franceme/staticpy/master/ezgit.py',
    '/pyshark':'https://raw.githubusercontent.com/franceme/staticpy/master/shark.py',
    '/pydockinstall':'https://raw.githubusercontent.com/franceme/staticpy/master/in_docker.py',
    '/pyvb':'https://raw.githubusercontent.com/franceme/staticpy/master/vb.py',
    '/pydock':'https://raw.githubusercontent.com/franceme/staticpy/master/pydock.py',
    '/python_get':'https://raw.githubusercontent.com/franceme/staticpy/master/python.sh',
    '/python_shell':'https://raw.githubusercontent.com/franceme/Scripts/master/python_shell.sh',
    '/python_shell_root':'https://raw.githubusercontent.com/franceme/Scripts/master/python_shell_root.sh',
    '/python_split':'https://raw.githubusercontent.com/franceme/Scripts/master/jupyter_split.py',
    '/python_save':'https://raw.githubusercontent.com/franceme/staticpy/master/ipython_save.py',
    '/py_task':'https://raw.githubusercontent.com/franceme/Scripts/master/tasks.py',
    '/pyzz':'https://raw.githubusercontent.com/franceme/staticpy/master/zz.py',
    '/pyhook':'https://raw.githubusercontent.com/franceme/staticpy/master/hook.py',
    '/pypyg':'https://github.com/Kanaries/pygwalker',
    '/splyt':'https://raw.githubusercontent.com/franceme/Scripts/master/split.py',
    '/gsync':'https://raw.githubusercontent.com/franceme/staticpy/master/gsync.py',
    '/ghspace':'https://raw.githubusercontent.com/franceme/staticpy/master/ghspace.py',

    #Tech Utils
    '/balget':'https://raw.githubusercontent.com/franceme/staticpy/master/bal_install.sh',
    '/pyscriptBadge':'https://github.com/franceme/py_scripts/actions/workflows/builder.yml/badge.svg',
    '/win_vm':'https://web.archive.org/web/20211114225054/https://developer.microsoft.com/en-us/microsoft-edge/tools/vms/',
    '/to_qr':'https://demos.hankruiger.com/kuu_er/',
    '/on_qr':'https://faizrktm.github.io/barcode-reader-wasm/',
    '/rechrome':'https://remotedesktop.google.com/access',
    '/installgh':'https://raw.githubusercontent.com/franceme/staticpy/master/install_gh.sh',
    '/sulis':'https://github.com/Grokmoo/sulis/releases/download/0.6.0/sulis-0.6.0-linux64.zip',
    '/mmail':'https://dropmail.me/en/',
    '/semgrep_rules_cut':'https://drive.google.com/file/d/1J4OBlhfJZvuXP7Sb54tru31L-eRFM9Ly/view?usp=sharing',
    '/bashrc':'https://raw.githubusercontent.com/franceme/Scripts/master/bashrc.txt',
    '/hugface':'https://www.plantuml.com/plantuml/svg/fPDTgzD048RlpwyOwEKXk_QWWbvLYRL2rM8jNfIoR3QJP37xmUx4sd_lcezI46dBkSlxPERPpGnPH9A1ZBQbaVxX4VRxXiZ7jvmtNLrhMrTI8LCELaDSfXWFXuV7_vVoqgcOMC6J5N_3DwoxLeR90Bq2tcq-zPfhdbAIZ4YH_vgp-Pozc828552QLCuQCYrifmYv97cd-eczJ6Qqt4lrKzOe0bOOq2hahPDbQXG6gN5bd4rDxEyBCIPO3rMG3_ckuwyVUjP_7lBzWtkTFg_pbrVkfpORM5O5Pp9_eiPPsFK8bWd1Pa0Pv5-_V8VTziDjcpypqNG5l4SYlBx-csIySSUCNDRvOVtZRNklRZ4-nrcwensjUNhyrtkXhJMbJgQSuLMGLg51lbL1UugyQ5t1ZOo4WLUTBR1DK0XjDGd1_6csVlNc2JvgMgNX_0ZIUmp9lq1RZl_X7m00',
    '/my_dock':'https://www.plantuml.com/plantuml/svg/hPT1RzCm5CVl-nG-WggHEwTH2cYeWufkuZ1DaMERrio9BTiPoxV7oKlSOlMG5tEoNwJ_x_tqQZdDZVFK-beslARcQaKscZqBUrlJWt1NgnLvV3nwRzpxeZX8VsohTqpNnIzB6oPgKUoPbSOxCgvFJo4oCrDGvgLk7Fa0wwoiwKetjjnrPqqnoRJnl7n5dIZvC1oo3dkO4sGnuRGxdb2signQgVW_9W-tQtW6mAN4L6ykZOkNG26Ri3p8FeH8vVKiTUN6lkNt2iAuT6P_mPGqJamEdw0429gIwQAwrybZsxr269NExCyjVTRDfB0PAa1W6PaY1ysrdpo-z0K0a8HCYrhhqy6uwmi080dvTyQ52oFZklWFTuMIVXWCsOOD1179fPrDvu-wYVrtGucsY9JBBdYC5ywVPEv3bGZXK4kdyvk-q3YRhw70JIOXBBNuOqFOWiJFOOznYFdyOzAFKZQ7ywDo3u-Y49wMvLKhaBdR3WRapJVjoUTMgOxih316yBU0cidAKB6jy_6i_0W5xgmaXDG21J7ToMBNHGaq84e023iHnwYYayiUYYY38sJyBXLLIbZPKF1OJsKqmLEYIqB3_tyUtnkJMl8ccXIlho-ZcER26Sg48n_3Tjzl--Otek7ZzyjV',
    '/dock':'https://www.plantuml.com/plantuml/svg/hPT1RzCm5CVl-nG-WggHEwTH2cYeWufkuZ1DaMERrio9BTiPoxV7oKlSOlMG5tEoNwJ_x_tqQZdDZVFK-beslARcQaKscZqBUrlJWt1NgnLvV3nwRzpxeZX8VsohTqpNnIzB6oPgKUoPbSOxCgvFJo4oCrDGvgLk7Fa0wwoiwKetjjnrPqqnoRJnl7n5dIZvC1oo3dkO4sGnuRGxdb2signQgVW_9W-tQtW6mAN4L6ykZOkNG26Ri3p8FeH8vVKiTUN6lkNt2iAuT6P_mPGqJamEdw0429gIwQAwrybZsxr269NExCyjVTRDfB0PAa1W6PaY1ysrdpo-z0K0a8HCYrhhqy6uwmi080dvTyQ52oFZklWFTuMIVXWCsOOD1179fPrDvu-wYVrtGucsY9JBBdYC5ywVPEv3bGZXK4kdyvk-q3YRhw70JIOXBBNuOqFOWiJFOOznYFdyOzAFKZQ7ywDo3u-Y49wMvLKhaBdR3WRapJVjoUTMgOxih316yBU0cidAKB6jy_6i_0W5xgmaXDG21J7ToMBNHGaq84e023iHnwYYayiUYYY38sJyBXLLIbZPKF1OJsKqmLEYIqB3_tyUtnkJMl8ccXIlho-ZcER26Sg48n_3Tjzl--Otek7ZzyjV',
    '/qscala2':'https://notebooks.gesis.org/binder/jupyter/user/almond-sh-examples-tc0zflur/lab',
    '/qscala':'https://www.tutorialspoint.com/scala/scala_quick_guide.htm',
    '/scala':'https://scastie.scala-lang.org',
    '/scalajs':'https://scribble.ninja/',

    #Tech Guides
    '/ondock':'https://www.plantuml.com/plantuml/svg/SoWkIImgoStCIybDBE3IKd39JyvEBUBIqbA8ZiueAIaejjBNpqbCAjOho4cir2tFBCdGJG4hqKlEpzLNyC_BoSnBZOr5rL2UcPsfbvXJ09G2IfTMwEKNfOC5zI76ApY2vHHA2r8IIq2w7LBpKg1k0000',

    #Ideas
    '/pptr':'https://www.plantuml.com/plantuml/svg/RL9DQzj04BtdL-obeSLCDawB71TC7QWRScdT3mWb137MZgHDjJloxifo_dqdaWMbxKKypS3xUBFhc30aPxrns9xDr3Pm5T2ftgRQUdKl2-xLw-tsXxenXlsRizdiD8q2P-hXeKwfZU-rxll-ufcxrEteec2dUqn5_U6m-fpTtbV7pS7kDkhdk5UR8xgseSV7Cm1rPmYZ052VcYub2YyO_c0MZyKlFb0e6-u7xdr7CLdsKMVBj_EhnMMcQ-uXCP3RaG4w2et7HW11QHkAO3qWbAC0j86Vg4XGSe1-JAE-tWns0FxAL35NpHWf4WR9j5-TU5vTNOREotVI4zYE3GeQEnGmAfnRMdMfXEjpda3HMF9fLTf09HzX1tDmwlRxeFAl6KV6TcumidvYB6hhN8lUu78nfM-myqKDneQNTEWvrP8MsnRAm0xaF67gO9YQkK5ybrqlIihKtPTHKtt4aFxNH21ZR1eC16qmf0PzfUNNIOgeutwVFI-rDEAjh_Afa_pKICojpyLFlfDhLe4xR_A3HQs-3RIYlIPlJa_nDm00',

    #College
    '/frantzme_transcript_grad':'https://drive.google.com/file/d/192BTnc1YdIkmdMpnTAWJ-cvM3cjbcz8o/view?usp=sharing',
    '/frantzme_transcript_undergrad':'https://drive.google.com/file/d/1FfpMv0saG-SMEBpmogmt-y4OwGM3YNAU/view?usp=sharing',
    '/frantzme_references':'https://docs.google.com/document/d/1HhZwyFzxgQVdL8iPMkvOrSdZmSY3iaNv/edit#bookmark=id.ssksbd1dnsbb',
    '/frantzme_transcript':'https://drive.google.com/file/d/192BTnc1YdIkmdMpnTAWJ-cvM3cjbcz8o/view?usp=sharing',
    '/csgc':'https://csgrad.cs.vt.edu/',
    '/HokieSpa':'https://banweb.banner.vt.edu/ssb/prod/twbkwbis.P_GenMenu?name=bmenu.P_StuMainMnu',
    '/frantzme_ms_thesis':'https://drive.google.com/file/d/1ZnKPDYF_rlFeS6pGdcfLIeaqs_-bTZ3I/view?usp=sharing',
    '/frantzme_cryptoguard_poster':'https://drive.google.com/file/d/12MPEaDSBt_d73jlRaeoy2-RIzGQPX2MR/view?usp=sharing',
    '/frantzme_cryptoguard_ccs':'https://drive.google.com/file/d/1ltQnGlsAeLQAnpWOQHpH-X5qhJ0VHL1h/view?usp=sharing',
    '/vt_funding':'https://www.plantuml.com/plantuml/svg/ZT1VIp9150RmUp_5tCixmnk854IQuc99g5j2Y2pZpDdPjPq_dZExbf--hRn8wgAxWJdydeTdG55YjANJLePEDsEJskdIcKwtVQ_NHOo1heGmWOWtaOEkMJ9FqyscFUZ-VY02UeFIaeXvu4Mq5Nj4sK3rQRFvr-_V18FwH2GeTIqZi2KGI5G56qDh-c31nJFqUs-4BKgdUVKc51d5Hcao-f6ilI9kl3SLSEMjo3ssqLg0-3yPJiDYbgfUEbxD3692jyVTHSzceqBD3jEdUrWzz_V5STZ_fovx_Tts8NzrTmlHb73uO6vg2jUKPrNfNivMMCA-1efjbm4uVTh_7G00',
    '/vt_etd_rsc':'https://vtechworks.lib.vt.edu/handle/10919/73192',
    '/vt_etd_docs':'https://guides.lib.vt.edu/c.php?g=547528&p=3756998',
    '/VT_ETD':'https://www.overleaf.com/latex/templates/virginia-tech-etd-template/cpqhbscstfrx#.WusPwtMvxBw',
    '/vt_stages':'https://secure.graduateschool.vt.edu/graduate_catalog/policies.htm?policy=002d14432c654287012c6542e3630013',
    '/vt_exams':'https://secure.graduateschool.vt.edu/graduate_catalog/policies.htm?policy=002d14432c654287012c6542e3630013',
    '/csgc_website':'https://www.plantuml.com/plantuml/svg/nLHHRzCm47xlhpZj2T0QjzacMFUoRe9DGa9eBPjWweFZt1Apn8xiSwE2-E-SanPMfasW8SX3LITttttttNS-zYGTXReQJ3vuT53BM_GWGPNI50ZMmFLrITJuYH25fZ9aYRArE9sTEPa7INXgWr6w6bvgLsYZvHnLAPGlrB35p6j2EDDq7hB5ucWm-MjOa0LTvHweHDXyMshvPB8YgsmcQka9dKXw3D5QTtjJsTQB2wnGUanMTRMc0bD5sXeVspEM49mkIXe0m8ixP1WzaKwLUec9TKKyYtIKfgE3SShFuIWL_upt5MRJdifYyIlF9W9asdJbhqRB2tcmjm_luziJRJWUJHwx74p-ez3WqQn7_qKtSACh1BBn_FJnkxwkXysV-tETbxZv2kVJMInToYLszLLm3Wq1wHfviUec9doq0PGqZ0AXgQpCjrpRCj7kXPSrWk6VcFF6Ef21x90RQBZ1NOw7u1-eqeDuL9Q5-J6ZHZhIKJFOURr4ju9tiGKuYPkp0rzZcSbyIpIMWfLAb4-Mb60Un8ObYwvPas20qOXpBkSmGyUe4v3D-6V6KOSwipLQ4-yHfLXoYfbyUCXeRr-bQZoVVWBbh24Prti8ptvtU_PUfeVYSLoslDnO_daaOxGf03jHJ1IbexqrPduuBSQ2fhkXuBLH64LmoAAiGus5Lguw6p92WIu6z9TKZ5YFP2FvGqACf4iFJlHdo96DiWAld6xep-JO7uz6ud7qRJbosvheIW-L9FPJpteN77EG2lsMvUwvrc3R9nmDlWsEkSzGLzy1',

    #Projects
    '/cryptoguard':'https://github.com/franceme/cryptoguard',
    '/cryptoguard4py':'https://github.com/franceme/CryptoGuard4Py',
    '/secdev':'https://mybinder.org/v2/gh/franceme/cryptoguard/2020_SecDev_Tutorial?filepath=SecDev_Tutorial.ipynb',
    '/cryptograde':'https://drive.google.com/file/d/1X8MSjJmc7qQ_kd4d3U_CogYw81nzFY3_/view?usp=sharing',

    #Academic | Research
    '/ssok':'https://oaklandsok.github.io',
    '/conferences':'http://www.plantuml.com/plantuml/svg/XPD1Yzim48Nl-olcr4D0rYQdqjCQDIs6JGWefOLbMRJZIIomPAEHcys_hnsvnFMcxCL8wBqtxnlm0qSJehE-TAQzMu1g_842UII-MopWwQcAiVqYvS5WLyTpXfn5uxgCoauUk-P0LZBX2_Qs5uucPbLqe0cxOEFv-RdFMC3UKe3bS9m4dawdp1AHu56SDU4ezqhgdIXyIMz3KWtwqowbpAniZspmua7af5LA_wlbKTmnUVkMn5S--Nhsnf5Std-67tgzBNxTTlkIMV3PjGtRpbrIOFjLwodTwaP5WtyRGgwqUeVHKfobxjPx_JzQR5nIqM_oaQLrAAumK6pIW8zNhFItdoTwbT0VUeiGa1VzLy3c4GvDW41jCzp5P0qMwv0XGg4UUyliSMYH1M8o0QjmcL4rZgJZ85RtgoLiT4YkMJLacY3mu8H2gtKIJoPus_8mVblizFZudJm5Ky-wfBqROnFfDLlcULx8oqjRjJ3SteDOT7MYt0oO3-JBySVu0m00',
    '/scolar':'https://scholar.google.com/citations?user=RKKj9VgAAAAJ',
    '/sok':'https://oaklandsok.github.io/',
    '/os_defcon':'https://www.defconlevel.com/current-level.php',
    '/my_conf':'https://www.plantuml.com/plantuml/svg/ZP5FQm8n4CNlVeevBsmYdafFsbMAi5B1taHap8vkQFw4pInRltqJfIZLGq-PWVT-UO-PHiQEhNQDnJ0gu9qSTMYWrkuhZee2Ak-Er95JbDS2DgJoMy1sspA7-2fbOmGgAtntakgcXbcrskqUj0SJiZ8D5x6CGSByhLu_IeTX4FRSzlg0JYXlx-1oyWBBLVNSeudeRnYP2jAtQDaQM2uMY-JyJmaPJADXNS-NLmEiwcS_iWy7p_4ICiqbasgTLcXAr2MwfhIcl0jJJiQJiOJFZtNYmUpAXihRW1sDRlX4FwBg3P-5YeBHzeAQNfvwVoGj8wbzXkuZ8-Tc-JImIKjCm2cvvlUgFm00',
    '/conf':'https://www.plantuml.com/plantuml/svg/ZP5FQm8n4CNlVeevBsmYdafFsbMAi5B1taHap8vkQFw4pInRltqJfIZLGq-PWVT-UO-PHiQEhNQDnJ0gu9qSTMYWrkuhZee2Ak-Er95JbDS2DgJoMy1sspA7-2fbOmGgAtntakgcXbcrskqUj0SJiZ8D5x6CGSByhLu_IeTX4FRSzlg0JYXlx-1oyWBBLVNSeudeRnYP2jAtQDaQM2uMY-JyJmaPJADXNS-NLmEiwcS_iWy7p_4ICiqbasgTLcXAr2MwfhIcl0jJJiQJiOJFZtNYmUpAXihRW1sDRlX4FwBg3P-5YeBHzeAQNfvwVoGj8wbzXkuZ8-Tc-JImIKjCm2cvvlUgFm00',
    '/mlconf':'https://aideadlin.es/?sub=ML,CV,CG,NLP,RO,SP,DM',
    '/secconf':'https://sec-deadlines.github.io/',
    '/confs':'https://www.plantuml.com/plantuml/svg/VPHVQzim5CNV-oak3FOGiDLaBsLFzTnq69eiJ1aRb59K-SOMioIZApVrjv_yPwiRPys3aQFpE_SSsVYQl71UAvDhKLyi8BNcW0wDHBfOBE3-llI-_ipOGSYcycqiAVP2Dp7c3IiQUq352EMZ3DXZiF9nwJLmb8rJldru21uBs2jqi0pBgU7nU8mL8aOqYcFh2hPF6Tz5cSdnfNEgW7_S1PSvIgeW8Nj6IXgqQShVQcaKDuH6lGpYrtxigJL28rjUNi4FljvclyxJ9YUAgDMr9TNetWMsDvnFswtEH1JoRq98KfxEQjJeJrntwpt_NrjfzQ32PpIUcD8oUYq3sMOouDqZJldjpoC-CGYBiS9NDEX4TQvyhlIp6DBTTClv4TMjVJeq9EEGC5HeVMaDVEl_4Xvpa3R7S34UoVSqS7lmH-4GrgPG1j4fKroyDPqyfiwtRZowFeMI5APaATy4hoaphIl5S5Iho-KL-r0xMpYXWQV97Ee6nGu9XPFbC8BGAIIcYBo0ZFDzCgCQYXnXhsueh5QV67pdww2B8aYoS8rWSmS7wy1XRRlxQ88hMRbOob3ZhaF2x_r4fTN8DBbeTRbQmeQxWJfvqf8mcfvR84FyT4WrdM1KJTtuRRRZu-Ru1fncwNo546fuSLwzMP8a6UjtwhA6xcvUH4bT3IqtOqsu4Lvmz7GgDTYu8TIRALrTbeggkhMkGocWNy9MgONxJR0Tg7-kymYrin8nLwQWU39Z93lW6aq-Vlt-0000',
    '/ndss':'https://calendar.google.com/calendar/u/0?cid=Y19hOTFzMGUzMjdpYmxjN2htMjZwY2l0czQ3NEBncm91cC5jYWxlbmRhci5nb29nbGUuY29t',
    '/sok.html':'https://oaklandsok.github.io',

    #Drives
    '/365':'https://login.microsoftonline.com/?whr=virginiatech.onmicrosoft.com',
    '/gdrive':'https://drive.google.com',
    '/idrive':'https://www.icloud.com/iclouddrive/',
    '/vmale':'https://outlook.office.com/mail/',
    '/365':'https://login.microsoftonline.com/?whr=virginiatech.onmicrosoft.com',

    #Locations
    '/atl':'https://maps.app.goo.gl/rtEHkrYyEidJfXiu7',
    '/ewr':'https://maps.app.goo.gl/E2jr4V3oByCD2KE98',

    #Personal
    '/travel':'https://www.google.com/travel/flights/search?tfs=CBwQAhoeEgoyMDI1LTAxLTMwagcIARIDRVdScgcIARIDQVRMGh4SCjIwMjUtMDItMDNqBwgBEgNBVExyBwgBEgNFV1JAAUgBcAGCAQsI____________AZgBAQ',
    '/gift_rents':'https://docs.google.com/document/d/14CYdx3o_15LrhV9wCYv0X-MJv5fqhgPI/edit?usp=sharing&ouid=103289071436703194896&rtpof=true&sd=true',
    '/gift_rent':'http://google.com',
    '/gift_shak':'https://docs.google.com/document/d/1Hock_q21oJto4zHtZilbDIMDRT0HX7n-/edit?usp=sharing&ouid=103289071436703194896&rtpof=true&sd=true',
    '/gift_self':'https://docs.google.com/document/d/1eI4C3MiRPDO-VElCZF2_NBaV2-z8LxYp/edit?usp=sharing&ouid=103289071436703194896&rtpof=true&sd=true',
    '/gift_selfshak':'https://docs.google.com/document/d/1D68CY8765mevTuMtAKJEenK8rUKf5oEE/edit?usp=sharing&ouid=103289071436703194896&rtpof=true&sd=true',
    '/gift_browns':'https://docs.google.com/document/d/1HfcsVm-3YY19MCmoI-v3EISh6mfc_43J/edit?usp=sharing&ouid=103289071436703194896&rtpof=true&sd=true',
    '/task':'https://app.asana.com/0/1202250158074124/list',
    '/frantzme_latex':'https://drive.google.com/uc?export=download&id=1EjUCp54i4KXiXbroPvrGqiZEvdWkF2Lu',
    '/frantzme_adobe':'https://acrobat.adobe.com/link/home/?locale=en-US',
    '/frantzme_linkedin':'https://www.linkedin.com/in/frantzme/',    '/frantzme_cv':'https://drive.google.com/file/d/18qCa6lW4718-tTrpE5_H5Nr0s6ssG5Na/view?usp=sharing',
    '/frantzme_resume':'https://drive.google.com/file/d/1wq_hU272QvwmW1Cj1on7MaufEvGxzA7C/view?usp=sharing',
    '/resume.html':base_info["RESUME"],
    '/resume':base_info["RESUME"],
    '/cv.html':base_info["CV"],
    '/cv':base_info["CV"],

    #Website Aide
    '/frantzme_qr':'https://franceme.github.io/qr.html',
    '/rsc_gen':'https://www.plantuml.com/plantuml/svg/RT7FIiD040RmUvzYm6D95pnwgWJffNYeMW-bbEdks2pidxWxIUhRknqN3E9nvfllHyYkCsDYRuFns2-M9zXGe8GETfJZa3JbnR9iMtGK3AOoBE5mw9Zx1wMcQLfrxDszrUXMEdfL7Bgk-gw7nu6ZHxubxWjq8cG215qX-4ZHmzjkUppEp5nGiJocmKGM4ref_rPffC1PYYVObkWASwD-cBi53UFPKHRdhjw-oghMt-dyRBLbI_aVupCrEXfgBl9JE2Q1SdG3snYo6ZKcqzGh1VksZ1L-sM_WoTZI-GldyK8InE1i825_5chMAioQWgalymq0',
    '/uful':'https://franceme.github.io/secure_useful.html#staticrypt_pwd=47b333df359460a3ff8812fb5db669f0083a25d3fd1c6cd4073f2685f0cb5a41',

    #Utils
    '/frantzme_frac':'https://franceme.github.io/frac.html',
    '/frantzme_frac_hashsha_example_00':'https://franceme.github.io/frac.html?code=from%20hashlib%20import%20sha1%0Ainsecure_value%20=%20sha1(%22My%20Password%22).hexdigest()%0Aprint(insecure_value)',
    '/chef':'https://gchq.github.io/CyberChef/',
    '/chief':'https://gchq.github.io/CyberChef/',
    '/txt':'https://www.onlinetexteditor.com/',
    '/smartware':'https://github.com/Malware-Research/Resources',
    '/telatex':'https://www.latex-tables.com/#',
    '/xelatex':'https://www.latex-tables.com/#',
    '/latex_table':'https://texblog.org/2012/07/30/single-column-figuretable-in-a-two-multi-column-environment/',
    '/ml_metrics':'https://en.wikipedia.org/wiki/Precision_and_recall',
    '/delatex':'https://detexify.kirelabs.org/classify.html',
    '/my_pdf':'https://localpdf.tech/',
    '/farsi':'https://www.plantuml.com/plantuml/svg/ZPFHRzem4CRV-rVugIyeyRfAAvl4McZfDgaCHYkaKLN8n9VuEiVsx2CP--iNd81Q7gO--hlxVT_bJhaA93oLQ6Gft4cFtGeVaDs1y0PDSTBhiGSlJD22q9hGl7liyL4HkV29S-fAa1RM5XhIp9RyCkW1c5FIWroSMZSuDB6nAJG6nPBFRSpJqv7Vipmxl-Yd1PBQh5Eqt47J9an2Dd7OqhnbeqadlV9fRC9ML2AeE8spdeJcU_fzleDvPaq5dgoF7lyVQWtAG8KXse7XRq0aPhjr2RzDOruQCcMjvkpcK8WCkzcjvJeE4nhzoAQkwvH4eIeiOtWtDNZE7bhvE3aYw8N9b2ZNu5jCQ31I-1VyhWM5MUrBgqCfTShj3zMkDadO77BmO388pIjv-Q4UgrV7pr43b_oCzAG_lBl8t7Iaho_Mj3AabeZrkr7oS_jdrESLGdsv2MuGBOBynHRWrsnY9UO8FkQ-AMdYxFrORrOBkPmz3_zEFsRBBrytszlptxCFkFenZKbi14JWsKnPicpHACSHtUuyI8aK0poVZUVttuRVEPj7jG6kmCZkN_a7',
    '/playlists':'https://www.chosic.com/',
    '/audible':'https://www.audible.com/webplayer?asin=B06X3QQTFH&contentDeliveryType=MultiPartBook&ref_=a_minerva_cloudplayer_B06X3QQTFH&overrideLph=false&initialCPLaunch=true',
    '/motivate':'https://homeforfiction.com/apps/locked/quoteJux/',
    '/dcap':'https://app.capacities.io/c9a15b2f-13da-45dc-a81c-cec3a70c540f/154e5043-6462-48f6-b49f-b133bec368b6',
    '/audio':'https://noises.online/player.php?g=ca5fa5',
    '/tele':'https://web.telegram.org/z/',
    '/capz':'https://app.capacities.io/',
    '/corers':'https://raw.githubusercontent.com/franceme/staticpy/master/sample.rs',
    '/graphz':'https://www.plantuml.com/plantuml/svg/ZLPlRzis4t_VJq7W0Hwq22GbJLUqUzKqQRUbpkfDtJgiA8oJT9Lfapo2FCLMF_qeKau2oyxsmk4T-RiVxyyTepUUmR6Mfj5Wdvmin1KmFCcoXRZkRC_enA_4M16jnKokCPo4exUEDXxTe6JYovSbi_K_5aLD2ghSeKTmzJ9lYLg5UKsw43z5MLmEYAzVfuOrg7f01iHb4ASGtLV1HtGvkROGD_tRg4rnPlJMv_2zS-Fj5uCunJR0e2Y091NYQbIciCrcaw-GAmVI-4ZeK1DZrk0jAh8Q3HSjC6wW3v4c8T4in6m8xH2Zjtq889CDff3Ag4zlNwKo9D2k9hCnYwbSOYujAcd6wboIjk2a9-FtoLh9owwACTn8qtU-cFUy9BEOGxs65ltY6xd5ZcxncTpwcwADIAY7pE8iE72StJQIIMlmLC06FMdCxCYwOnb8dYUIQKTD6Icq57hUhU9ZMX_DCvDKkKDeU8aDrJwN93w5lMXq_2QBPjEe8lp4vwlP51ph5v2Qp4R5mdGUtQBjP8E5kFmycwRcEzeOVGuMwkLOyeieYx_3MJYQ6bMAshpg7PcLry6_w1r3M-nIwVCbQoLA0slKuJUbM6FZQ2y51Ph2CrGAYzEpXJJigEbgbcJszKJ_OU2OKazxQUVMzguX_peyJQZ0inm6lbZB2WmKuaDS_nKktaKvlJ0FHw1aSj2E4_2Ud0OUkx_yRIOPatpjoIJfilmp2Jz3GsJthoLZjZd8GWp2NO_9oe6J68YJ3gODSbBIY4Gjgc0Qy4zEJeAeY5cQDYX1-qIaXlru0h8HJpSXaOAT1EMVnOEJlVYrh1rv-iOnsMYoaEkxlUpyvGy5RcjKujtmDpXxY4DMEWrcAgullFK-ymmiXznwKSxBCjf6r_Qi8vWxfkXb98fRDWQTLU03HR5x9dunZAs3eOEEU1Ex3xf893ubvT3b4p1Kr74SZEBvwTdhuaMXy1Q7ocUMDkYo4Po1QNRUMOU-TjAolCMm3weV0ixEJb-yFdtvttqc9rjf5CIM5n-ZTWIwqdOirIAKQaaQqoHTtyoFM6XfP73zGO75JTeQ3K9JEyI9RRq4nvddhf6KMqMi-iXHEmJ6ud-X9d7pmBMDWz0M9Ax2Akc8NrQ1uKwh6FDyKFxGwbZKeEbMZl-eedm0k09lOzlv4NXH7ij9w6wuRz0OLaobNLfHVdn_4StYLCPvkXl1FIeD71CZg-56SQy6-pseHwZ8cTps3J0a1yUzAVX1jbEZxUNwy5EfvHeRt80hcdFRYwlpB7ezvK-jxtejcU87oaqGoYKYJw4Lw8feYF3LwQjJ1LNAbdWxx8VyFEgHwhPPY7HOnQpRFefT1I0kBTrzPbsNzz-7GNuwJjF_Gs3F4jCYzC8jb740zvcRyrLgWm3VeN_l_1H7eVxEnvGp1a41e-TxNSn7QSSo2u1jV5ZyeRoguJYz5IbLoI1B5e7a3Pfc_2Z-1m00',
    '/mendeley':'https://www.mendeley.com/reference-manager/library/all-references',
    '/my_mendeley':'https://www.mendeley.com/reference-manager/library/all-references',
    '/g_tasks':'https://script.google.com/a/macros/vt.edu/s/',
    '/thenticate':'https://shibboleth.turnitin.com/shibboleth/ithenticate',
    '/ithenticate':'https://shibboleth.turnitin.com/shibboleth/ithenticate',
    '/mythenticate':'https://shibboleth.turnitin.com/shibboleth/ithenticate',
    '/feedly':'https://feedly.com/i/collection/content/user/420bc1de-a3e3-4023-84fa-752509fde431/category/global.all',
    '/g_task':'https://tasks.google.com/embed/?origin=https://calendar.google.com&fullWidth=1',

}.items():
    if route.replace('/','') in app._current_rules():
        print(f"Route /{route} already exists")
        sys.exit(-1)

    function_name = "def_gen_" + route.replace('/','').replace('.','_').replace('-','_')
    app.add_url_rule(route, view_func=create_dynamic_function(function_name, f"""
def {function_name}():
    return page_redirect("{url}")
""".strip()))

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

    response = flask.make_response(fg.rss_str())
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

#region Skill & util Functions
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

    return flask.render_template_string(f"""
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

    return flask.render_template_string(f"""
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
    return flask.render_template_string(f"""
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
    page_name = mystring.string.str(page_name)
    return flask.render_template_string(f""" <a href="/{page_name.lower()}.html">{page_name.title()}_{extra_info}</a> """)

app.jinja_env.filters['get_main_url'] = get_main_url
#endregion
#region Commands
def arg(string):
    return __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[0].endswith('setup.py') and mystring.string(sys.argv[1]).upper().replace("--",'') == mystring.string(string).upper()

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
#endregion

setuptools.setup(name='My Website',
        version='0.0.0',
        description='Python Website',
        author='Miles Frantz',
        author_email='frantzme@vt.edu',
        url='',
        packages=setuptools.find_packages(),
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
