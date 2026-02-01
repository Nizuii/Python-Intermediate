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

- Custom TCP SYN scans.
- Stealthy ICMP probes.
- OS fingerprinting experiments.
- Firewall rule testing.

### 3. ARP spoofing and MITM attacks

Scapy is commonly used to:

- Poison ARP caches.
- Intercept traffic in local networks.
- Demonstrate Man-in-the-Middle attacks in labs.

### 4. Denial-of-Service (DoS) research

In controlled environments, Scapy is used to:

- Generate packet floods.
- Test rate-limiting.
- Validate IDS/IPS rules.

### 5. Exploit development and protocol fuzzing

- Fuzz protocol fields.
- Send malformed packets.
- Trigger edge-case behavior in services.
- Discover crashes or unexpected responses.

### 6. IDS/IPS and detection engineering

Blue teams use Scapy to:

- Generate attack traffic.
- Test detection rules.
- Validate alert thresholds.
- Reproduce suspicious packets from logs.
