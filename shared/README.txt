Python files from the Peer or Relay directory can import the modules of this "shared" directory by doing:

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from shared.Path_finding_V3 import Dijkstra