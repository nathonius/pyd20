#!/usr/bin/env python
"""DnD Roller Nathan Smith 2013/06/26"""
import random
import argparse

def main():
	random.seed()
	parser = argparse.ArgumentParser(description="DnD Roller")
	parser.add_argument('dice', nargs='*', help="Dice to roll. Examples: [d10, 2d5 1d8, 4d12, d27] d2 flips a coin.")
	parser.add_argument('-s', nargs='*', type=str, dest='special', help="Special dice to roll.")
	parser.add_argument('-m', '--multiple', action='store_true', dest='multiple', default=False, help="Enter interactive roll mode.")
	args = parser.parse_args()

	if(args.multiple == True):
		roll_console()
	else:
		try:
			roll(args)
		except:
			parser.error("Invalid dice! Dice should be in the format d10, 2d20, etc. Do not comma separate dice!")
	print(""),

def roll(args):
	"""Roll all given dice"""
	if(args.dice != None):
		(dice, coins) = getDice(args.dice)
		#We have our dice, now we roll. Coins first
		if(coins != 0):
			print("\nCoin Toss(es):\t")
			flipCoins(coins)
			print("")
		#Now dice
		if(len(dice) > 0):
			print("\nDice Total:")
			getRolls(dice)
	if(args.special != None):
		(sdice, scoins) = getDice(args.special)
		#We have our dice, now we roll. Coins first
		if(scoins != 0):
			print("\nSpecial Coin(s):\t")
			flipCoins(scoins)
			print("")
		#Now dice
		if(len(sdice) > 0):
			print("\nSpecial Dice:")
			getRolls(sdice)

def roll_console():
	"""Interactive roller"""
	helptext = "\nWelcome to the interactive roller.\nEnter a roll, press enter to re-roll, or enter q to quit."
	print(helptext)
	lastroll = None
	while True:
		try:
			#Ask for input
			buff = raw_input(">>> ")
			#Quit?
			if(buff.lower() == 'q'):
				break
			elif(buff == "" and lastroll != None):
				roll(lastroll)
			else:
				buff = buff.split(" ")
				if("-s" in buff):
					dice = buff[:buff.index("-s")]
					spec = buff[buff.index("-s")+1:]
					args = consoleArgs(dice, spec)
				else:
					args = consoleArgs(buff, None)
				lastroll = args
				roll(args)
		except:
			print("Invalid dice! Dice should be in the format d10, 2d20, etc. Do not comma separate dice!")
			continue

class consoleArgs:
	def __init__(self, dice, special):
		self.dice = dice
		self.special = special

class die:
	"""Die class. Can be 'rolled' by calling roll function"""
	def __init__(self, sides):
		self.sides = sides
	def roll(self):
		return random.randint(1, self.sides)

def flipCoins(coins):
	"""Flip a bunch of coins!"""
	for i in range(coins):
		flip = random.randint(1, 2)
		if(flip == 1):
			print("HEADS\t"),
		else:
			print("TAILS\t"),

def getRolls(dice):
	"""Print out the values of the rolls"""
	#Print the dice
	for each in dice:
		print('{:<7}'.format("d"+str(each.sides))),
	#Print the values
	print("\n"),
	total = 0
	for i in range(len(dice)):
		thisRoll = dice[i].roll()
		total += thisRoll
		print('{:<4}'.format(str(thisRoll))),
		if(i != len(dice)-1):
			print("+ "),
	print("= "+str(total))
	return total

def getDice(dices):
	"""Figure out what our dice are."""
	dice = []
	coins = 0
	for item in dices:
		#How many are we rolling?
		number = 0
		if(item.startswith('d')):
			number = 1
		else:
			number = int(item.split("d")[0])
		if(number < 0):
			raise AttributeError("Cannot have negative dice!")
		#How many sides?
		sides = 0
		if(item.startswith('d')):
			sides = int(item[1:])
		else:
			sides = int(item.split("d")[1])
		if(sides < 0):
			raise AttributeError("Cannot have negative sides!")
		#Are they coins?
		if(sides == 2):
			coins += number
		else:
			for x in range(number):
				dice.append(die(sides))
	return (dice, coins)

if __name__ == "__main__":
    main()