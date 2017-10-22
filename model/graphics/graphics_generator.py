__author__ = 'tsarev alexey'

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
from scipy.interpolate import spline
#--------------------------------------------------------------------------------------------------------------------#
#													   GRAPHICS GENERATOR   										 #
#--------------------------------------------------------------------------------------------------------------------#
class Graphics_generator:

    def plot(x, x_name, y_dict, filename):
        with PdfPages(filename) as pdf:
            for key, values in y_dict.items():
                fig = plt.figure()

                ax = fig.add_subplot(111)

                x_sm = np.array(x)
                y_sm = np.array(values)

                x_smooth = np.linspace(x_sm.min(), x_sm.max(), 100)
                y_smooth = spline(x, values, x_smooth)

                ax.plot(x_smooth, y_smooth, color='red')

                ax.set_xlabel(x_name)
                ax.set_ylabel(key, rotation=0)

                x0, x1 = ax.get_xlim()
                y0, y1 = ax.get_ylim()
                ax.set_aspect(abs(x1 - x0) / abs(y1 - y0))
                ax.grid(b=True, which='major', axis='both', color='grey', linestyle=':')


                pdf.savefig()
                plt.close()
