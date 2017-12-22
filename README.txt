To launch this shallot network on a single computer, and to allow relays not to be 
all neigbor of each others:
1) Copy the program folder as many times as the number of wanted relays, and at least 2 times to
   have 2 Peers.

2) In the first and the second copy, go in Peer_program.py and implement manually the Peers,
   the relays and the topology, for example as follows:
	Alice = Relay_object("your_ip",9000)
	Bob = Relay_object("your_ip",9001)
	r = Relay_object("your_ip",9999)
	Alice.connect(r,5)
	r.connect(Bob,5)
	TOPOLOGY = {}
	TOPOLOGY["your_ip"] = [Alice,r,Bob]

3) In the first folder, go in peer/config/host.ini and put the same IP and port as specified manually
   for Alice.

4) In the second folder, go in peer/config/host.ini and put the same IP and port as specified manually
   for Bob.

5) In each relay's folder, go in Relay/config/host.ini and put the same IP and port as specified manually
   for the corresponding Relay.

6) Launch the Peer_relay in the relay's folders as well as the Peer_program in the 2 peer's folders to initialize 2 windows of Shallot Messenger, and from one to the other by specifying the destination IP:port of the other Peer. 
