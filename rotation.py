from __future__ import division
import sys
import os
import math
import pickle
import matplotlib.pyplot as plt
import csv

players = [0]
val_array = []

# initialize variables
V1 = 0.0	# value of my current data
V2 = 0.0	# average value of cybex data
Sc = 0.0    # set initial value for Sc
Sf = 0.0    # set initial value for Sf
x = 0.01   	# set cost per GB for processing
Q = 0.0     # set initial value for Q
R = 0.0		# set initial value for R
Ra = 0.0    # set initial value for Ra
r1 = 0.0     # set initial value for r
r2 = 0.0
a = 1		# scaling factor for sharing utility
b = 1		# scaling factor for value
c = 1		# cost charged by CYBEX for participation
round = 0	# initialize round in game

def calculate(I,s,q):
	global round,Sc,Sf,Q,R,Ra,r,a,b,c,x,V1,V2

#	for x in range(0,10):
	for x in range(0,1):
		for player in players:

			# open file and insert previous values
			if not os.path.isfile('/home/jay/game-theory/cybex.txt'):
				pass
			else:
				with open('/home/jay/game-theory/cybex.txt', 'r') as infile:
					input_list = []
					for line in infile:
						input_list.append(line)

					Q = float(input_list[0])
					Sc = float(input_list[1])

			if not os.path.isfile('/home/jay/game-theory/' + str(player) + '.txt'):
				pass
			else:
				with open('/home/jay/game-theory/' + str(player) + '.txt', 'r') as infile:
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
			V2 = (b * (math.log(1 + (Sc * Q)))) - Ra   # this is the average value of the data in CYBEX
			V1 = (b * (math.log(1 + (s * q)))) - Ra    # this is the value of the data I'm sharing now

			# calculate sharing utility
			if V2 - V1 < 0:
				share = (a * math.log10(1 + I)) - x - c   # i'm the only one that has shared
			else:
				share = (V2 - V1) * (a * math.log10(1 + I)) - x - c   # value is the difference between CYBEX value and my value

			# write current values out to file
			with open('/home/jay/game-theory/cybex.txt','w') as outfile:
				outfile.write(str(Q) + '\n')
				outfile.write(str(Sc) + '\n')

			with open('/home/jay/game-theory/firm-' + str(player) + '.txt', 'w') as outfile:
				outfile.write(str(Ra) + '\n')
				outfile.write(str(Sf) + '\n')

			# save amount and quality of database to file as tuple list
			#val_array.append((round,player,I,s,q,Sc,Sf,Q,Ra,c,x,V2,V1))
			val_array.append((round,player,I,s,q,V2,V1))			
			round += 1

			with open('/home/jay/game-theory/cybex_value.txt', 'wb') as outfile:
				pickle.dump(val_array, outfile)

def graph():
	# global variables
	global round,player,I,s,q,Sc,Sf,Q,R,Ra,r1,r2,a,b,c,x,V1,V2

	# create .csv file from data
	with open('/home/jay/game-theory/cybex_value.csv', 'w') as csvFile:
		writer = csv.writer(csvFile)
		#writer.writerow(("round","player","invest.","quantity","quality","q-cybex","q-firm","av-quality","av-risk","cost-cybex","cost-proc","val-cybex","val-mydata"))
		writer.writerow(("round","invest.","quantity","quality","val-cybex","val-mydata"))
		writer.writerows(val_array)
	csvFile.close()


def main(argv):
	I = float(argv[1])
	s = float(argv[2])
	q = float(argv[3])
	calculate(I,s,q)
	graph()

if __name__ == '__main__':
	main(sys.argv)

#tuple example
#(player,I,s,q,Q,Sc,Sf,R,Ra,r1,r2,c,x)
#(round#,investment,quantity,quality,average-quality,quantity-in-cybex,quantity-in-firm,
#current-risk-sum,average-risk,risk-investment,risk-quantity,scaling-factor-value,scaling-factor-value,cybex-cost,processing-cost)