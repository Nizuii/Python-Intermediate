import csv
import ipaddress

log_file = "/home/nizam/Work/SpaceX/logs/loginLog.csv"

def failed_attempts():
    with open(log_file, newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row["event"].strip().lower() == "login_failed":
                print(
                    f"Time: {row['timestamp']} | "
                    f"User: {row['user']} | "
                    f"Status: {row['event']} | "
                    f"IP: {row['ip']}"
                )

def is_external_ip(ip):
    ip_obj = ipaddress.ip_address(ip)
    return not (
        ip_obj.is_private or
        ip_obj.is_loopback
    )

def external_failed_logins():
    with open(log_file, newline="") as file:
        reader = csv.DictReader(file)

        print("=== External Failed Login Attempts ===\n")

        for row in reader:
            if row["event"].strip().lower() == "login_failed":
                ip = row["ip"].strip()

                if is_external_ip(ip):
                    print(
                        f"Time: {row['timestamp']} | "
                        f"User: {row['user']} | "
                        f"Status: {row['event']} | "
                        f"IP: {ip}"
                    )


def is_internal_ip(ip):
    ip_obj = ipaddress.ip_address(ip)
    return ip_obj.is_private or ip_obj.is_loopback

def internal_failed_logins():
    with open(log_file, newline="") as file:
        reader = csv.DictReader(file)

        print("=== Internal Failed Login Attempts ===\n")

        for row in reader:
            if row["event"].strip().lower() == "login_failed":
                ip = row["ip"].strip()

                if is_internal_ip(ip):
                    print(
                        f"Time: {row['timestamp']} | "
                        f"User: {row['user']} | "
                        f"IP: {ip}"
                    )

while True:
    choice = int(input("1. To Filter all Failed login attempts. \n2. To Filter all Failed External IP Login Attempts.  \n3. To Filter all Failed Internal IP Login Attempts. \nEmter your choice: "))
    if choice == 1:
        failed_attempts()
        print("\n")
    elif choice == 2:
        external_failed_logins()
        print("\n")
    elif choice == 3:
        internal_failed_logins()
        print("\n")
    else:
        print("Gracias, Adios :)")
        break