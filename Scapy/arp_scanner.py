from scapy.all import *

target_range = input("Enter target subnet (e.g. 192.168.1.0/24): ")

arp = ARP(pdst=target_range)
ether = Ether(dst="ff:ff:ff:ff:ff:ff")
packet = ether / arp

print("\nScanning...\n")

answered = srp(packet, timeout=2, verbose=0)[0]

print("IP Address\t\tMAC Address")
print("-----------------------------------------")

for sent, received in answered:
    print(f"{received.psrc}\t\t{received.hwsrc}")
