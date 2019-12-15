import matplotlib.pyplot as plt
import numpy as np

num_plots = 20

# Have a look at the colormaps here and decide which one you'd like:
# http://matplotlib.org/1.2.1/examples/pylab_examples/show_colormaps.html
colormap = plt.cm.gist_ncar
plt.gca().set_color_cycle([colormap(i) for i in np.linspace(0, 0.9, num_plots)])

# Plot several different functions...
x = np.arange(10)
labels = []
for i in range(1, num_plots + 1):
    plt.plot(x, i * x + 5 * i)
    labels.append(r'$y = %ix + %i$' % (i, 5*i))

# I'm basically just demonstrating several different legend options here...
plt.legend(labels, ncol=4, loc='upper center',
           bbox_to_anchor=[0.5, 1.1],
           columnspacing=1.0, labelspacing=0.0,
           handletextpad=0.0, handlelength=1.5,
           fancybox=True, shadow=True)

plt.show()
