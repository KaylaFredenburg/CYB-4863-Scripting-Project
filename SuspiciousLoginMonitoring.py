import re
import time
from collections import defaultdict
# Log file path (adjust to your system)
log_file = "auth.log" # Example: /var/log/auth.log on Linux
# Failed login threshold
threshold = 5
time_window = 600 # 10 minutes in seconds
# Dictionary to store failed login attempts (IP: [timestamps])
failed_attempts = defaultdict(list)
def analyze_logs():
    while True:
        try:
            with open(log_file, "r") as f:
                for line in f:
# Regex to extract IP and login status (adapt to your log format)

match = re.search(r"(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*(Failed|failure|invalid) password", line, re.IGNORECASE)
if match:
    ip = match.group("ip")
    failed_attempts[ip].append(time.time())
# Check for threshold
now = time.time()
recent_attempts = [t for t in failed_attempts[ip] if now - t < time_window]
failed_attempts[ip] = recent_attempts # Keep only recent attempts

if len(recent_attempts) >= threshold:
    print(f"ALERT: Potential brute-force attack from IP: {ip}")
# You could add code here to block the IP (Bonus Challenge)
time.sleep(60) # Check every minute
except FileNotFoundError:
print(f"Error: Log file '{log_file}' not found.")
break
except Exception as e:
print(f"An error occurred: {e}")
    break

if __name__ == "__main__":
    analyze_logs()