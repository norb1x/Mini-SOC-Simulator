import re
from collections import defaultdict, deque
from collections import deque

last_logs = deque(maxlen=100)

stats = {
    "failed": {},      # {user/ip: count}
    "successful": {},  # {user/ip: count}
}

failed_logins = {}  # {ip: count}

def parse_log_line(line):
    last_logs.append(line)

    lower_line = line.lower()

    # Example detection of failed login attempts
    if "failed password" in lower_line:
        # Extract IP address (assumes format "from <ip>" always present in the log)
        parts = line.split()
        ip = None
        for i, part in enumerate(parts):
            if part == "from" and i + 1 < len(parts):
                ip = parts[i + 1]
                break
        if ip:
            stats['failed'][ip] = stats['failed'].get(ip, 0) + 1
            failed_logins[ip] = failed_logins.get(ip, 0) + 1

    elif "accepted password" in lower_line:
        # Extract IP address similarly for successful logins
        parts = line.split()
        ip = None
        for i, part in enumerate(parts):
            if part == "from" and i + 1 < len(parts):
                ip = parts[i + 1]
                break
        if ip:
            stats['successful'][ip] = stats['successful'].get(ip, 0) + 1
