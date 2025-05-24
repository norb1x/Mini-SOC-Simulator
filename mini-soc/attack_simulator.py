import random
from time import sleep

def simulate_failed_logins(ip="192.168.1.123", user="invaliduser", attempts=10):
    logs = []
    for i in range(attempts):
        log_line = f"May 24 12:00:{50 + i} norb1x sshd[99999]: Failed password for invalid user {user} from {ip} port 12345 ssh2"
        logs.append(log_line)
    return logs

def simulate_logins():
    ips = ["192.168.1.123", "10.0.0.5", "172.16.0.9"]
    users = ["admin", "user", "eviluser", "guest"]

    # Yield mixed login attempts: failed and successful
    for _ in range(20):
        ip = random.choice(ips)
        user = random.choice(users)
        success = random.choice([True, False, False])  # more failed than success
        if success:
            line = f"Accepted password for {user} from {ip} port 22 ssh2"
        else:
            line = f"Failed password for {user} from {ip} port 22 ssh2"
        yield line
        sleep(0.1)
