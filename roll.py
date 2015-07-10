#!/usr/bin/env python3
"""DnD Roller Nathan Smith 2013/06/26"""
import random
import argparse
import cmd
import re
import statistics


def main():
    """Types:
    parser: ArgumentParser
    args: namespace"""
    random.seed()
    parser = argparse.ArgumentParser(description="DnD Roller")
    parser.add_argument('dice', nargs='*', help="Dice to roll.")
    parser.add_argument('-m', '--multiple', action='store_true', dest='multiple', default=False,
                        help="Enter interactive roll mode.")
    args = parser.parse_args()

    if args.multiple:
        print("Enter q to quit.")
        console = RollConsole()
        console.prompt = ">>> "
        console.cmdloop()
    elif not args.dice:
        parser.print_help()
    else:
        if args.dice != "":
            roll_dice(args.dice)


class RollConsole(cmd.Cmd):
    def default(self, line):
        if line != "":
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
        self.success: bool"""
        self.value = 0
        self.values = []
        self.options = {}
        # self.success will be set true/false if 's' option is specified
        self.success = True
        # Get the sides of the dice and any options (re.findall returns ([group1, group2]), so we get the 0th element)
        try:
            self.die_string, options = re.findall(r"(\d*d\d+)([a-ce-np-z0-9]+)?", args)[0]
        except IndexError:
            print("No valid dice found!")
            raise
        # If the input is in the form d20, d10, d4, etc, we change it to 1d20, 1d10, 1d4, etc.
        if self.die_string.startswith('d'):
            self.times = 1
        # Otherwise, we extract how many times to roll die_string.split('d') should give [x, y] where input is xdy
        else:
            self.times = int(self.die_string.split('d')[0])
        self.sides = int(self.die_string.split('d')[1])
        # Roll the die
        self.roll(self.sides, self.times)
        # Parse options into dictionary for ease of use
        self.parse_options(options)

    def __repr__(self):
        if self.success:
            return str(self.value)
        else:
            return "0"

    def __str__(self):
        if self.success :
            return "[" + str(self.times) + "d" + str(self.sides) + "=" + str(self.value) + "]"
        else:
            return "[" + str(self.times) + "d" + str(self.sides) + "=" + str(self.value) + "(failed)]"

    def roll(self, sides, times):
        for i in range(times):
            die = random.randint(1, sides)
            self.values.append(die)
            self.value += die

    def parse_options(self, options):
        """Types:
        options: string
        keep: re.match object
        success: re.match object
        dice_to_keep: int
        which_to_keep: string
        middle_values: list of ints
        middle: int

        Possible Options:
        k<h/m/l><num> - keep highest/middle/lowest number of dice
        s<b/m><num> - sets this die's success if it beats/meets (default is meets) value
        g - roll is only counted if previous roll is successful"""
        # Check for keep option
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
                    # Sum the middle x values. Works by taking the (high) median of the set out until we have enough.
                    middle_values = []
                    for i in range(dice_to_keep):
                        middle = statistics.median_high(self.values)
                        middle_values.append(middle)
                        self.values.remove(middle)
                    self.value = sum(middle_values)
                    self.values = middle_values
                self.times = dice_to_keep
        # Check for success option
        success = re.search(r"s[bm]?\d+", options)
        if success:
            test_value = int(re.search(r"\d+", success.group(0)).group(0))
            # Success if x beats y
            if "b" in success.group(0):
                self.success = self.value > test_value
            # Success if x beats or meets y
            else:
                self.success = self.value >= test_value
        # Set the groupie option
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
                try:
                    dice.append(Die(die_string))
                except IndexError:
                    return
        # Check groupies
        dice = eval_groupies(dice)
        # Numerical is the string we can eval, displayed includes the dice as well as results.
        numerical = ""
        displayed = ""
        for die in dice:
            if is_operator(die):
                numerical += die
                displayed += die
            else:
                numerical += repr(die)
                displayed += str(die)
        # Eval, and add the result to the displayed string
        result = eval(numerical)
        displayed = displayed + " = " + str(result)
        results.append(displayed)

    # Show the user something. Print groups on separate lines.
    output = "\n".join(results)
    print(output)


def eval_groupies(dice):
    """Types:
    last_die: Die object/None, used for groupies
    dice: list of Die objects AND operator strings"""
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
    """Actually returns True if criteria is an operator ()+-*/\\ OR it is a integer"""
    return type(criteria) is str and (criteria in ("()+-*/\\") or criteria.isdigit())


if __name__ == "__main__":
    main()
