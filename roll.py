#!/usr/bin/env python3
"""DnD Roller Nathan Smith 2013/06/26"""
import random
import argparse
import cmd
import re
import statistics


def main():
    random.seed()
    parser = argparse.ArgumentParser(description="DnD Roller")
    parser.add_argument('dice', nargs='*', help="Dice to roll.")
    parser.add_argument('-m', '--multiple', action='store_true', dest='multiple', default=False,
                        help="Enter interactive roll mode.")
    args = parser.parse_args()

    if args.multiple:
        console = RollConsole()
        console.prompt = ">>> "
        console.cmdloop()
    elif not args.dice:
        parser.print_help()
    else:
        roll_dice(args.dice)


class RollConsole(cmd.Cmd):
    def default(self, line):
        roll_dice(line)

    def do_EOF(self, line):
        return True

    def do_q(self, line):
        return True


class Die:
    def __init__(self, args):
        """Types:
        self.die_string: string
        self.options: dict
        self.times: int
        self.sides: int
        self.value: int
        self.values: list of ints
        self.success: bool/None"""
        self.value = 0
        self.values = []
        self.options = {}
        # self.success will be set true/false if s option is specified
        self.success = None
        # Get the sides of the dice and any options
        self.die_string, options = re.findall(r"(\d*d\d+)([a-ce-np-z0-9]+)?", args)[0]
        if self.die_string.startswith('d'):
            self.times = 1
        else:
            self.times = int(self.die_string.split('d')[0])
        self.sides = int(self.die_string.split('d')[1])
        # Roll the die
        self.roll(self.sides, self.times)
        # Parse options into dictionary for ease of use
        self.parse_options(options)

    def __repr__(self):
        return str(self.value)

    def __str__(self):
        if self.value != 0:
            return "[" + str(self.times) + "d" + str(self.sides) + "=" + str(self.value) + "]"
        else:
            return "[" + str(self.times) + "d" + str(self.sides) + "=FAILED]"

    def roll(self, sides, times):
        for i in range(times):
            die = random.randint(1, sides)
            self.values.append(die)
            self.value += die

    def parse_options(self, options):
        """Types:
        options: string

        Possible Options:
        k<h/m/l><num> - keep highest/middle/lowest number of dice
        s<b/m><num> - sets this die's success if it beats/meets (default is meets) value
        g - roll is only counted if previous roll is successful"""
        # Check for each option
        keep = re.search(r"k[hml]\d+", options)
        if keep:
            dice_to_keep = int(keep.group(0)[2:])
            # If we are keeping all the dice, we don't need to do anything, so we check that its less than
            if dice_to_keep < len(self.values):
                which_to_keep = keep.group(0)[1]
                if which_to_keep is "h":
                    # Sum the highest x, works by sorting then slicing the list
                    self.value = sum(sorted(self.values)[len(self.values)-dice_to_keep:])
                elif which_to_keep is "l":
                    # Sum the lowest x, works by sorting (reversed), then slicing the list
                    self.value = sum(sorted(self.values, reversed=True)[len(self.values)-dice_to_keep:])
                else:
                    # Sum the middle x values
                    middle_values = []
                    for i in range(dice_to_keep):
                        middle = statistics.median_low(self.values)
                        middle_values.append(middle)
                        self.values.remove(middle)
                    self.value = sum(middle_values)
                    self.values = middle_values
                self.times = dice_to_keep

        success = re.search(r"s[bm]?\d+", options)
        if success:
            test_value = int(re.search(r"\d+", success.group(0)).group(0))
            if "b" in success.group(0):
                self.success = self.value > test_value
            else:
                self.success = self.value >= test_value
        self.options["g"] = "g" in options


def roll_dice(dice_groups):
    """Types:
    dice_groups: list
    dice_and_operators: list
    die_string: string
    dice: list of die objects AND operators
    numerical: string
    displayed: string
    result: int
    results: list of ints"""

    # Remove whitespace and split based on commas
    dice_groups = "".join(dice_groups)
    dice_groups = dice_groups.replace(" ", "")
    dice_groups = dice_groups.split(",")
    results = []

    # Process each group
    for group in dice_groups:
        # split into dice and operators/parens
        dice_and_operators = re.split(r"([()+*/-])", group)
        # Remove all empty strings
        dice_and_operators = filter(bool, dice_and_operators)
        # Build and roll dice objects
        dice = []
        for die_string in dice_and_operators:
            if is_operator(die_string):
                dice.append(die_string)
            else:
                dice.append(Die(die_string))
        # Check groupies
        dice = eval_groupies(dice)
        # Put it all together and eval
        numerical = ""
        displayed = ""
        for die in dice:
            if is_operator(die):
                numerical += die
                displayed += die
            else:
                numerical += repr(die)
                displayed += str(die)
        result = eval(numerical)
        displayed = displayed + " = " + str(result)
        results.append(displayed)

    # Show the user something
    output = "\n".join(results)
    print(output)


def eval_groupies(dice):
    last_die = None
    for i in range(len(dice)):
        if is_operator(dice[i]):
            continue
        else:
            # Eval groupies
            if dice[i].options["g"]:
                # If this is the first die or the last die failed, this one is 0 and not successful
                if last_die is None or not dice[last_die].success:
                    dice[i].value = 0
                    dice[i].success = False
                # Unless the die has already been deemed failing
                elif dice[i].success is False:
                    pass
                # Otherwise, it is successful
                else:
                    dice[i].success = True
            last_die = i
    return dice


def is_operator(criteria):
    return type(criteria) is str and (criteria in ("()+-*/\\") or criteria.isdigit())


if __name__ == "__main__":
    main()
