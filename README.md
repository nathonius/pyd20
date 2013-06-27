So I’ve had DnD on the brain lately, and so I made up a dice roller with a CLI.

Usage is like so:

roll.py d10 d20 2d8

This will roll 1d10, 1d20, and 2d8. There are a few other features:

roll.py 4d2 -s 1d5

This will flip four coins (‘d2′s are read as coins) and roll one ‘special’ 5 sided die. It wouldn’t be totalled up with any other dice. There is also an interactive mode where you can roll many dice at a quicker pace. Just run:

roll.py -m
