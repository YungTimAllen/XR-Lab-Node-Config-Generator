#!/usr/bin/env python3
# Personal scripts for generating INE-Style XR config for labs

import sys

class Router:
  n_id = ""
  peers = []
  uplink = "g0/0/0/0"

  def __init__(self, n_id, peers, uplink):
    self.n_id   = n_id
    self.peers  = peers
    self.uplink = uplink

  def printHeader(self):
    print(""" 
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
- - - - - - - - - -  ROUTER XR$this\t  - - - - - - - - - - - - - - - - - - - - - - -
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
""".replace("$this", self.n_id))

  def genConfig(self):
    #debug
    print(self.getGeneralConfig(self.n_id))
    print(self.getPhysInterfaceConfig(self.uplink))
    
    for t in self.peers:
      print(self.getSubInterfaceConfig(self.uplink, self.n_id, t))

    print(self.getIGPConfig(self.uplink, self.n_id, self.peers))

    print(self.getRSVPTEConfig(self.uplink, self.n_id, self.peers))

  def getGeneralConfig(self, n_id):
    XRvConfigTemplateGeneral = """
hostname XR$this
logging console debug
mpls oam
 exit
line con 0
 exec-timeout 0
 exit
int lo0
 ipv4 address 1.1.1.$this/32
 ipv6 address 2001:db8::$this/128
 exit
mpls ldp
 exit"""
    return XRvConfigTemplateGeneral.replace("$this", n_id)

  def getPhysInterfaceConfig(self, uplink):
    XRvConfigTemplatePhysInterface = """
interface $phys
 no shut
 exit"""
    return XRvConfigTemplatePhysInterface.replace("$phys", uplink)

  def getSubInterfaceConfig(self, phys_if, src_nid, dst_nid):
    # $phys $owner $target -> ($lower $higher)
    lower = int(src_nid) if int(src_nid) < int(dst_nid) else int(dst_nid)
    higher = int(src_nid) if int(src_nid) > int(dst_nid) else int(dst_nid) # lmao

    XRvConfigTemplateSubInterfaces = """
interface $phys.$lower$higher
 description Link to $target
 encapsulation dot1q $lower$higher
 ipv4 address 10.$lower.$higher.$owner/24
 ipv6 address 2001:db8:$lower:$higher::$owner/64
 exit"""

    return XRvConfigTemplateSubInterfaces.replace("$phys", phys_if).replace("$owner", src_nid).replace("$target", dst_nid).replace("$lower",str(lower)).replace("$higher",str(higher))

  def getIGPConfig(self, uplink, n_id, peers):
    XRvConfigTemplateIGPISIS = """
router isis 1
 net 49.1234.0010.0100.100$this.00
 is-type level-2-only
 address-family ipv4 unicast
  metric-style wide
  exit
"""
    for n in peers:
      lower = int(n_id) if int(n_id) < int(n) else int(n)
      higher = int(n_id) if int(n_id) > int(n) else int(n)
      XRvConfigTemplateIGPISIS += " interface " + uplink + "." + str(lower) + str(higher) + "\n"
      XRvConfigTemplateIGPISIS += "  point-to-point" + "\n"
      XRvConfigTemplateIGPISIS += "  address-family ipv4 unicast" + "\n"
      XRvConfigTemplateIGPISIS += "   exit" + "\n"
      XRvConfigTemplateIGPISIS += "  exit" + "\n"

    XRvConfigTemplateIGPISIS += """ interface loopback0
  passive
  address-family ipv4 unicast
   root"""

    return XRvConfigTemplateIGPISIS.replace("0$this", n_id) if ("0$this" in XRvConfigTemplateIGPISIS and len(str(n_id)) is 2) else XRvConfigTemplateIGPISIS.replace("$this", n_id)

  def getRSVPTEConfig(self, uplink, n_id, peers):

    rtn = """
mpls traffic-eng
"""
    for n in peers:
      lower = int(n_id) if int(n_id) < int(n) else int(n)
      higher = int(n_id) if int(n_id) > int(n) else int(n)
      rtn += " interface " + uplink + "." + str(lower) + str(higher) + "\n"

    rtn +=""" root
rsvp
"""
    for n in peers:
      lower = int(n_id) if int(n_id) < int(n) else int(n)
      higher = int(n_id) if int(n_id) > int(n) else int(n)
      rtn += " interface " + uplink + "." + str(lower) + str(higher) + "\n"
      rtn += "  bandwidth 1000000\n"

    rtn +=""" root
router isis 1
 address-family ipv4 unicast
  mpls traffic-eng router-id lo0
  mpls traffic-eng level-2
"""

    return rtn

def main():
  
  while(True):
    name = input("XRv Router #:\t")
    peers = input("Connects to the following (Comma delimited):\t")
    
    tmp = Router(name, peers.replace(' ', '').split(','), "g0/0/0/0")
    tmp.printHeader()
    tmp.genConfig()

if __name__ == "__main__":
  main()
