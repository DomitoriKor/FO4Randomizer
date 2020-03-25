import random
from data import perks
from copy import deepcopy

def randomize(max_level=50,
              special_book=True,
              stat_leveling=True,
              bobbleheads=True,
              stats_only=False):
    
    print("### CHARACTER CREATION ###")
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
        print("%s: %d" % (k, special_stats[k]))

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

    if stats_only: return

    print()
    print("### CHARACTER LEVELING ###")
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
    print("%-3s %s" % (1, "--"))
    while level < max_level:
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
        print("%-3s %s %s" % (level_str, perk["title"], rank_str))

if __name__ == "__main__":
    randomize()
