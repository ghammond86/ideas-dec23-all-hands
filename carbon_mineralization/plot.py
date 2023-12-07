import sys
import os
import re
import shutil
try:
  pflotran_dir = os.environ['PFLOTRAN_DIR']
except KeyError:
  try:
    pflotran_dir = '../../'
  except KeyError:
    print('PFLOTRAN_DIR must point to PFLOTRAN installation directory and be defined in system environment variables.')
    sys.exit(1)
sys.path.append(pflotran_dir + '/src/python')
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import math
import pflotran as pft

def fix_small_numbers(filename):
    swap = re.compile(r'(?P<pre>\s+[0-9]+\.[0-9]*)(?P<post>-[0-9]{3})')
    f2 = open(filename+'.tmp','w')
    for line in open(filename,'r'):
        f2.write(swap.sub('\g<pre>E\g<post>',line))
    f2.close()
    shutil.copy(filename+'.tmp',filename)
    os.remove(filename+'.tmp')

def plot_aqueous(plt,filename,scale_string):
    plt.xlabel('Time [d]')
    plt.ylabel('Aqueous Concentration [M]')

    plt.yscale(scale_string)

    maxval = -1.e20
    if scale_string == 'linear':
        minval = 1.e-10
    else:
        minval = 1.e20
    columns = [2,3,4,5,6,7]
    for icol in range(len(columns)):
        data = pft.Dataset(filename,1,columns[icol])
        ydata = data.get_array('y')
        maxval = max(maxval,np.amax(ydata))
        if scale_string == 'log':
            minval = min(minval,np.amin(ydata))
        plt.plot(data.get_array('x'),data.get_array('y'),
                 label=aq_labels[icol],c=aq_colors[icol])
    if scale_string == 'linear':
        plt.ylim(-.05*maxval,1.05*maxval)
        legend_loc = 'upper right'
    else:
        plt.ylim(0.5*minval,2.*maxval)
        legend_loc = 'lower right'

#'best'         : 0, (only implemented for axis legends)
#'upper right'  : 1,
#'upper left'   : 2,
#'lower left'   : 3,
#'lower right'  : 4,
#'right'        : 5,
#'center left'  : 6,
#'center right' : 7,
#'lower center' : 8,
#'upper center' : 9,
#'center'       : 10,
# xx-small, x-small, small, medium, large, x-large, xx-large, 12, 14
    plt.legend(title='Aqueous',loc=legend_loc,fontsize=legend_fontsize)
    legend = plt.gca().get_legend()
    legend.get_frame().set_fill(False)
    legend.draw_frame(False)

scale_string = 'linear'
if len(sys.argv) > 1:
    scale_string = sys.argv[1]
    if not (scale_string == 'linear' or scale_string == 'log'):
        print('\nERROR: The second argument to {} '.format(sys.argv[0]) +
              'must be either "linear" or "log".\n')
        sys.exit(0)

observation_filename = 'carbon_mineralization-obs-0.pft'
fix_small_numbers(observation_filename)

legend_fontsize = 'small'
aq_labels = []
aq_labels.append('O2(aq)')
aq_labels.append('NO3-')
aq_labels.append('NO2-')
aq_labels.append('N2(aq)')
aq_labels.append('CH2O(aq)')
aq_labels.append('CO2(aq)')

aq_colors = []
aq_colors.append('blue')
aq_colors.append('green')
aq_colors.append('red')
aq_colors.append('cyan')
aq_colors.append('magenta')
aq_colors.append('orange')
aq_colors.append('y')

f = plt.figure(figsize=(10,6))

plt.title('Carbon Mineralization Time History')
plot_aqueous(plt,observation_filename,scale_string)

f.subplots_adjust(hspace=0.2,wspace=0.10,
                  bottom=.12,top=.92,
                  left=.1,right=.85)

plt.show()
