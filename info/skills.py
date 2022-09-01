with open('tech.txt','w+') as writer:
    odd = False
    for order in ['lang','framework','projectType']:
        for skill in skills:
            if skill['TYPE'] == order:
                if odd:
                    odd = False
                    content = f"'{skill['NAME']}'|get_skill({skill['PERCENT']})|safe"
                else:
                    odd = True
                    content = f"'{skill['NAME']}'|get_skill({skill['PERCENT']},False)|safe"
                writer.write(f"{{{{{content}}}}}\n")