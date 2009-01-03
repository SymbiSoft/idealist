#
#=============================================================================================
#    file        : pys60crypto.py
#    author      : LEFEVRE Damien
#    version     : 0.1
#    description : python loader for 3rd Edition phones
#    copyright   :
#=============================================================================================
#

import e32

if e32.s60_version_info>=(3,0):
    import imp
    _akntextutils = imp.load_dynamic('_akntextutils', 'c:\\sys\\bin\\_akntextutils.pyd')

else:
    import _akntextutils

del e32, imp #remove unnecessary names from namespace
from _akntextutils import *
del _akntextutils