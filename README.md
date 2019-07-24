# game-theory
Game theory project for CYBEX-P
Variables:

Sc – total shared with CYBEX
Sf – total shared by firm
s – amount of data currently being shared by firm
X – current cost of processing
x – processing cost to firm for sharing
Q – average quality of data in CYBEX
q – quality of data currently being shared
R – average risk level of data in CYBEX
Ra – average risk level for firm
I – investment level by firm for current round
Ia – previous average risk level for firm
In – current average risk level for firm
a – smoothing factor for calculating share/noshare
b – smoothing factor for calculating utility
c – cost charged/paid out  by CYBEX to firms
V0 – current value of shared data by firm including privacy factor
V1 – current value of shared data by firm without privacy factor
V2 – current value of data in CYBEX

Factors on input:

amount of firm’s investment (can be edited on each round and stored as average)
amount of data being shared
average quality of data being shared
privacy level for data being shared


Other calculated factors:

Risk – calculated based on firm’s investment, quality, and amount of data being shared.

Calculations:

In = ((Ia * Sf) + (I * s)) / (Sf + s)	// firms average investment as a weighted average

R = ((1 / In) * (s * (1 / q)))		// risk is inverse of avg. invesment divided by amount of data 						currently being shared multiplied by inverse of quantity currently 						being shared.

X = (x * s)				// current sharing overhead is sharing cost divided by current 						amount of data being shared.

Ra = ((Ra * Sf) + (R * S)) / (Sf + s)	// average risk as a weighted average

Q = ((Q * Sc) + (q * s)) / (Sc + s)	// quality of CYBEX data as a weighted average


V0 = (V1 – (V1 * p))			// current value (privacy) is current value – (privacy * current 						value without privacy)

V1 = (b * (log(1 + (s * q)))) – Ra	// smoothing factor * log(current data * current quality) – 							average risk for firm

V2 = (b * (log(1 + (Sc * Q)))) – Ra	// smoothing factor * log(CYBEX total data * avg. quality) – 						average risk for firm

if value of data is less than zero:
share = (a * log10(1 + In)) – x – c 	// no value in data, firm shares, (scaled)

if value of data is greater than zero:
share = (V2 – V1) * (a * log10(1 + In)) – x – c // data has value, firm shares, result is scaled.

noshare = a * log10(1 + In)		// smoothing factor times log of investment

Privacy (amount of protected data) is taken as a percentage, and the total value of the data being shared is reduced by that percentage; i.e. I protect 50% of my data, so its value is reduced by 50%.
