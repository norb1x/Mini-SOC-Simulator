# 1. Log File Paths and Permissions
Make sure the log files (e.g., alerts.log, blocked_ips.log) exist and are writable by the script.

If you get permission errors, run the scripts with appropriate user rights or adjust file permissions with chmod or chown.

# 2. IP Blocking Not Working
The defense.py script uses OS-level commands (e.g., iptables on Linux) to block IPs.

Verify your user has sufficient privileges (usually root) to execute these commands.

On some systems, the firewall commands might differ — you may need to adjust the code accordingly.

# 3. Log Parsing Errors
Ensure that the log format matches what log_parser.py expects.

Custom or unexpected log entries can cause parsing to fail or generate false positives.

# 4. CPU/RAM Monitoring Accuracy
system_stats.py reads system info from /proc or uses system utilities — these can vary between Linux distros.

If stats appear incorrect, check compatibility or adjust code to your environment.

# 5. Attack Simulation
The attack simulator (attack_simulator.py) mimics SSH login attempts by appending to logs.

Make sure your log file is correctly targeted, or adjust the simulator to your environment.

# 6. Script Naming & File Structure
You can rename the main script (mini-soc.py) but update any references accordingly.
Keep the file structure consistent to avoid import errors.
