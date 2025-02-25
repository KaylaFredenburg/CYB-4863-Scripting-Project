#!/bin/bash

# Target user (must exist on the system)
USER="root"

# Target host (localhost for testing)
HOST="10.30.250.77"

# Number of failed login attempts
ATTEMPTS=300

# Time interval between attempts (in seconds)
INTERVAL=1

echo "🚨 Simulating brute-force attack against SSH ($ATTEMPTS failed attempts)..."

for i in $(seq 1 $ATTEMPTS); do
    echo "Attempt $i: Trying invalid SSH login..."
    ssh $USER@$HOST -p 22 -o StrictHostKeyChecking=no -o BatchMode=yes -o ConnectTimeout=1 exit &> /dev/null
    sleep $INTERVAL
done

echo "✅ Brute-force simulation complete. Check /var/log/auth.log for failed login entries."
