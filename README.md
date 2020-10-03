# Avendar ID Parser

This is a toolset I use when playing avendar.net, a text-based roleplaying game
that's been going on for many years. This program will parse your game logs for 
identification of items, so you can more easily find things of interest. It's 
currently more of a database, but eventually, it would be nice for it to do 
equipment optimization as well.

## Usage

### Index your logs 
This looks for .log files by default. It will print out just the item blocks, which you can then process later.

```
$ python3 logs-to-item-list.py --logdir ~/Dropbox/avendar/ > item_descriptions.txt
```

### Use the logs to find items
#### By name
```
$ python3 avendar-id-parser.py --name a doublet of meshed steel
a doublet of meshed steel  (New format? True)
        Level: 30
        Weight: 11.0
        hp: 5
        hit roll: 1
        damage roll: 1
```

#### By partial name
```
$ python3 avendar-id-parser.py --find meshed
a doublet of meshed steel  (New format? True)
        Level: 30
        Weight: 11.0
        hp: 5
        hit roll: 1
        damage roll: 1

some sleeves of meshed steel  (New format? True)
        Level: 30
        Weight: 8.0
        hp: 2
        damage roll: 1

a skirt of meshed steel  (New format? False)
        Level: 30
        Flags: none
        Weight: 5.0
        Comment:  Brintor Mountains
        hp: 3
        damage roll: 1
```