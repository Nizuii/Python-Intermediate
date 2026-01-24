# What is Scapy?

Scapy is not a scanner like Nmap. Scapy is a packet crafting and packet manipulation framework. We can create packets manually, send them alive directly on the wire, recieve raw responses, we can decide what to do with them. We will be covering ARP scanning first using scapy. So before we dive in lets just sneak peek into ARP.

## What is ARP and what does i do?

- ARP stands for **address resolution protocol** and it answers one simple question:

  > "Who has IP `x.x.x.x`? Tell me your MAC address."

- ARP works only inside Local Area Network (LAN).
- All ARP request are broadcast.
- Active hosts must reply.
- This makes ARP scanning faster than ICMP ping, more reliable because firewalls dont usually block ARP and its perfect for host discovery.
