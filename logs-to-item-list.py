from os import listdir
from os.path import isfile, join

logdir = '/home/justin/Dropbox/avendar'

filenames = [join(logdir, f) for f in listdir(logdir) if isfile(join(logdir, f)) and '.log' in f]
lines = []

for fname in filenames:
    with open(fname) as f:
        lines.extend(f.readlines())

started = False
object_lines = []
current_lines = []
for line in lines:
    if '+------' in line:
        if line.index('+') != 0:
            # remove prefixes if we find them
            line = line[line.index('+'):]
                      
        if started:
            started = False
            current_lines.append(line)
            object_lines.append(current_lines)
            current_lines = []
        else:
            started = True
    elif '|' not in line:
        if started:
            started = False
            current_lines.append(line)
            object_lines.append(current_lines)
            current_lines = []
        
            

    if started:
        current_lines.append(line)


for x in object_lines:
    print(''.join(x)) 


