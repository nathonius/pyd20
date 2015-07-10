#pyd20
##A (Fancy) Dice Roller
I wrote pyd20 over the span of a very long time - writing and rewriting over and over. It's been a pet project of mine focused more on the code itself over the functionality of the project. However, it's now in a workable state.

###Requirements
Python 3.x

###Installation
Just clone this repo and place roll.py somewhere easy to access. I like to make a symlink or add it to my path so I can just call roll from any directory.

###Usage
General usage is like so:
`$ roll.py 1d20+3, 2d8+5 + 3d6, d2`
This will produce the output:
`[1d20=4]+3 = 7`
`[2d8=9]+5+[3d6=9] = 23`
`[1d2=1] = 1`

As you can see, dice are treated just like numbers. You can add, subtract, multiply, or even divide them. Parentheses are also understood. Each statement should be separated by a comma.

Additionally, if you wish to roll multiple dice, running `$ roll.py -m` will enter the dice rolling console which supports history like a terminal. For example:
`$ roll.py -m`
`Enter q to quit.`
`>>> 4d4+3`
`[4d4=14]+3 = 17`
`>>> `

Dice can also make use of some advanced options.

| Option | Description | Example |
| --- | --- | --- |
| `k<h/m/l><x>` | Keep x highest/middle/lowest dice. | `10d10kh3` might give `[3d10=28]` |
| `s<m/b><x>` | The die is successful if it meets/beats x. Defaults to meets. Useful in tandem with the groupie option. Unsuccessful dice are not counted toward the total. However any +/- modifiers following them are counted. | `1d20sb17` is a d20 that is successful if it beats 17. |
| `g` | This die's value is only used if the previous die was successful. This die is unsuccessful if the previous die was unsuccessful, even if this die also has the success option specified. | `1d20s10 + 2d8g` might give `[1d20=1(failed)] + [2d8=8(failed)] = 0` |
