import re
from utils import preprocess_line, merge, Item

def get_objects__old_format(text):
    objects = []
    object_lines = []
    current_lines = []
    for line in text.splitlines():
        line = preprocess_line(line)
        if preprocess_line(line).strip() != "":
            current_lines.append(line)
        else:
            object_lines.append(current_lines)
            current_lines = []
    object_lines.append(current_lines)


    name = re.compile(r"Object: '(?P<name>[\w -\\\'\\\"]+)' is type (?P<armor_type>\w+).")
    weapon_type = re.compile("Weapon type is (?P<weapon_type>\w+).")
    damage = re.compile("Damage is (?P<dice_count>\d+)d(?P<dice_size>\d+) \(average (?P<avg>\d+)\).?")
    # @@@ check it parses negative stoo
    affect = re.compile("Affects (?P<stat>[\w ]+) by (?P<amount>[\d-]+).?")
    comment = re.compile(r"[/\\]+(?P<comment>.*)")
    armor = re.compile("Armor class is (?P<pierce>\d+) pierce, (?P<bash>\d+) bash, (?P<slash>\d+) slash, and (?P<magic>\d+) vs. magic.")
    extra_flags = re.compile("Extra flags (?P<flags>[\w -]+)")
    material = re.compile("Material is (?P<material>\w+)\.?")
    # Note: This explicitly excludes the 'value' param in lore. I don't think it's particularly useful to me
    weight = re.compile("Weight is (?P<weight>[\d.]+\d+),.*? level is (?P<level>\d+)\.?")
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
