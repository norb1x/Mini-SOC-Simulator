from datetime import datetime, timedelta

# Keep track of timestamps of failed attempts per IP
failed_attempts_history = {}

def check_alerts(failed_logins):
    alerts = []
    now = datetime.now()

    # Remove timestamps older than 5 minutes
    for ip in list(failed_attempts_history.keys()):
        failed_attempts_history[ip] = [t for t in failed_attempts_history[ip] if now - t < timedelta(minutes=5)]
        if not failed_attempts_history[ip]:
            del failed_attempts_history[ip]

    # Add current failed login timestamps
    for ip, count in failed_logins.items():
        if ip not in failed_attempts_history:
            failed_attempts_history[ip] = []
        for _ in range(count):
            failed_attempts_history[ip].append(now)

    # Alert if more than 5 failed attempts in last 5 minutes
    for ip, times in failed_attempts_history.items():
        if len(times) > 5:
            alert_msg = f"[ALERT] High failed login attempts from {ip}: {len(times)} in last 5 minutes"
            alerts.append(alert_msg)
            with open("alerts.log", "a") as f:
                f.write(f"{datetime.now()}: {alert_msg}\n")

    return alerts
