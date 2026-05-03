#!/usr/bin/env python3
"""
Sync ZKTeco device clock to server time.

Usage:
    python3 sync_device_time.py
    ZKTECO_IP=192.168.1.100 python3 sync_device_time.py

Requires: pip install pyzk
"""

import os
from datetime import datetime
from zk import ZK

DEVICE_IP   = os.getenv("ZKTECO_IP",       "192.168.1.201")
DEVICE_PORT = int(os.getenv("ZKTECO_PORT", "4370"))
COMM_KEY    = int(os.getenv("ZKTECO_KEY",  "0"))

zk = ZK(DEVICE_IP, port=DEVICE_PORT, timeout=10, password=COMM_KEY, force_udp=True)
conn = zk.connect()
if conn:
    now = datetime.now()
    zk.set_time(now)
    device_time = zk.get_time()
    zk.disconnect()
    print(f"Set time to: {now}")
    print(f"Device now:  {device_time}")
else:
    print("Connection failed")
