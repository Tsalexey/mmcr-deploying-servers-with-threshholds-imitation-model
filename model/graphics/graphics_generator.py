__author__ = 'tsarev alexey'

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
from scipy.interpolate import spline
from scipy.ndimage import zoom
from scipy.interpolate import interp1d
from scipy import interpolate
#--------------------------------------------------------------------------------------------------------------------#
#													   GRAPHICS GENERATOR   										 #
#--------------------------------------------------------------------------------------------------------------------#

class Graphics_generator:

    def plot(x, x_name, y_dict, filename):
        with PdfPages(filename) as pdf:
            for key, values in y_dict.items():
                fig = plt.figure()

                ax = fig.add_subplot(111)

                x_sm = np.array(x).astype(np.float)
                y_sm = np.array(values).astype(np.float)

                # #1
                # interpolate_func = interp1d(x_sm, y_sm, kind='cubic')
                # xnew = np.arange(min(x_sm), max(x_sm), 0.0001)
                # ynew = interpolate_func(xnew)

                x_smooth = np.linspace(x_sm.min(), x_sm.max(), 1000)
                y_smooth = spline(x, y_sm, x_smooth)

                # pw = 10  # power of the smooth
                # x_smooth1 = zoom(x_sm, pw)
                # y_smooth1 = zoom(y_sm, pw)
                # tck = interpolate.splrep(x, values, s=0)
                # xnew = np.arange(0, 2 * np.pi, np.pi / 50)
                # ynew = interpolate.splev(xnew, tck, der=0)

                ax.plot(x_smooth, y_smooth)
                # plt.legend(['point', 'spline', 'zoom', 'splev'])
                ax.set_xlabel(x_name)
                ax.set_ylabel(key, rotation=0)

                x0, x1 = ax.get_xlim()
                y0, y1 = ax.get_ylim()
                ax.set_aspect(abs(x1 - x0) / abs(y1 - y0))
                ax.grid(b=True, which='major', axis='both', color='grey', linestyle=':')


                pdf.savefig()
                plt.close()
