from __future__ import division
import sys
import os
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import math

players = [0,1,2,3,4,5,6,7,8,9]

def calculate(I,s,q):

	for x in range(0,10):
		for player in players:

			# initialize variables
			Sc = 0.0    # set initial value for Sc
			Sf = 0.0    # set initial value for Sf
			x = 0.01   	# set cost per GB for processing
			Q = 0.0     # set initial value for Q
			R = 0.0		# set initial value for R
			Ra = 0.0    # set initial value for Ra
			r = 0.0     # set initial value for r
			a = 1		# scaling factor for sharing utility
			b = 1		# scaling factor for value
			c = 1		# cost charged by CYBEX for participation

			# open file and insert previous values
			if not os.path.isfile('/home/jay/Desktop/cybex.txt'):
				pass
			else:
				with open('/home/jay/Desktop/cybex.txt', 'r') as infile:
					input_list = []
					for line in infile:
						input_list.append(line)

					Q = float(input_list[0])
					Sc = float(input_list[1])

			if not os.path.isfile('/home/jay/Desktop/' + str(player) + '.txt'):
				pass
			else:
				with open('/home/jay/Desktop/' + str(player) + '.txt', 'r') as infile:
					input_list = []
					for line in infile:
						input_list.append(line)

					Ra = float(input_list[0])
					Sf = float(input_list[1])

			# update average quality of data in CYBEX
			Q = ((Q * Sc) + (q * s))/(Sc + s)

			# calculate risk multiplier for firm based on investment level and amount of data shared
			r1 = (1 / I)
			r2 = (s * (1/q))
			R = (r1 * r2)

			# update averate risk level for firm
			Ra = ((Ra * Sf) + (R * s)) / (Sf + s)

			# processing cost for current transaction
			X = (x * s)

			# add shared data to CYBEX running total
			Sc += s

			# add shared data to firm's running total
			Sf += s

			# calculate current value of CYBEX data for sharing (for the firm)
			V2 = (b * (math.log(1 + (Sc * Q)))) - Ra   # this is the value of the data in CYBEX plus my data
			V1 = (b * (math.log(1 + (s * q)))) - Ra    # this is the value of my data only

			# calculate sharing utility
			if V2 - V1 < 0:
				share = (a * math.log10(1 + I)) - x - c   # i'm the only one that has shared
			else:
				share = (V2 - V1) * (a * math.log10(1 + I)) - x - c   # value is the difference between CYBEX value and my value

			# calculate not sharing utility
			noshare = a * math.log10(1 + I)

			# if share > noshare:
			# 	print('Player-' + str(player) + ' chooses to share')
			# else:
			# 	print('Player-' + str(player) + ' chooses not to share')
			print('player-' + str(player) + ' share = ',share)
			print('player-' + str(player) + ' share = ',noshare)

			# write current values out to file
			with open('/home/jay/Desktop/cybex.txt','w') as outfile:
				outfile.write(str(Q) + '\n')
				outfile.write(str(Sc) + '\n')

			with open('/home/jay/Desktop/firm-' + str(player) + '.txt', 'w') as outfile:
				outfile.write(str(Ra) + '\n')
				outfile.write(str(Sf) + '\n')

def main(argv):
	calculate(1000,25,1)

if __name__ == '__main__':
	main(sys.argv)