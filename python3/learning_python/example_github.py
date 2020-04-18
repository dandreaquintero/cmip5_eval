import matplotlib.pyplot as plt
import numpy as np

times = np.array([ 93.,  96.,  99., 102., 105., 108., 111., 114., 117.,
                  120., 123., 126., 129., 132., 135., 138., 141., 144.,
                  147., 150., 153., 156., 159., 162.])
temps = np.array([310.7, 308.0, 296.4, 289.5, 288.5, 287.1, 301.1, 308.3,
                  311.5, 305.1, 295.6, 292.4, 290.4, 289.1, 299.4, 307.9,
                  316.6, 293.9, 291.2, 289.8, 287.1, 285.8, 303.3, 310.])

# Create a figure
fig=plt.figure(figsize=(10, 6))

# Ask, out of a 1x1 grid, the first axes.
ax = fig.add_subplot(3, 2, 6)

# Plot times as x-variable and temperatures as y-variable

ax.set_title('GFS Temperature Forecast', fontdict={'size':16})

# Add some labels to the plot
ax.set_xlabel('Time')
ax.set_ylabel('Temperature')
ax.set_title('GFS Temperature Forecast', fontdict={'size':16})


times = np.array([ 93.,  96.,  99., 102., 105., 108., 111., 114., 117.,
                  120., 123., 126., 129., 132., 135., 138., 141., 144.,
                  147., 150., 153., 156., 159., 162.])
temps = np.array([310.7, 308.0, 296.4, 289.5, 288.5, 287.1, 301.1, 308.3,
                  311.5, 305.1, 0.6, 292.4, 290.4, 289.1, 299.4, 307.9,
                  316.6, 293.9, 291.2, 289.8, 287.1, 285.8, 303.3, 310.])
temps_1000 = np.array([316.0, 316.3, 308.9, 304.0, 302.0, 300.8, 306.2, 309.8,
                       313.5, 313.3, 308.3, 304.9, 301.0, 299.2, 302.6, 309.0,
                       311.8, 304.7, 304.6, 301.8, 300.6, 299.9, 306.3, 311.3])

ax = fig.add_subplot(1, 1, 1)

# Plot two series of data
# Specify how our lines should look
ax.plot(times, temps, color='tab:red', label='Temperature (surface)')
ax.plot(times, temps_1000, color='tab:red', linestyle='--',
        label='Temperature (isobaric level)')


# Add labels and title
ax.set_xlabel('Time')
ax.set_ylabel('Temperature')
ax.set_title('Temperature Forecast')


# Add gridlines
ax.grid(True)

# Add a legend to the upper left corner of the plot
ax.legend(loc='upper left')

plt.show()
