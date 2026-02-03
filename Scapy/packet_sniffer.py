from scapy.all import sniff, IP, TCP, UDP, ICMP, ARP

def packet_handler(packet):

    # ---- ARP (Layer 2) ----
    if ARP in packet:
        op = packet[ARP].op
        src_ip = packet[ARP].psrc
        src_mac = packet[ARP].hwsrc
        dst_ip = packet[ARP].pdst

        if op == 1:
            print(f"[ARP-REQUEST] Who has {dst_ip}? Tell {src_ip} ({src_mac})")
        elif op == 2:
            print(f"[ARP-REPLY] {src_ip} is at {src_mac}")
        return

    # ---- IP-based protocols ----
    if IP in packet:
        src = packet[IP].src
        dst = packet[IP].dst

        if ICMP in packet:
            icmp_type = packet[ICMP].type
            icmp_code = packet[ICMP].code
            print(f"[ICMP] {src} → {dst} | Type: {icmp_type} Code: {icmp_code}")

        elif TCP in packet:
            print(f"[TCP] {src} → {dst} | Sport: {packet[TCP].sport} Dport: {packet[TCP].dport}")

        elif UDP in packet:
            print(f"[UDP] {src} → {dst} | Sport: {packet[UDP].sport} Dport: {packet[UDP].dport}")

        else:
            print(f"[IP] {src} → {dst}")

sniff(iface="wlan0", prn=packet_handler, store=False)

