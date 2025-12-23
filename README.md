# goal

set up a VPN connection betweeen my local machine and GCP

steps
strongswan
ipsec version
sudo vi /usr/local/etc/ipsec.conf
sudo vi /usr/local/etc/ipsec.secrets.conf
add your subnet and your VPN IP address to GCP

- remote peer IP = your VM public IP
- remote IP network range = subnet

sudo sysctl -w net.inet.ip.forwarding=1
sudo ipsec start
sudo ipsec up gcp-site-to-site

this sets up the VPN but not the TUNNEL
in order to use the tunnel, the destination IP and source IP must be the internal subnets
right now, my route for my destination LAN's internal IP is through the gateway, not through the tunnel
(base) ~/Desktop/PROJECTS/VPN> route -n get <GCP VM INTERNAL IP>
route to: <GCP VM INTERNAL IP>
destination: default
mask: default
gateway: 192.168.1.1
interface: en0
flags: <UP,GATEWAY,DONE,STATIC,PRCLONING,GLOBAL>
recvpipe sendpipe ssthresh rtt,msec rttvar hopcount mtu expire
0 0 0 0 0 0 1500 0
(base) ~/Desktop/PROJECTS/VPN>

the problem is that my computer cannot create SOURCE IP that corresponds to the selector because my computers interface does not own the internal IP of the mac (my ISP does)

- the selector is what the kernel uses to determine if a packet should be encrypted and sent through the tunnel.

in order to create the source IP to match your VPN config
prerequistie) the fake subnet you create in your ipsec.config, assign that to a local interface
sudo ifconfig lo0 alias 10.100.0.10/32

1. add a route from the internal IP to that device
   sudo route add -net 10.142.0.0/20 -interface lo0
   or BIND it in your appliation
   SRC="10.100.0.10"
   PORT=12345
   s=socket.socket()
   s.bind((SRC, 0))

now when a packet gets created, its source IP will be 10.100.0.10.

- the source IP is chosen at socket creation time. its based on either the bind address or the interface for routing
  and if its destination IP is the internal IP on the other side, the packet gets sent through the tunnel
