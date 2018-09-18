org = open('organizers','r').readlines()
name = open('names','r').readlines()
shortname =open('shortnames','r').readlines()
for i in range(0,14):
    print("""
      \\begin{wsschedule}
      {%s}
      {%s}{WShop%s}
      {workshop%s}
      {\WShopLoc%s}
      \\input{auto/%s/schedule}
      \\end{wsschedule}
      """%(name[i].strip(),i+1,chr(ord('A')+i),i+1,chr(ord('A')+i),shortname[i].strip()))
