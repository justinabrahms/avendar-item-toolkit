#!/usr/bin/env python3
from os import path
import re
from hashlib import sha256
from parse_old import get_objects__old_format
from parse_new import get_objects__new_format


dim = lambda x: f"\033[90m{x}\033[0m"




from pprint import pprint
# print("Known: ", len(objects))




def best_items_with_affect(objects, affect, limit=20, minimum=None, maximum=None):
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

def printItem(item, debug=False):
    if item is None:
        return print('Not found')
    item = item.item
    retval = f"{item.get('name', {})}  (New format? {item.get('new_format', False)})\n"
    if item.get('level'):
        retval += dim(f"\tLevel: {item.get('level')}\n")
    if item.get('comments'):
        retval += f"\tComments: {item.get('comments')}\n"
    if item.get('flags') is not None:
        retval += dim(f"\tFlags: {item.get('flags')}\n")
    if item.get('weight'):
        retval += dim(f"\tWeight: {item.get('weight')}\n")
    if item.get('avg') or item.get('average'):
        count = item.get('dice_count')
        size = item.get('dice_size')
        retval += f"\tDice: {count}d{size} (Avg {item.get('avg') or item.get('average')})\n"
        retval += dim(f"\tWeapon type: {item.get('weapon_type')}\n")
        dtype = item.get('damage_type')
        if dtype is not None:
            retval += dim(f"\tDamage type: {dtype}\n")
        wflags = item.get('weapon_flags')
        if wflags is not None:
            retval += dim(f"\tWeapon flags: {wflags}\n")
    if item.get('comment'):
        retval += f"\tComment: {item.get('comment')}\n"
    if item.get('spell'):
        retval += f"\tSpell: {item.get('spell')}\n"
    affects = item.get('affects')
    if affects is not None:
        for key, val in affects.items():
            retval += f"\t{key}: {val}\n"
    if debug:
        retval += 'Keys: %s\n' % ' '.join(item.keys())
    print(retval)


def fetch_by_name(name, objects):
    matches = []
    for x in objects:
        if x.item.get('name') == name:
            matches.append(x)
    if matches:
        return matches[0]
    return None

def fuzzy_find_by_name(name, objects):
    matches = []
    for x in objects:
        if name in x.item.get('name'):
            matches.append(x)
    if matches:
        return set(matches)
    return None
    


def main(args):
    if args.find is not None:
        args.find = ' '.join(args.find)
    if args.name is not None:
        args.name = ' '.join(args.name)

    objects = []

    if path.exists('./old-items.txt'):
        with open('./old-items.txt', 'r') as f:
            old_text = f.read()
            objects.extend(get_objects__old_format(old_text))

    if path.exists('./new-items.txt'):
        with open('./new-items.txt', 'r') as f:
            new_text = f.read()
            objects.extend(get_objects__new_format(new_text))

    if path.exists('./more-new-items.txt'):
        with open('./more-new-items.txt', 'r') as f:
            new_text = f.read()
            objects.extend(get_objects__new_format(new_text))

    objects.reverse() # newest first
    
    if args.name is not None:
        return printItem(fetch_by_name(args.name, objects), debug=args.debug)

    if args.find is not None:
        items = sorted(fuzzy_find_by_name(args.find, objects))
        return [printItem(x, debug=args.debug) for x in items]

    if args.dump_highlights is not None:
        for name in set([x.item.get('name') for x in objects]):
            # name = item.item.get('name')
            if not name:
                continue
            print("#highlight {%s} {orange}" % name)

        # return printItem(fetch_by_name(args.name, objects))

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', help='find item by name', nargs='+')
    parser.add_argument('--debug', help='print known properties when dumping item', action="store_true")
    parser.add_argument('--find', help='fuzzy find item by name', nargs='+')
    parser.add_argument('--dump-highlights', action='store_const', const=True,
                        help='dump all known items into a highlights file for tt++')

    main(parser.parse_args())
