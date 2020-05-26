# XR-Lab-Node-Config-Generator

This is some of the absolute worst code I have ever written. I'm ashamed to share it but its way more valuable to me in a place that I cant lose it - the internet.

**This Python script prompts for a router node number (n_id) and a comma-delimited string of other n_ids that this node attaches too**

Then, INE-style config is generated. This script assumes that a single physical link is connected to a central dot1q switch, and that all rotuer connections are dot1q subinterfaces. There is a specific focus on spinning up an MPLS TE ready XR lab very quickly.

## Example usage

```python
XRv Router #:	16
Connects to the following (Comma delimited):	12,13,15
 
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
- - - - - - - - - -  ROUTER XR16	  - - - - - - - - - - - - - - - - - - - - - - -
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


hostname XR16
logging console debug
mpls oam
 exit
line con 0
 exec-timeout 0
 exit
int lo0
 ipv4 address 1.1.1.16/32
 ipv6 address 2001:db8::16/128
 exit
mpls ldp
 exit

interface g0/0/0/0
 no shut
 exit

interface g0/0/0/0.1216
 description Link to 12
 encapsulation dot1q 1216
 ipv4 address 10.12.16.16/24
 ipv6 address 2001:db8:12:16::16/64
 exit

interface g0/0/0/0.1316
 description Link to 13
 encapsulation dot1q 1316
 ipv4 address 10.13.16.16/24
 ipv6 address 2001:db8:13:16::16/64
 exit

interface g0/0/0/0.1516
 description Link to 15
 encapsulation dot1q 1516
 ipv4 address 10.15.16.16/24
 ipv6 address 2001:db8:15:16::16/64
 exit

router isis 1
 net 49.1234.0010.0100.1016.00
 is-type level-2-only
 address-family ipv4 unicast
  metric-style wide
  exit
 interface g0/0/0/0.1216
  point-to-point
  address-family ipv4 unicast
   exit
  exit
 interface g0/0/0/0.1316
  point-to-point
  address-family ipv4 unicast
   exit
  exit
 interface g0/0/0/0.1516
  point-to-point
  address-family ipv4 unicast
   exit
  exit
 interface loopback0
  passive
  address-family ipv4 unicast
   root

mpls traffic-eng
 interface g0/0/0/0.1216
 interface g0/0/0/0.1316
 interface g0/0/0/0.1516
 root
rsvp
 interface g0/0/0/0.1216
  bandwidth 1000000
 interface g0/0/0/0.1316
  bandwidth 1000000
 interface g0/0/0/0.1516
  bandwidth 1000000
 root
router isis 1
 address-family ipv4 unicast
  mpls traffic-eng router-id lo0
  mpls traffic-eng level-2```
