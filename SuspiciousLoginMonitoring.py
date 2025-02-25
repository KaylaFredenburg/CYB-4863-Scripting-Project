import re
import time
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

    while True:
        try:
            with open(log_file, "r") as f, open(output_file, "a") as log_output:
                for line in f:
                    match = re.search(r"(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*(Failed|failure|invalid) password", line, re.IGNORECASE)
                    if match:
                        ip = match.group("ip")
                        failed_attempts[ip].append(time.time())

                        now = time.time()
                        recent_attempts = [t for t in failed_attempts[ip] if now - t < time_window]
                        failed_attempts[ip] = recent_attempts  

                        if len(recent_attempts) >= threshold:
                            alert_msg = f"ALERT: Potential brute-force attack from IP: {ip}\n"
                            print(alert_msg)  
                            log_output.write(alert_msg) 

            time.sleep(60) 

        except FileNotFoundError:
            print(f"Error: Log file '{log_file}' not found.")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            break

if __name__ == "__main__":
    analyze_logs()