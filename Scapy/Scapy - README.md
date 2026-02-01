# What is Scapy?

- Think of scapy as a network packet manipulation tool. Scapy is not a network scanner, not a network sniffer, not an exploitation tool. Scapy lets us create a packet from scratch, modify any filed at any layer it also lets us send, recieve, sniff, replay packet. In simple words scapy lets us impersonate the network itself.

## How Scapy Works

Scapy works by representing packets as python objects. Instead of saying: “Send a TCP SYN packet to port 80” we say:  
“Create an IP packet ➡️ add a TCP layer ➡️ set flags ➡️ send it”.  
We can stack layers like Lego blocks:

- Ethernet
- IP
- TCP / UDP / ICMP
- Raw payloads

And we can inspect or alter any field: flags, sequence numbers, TTL, checksums, payload bytes.

## How Scapy is useful in cyber security.

### 1. Packet sniffing and traffic analysis

Scapy can sniff live network traffic and dissect packets in real time. This is useful for:

- Detecting suspicious traffic patterns.
- Analyzing malware C2 communication.
- Understanding proprietary or obscure protocols.
- Learning how real network traffic behaves (not textbook examples).

### 2. Network scanning and reconnaissance

Scapy allows you to build custom scanners, not just rely on Nmap defaults. Example:

- Custom TCP SYN scans
- Stealthy ICMP probes
- OS fingerprinting experiments
- Firewall rule testing
