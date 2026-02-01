# What is Scapy?

- Think of scapy as a network packet manipulation tool. Scapy is not a network scanner, not a network sniffer, not an exploitation tool. Scapy lets us create a packet from scratch, modify any filed at any layer it also lets us send, recieve, sniff, replay packet. In simple words scapy lets us impersonate the network itself.

## How Scapy Works

Scapy works by representing packets as python objects. Instead of saying: “Send a TCP SYN packet to port 80” we say: “Create an IP packet ➡️ add a TCP layer ➡️ set flags ➡️ send it”. We can stack layers like Lego blocks:

- Ethernet
- IP
- TCP / UDP / ICMP
- Raw payloads

And we can inspect or alter any field: flags, sequence numbers, TTL, checksums, payload bytes.
