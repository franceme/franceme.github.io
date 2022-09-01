import os,sys,json
with open("education.json","r") as reader:
    items = json.load(reader)

with open("tech.txt","w+") as writer:
    for itym in items:
        writer.write(f"""{{{{
   "{itym['TITLE']}"|get_base(
   "{itym['NAME']}",
   "{itym['FROM']}",
   "{itym['TO']}",
   "{' '.join(itym['TEXT-DESC'])}",
   False)|safe
}}}}
""")