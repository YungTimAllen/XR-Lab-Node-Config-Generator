# xr-lab-gen 

Python frontend to a prewritten Jinja2 template. Creates a data-structure from Argparse'd values and feeds Jinja. 

Template is "INE-Like" whereby all core node interconnects are sub-interfaces connecting to a switch, tagged as {lower}{higher} and addressed as 10.{lower}.{higher}.{self} (e.g. R2's link to R4: 10.2.4.2/24)

![Image of Example Topology](https://i.imgur.com/dzIfi3Q.png)

The motivation and purpose of this template is to create a working underlay for SP topologies extremely quickly. This template also enables RSVP-TE fundamentals.
```
usage: xr-lab-gen.py [-h] [--uplink UPLINK] [--template TEMPLATE]
                     node_num node_nei_str

INE-Style XRv Config Generator for Large Labs

positional arguments:
  node_num             Numerical ID of this node.
  node_nei_str         Comma-delimited list of nodes this node attaches to.

optional arguments:
  -h, --help           show this help message and exit
  --uplink UPLINK      Physical uplink from which to create subinterfaces
  --template TEMPLATE  J2 template to use (From pwd)
```
## Example usage

```
$ ./xr-lab-gen.py 2 1,3,4
hostname R2
logging console debug
mpls oam
 exit
line con 0
 exec-timeout 0
 exit
int lo0
 ipv4 address 2.90.0.2/32
 ipv6 address 2001:db8::2.90.0.2/128
 exit

mpls ldp
 exit

interface g0/0/0/0
 no shut
 exit

interface Gi0/0/0/0.12
 description Link to R1
 encapsulation dot1q 12
 ipv4 address 10.1.2.2/24
 ipv6 address 2001:db8:1:2::2/64
 exit

interface Gi0/0/0/0.23
 description Link to R3
 encapsulation dot1q 23
 ipv4 address 10.2.3.2/24
 ipv6 address 2001:db8:2:3::2/64
 exit

interface Gi0/0/0/0.24
 description Link to R4
 encapsulation dot1q 24
 ipv4 address 10.2.4.2/24
 ipv6 address 2001:db8:2:4::2/64
 exit


router isis 1
 log-adjacency-changes
 net 49.1234.0020.9000.0002.00
 is-type level-2-only
 address-family ipv4 unicast
  mpls traffic-eng router-id Loopback0
  mpls traffic-eng level-2
  metric-style wide
  exit

 interface Gi0/0/0/0.12
  point-to-point
  suppressed
   address-family ipv4 unicast
    exit
   exit

 interface Gi0/0/0/0.23
  point-to-point
  suppressed
   address-family ipv4 unicast
    exit
   exit

 interface Gi0/0/0/0.24
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

 interface Gi0/0/0/0.12
  admin-weight 128

 interface Gi0/0/0/0.23
  admin-weight 128

 interface Gi0/0/0/0.24
  admin-weight 128

 root


rsvp

 interface Gi0/0/0/0.12
  bandwidth 1000000

 interface Gi0/0/0/0.23
  bandwidth 1000000

 interface Gi0/0/0/0.24
  bandwidth 1000000
```
