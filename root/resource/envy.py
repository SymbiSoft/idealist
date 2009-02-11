__ALL__=['app_capabilities','SELFSIGNED','UNSIGNED','has_capabilities','has_cap']

from _envy import *
import _envy

SELFSIGNED=(ECapabilityReadUserData,ECapabilityWriteUserData,ECapabilityUserEnvironment,ECapabilityNetworkServices,ECapabilityLocalServices)
UNSIGNED=SELFSIGNED+(ECapabilityLocation,ECapabilitySurroundingsDD,ECapabilitySwEvent,ECapabilityTrustedUI,ECapabilityReadDeviceData,ECapabilityWriteDeviceData,ECapabilityPowerMgmt,ECapabilityProtServ) 
ALL=UNSIGNED+(ECapabilityNetworkControl,ECapabilityCommDD,ECapabilityMultimediaDD,ECapabilityDiskAdmin,ECapabilityDRM,ECapabilityTCB,ECapabilityAllFiles)
'''
examples:
has_capabilities('unsigned')
has_capabilities('selfsigned')
has_capabilities(UNSIGNED)
has_capabilities(SELFSIGNED)
has_capabilities((ECapabilityLocation,ECapabilitySurroundingsDD))
has_capabilities('Location+SurroundingsDD')
has_capabilities(ECapabilityLocation)
has_capabilities('Location')

 ret : 1 (True)
       0 (False)
'''   
def has_capabilities(caps):
  if caps=='unsigned':
    caps=UNSIGNED
  elif caps=='selfsigned':
    caps=SELFSIGNED
  if type(caps)==type(2):
    caps=(caps,)
  elif type(caps)==type('') and caps.startswith('ALL'):
    list_exc_caps=[eval('_envy.ECapability'+c) for c in caps.split('-')[1:]]
    #return list_exc_caps
    caps=[c for c in ALL if c not in list_exc_caps]
  if type(caps)==type(''):
    list_caps_values=[eval('_envy.ECapability'+c) for c in caps.split('+')]
    return reduce(lambda x,y : x and y , map(has_cap,list_caps_values))
  elif type(caps)==type(()) or type(caps)==type([]):
    return reduce(lambda x,y : x and y , map(has_cap,caps))
   
'''
ret : example :
 'Location+SurroundingsDD'
'''  
def app_capabilities():
    list_caps=[w[11:] for w in dir(_envy) if w.startswith('ECapability') and has_capabilities(w[11:])]
    return reduce(lambda x,y : x+'+'+y,list_caps)     


