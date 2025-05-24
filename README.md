# 🛡️ Mini SOC - Log Monitoring & Alerting Simulator

Mini SOC is a lightweight security monitoring simulator designed to run on a Raspberry Pi or any Linux system. It tracks SSH login activity in real time, summarizes events, detects suspicious behavior, triggers alerts, and optionally blocks attacking IPs.

## 🎬 Preview [ DEMO ] 
![Demo](https://s1.ezgif.com/tmp/ezgif-18bb3453e18e72.gif)

## ✨ Features

- 🔍 Real-time monitoring of `sshd` logs
- 📊 Summary of failed and successful login attempts
- 🚨 Detection of high failed login rates with alerts
- ⛔ Automatic IP blocking on suspicious activity
- 🧪 Simulated login attempts from spoofed IPs
- 🧼 Masking of IP addresses and ports for clean output

## 🗂️ File Structure

mini-soc/
├── norb1x-soc.py # Main SOC application - Change it to whatever name u want 
├── system_stats.py # CPU temperature and RAM usage reader
├── log_parser.py # Log parsing and event tracking
├── alerts.py # Alert detection logic
├── defense.py # IP blocking mechanism
├── attack_simulator.py # Simulated SSH login attempts
├── README.md # This file


## ⚙️ Requirements

- Python 3.7+
- `rich` library (`pip install rich`)
- Linux system with `journalctl` access
- Root privileges for IP blocking (`iptables` or similar)

## 🚀 Running the Project

1. Install required packages:
   ```bash
   pip install rich
   
2.Run with real SSH logs:
python nameofursoc.py

3. Or run in simulation mode:
   python norb1x-soc.py -- simulate

   
# 🧠 How It Works
The script reads real-time SSH logs via journalctl.

Logs are parsed and stored in memory, tracking login attempts by IP.

IPs and ports in log output are masked (e.g., 1.x.x.x, port 4xxx) for privacy.

If an IP exceeds a threshold of failed logins, an alert is triggered.

Attacking IPs can be automatically blocked using system firewall rules.

In --simulate mode, fake login attempts are generated from random IPs to demonstrate alerts and blocking.


# 🔐 Privacy & Security
All displayed IP addresses are obfuscated.

No data is sent externally – everything runs locally.

Safe to share screenshots or log output publicly.


# 📄 License
This project was built for educational and demonstration purposes.
You are free to use, modify, and share it.

Author: norb1x
