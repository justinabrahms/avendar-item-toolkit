import re
from utils import preprocess_line, merge, Item

def get_objects__new_format(text):
    objects = set()
    object_lines = []
    current_lines = []
    for line in text.splitlines():
        line = line.strip('#')
        line = preprocess_line(line)
        if line == "":
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
    # name = re.compile(pipe_re( "Object", "name", r'[\w, "\'"-]+?'))
    name = re.compile(pipe_re( "Object", "name", r'.*?'))
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
    ac_pierce = re.compile(pipe_re("AC vs pierce", "ac_pierce", num_re), re.IGNORECASE)
    ac_bash =   re.compile(pipe_re("AC vs bash",   "ac_bash", num_re), re.IGNORECASE)
    ac_slash =  re.compile(pipe_re("AC vs slash" , "ac_slash", num_re), re.IGNORECASE)
    ac_magic =  re.compile(pipe_re("AC vs magic",  "ac_magic", num_re), re.IGNORECASE)
    ac_other =  re.compile(pipe_re("AC vs other",  "ac_other", num_re), re.IGNORECASE)
     # = simple_str("")
     # = simple_str("")

    regexen = [
        name, weight, size, level, material, item_type, flags, spell, size,
        multiplier, capacity, wear, weapon_type, weapon_flags, damage_type,
        damage_dice, damage_dice, ac_pierce, ac_bash, ac_slash, ac_magic, ac_other,
        spell_mod, color, liquid, charges, hp_regen, mana_regen
    ]

    affect = re.compile('.*Affects (?P<stat>[\w ]+) by (?P<amount>[\d-]+).*')
    affect2 = re.compile('\| -\s+(?P<stat>[\w \(\)]+)\s+(?P<amount>[\d-]+)')
    affect_regexen = [affect, affect2]

    for obj_lines in object_lines:
        current_object = {'new_format': True}

        for line in obj_lines:
            if 'Object' in line:
                pass

            if '+------' in line:
                continue
            elif '--+' in line:
                continue
            elif '| -----'  in line:
                continue
            found = False
            for regex in regexen:
                if not found and regex.match(line):
                    if 'Spell:' in line:
                        # import pdb; pdb.set_trace()
                        pass
                    current_object = merge(current_object, regex.match(line).groupdict())
                    found = True

            for regex in affect_regexen:
                if regex.match(line):
                    found = True
                    if 'affects' not in current_object:
                        current_object['affects'] = {}
                    group = regex.match(line).groupdict()
                    current_object['affects'][group['stat']] = group['amount']

            if current_object.get('flags', False) == 'none':
                del current_object['flags']

            if not found:
                if 'Effect' in line and 'Modifies' in line:
                    # '| Effect Modifies           Modifier  |'
                    continue
                # if '//' not in line:
                #     import pdb; pdb.set_trace()
                if 'comments' not in current_object:
                    current_object['comments'] = []
                current_object['comments'].append(line)
        if current_object.get('name'):
            try:
                objects.add(Item(current_object))
            except:
                import pdb;pdb.set_trace()
    return objects

