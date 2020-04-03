import random
from data import perks as perkschart
from copy import deepcopy
from tkinter import *
from tkinter import scrolledtext

def randomize(max_level=50,
              special_book=True,
              stat_leveling=True,
              bobbleheads=True,
              stats_only=False):
    
    perks = deepcopy(perkschart)
    output = ""
    output += "### CHARACTER CREATION ###" + "\n"
    special_points = 21 + special_book
    special_stats = {k:1 for k in perks.keys()}
    stats_temp = list(special_stats.keys())
    while special_points > 0:
        stat = random.choice(stats_temp)
        special_stats[stat] += 1
        perks[stat][0]["ranks"].pop(0)
        if special_stats[stat] == 10:
            stats_temp.remove(stat)
        special_points -= 1

    for k in "SPECIAL":
        output += "%s: %d" % (k, special_stats[k]) + "\n"

    available_by_stat = dict()  
    
    def stat_up(k):
        try:
            available_by_stat[k].append(perks[k].pop(0))
        except IndexError:
            pass

    for k in perks.keys():
        available_by_stat[k] = []
        if not stat_leveling:
            perks[k].pop(0)
        for i in range(special_stats[k] + stat_leveling):
            stat_up(k)
        if bobbleheads:
            available_by_stat[k].append(perks[k].pop(-1))
        else:
            perks[k].pop(-1)

    if stats_only: return output

    output += "\n"
    output += "### CHARACTER LEVELING ###" + "\n"
    level = 1
    available_by_level = dict()

    def level_up():
        for k in perks.keys():
            i = 0
            indexes_to_pop = list()
            for perk in available_by_stat[k]:
                if len(perk["ranks"]) == 0:
                    indexes_to_pop.append(i)
                elif perk["ranks"][0]["level"] <= level and perk["id"] not in available_by_level.keys():
                    perk_full = deepcopy(perk)
                    perk_rank_0 = perk_full["ranks"].pop(0)
                    perk_full["ranks"].clear()
                    perk_full["ranks"].append(perk_rank_0)
                    available_by_level[perk_full["id"]] = perk_full
                    perk["ranks"].pop(0)
                    if len(perk["ranks"]) == 0:
                        indexes_to_pop.append(i)
                i += 1
            j = 0
            for i in indexes_to_pop:
                available_by_stat[k].pop(i - j)
                j += 1

    level_up()
    output += "%-3s %s" % (1, "--") + "\n"
    while level <= max_level - 1:
        try:
            rand_index = random.choice(list(available_by_level.keys()))
        except IndexError:
            break
        perk = available_by_level.pop(rand_index)
        
        if "free_stat_up" in perk.keys():
            stat_up(perk["free_stat_up"])
            level_str = "--"
            rank_str = ""
        else:
            if "stat_up" in perk.keys():
                stat_up(perk["stat_up"])
            level += 1
            level_up()
            level_str = str(level)
            rank_str = str(perk["ranks"][0]["rank"])
        output += "%-3s %s %s" % (level_str, perk["title"], rank_str) + "\n"
    return output

def gui():
    window = Tk()
    window.title("Fallout 4 Build Randomizer GUI")

    frm1 = Frame(master=window, padx=5, pady=5)
    frm1.pack(fill=X)

    lbl0 = Label(master=frm1, text="FO4Randomizer parameters")
    lbl0.pack(side=TOP)

    frm2 = Frame(master=window, padx=5, pady=5)
    frm2.pack(fill=X)

    p1_f = Frame(master=frm2, pady=5)
    p1_f.pack(fill=X)
    p1_v=StringVar()
    p1_v.set("")
    p1_c = Entry(master=p1_f, width=3, textvariable=p1_v)
    p1_c.pack(side=LEFT, padx=3)
    p1_l = Label(master=p1_f, text=" max_level ", bg="white")
    p1_l.pack(side=LEFT)
    p1_d = Label(master=p1_f, text=" - determines max character level")
    p1_d.pack(side=LEFT)

    p2_f = Frame(master=frm2, padx=5, pady=5)
    p2_f.pack(fill=X)
    p2_v = BooleanVar()
    p2_v.set(True)
    p2_c = Checkbutton(master=p2_f, var=p2_v)
    p2_c.pack(side=LEFT)
    p2_l = Label(master=p2_f, text=" special_book ", bg="white")
    p2_l.pack(side=LEFT)
    p2_d = Label(master=p2_f, text=" - adds one SPECIAL point to alloc during character creation")
    p2_d.pack(side=LEFT)

    p3_f = Frame(master=frm2, padx=5, pady=5)
    p3_f.pack(fill=X)
    p3_v = BooleanVar()
    p3_v.set(True)
    p3_c = Checkbutton(master=p3_f, var=p3_v)
    p3_c.pack(side=LEFT)
    p3_l = Label(master=p3_f, text=" stat_leveling ", bg="white")
    p3_l.pack(side=LEFT)
    p3_d = Label(master=p3_f, text=" - adds SPECIAL perks that randomly increace SPECIAL stats up to 10")
    p3_d.pack(side=LEFT)

    p4_f = Frame(master=frm2, padx=5, pady=5)
    p4_f.pack(fill=X)
    p4_v = BooleanVar()
    p4_v.set(True)
    p4_c = Checkbutton(master=p4_f, var=p4_v)
    p4_c.pack(side=LEFT)
    p4_l = Label(master=p4_f, text=" bobbleheads ", bg="white")
    p4_l.pack(side=LEFT)
    p4_d = Label(master=p4_f, text=" - adds seven SPECIAL Bobblehead perks to perk chart")
    p4_d.pack(side=LEFT)

    p5_f = Frame(master=frm2, padx=5, pady=5)
    p5_f.pack(fill=X)
    p5_v = BooleanVar()
    p5_v.set(False)
    p5_c = Checkbutton(master=p5_f, var=p5_v)
    p5_c.pack(side=LEFT)
    p5_l = Label(master=p5_f, text=" stats_only ", bg="white")
    p5_l.pack(side=LEFT)
    p5_d = Label(master=p5_f, text=" - stops build randomization after character creation")
    p5_d.pack(side=LEFT)
    
    frm3 = Frame(master=window, padx=5, pady=5)
    frm3.pack(fill=X)

    btn_frm = Frame(master=frm3)
    btn_frm.pack(side=LEFT)

    btn1 = Button(master=btn_frm, text="Randomize", width=12)
    btn1.pack(side=LEFT, padx=5)

    btn2 = Button(master=btn_frm, text="Copy", width=12)
    btn2.pack(side=LEFT, padx=5)
    
    frm4 = Frame(master=window, padx=5, pady=5)
    frm4.pack(fill=BOTH, expand=True)

    txt = scrolledtext.ScrolledText(master=frm4, width=30, height=12)
    txt.pack(side=LEFT, fill=BOTH, expand=True)

    def handle_btn1_click(event):
        txt.delete(1.0, END)
        params = dict()
        p1_vs = p1_v.get()
        p1_vi = 0
        if p1_vs == "": 
            p1_v.set("50")
            p1_vi = 50
        else:
            try: 
                p1_vi = int(p1_vs)
            except: 
                txt.insert(1.0, "Incorrect 'max_level' value")
                return
        params["max_level"] = p1_vi
        params["special_book"] = p2_v.get()
        params["stat_leveling"] = p3_v.get()
        params["bobbleheads"] = p4_v.get()
        params["stats_only"] = p5_v.get()
        
        txt.insert(1.0, randomize(**params))

    def handle_btn2_click(event):
#        window.withdraw()
        window.clipboard_clear()
        window.clipboard_append(txt.get(1.0, END))
        window.update()


    btn1.bind("<Button-1>", handle_btn1_click)
    btn2.bind("<Button-1>", handle_btn2_click)

    window.mainloop()

if __name__ == "__main__":
    gui()

