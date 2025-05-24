import subprocess
from time import sleep, time
import sys
from rich.console import Console, Group
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
import re

from alerts import check_alerts
from system_stats import get_cpu_temp, get_ram_usage_percent
from log_parser import parse_log_line, last_logs, stats, failed_logins

from defense import block_ip
from attack_simulator import simulate_logins  # new mixed login simulation

console = Console()

def colorize_log_line(line):
    text = Text(line)
    lower_line = line.lower()
    if "error" in lower_line:
        text.stylize("red")
    elif "failed" in lower_line:
        text.stylize("yellow")
    return text

# Funkcja maskująca pojedyncze IP (IPv4) do postaci np. "1.x.x.x"
def mask_ip(ip):
    parts = ip.split('.')
    if len(parts) == 4:
        first_digit = parts[0][0] if parts[0] else "x"
        return f"{first_digit}.x.x.x"
    else:
        return ip  # Jeśli nie IPv4, zwróć bez zmian

# Funkcja maskująca port, np. "58384" -> "5xxx"
def mask_port(port_str):
    if port_str.isdigit() and len(port_str) > 0:
        return port_str[0] + "xxx"
    return port_str

# Funkcja maskująca wszystkie IP i porty w linii tekstu
def mask_ips_and_ports_in_line(line):
    # Maskowanie IP
    ip_pattern = r'(\d{1,3}\.){3}\d{1,3}'
    def ip_replacer(match):
        ip = match.group(0)
        return mask_ip(ip)
    line = re.sub(ip_pattern, ip_replacer, line)

    # Maskowanie portów (np. "port 58384" -> "port 5xxx")
    port_pattern = r'(port )(\d+)'
    def port_replacer(match):
        prefix = match.group(1)
        port = match.group(2)
        return prefix + mask_port(port)
    line = re.sub(port_pattern, port_replacer, line, flags=re.IGNORECASE)

    return line

def main():
    simulated_logs = None
    if "--simulate" in sys.argv:
        simulated_logs = iter(simulate_logins())

    command = ['journalctl', '-u', 'ssh', '-f', '--no-pager']
    process = subprocess.Popen(command, stdout=subprocess.PIPE, text=True)

    active_alerts = {}

    with Live(console=console, refresh_per_second=2) as live:
        while True:
            if simulated_logs:
                try:
                    for _ in range(3):
                        line = next(simulated_logs)
                        parse_log_line(line)
                except StopIteration:
                    simulated_logs = None

            if not simulated_logs and process.stdout.readable():
                line = process.stdout.readline()
                if line:
                    line = line.strip()
                    parse_log_line(line)
                else:
                    sleep(0.1)
                    continue

            temp = get_cpu_temp()
            ram = get_ram_usage_percent()

            system_panel = Panel(
                f"CPU Temp: {temp:.1f}°C\nRAM Usage: {ram:.1f}%",
                title="System Status"
            )

            colored_logs = [colorize_log_line(mask_ips_and_ports_in_line(line)) for line in list(last_logs)[-10:]]
            logs_panel = Panel(Group(*colored_logs), title="Last log entries")

            summary_table = Table(title="Mini SOC Log Summary")
            summary_table.add_column("Type")
            summary_table.add_column("User/IP")
            summary_table.add_column("Count", justify="right")

            for key, count in stats['failed'].items():
                masked = mask_ip(key)
                summary_table.add_row("[red]Failed[/red]", f"[bold]{masked}[/bold]", f"[red]{count}[/red]")

            for key, count in stats['successful'].items():
                masked = mask_ip(key)
                summary_table.add_row("[green]Successful[/green]", f"[bold]{masked}[/bold]", f"[green]{count}[/green]")

            new_alerts = check_alerts(failed_logins)
            now = time()
            for alert in new_alerts:
                parts = alert.split()
                for i, part in enumerate(parts):
                    if part == "from" and i + 1 < len(parts):
                        ip = parts[i + 1].strip(":")
                        active_alerts[ip] = now
                        block_ip(ip)

            active_alerts = {ip: ts for ip, ts in active_alerts.items() if now - ts <= 60}

            if active_alerts:
                alert_text = "\n".join(
                    f"[ALERT] High failed login attempts from {mask_ip(ip)} (active for {int(now - ts)}s)"
                    for ip, ts in active_alerts.items()
                )
                alert_style = "bold red"
            else:
                alert_text = "No alerts."
                alert_style = "green"

            alert_panel = Panel(alert_text, title="Alerts", style=alert_style)

            layout = Group(
                system_panel,
                logs_panel,
                summary_table,
                alert_panel
            )

            live.update(layout)
            sleep(0.1)

if __name__ == "__main__":
    main()
