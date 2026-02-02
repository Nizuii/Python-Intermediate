import pandas as pd
import matplotlib.pyplot as plt
import ipaddress

df = pd.read_csv("~/Work/SpaceX/logs/traffic.csv")
df = df.dropna(subset=["ip.src", "ip.dst"])

# Function to view 
def top_external_talkers():
    # df["ip.src"].value_counts().head(10).plot(kind="pie")
    # plt.title("Top Talkers")
    # plt.show()

    private_networks = [
        ipaddress.ip_network("10.0.0.0/8"),
        ipaddress.ip_network("172.16.0.0/12"),
        ipaddress.ip_network("192.168.0.0/16"),
    ]
    def is_internal(ip):
        try:
            ip_obj = ipaddress.ip_address(ip)
            return any(ip_obj in net for net in private_networks)
        except ValueError:
            return False
        
    external_sources = df[
        (~df["ip.src"].apply(is_internal)) &
        (df["ip.dst"].apply(is_internal))
    ]
    top_external_ips = external_sources["ip.src"].value_counts().head(10)

    top_external_ips.plot(kind="pie")
    plt.title("Top External IPs Communicating with Internal Network")
    plt.xlabel("External IP")
    plt.ylabel("Number of Packets")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def top_internal_talkers():
    private_networks = [
        ipaddress.ip_network("10.0.0.0/8"),
        ipaddress.ip_network("172.16.0.0/12"),
        ipaddress.ip_network("192.168.0.0/16"),
    ]

    def is_internal(ip):
        try:
            ip_obj = ipaddress.ip_address(ip)
            return any(ip_obj in net for net in private_networks)
        except ValueError:
            return False
        
    internal_sources = df[df["ip.src"].apply(is_internal)]
    internal_destinations = df[df["ip.dst"].apply(is_internal)]
    top_internal_src = internal_sources["ip.src"].value_counts().head(10)
    top_internal_src.plot(kind="pie")
    plt.title("Top Internal IPs (Traffic Sources)")
    plt.xlabel("Internal IP")
    plt.ylabel("Number of Packets")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def internal_vs_external():
    internal = df["ip.src"].str.startswith("192.168.")
    counts = internal.value_counts()

    counts.plot(kind="pie", autopct="%1.1f%%", labels=["External IP", "Internal IP"])
    plt.title("Internal vs External IP Traffic")
    plt.ylabel("")
    plt.show()

def identify_proto():
    protocol_map = {
        1: "ICMP",
        6: "TCP",
        17: "UDP"
    }

    df["protocol_name"] = df["ip.proto"].map(protocol_map)

    protocol_counts = df["protocol_name"].value_counts()
    print(protocol_counts)

    protocol_counts.plot(kind="pie", autopct="%1.1f%%")
    plt.title("Most Used Protocols in PCAP")
    plt.xlabel("Protocol")
    plt.ylabel("Number of Packets")
    plt.tight_layout()
    plt.show()

while True:
    choice = int(input("1. To view top external talkers \n2. To view top internal talkers \n3. To view internal & external IP \n4. View Protocols \nEnter your choice: "))
    if choice==1:
        top_external_talkers()
    elif choice==2:
        top_internal_talkers()
    elif choice==3:
        internal_vs_external()
    elif choice==4:
        identify_proto()
    else:
        print("[+] Gracias, Exiting")
        break