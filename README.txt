To launch this shallot network on a single computer, and to allow relays not to be 
all neigbor of each others:
1) Copy the program folder as many times as the number of wanted relays, and at least 2 times to
   have 2 Peers.

2) In the first and the second copy, go in Peer_program.py and implement manually the Peers,
   the relays and the topology, for example as follows:
	Alice = Relay_object("192.168.0.10",9000)
	Bob = Relay_object("192.168.0.25",9000)
	r1 = Relay_object("192.168.0.25",9001)
	Alice.connect(r1,5)
	r1.connect(Bob,5)
	TOPOLOGY = {}
	TOPOLOGY["192.168.0.10"] = [Alice]
	TOPOLOGY["192.168.0.25"] = [r1,Bob]

3) In the first folder, go in peer/config/host and put the same IP and port as specified manually
   for Alice.

4) In the second folder, go in peer/config/host and put the same IP and port as specified manually
   for Bob.

5) In each folder, go in Relay/config/host and put the same IP and port as specified manually
   for the corresponding Relay.

6) Launch Peer_program in the 2 first folders to initialize 2 windows of Shallot Messenger, and
   from one to the other by specifying the destination IP:port of the other Peer. 