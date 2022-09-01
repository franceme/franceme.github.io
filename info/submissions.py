import os,sys,json
with open("submissions.json","r") as reader:
    items = json.load(reader)

with open("tech.txt","w+") as writer:
    for itym in items:
        writer.write(f"""{{{{
   "<a href='{itym['SELF_FILE_URL']}' >{itym['FULL_NAME']}</a>"|get_base(
   "<a href='{itym['CONF_URL']}'>{itym['CONF_NAME']}</a>",
   "{itym['DATE']}",
   "",
   "")|safe
}}}}
""")