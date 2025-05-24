import subprocess

def block_ip(ip):
    subprocess.run(["sudo", "iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"])
    with open("blocked_ips.log", "a") as f:
        f.write(f"Blocked IP: {ip}\n")
