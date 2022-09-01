import os,sys,json
with open("projects.json","r") as reader:
    items = json.load(reader)

with open("tech.txt","w+") as writer:
    for itym in items:
        writer.write(f"""{{{{
   "{itym['NAME']}"|get_base(
   "<a href='{itym['URL']}'>Website</a>",
   "{itym['FROM']}",
   "{itym['TO']}",
   "{' '.join(itym['TEXT-DESC'])}")|safe
}}}}
""")