#!/usr/bin/env python3
from os import path
import re
from hashlib import sha256


class Item(object):
    def __init__(self, item):
        self.item = item

    def __str__(self):
        return self.item['name']

    def __repr__(self):
        return 'Item("' + self.item['name'] + '")'

    def __hash__(self):
        try:
            return hash(self.item['name'])
        except:
            print(self.item)

merge = lambda a, b: {**a,**b}

def get_objects__old_format(text):
    objects = []
    object_lines = []
    current_lines = []
    for line in text.splitlines():
        if line.strip() != "":
            current_lines.append(line)
        else:
            object_lines.append(current_lines)
            current_lines = []
    object_lines.append(current_lines)

    name = re.compile(r"Object: '(?P<name>[\w -\\\']+)' is type (?P<armor_type>\w+).")
    weapon_type = re.compile("Weapon type is (?P<weapon_type>\w+).")
    damage = re.compile("Damage is (?P<dice_count>\d+)d(?P<dice_size>\d+) \(average (?P<avg>\d+)\).?")
    # @@@ check it parses negative stoo
    affect = re.compile("Affects (?P<stat>[\w ]+) by (?P<amount>[\d-]+).?")
    comment = re.compile(r"[/\\]+(?P<comment>.*)")
    armor = re.compile("Armor class is (?P<pierce>\d+) pierce, (?P<bash>\d+) bash, (?P<slash>\d+) slash, and (?P<magic>\d+) vs. magic.")
    extra_flags = re.compile("Extra flags (?P<flags>[\w -]+)")
    material = re.compile("Material is (?P<material>\w+).")
    weight = re.compile("Weight is (?P<weight>[\d.]+\d+), level is (?P<level>\d+).")
    weapons_flags = re.compile("Weapons flags: (?P<weapon_flags>[\w-]+)")
    spells = re.compile("Level (?P<level>\d+) spells of: (?P<spells>.*).")
    charges = re.compile("Has (?P<charges>\d+) charges of level (?P<level>\d+) (?P<spell>.*).")
    capacity = re.compile("Capacity: (?P<capacity>\d+)#? Maximum weight: (?P<max_weight>\d+)#? flags: (?P<container_flags>.*)")
    weight_multi = re.compile("Weight multiplier: (?P<weight_multiplier>\d+)%")

    regexen = [
        name, weapon_type, damage, comment, armor, extra_flags, 
        material, weight, weapons_flags, spells, charges, capacity,
        weight_multi,
    ]
    special_regexen = [affect]

    for lines in object_lines:
        current_object = {}
        for line in lines:
            line = line.strip()
            if 'You have become better at' in line:
                continue
            if "chant softly" in line:
                continue
            if "rush of knowledge" in line:
                continue

            found = False
            for regex in regexen:
                if not found and regex.match(line):
                    current_object = merge(current_object, regex.match(line).groupdict())
                    found = True

            if affect.match(line):
                found = True
                if 'affects' not in current_object:
                    current_object['affects'] = {}
                group = affect.match(line).groupdict()
                current_object['affects'][group['stat']] = group['amount']

            if not found:
                if 'comment' not in current_object:
                    current_object['comment'] = []
                current_object['comment'].append(line)
        if current_object != {}:
            objects.append(Item(current_object))
    return objects

def get_objects__new_format(text):
    objects = set()
    object_lines = []
    current_lines = []
    for line in text.splitlines():
        line = line.strip('#')
        if line.strip() == "":
            if current_lines != []:
                object_lines.append(current_lines)
                current_lines = []
            else:
                continue
        else:
            # print("line: ", line)
            # print(len(current_lines))
            current_lines.append(line)
    # And once more for the last one.
    object_lines.append(current_lines)

    num_re = r"[\d.]+"
    pipe_re = lambda x,y,z: f".*{x}:\s+(?P<{y.replace(' ', '_')}>{z})\s+\|"
    simple_number = lambda x: re.compile(pipe_re(x, x.lower(), num_re))
    simple_str = lambda x: re.compile(pipe_re(x, x.lower(), r"[\w' -]+?"))
    # pipe_re = lambda x, y, z: ".*"
    name = re.compile(pipe_re( "Object", "name", r'[\w, "\'-]+?'))
    weight = simple_number("Weight")
    size = simple_number("Size")
    level = simple_number("Level")
    material = simple_str("Material")
    item_type = simple_str("Type")
    spell = simple_str("Spell")
    spell_mod = simple_str("Spell Modifier")
    flags = simple_str("Flags")
    size = simple_str("Size")
    capacity = simple_str("Capacity")
    multiplier = simple_str("Multiplier")
    wear = simple_str("Wear")
    color = simple_str("Color")
    liquid = simple_str("Liquid")
    charges = simple_str("Charges")
    hp_regen = simple_str("Hp regen")
    mana_regen= simple_str("Mana regen")
    weapon_type = re.compile(pipe_re("Weapon type", 'weapon_type', r'[\w, -/]+?'))
    weapon_flags = simple_str("Weapon flags")
    damage_type = simple_str("Damage type")
    damage_dice = re.compile(r'.*Damage(?: dice)?:\s+(?P<dice_count>\d+)d(?P<dice_size>\d+) \(average (?P<average>[\d.]+)\).*')
    # damage_line = re.compile(r'.*Damage( dice)?:\s+(?P<dice_count>\d+)d(?P<dice_size>\d+) \(average (?P<average>[\d.]+)\).*')
    ac_pierce = re.compile(pipe_re("AC vs pierce", "ac_pierce", num_re), re.IGNORECASE)
    ac_bash =   re.compile(pipe_re("AC vs bash",   "ac_bash", num_re), re.IGNORECASE)
    ac_slash =  re.compile(pipe_re("AC vs slash" , "ac_slash", num_re), re.IGNORECASE)
    ac_magic =  re.compile(pipe_re("AC vs magic",  "ac_magic", num_re), re.IGNORECASE)
    ac_other =  re.compile(pipe_re("AC vs other",  "ac_other", num_re), re.IGNORECASE)
     # = simple_str("")
     # = simple_str("")

    regexen = [
        name, weight, size, level, material, item_type, spell, flags, size,
        multiplier, capacity, wear, weapon_type, weapon_flags, damage_type,
        damage_dice, damage_dice, ac_pierce, ac_bash, ac_slash, ac_magic, ac_other,
        spell_mod, color, liquid, charges, hp_regen, mana_regen
    ]

    affect = re.compile('.*Affects (?P<stat>[\w ]+) by (?P<amount>[\d-]+).*')
    affect2 = re.compile('\| -\s+(?P<stat>[\w \(\)]+)\s+(?P<amount>[\d-]+)')
    affect_regexen = [affect, affect2]

    for obj_lines in object_lines:
        current_object = {}

        for line in obj_lines:
            if 'Object' in line:
                pass

            if '+------' in line:
                continue
            elif '| -----'  in line:
                continue
            found = False
            for regex in regexen:
                if not found and regex.match(line):
                    current_object = merge(current_object, regex.match(line).groupdict())
                    found = True

            for regex in affect_regexen:
                if regex.match(line):
                    found = True
                    if 'affects' not in current_object:
                        current_object['affects'] = {}
                    group = regex.match(line).groupdict()
                    current_object['affects'][group['stat']] = group['amount']

            if not found:
                if 'Effect' in line and 'Modifies' in line:
                    # '| Effect Modifies           Modifier  |'
                    continue
                # if '//' not in line:
                #     import pdb; pdb.set_trace()
                if 'comments' not in current_object:
                    current_object['comments'] = []
                current_object['comments'].append(line)
        objects.add(Item(current_object))
    return objects


from pprint import pprint
# print("Known: ", len(objects))




def best_items_with_affect(affect, limit=20, minimum=None, maximum=None):
    print("affect: ", affect)
    looking_for = set()
    for i in objects:
        item = i.item
        if 'affects' not in item:
            continue
        if affect not in item['affects']:
            continue
        if minimum is not None and int(item['affects'][affect]) < minimum:
            continue
        if maximum is not None and int(item['affects'][affect]) > maximum:
            continue
        looking_for.add(i)
    return sorted(looking_for, key=lambda x: x.item['affects'][affect], reverse=True)[0:limit]
    
    

# pprint(['comments' in x and x['comments'] for x in looking_for])
# pprint(looking_for)
# print(len(looking_for))
# items = sorted(looking_for, key=lambda x: x.item['affects']['hit roll'], reverse=True)[0:20]
# for item in items:
#     print(f"{item.item['affects']['hit roll']}: {item.item['name']} {item.item['comments']}")



# affect = 'hp'
# for item in best_items_with_affect(affect, limit=30, minimum=0):
#     try:
#         affect_score = item.item['affects'][affect]
#     except: 
#         print(item.item)
#     # print(f"{item.item['affects'].get('saves')} / {item.item['affects'].get('hp')}: {item.item['name']} {item.item.get('comments')}")
#     from pprint import pprint
#     print(f"{item.item['name']}\n\t{item.item['affects']}\n\t{item.item.get('comments')}")

def printItem(item):
    if item is None:
        return print('Not found')
    item = item.item
    print(f"{item.get('name', {})}\n\tAffects: {item.get('affects')}\n\t{item.get('comments')}")


def fetch_by_name(name, objects):
    matches = []
    for x in objects:
        if x.item.get('name') == name:
            matches.append(x)
    if matches:
        return matches[0]
    return None


def main(args):
    objects = []

    if path.exists('./old-items.txt'):
        with open('./old-items.txt', 'r') as f:
            old_text = f.read()
            objects.extend(get_objects__old_format(old_text))

    if path.exists('./new-items.txt'):
        with open('./new-items.txt', 'r') as f:
            new_text = f.read()
            objects.extend(get_objects__new_format(new_text))
    
    if args.name is not None:
        return printItem(fetch_by_name(args.name, objects))

    if args.dump_highlights is not None:
        for item in objects:
            name = item.item.get('name')
            if not name:
                continue
            print("#highlight {%s} {dark orange}" % name)

        # return printItem(fetch_by_name(args.name, objects))

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', help='find item by name')
    parser.add_argument('--dump-highlights', action='store_const', const=True,
                        help='dump all known items into a highlights file for tt++')

    main(parser.parse_args())
