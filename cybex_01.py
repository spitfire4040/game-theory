# import libraries
from __future__ import division
import sys
import os
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import math

# initialize variables
Sc = 0.0    # set initial value for Sc, amount shared in Cybex
Sf = 0.0    # set initial value for Sf, amount shared in firm
x = 0.01   	# set cost per GB for processing
Q = 0.0     # set initial value for Q, quality of data in cybex
R = 0.0		# set initial value for R, risk level in cybex
Ra = 0.0    # set initial value for Ra
I = 0.0		# set current investment level
Ia = 0.0	# last average investment level
In = 0.0	# new average investment by firm
r = 0.0     # set initial value for r
a = 1		# scaling factor for sharing utility
b = 1		# scaling factor for value
c = 1		# cost charged by CYBEX for participation (this needs to be fluctuated by CYBEX to stimulate sharing)

investflag = False
zeroshareflag = False

# open file and insert previous values
if not os.path.isfile('/home/jay/Desktop/cybex.txt'):

	# prompt user for initial investment level if 1st run
	I = float(input("Enter the amount of your current security investment: "))
	investflag = True
else:
	with open('/home/jay/Desktop/cybex.txt', 'r') as infile:
		input_list = []
		for line in infile:
			input_list.append(line)

		# input values from file (last round)
		Ia = float(input_list[0])
		Q = float(input_list[1])
		Ra = float(input_list[2])
		Sc = float(input_list[3])
		Sf = float(input_list[4])

# set flag for recheck investment level
if investflag == False:

	# prompt user for investment, amount, and quality of data to be shared
	change = input("Would you like to change your initial investment? 1-yes, 2-no: ")
	if change == '1':
		I = float(input("Enter the amount of your new security investment: "))

# get current values for s
s = float(input("Enter amount in GB to share: "))
if s <= 0:
	s = 1
	zeroshareflag = True

# get current value for q
q = float(input("Enter avg. quality (.001-1): "))
if q <= 0:
	q = .001
if q > 1:
	q = 1

# enter privacy level
p = float(input("Enter your privacy level (.001-1) "))
if p <= 0:
	p = .001
if p > 1:
	p = 1

# set In
if Ia <= 0:
	In = I
elif Ia > 0 and I == 0.0:
	In = Ia
else:
	In = ((Ia * Sf) + (I * s)) / (Sf + s)
	#Ra = ((Ra * Sf) + (R * s)) / (Sf + s)

# update average quality of data in CYBEX
Q = ((Q * Sc) + (q * s))/(Sc + s)

# calculate risk multiplier for firm based on investment level and amount of data shared
r1 = (1 / In)
r2 = (s * (1/q))
R = (r1 * r2)

# update averate risk level for firm
Ra = ((Ra * Sf) + (R * s)) / (Sf + s)

# processing cost for current transaction
X = (x * s)

# check for zeroshareflag
if zeroshareflag == False:
	# add shared data to CYBEX running total
	Sc += s

	# add shared data to firm's running total
	Sf += s

# calculate current value of CYBEX data for sharing (for the firm)
V2 = (b * (math.log(1 + (Sc * Q)))) - Ra 	# this is the current value of CYBEX
V1 = (b * (math.log(1 + (s * q)))) - Ra 	# this is the current value of the firm
V0 = (V1 - (V1 * p))						# this is the value of the firm with privacy

# calculate sharing utility
if V2 - V0 < 0:
	share = (a * math.log10(1 + In)) - x - c
else:
	share = (V2 - V0) * (a * math.log10(1 + In)) - x - c

# calculate not sharing utility
noshare = a * math.log10(1 + In)

# output current values for testing
print('****************************')
print('s: ',s)
print('Sc: ',Sc)
print('Sf: ',Sf)
print('X: ',X)
print('x: ',x)
print('q: ',q)
print('Q: ',Q)
print('r1: ',r1)
print('r2: ',r2)
print('R: ',R)
print('Ra: ',Ra)
print('a: ',a)
print('b: ',b)
print('c: ',c)
print('I: ',I)
print('In: ',In)
print('V0: ',V0)
print('V1: ',V1)
print('V2: ',V2)
print('share: ',share)
print('noshare: ',noshare)
print('****************************')

# print results
print('************************************')
print('current Value of firm with privacy (V0): ',V0)
print('Current Value of firm w/o privacy (V1): ',V1)
print('Current Value of CYBEX (V2): ',V2)
print('Average Investment by Firm: ',In)
print('Average Quality in CYBEX',Q)
print('Total Shared Data by Firm: ',Sf)
print('Total Shared Data in CYBEX: ',Sc)
print('Current Risk for Firm: ',R)
print('Average Risk for Firm: ',Ra)
print('Processing Cost: ',X)
print('Utility for Sharing: ',share)
print('Utility for Not Sharing: ',noshare)
print('************************************')

# generate bar graph
objects = ('share','noshare','V0 (x100)', 'V2 (x100)', 'Qual.', 'Risk', 'Process.')
y_pos = np.arange(len(objects))
performance = [share,noshare,V0,V2,Q,Ra,X]
plt.bar(y_pos, performance, align='center', alpha=0.5)
plt.xticks(y_pos, objects)
plt.ylabel('Utility')
plt.title('CYBEX Value and Variables')
plt.show()

# write current values to file for next round
with open('/home/jay/Desktop/cybex.txt','w') as outfile:
	outfile.write(str(In) + '\n')	# current average investment by firm
	outfile.write(str(Q) + '\n')	# average quality in CYBEX
	outfile.write(str(Ra) + '\n')	# average risk level in CYBEX
	outfile.write(str(Sc) + '\n')	# amount of data in CYBEX
	outfile.write(str(Sf) + '\n')	# total amount shared 