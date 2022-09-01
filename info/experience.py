import os,sys,json
with open("experience.json","r") as reader:
    items = json.load(reader)

with open("tech.txt","w+") as writer:
    for itym in items:
        if len(itym['SKILLS']) > 0:
            skillz = f"<br><br>Skills: {', '.join(itym['SKILLS'])}"
        else:
            skillz = f""
        writer.write(f"""{{{{
   "{itym['JOB_TITLE']}"|get_base(
   "{itym['NAME']}",
   "{itym['FROM']}",
   "{itym['TO']}",
   "{' '.join(itym['TEXT-DESC'])}{skillz}")|safe
}}}}
""")