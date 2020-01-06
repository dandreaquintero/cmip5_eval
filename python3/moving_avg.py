import numpy as np


def moving_average(a, n=3):
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n


a = np.arange(20)
print(a)

b = moving_average(a, n=5)
print(b)

c = moving_average(a, n=4)

#print(c)



# def running_mean(x, N):
#     cumsum = numpy.cumsum(numpy.insert(x, 0, 0))
#     return (cumsum[N:] - cumsum[:-N]) / float(N)
#
# x = numpy.random.random(100000)
# N = 1000
# timeit result1 = numpy.convolve(x, numpy.ones((N,))/N, mode='valid')
# 10 loops, best of 3: 41.4 ms per loop
# In[6]: %timeit result2 = running_mean(x, N)
# 1000 loops, best of 3: 1.04 ms per loop

# mylist = [1, 2, 3, 4, 5, 6, 7]
# N = 3
# cumsum, moving_aves = [0], []
#
# for i, x in enumerate(mylist, 1):
# cumsum.append(cumsum[i-1] + x)
# if i>=N:
#     moving_ave = (cumsum[i] - cumsum[i-N])/N
#     #can do stuff with moving_ave here
#     moving_aves.append(moving_ave)
