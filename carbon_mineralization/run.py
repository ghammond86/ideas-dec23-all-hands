import sys
import os
import re
import shutil
from plot import plot_results
try:
  pflotran_dir = os.environ['PFLOTRAN_DIR']
except KeyError:
  try:
    pflotran_dir = '../../'
  except KeyError:
    print('PFLOTRAN_DIR must point to PFLOTRAN installation directory and be defined in system environment variables.')
    sys.exit(1)
sys.path.append(pflotran_dir + '/src/python')

if len(sys.argv) == 1:
    print('\nERROR: Please include the PFLOTRAN input prefix.')
    sys.exit(0)

plotfig = False
if len(sys.argv) > 2:
    plotfig = (sys.argv[2] == 'plotfig')

prefix = sys.argv[1]
os.system(f'$PFLOTRAN_DIR/src/pflotran/pflotran -input_prefix {prefix} '+
          f'2>&1 > {prefix}.stdout')
os.system(f'tail -30 {prefix}.stdout')
yscale = 'linear'
savefig = (not plotfig)
plot_results(prefix+'-obs-0.pft',yscale,savefig)
yscale = 'log'
plot_results(prefix+'-obs-0.pft',yscale,savefig)

