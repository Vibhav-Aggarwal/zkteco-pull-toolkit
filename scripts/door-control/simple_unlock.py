#!/usr/bin/env python3
"""
ZKTeco door unlock — one command, no interactive prompt.

Usage:
    python3 simple_unlock.py
    ZKTECO_IP=192.168.1.100 python3 simple_unlock.py

Requires: pip install pyzk
"""

import os
from zk import ZK

DEVICE_IP   = os.getenv("ZKTECO_IP",       "192.168.1.201")
DEVICE_PORT = int(os.getenv("ZKTECO_PORT", "4370"))
COMM_KEY    = int(os.getenv("ZKTECO_KEY",  "0"))      # device comm key (Menu → Comm → PC Connection)

def unlock():
    zk = ZK(DEVICE_IP, port=DEVICE_PORT, timeout=5, password=COMM_KEY, force_udp=True)
    try:
        conn = zk.connect()
        if conn:
            result = zk.unlock()
            zk.disconnect()
            print("UNLOCKED" if result else "UNLOCK FAILED")
            return result
        else:
            print("CONNECTION FAILED")
            return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    unlock()
