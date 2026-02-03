from scapy.all import *
import threading

target_ip = input("Enter ip address of the target: ")
startingPort = int(input("Enter the starting port range: "))
endingPort = int(input("Enter the ending port range: "))

lock = threading.Lock()
MAX_THREADS = 100
semaphore = threading.Semaphore(MAX_THREADS)

def scan_port(port):
    with semaphore:
        packet = IP(dst=target_ip)/TCP(dport=port, flags="S")
        response = sr1(packet, timeout=2, verbose=0)

        with lock:
            if response and response.haslayer(TCP):
                if response[TCP].flags == 18:
                    print(f"[OPEN] Port {port}")
                elif response[TCP].flags == 20:
                    print(f"[CLOSED] Port {port}")
            else:
                print(f"[FILTERED] Port {port}")

threads = []

for port in range(startingPort, endingPort + 1):
    t = threading.Thread(target=scan_port, args=(port,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()