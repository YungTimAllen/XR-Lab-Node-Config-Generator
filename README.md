# xr-lab-gen 

Python frontend to a prewritten Jinja2 template. Creates a data-structure from Argparse'd values and feeds Jinja. 

Template is "INE-Like" whereby all core node interconnects are sub-interfaces connecting to a switch, tagged as {lower}{higher} and addressed as 10.{lower}.{higher}.{self} (e.g. R2's link to R4: 10.2.4.2/24)

![Image of Example Topology](https://i.imgur.com/dzIfi3Q.png)

The motivation and purpose of this template is to create a working underlay for SP topologies extremely quickly. This template also enables RSVP-TE fundamentals.
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
$ ./xr-lab-gen.py 7 3,2,14

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

interface Gi0/0/0/0.27
 description Link to R2
 encapsulation dot1q 27
 ipv4 address 10.2.7.7/24
 ipv6 address 2001:db8:2:7::7/64
 exit

interface Gi0/0/0/0.714
 description Link to R14
 encapsulation dot1q 714
 ipv4 address 10.7.14.7/24
 ipv6 address 2001:db8:7:14::7/64
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

 interface Gi0/0/0/0.27
  point-to-point
  suppressed
   address-family ipv4 unicast
    exit
   exit

 interface Gi0/0/0/0.714
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
 interface Gi0/0/0/0.27
  administrative 128

mpls traffic-eng
 interface Gi0/0/0/0.714
  administrative 128

 root


rsvp
 interface Gi0/0/0/0.37
  bandwidth 1000000

rsvp
 interface Gi0/0/0/0.27
  bandwidth 1000000

rsvp
 interface Gi0/0/0/0.714
  bandwidth 1000000
```
