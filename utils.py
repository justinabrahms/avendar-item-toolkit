def preprocess_line(line):
    return line\
        .strip()\
        .replace('[22m', '')\
        .replace('[38;5;130m', '')\
        .replace('[0m', '')\
        .replace('[1;37m', '')

def merge(left,right):
    for k in right.keys():
        if k in left:
            if left[k] != right[k]:
                if type(left[k]) not in (list, set):
                    left[k] = [left[k]]
                left[k].append(right[k])
        else:
            left = {**left, **right}
    return left

class Item(object):
    def __init__(self, item):
        self.item = item

    def __str__(self):
        return self.item['name']

    def __repr__(self):
        return 'Item("' + self.item['name'] + '")'

    def __eq__(self, other):
        return self.item['name'] == other.item['name']

    def __gt__(self, other):
        mine = self.item['level']
        theirs = other.item['level']
        if isinstance(mine, list):
            mine = mine[0]
        if isinstance(theirs, list):
            theirs = theirs[0]
        
        return int(mine) > int(theirs)

    def __hash__(self):
        try:
            return hash(self.item['name'])
        except:
            print("ERROR on generating hash for item %s", self.name)
