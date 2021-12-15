# Live testing for important car specs during runtime

import matplotlib.pyplot as plt
import numpy as np

plt.style.use('ggplot')

def live_plotter(x_vec, y1_data, line1, identifier='', pause_time = 0.1):
    if line1 =  []:
        
        # call to matplotlib that allows dynamic plotting
        plt.ion()
        fig = plt.figure(figsize=(13, 6))
        ax = fig.add_subplot(111)
        # create a variable for the line to update later
        line1 = ax.plot(x_vec, y1_data, '-o', alpha=0.8)

        # update plot label/title (just testing with intake manifold pressure for now)
        plt.ylabel('kPa')
        plt.title('INTAKE MANIFOLD PRESSURE'.format(identifier))
        plt.show()

        # update y data
        line1.set_ydata(y1_data)
        # adjust limits if data goes beyond bounds
        if np.min(y1_data) <= line1.axes.get_ylim()[0] or np.max >= line1.axes.get_ylim()[1]:
            plt.ylim([np.min(y1_data) - np.std(y1_data), np.max(y1_data) + np.std(y1_data)])

        plt.pause(pause_time)

        return line1
