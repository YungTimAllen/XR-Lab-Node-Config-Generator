# xr-lab-gen 

Python frontend to a prewritten Jinja2 template. Creates a data-structure from Argparse'd values and feeds Jinja. 

Template is "INE-Like" whereby all core node interconnects are sub-interfaces named {lower}{higher} and addressed as 10.{lower}.{higher}.{self} (e.g. R2's link to R4: 10.2.4.2/24)
```
usage: xr-lab-gen.py [-h] [--uplink UPLINK] node_num node_nei_str

INE-Style XRv Config Generator for Large Labs

positional arguments:
  node_num         Numerical ID of this node.
  node_nei_str     Comma-delimited list of nodes this node attaches to.

optional arguments:
  -h, --help       show this help message and exit
  --uplink UPLINK  Physical uplink from which to create subinterfaces
```
## Example usage

```
$ ./xr-lab-gen.py 7 3,4,5

hostname R7
logging console debug
mpls oam
 exit
line con 0
 exec-timeout 0
 exit
int lo0
 ipv4 address 2.90.0.7/32
 ipv6 address 2001:db8::2.90.0.7/128
 exit

mpls ldp
 exit

interface g0/0/0/0
 no shut
 exit

interface Gi0/0/0/0.37
 description Link to R3
 encapsulation dot1q 37
 ipv4 address 10.3.7.7/24
 ipv6 address 2001:db8:3:7::7/64
 exit

interface Gi0/0/0/0.47
 description Link to R4
 encapsulation dot1q 47
 ipv4 address 10.4.7.7/24
 ipv6 address 2001:db8:4:7::7/64
 exit

interface Gi0/0/0/0.57
 description Link to R5
 encapsulation dot1q 57
 ipv4 address 10.5.7.7/24
 ipv6 address 2001:db8:5:7::7/64
 exit


router isis 1
 log-adjacency-changes
 net 49.1234.0020.9000.0007.00
 is-type level-2-only
 address-family ipv4 unicast
  mpls traffic-eng router-id Loopback0
  mpls traffic-eng level-2
  metric-style wide
  exit

 interface Gi0/0/0/0.37
  point-to-point
  suppressed
   address-family ipv4 unicast
    exit
   exit

 interface Gi0/0/0/0.47
  point-to-point
  suppressed
   address-family ipv4 unicast
    exit
   exit

 interface Gi0/0/0/0.57
  point-to-point
  suppressed
   address-family ipv4 unicast
    exit
   exit

 interface loopback0
  passive
   address-family ipv4 unicast
 root


mpls traffic-eng
 interface Gi0/0/0/0.37
  administrative 128

mpls traffic-eng
 interface Gi0/0/0/0.47
  administrative 128

mpls traffic-eng
 interface Gi0/0/0/0.57
  administrative 128

 root


rsvp
 interface Gi0/0/0/0.37
  bandwidth 1000000

rsvp
 interface Gi0/0/0/0.47
  bandwidth 1000000

rsvp
 interface Gi0/0/0/0.57
  bandwidth 1000000
```
