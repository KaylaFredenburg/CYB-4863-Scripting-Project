import re
import time
from datetime import datetime
from collections import defaultdict

# Log file path
log_file = "/var/log/auth.log" 
output_file = "detection_log.txt"

# Failed login threshold
threshold = 5
time_window = 600 

# Dictionary to store failed login attempts
failed_attempts = defaultdict(list)

def analyze_logs():
    with open(output_file, "w") as log_output:
        log_output.write("Brute Force Detection Log\n")
        log_output.write("=" * 40 + "\n")

    print("Testing... status will be output every 60 seconds")
    while True:
        try:
            with open(log_file, "r") as f, open(output_file, "a") as log_output:
                potential_attack_ips = dict()
                root_login_ips = dict()
                for line in f:
                    # Check for failed logins of any account
                    match_failed_logins = re.search(r"(?:Failed|failure|invalid).*?from\s+(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", line, re.IGNORECASE)
                    if match_failed_logins:
                        ip = match_failed_logins.group("ip")
                        now = time.time()

                        # Store timestamps
                        failed_attempts[ip].append(now)
                        failed_attempts[ip] = [t for t in failed_attempts[ip] if now - t < time_window]

                        # Detect brute force attempts
                        if len(failed_attempts[ip]) >= threshold:
                            potential_attack_ips[ip] = potential_attack_ips.get(ip, 0) + 1

                    # Check for successful logins of root account
                    match_root_logins = re.search(r"Accepted password for root from (?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) port \d+")
                    if match_root_logins:
                        ip = match_root_logins.group("ip")
                        now = time.time()

                        # Store timestamps
                        match_root_logins[ip].append(now)
                        match_root_logins[ip] = [t for t in failed_attempts[ip] if now - t < time_window]

                        # Detect brute force attempts
                        if len(match_root_logins[ip]):
                            root_login_ips[ip] = root_login_ips.get(ip, 0) + 1



                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"=============== Report at {now} ===============")
                for ip, count in potential_attack_ips.items():
                    print(f"ALERT: Potential brute-force attack from IP: {ip} ({count} attempts in {time_window // 60} minutes)")
                for ip, count in root_login_ips.items():
                    print(f"ALERT: Successful root login from {ip} ({count} attempts in {time_window // 60} minutes)")

            time.sleep(60) 

        except FileNotFoundError:
            print(f"Error: Log file '{log_file}' not found.")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            break

if __name__ == "__main__":
    analyze_logs()