# dhtsession

This prototype attempts to store TCP sessions in a DHT. Atm its nice and slow and not fully working :)


## Installation:
```
pip install kademlia
pip install pynetfilter_conntrack
pip install twisted
pip install ipy
```

and 

```
apt install libnetfilter-conntrack3
```

##Requirements:
Make sure you are tracking connections. Easiest way to do this is by adding following rule in IPTABLES

```
iptables -I INPUT -m state --state NEW,RELATED,ESTABLISHED,INVALID,UNTRACKED -j ACCEPT
```

Furthermore as this is all in userspace and in python :) you need to add a bit of a delay on the link to make it
work as expected. We do this with the tc tool 

```
tc qdisc add dev eth1 root netem delay 10ms
```