# import libraries
from __future__ import division
import sys
import os
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import math

# initialize variables
Sc = 0.0    # set initial value for Sc
Sf = 0.0    # set initial value for Sf
x = 0.01   	# set cost per GB for processing
Q = 0.0     # set initial value for Q
Ra = 0.0    # set initial value for Ra
r = 0.0     # set initial value for r
a = 1		# scaling factor for sharing utility
b = 1		# scaling factor for value
c = 1		# cost charged by CYBEX for participation

# open file and insert previous values
if not os.path.isfile('/home/jay/Desktop/cybex.txt'):

	# prompt user for initial investment level if 1st run
	I = input("Enter the amount of your own security investment: ")
else:
	with open('/home/jay/Desktop/cybex.txt', 'r') as infile:
		input_list = []
		for line in infile:
			input_list.append(line)

		I = float(input_list[0])
		Q = float(input_list[1])
		Ra = float(input_list[2])
		Sc = float(input_list[3])
		Sf = float(input_list[4])

# prompt user for investment, amount, and quality of data to be shared
change = input("Would you like to change your initial investment? 1-yes, 2-no: ")
if change == 1:
	I = input("Enter the amount of your own security investment: ")	
s = input("Enter amount in GB to share: ")
q = input("Enter avg. quality (.1-10): ")

# update average quality of data in CYBEX
Q = ((Q * Sc) + (q * s))/(Sc + s)

# calculate risk multiplier for firm based on investment level and amount of data shared
#r = float((s * I) / 100)
r = ((s) / I)

# update averate risk level for firm
Ra = ((Ra * Sf) + (r * s)) / (Sf + s)

# processing cost for current transaction
X = (x * s)

# add shared data to CYBEX running total
Sc += s

# add shared data to firm's running total
Sf += s

# calculate current value of CYBEX data for sharing (for the firm)
V2 = (b * (math.log(1 + (Sc * Q)))) - Ra
V1 = (b * (math.log(1 + (s * q)))) - Ra

# calculate sharing utility
if V2 - V1 < 0:
	share = (a * math.log10(1 + I)) - x - c
else:
	share = (V2 - V1) * (a * math.log10(1 + I)) - x - c

# calculate not sharing utility
noshare = a * math.log10(1 + I)

# print results
print '************************************'
print 'Current Value of CYBEX (V1): ',V1
print 'Current Value of Firm (V2): ',V2
print 'Initial Investment: ',I
print 'Average Quality in CYBEX',Q
print 'Total Shared Data by Firm: ',Sf
print 'Total Shared Data in CYBEX: ',Sc
print 'Current Risk for Firm: ',r
print 'Average Risk for Firm: ',Ra
print 'Processing Cost: ',X
print 'Utility for Sharing: ',share
print 'Utility for Not Sharing: ',noshare
print '************************************'

# if value is greater than 0
if V1 > 0 and V2 > 0:

	# generate bar graph
	objects = ('V1 (x100)', 'V2 (x100)', 'Qual.', 'Risk', 'Process.')
	y_pos = np.arange(len(objects))
	performance = [V1,V2,Q,Ra,X]

	plt.bar(y_pos, performance, align='center', alpha=0.5)
	plt.xticks(y_pos, objects)
	plt.ylabel('Utility')
	plt.title('CYBEX Value and Variables')

	plt.show()

else:
	print 'No utility, value is less than zero'

with open('/home/jay/Desktop/cybex.txt','w') as outfile:
	outfile.write(str(I) + '\n')
	outfile.write(str(Q) + '\n')
	outfile.write(str(Ra) + '\n')
	outfile.write(str(Sc) + '\n')
	outfile.write(str(Sf) + '\n')