#!/usr/bin/env python3
"""
Extract all attendance records from a ZKTeco device and write to CSV.

Usage:
    python3 extract_attendance.py [output.csv]
    ZKTECO_IP=192.168.1.100 python3 extract_attendance.py

Requires: pip install pyzk
"""

import csv
import os
import sys
from datetime import datetime
from zk import ZK

DEVICE_IP   = os.getenv("ZKTECO_IP",       "192.168.1.201")
DEVICE_PORT = int(os.getenv("ZKTECO_PORT", "4370"))
COMM_KEY    = int(os.getenv("ZKTECO_KEY",  "0"))
OUTPUT_FILE = sys.argv[1] if len(sys.argv) > 1 else f"attendance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

zk = ZK(DEVICE_IP, port=DEVICE_PORT, timeout=10, password=COMM_KEY, force_udp=True)
conn = zk.connect()
if not conn:
    print("Connection failed")
    sys.exit(1)

records = zk.get_attendance()
zk.disconnect()
print(f"Fetched {len(records)} records")

with open(OUTPUT_FILE, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["user_id", "timestamp", "status", "punch"])
    for r in records:
        writer.writerow([r.user_id, r.timestamp, r.status, r.punch])

print(f"Written to {OUTPUT_FILE}")
