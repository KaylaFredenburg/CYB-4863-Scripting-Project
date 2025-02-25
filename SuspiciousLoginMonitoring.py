import re
import time
from datetime import datetime
from collections import defaultdict

# Log file path
log_file = "/var/log/auth.log"
output_file = "detection_log.txt"

# Failed login threshold
threshold = 5
time_window = 600  # 10 minutes

# Dictionaries to store login attempts
failed_attempts = defaultdict(list)
root_login_ips = defaultdict(list)

def analyze_logs():
    with open(output_file, "w") as log_output:
        log_output.write("Brute Force Detection Log\n")
        log_output.write("=" * 40 + "\n")

    print("Testing... status will be output every 60 seconds")

    # Open log file in "read" mode and seek to the end to avoid re-reading old entries
    with open(log_file, "r") as f:
        f.seek(0, 2)  # Move to the end of the file

        while True:
            try:
                new_lines = f.readlines()
                if not new_lines:
                    time.sleep(1)
                    continue  # No new lines, wait and check again

                potential_attack_ips = {}

                for line in new_lines:
                    now = time.time()

                    # Detect failed login attempts
                    match_failed_logins = re.search(r"(?:Failed|failure|invalid).*?from\s+(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", line, re.IGNORECASE)
                    if match_failed_logins:
                        ip = match_failed_logins.group("ip")
                        failed_attempts[ip].append(now)
                        failed_attempts[ip] = [t for t in failed_attempts[ip] if now - t < time_window]

                        if len(failed_attempts[ip]) >= threshold:
                            potential_attack_ips[ip] = potential_attack_ips.get(ip, 0) + 1

                    # Detect successful root logins
                    match_root_logins = re.search(r"Accepted password for root from (?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) port \d+", line, re.IGNORECASE)
                    if match_root_logins:
                        ip = match_root_logins.group("ip")
                        root_login_ips[ip].append(now)
                        root_login_ips[ip] = [t for t in root_login_ips[ip] if now - t < time_window]

                # Report every 60 seconds
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"\n=============== Report at {now} ===============")

                if potential_attack_ips:
                    for ip, count in potential_attack_ips.items():
                        print(f"🚨 ALERT: Potential brute-force attack from {ip} ({count} attempts in {time_window // 60} minutes)")
                else:
                    print("✅ No recent brute-force attempts detected.")

                if root_login_ips:
                    for ip, count in root_login_ips.items():
                        print(f"⚠️ ALERT: Successful root login from {ip} ({count} logins in {time_window // 60} minutes)")
                else:
                    print("✅ No successful root logins detected.")

                time.sleep(60)

            except FileNotFoundError:
                print(f"Error: Log file '{log_file}' not found.")
                break
            except Exception as e:
                print(f"An error occurred: {e}")
                break

if __name__ == "__main__":
    analyze_logs()
