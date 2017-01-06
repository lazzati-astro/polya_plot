import numpy as np
import os, sys
import matplotlib.pyplot as plt

# it turns out to be convientent to define a 'direction pool' where
# we can randomly select from.
moves = np.array([1,-1], dtype=np.int32)

# generates a 'spectrum' of walk lengths on a square lattice
# of side length g_len. The total number of sampled walks is 
# given n_tries. individual walks that exceed
# max_steps stop walking, and are considered to have escaped.
def walk_spectrum(n_dim, g_len, n_tries, max_steps):

    # the returned spectrum
    n_steps = np.zeros(n_tries, dtype=np.int32)

    # record the origin. for simplicity we take ox = ({0})
    ox = np.zeros(n_dim, dtype=np.int32)

    # the step. note that, on a lattice, dx will
    # always be [anti]parallel to on of the n_dim basis
    # vectors
    dx = np.zeros(n_dim, dtype=np.int32)
    
    for t in xrange(n_tries):
        # reset current walk location
        x = ox.copy()
        for s in xrange(max_steps):
            # init the random step
            dx[:] = 0.
            # select a random dimension, and move in a 
            # random direction
            dx[np.random.choice(n_dim)] = np.random.choice(moves) 

            # below are two different boundary conditions,
            # reflective or periodic. comment (or change) to
            # what's needed.
#            nx = x + dx
#            if any(nx > g_len - 1) or any(nx < 0):
#                dx = -dx
#            x += dx
            x = np.mod((x + dx), g_len)

            # if we have returned to the origin, exit this sample
            if all(x == ox) and s != 0:
                break

        # record number of steps sample took
        if s == max_steps - 1 and all(x != ox):
            n_steps[t] = max_steps
        else:
            n_steps[t] = s

    return n_steps


graphLen = 6
numTries = 100

# number of lattice dimensions to plot.
# if this is taking a while, try to set
# runDim = 2 first
runDim = 3

# parameters for increasing the 'escape' values
minWalk = 10
dWalk = 20
nWalk = 20

ws = np.zeros(nWalk)
ps = np.zeros((runDim,nWalk))

for nd in range(runDim):
    for i in range(nWalk):
        # increase escape point and resample
        maxWalk = minWalk + dWalk * i
        nsteps = walk_spectrum(nd + 1, graphLen, numTries, maxWalk)

        ps[nd][i] = np.mean(nsteps)
        ws[i] = maxWalk


#plotting

fig = plt.figure()
ax = fig.add_subplot(111)

for nd in range(runDim):
    ax.plot(ws, ps[nd], label='dim = {0}'.format(nd+1))
ax.set_xlabel('escape value')
ax.set_ylabel('avg. steps until return')
ax.set_title('Demonstration of Polya\'s Recurrence Theorem')
ax.legend(loc=2)
plt.show()
 
