import sys
from numpy import genfromtxt
from matplotlib.pyplot import plot, figure, savefig, legend, xticks

nucleotide_distribution=genfromtxt(sys.argv[1])

a=nucleotide_distribution[0,:]
c=nucleotide_distribution[1,:]
g=nucleotide_distribution[2,:]
t=nucleotide_distribution[3,:]
figure(figsize=(16,8),dpi=80)
plot(a,color='green',label='%A')
plot(c,color='blue',label='%C')
plot(g,color='black',label='%G')
plot(t,color='red',label='%T')
legend()
tick_locs=range(0,100,2)
tick_labels=range(0,100,2)
xticks(tick_locs,tick_labels)
savefig(sys.stdout,format='png')
