import os
import subprocess

src_addr = "/home/nizam/Work/SpaceX/logs/shark1.pcapng"
dst_addr = "/home/nizam/Work/SpaceX/logs/traffic.csv"

os.makedirs(os.path.dirname(dst_addr), exist_ok=True)

command = [
    "tshark",
    "-r", src_addr,
    "-T", "fields",
    "-e", "eth.type",
    "-e", "ip.proto",
    "-e", "udp.dstport",
    "-E", "header=y",
    "-E", "separator=,"
]

with open(dst_addr, "w") as outfile:
    result = subprocess.run(
        command,
        stdout=outfile,
        stderr=subprocess.PIPE,
        text=True
    )

if result.stderr:
    print("tshark error:", result.stderr)
