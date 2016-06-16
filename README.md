# dhtsession

This prototype attempts to store TCP sessions in a DHT. Atm its nice and slow and not fully working :)


## Installation:
Of course:

```
git clone https://github.com/pboers1988/dhtsession
```

```
pip install pynetfilter_conntrack
pip install ipy

```

Then you need to clone a dht implementation and install it. (Installing it with pip is broke)
```
git clone https://github.com/isaaczafuta/pydht
cd pydht
python setup.py install
```

and 

```
apt install libnetfilter-conntrack3
```

##Requirements:
Make sure you are tracking connections. The easiest way to do this is, by adding following rule in IPTABLES

```
iptables -I INPUT -m state --state NEW,RELATED,ESTABLISHED,INVALID,UNTRACKED -j ACCEPT
```

Furthermore as this is all in userspace and in python :) you need to add a bit of a delay on the link to make it
work as expected. We do this with the tc tool 

```
tc qdisc add dev eth1 root netem delay 10ms
```

## Usage

A number of options exist

```
-a The bootstrap address for the DHT server
-p The port of the DHT server (defaults to 7000)
-s The TCP port you want to filter on and store in the DHT (defaults to 8080)
-i The ip Identifier of the node.
-c The anycast ip that is configured
```

Example:

```
python main.py  -a 10.100.10.1 -i 10.100.10.4 -c 192.168.0.1
```