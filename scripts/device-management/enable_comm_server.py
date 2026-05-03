#!/usr/bin/env python3
"""
ZKTeco Communication Server enabler.

On some X2008 units the "Communication Server" is disabled by default,
causing pyzk to return Unauthenticated errors even with the correct password.
This script enables it via the device's telnet shell (port 23).

Usage:
    python3 enable_comm_server.py
    ZKTECO_IP=192.168.1.100 python3 enable_comm_server.py

If telnet access fails (credentials unknown or port closed), use the
physical menu instead:
    Menu → Comm → PC Connection → enable
"""

import os
import socket
import time

DEVICE_IP   = os.getenv("ZKTECO_IP",   "192.168.1.201")
TELNET_PORT = 23

# Common ZKTeco embedded Linux credentials (try in order)
TELNET_CREDENTIALS = [
    ("root", ""),
    ("root", "admin"),
    ("root", "123456"),
    ("admin", "admin"),
    ("admin", "123456"),
    ("", ""),
]

def _try_login(sock, username, password):
    sock.send((username + "\n").encode("ascii"))
    time.sleep(0.8)
    resp = sock.recv(2048).decode("utf-8", errors="ignore")
    if "Password:" in resp or "password:" in resp:
        sock.send((password + "\n").encode("ascii"))
        time.sleep(1.2)
        resp2 = sock.recv(2048).decode("utf-8", errors="ignore")
        return any(p in resp2 for p in ["#", "$", "~", ">"])
    return any(p in resp for p in ["#", "$", "~", ">"])

def enable_via_telnet():
    print(f"Connecting to {DEVICE_IP}:{TELNET_PORT} ...")
    for username, password in TELNET_CREDENTIALS:
        try:
            s = socket.socket()
            s.settimeout(8)
            s.connect((DEVICE_IP, TELNET_PORT))
            s.recv(1024)  # banner
            if _try_login(s, username, password):
                print(f"Shell access via {username!r}/{password!r}")
                # Enable the comm server service
                for cmd in ["service zknetservice start", "/etc/init.d/zkservice start"]:
                    s.send((cmd + "\n").encode("ascii"))
                    time.sleep(2)
                    out = s.recv(4096).decode("utf-8", errors="ignore")
                    if out.strip():
                        print(f"  {cmd}: {out.strip()[:200]}")
                s.close()
                return True
            s.close()
        except Exception:
            pass
    return False

if __name__ == "__main__":
    if enable_via_telnet():
        print("\nService started. Wait ~10s then test with pyzk.")
    else:
        print("\nTelnet access failed. Use the physical menu:")
        print("  Menu → Comm → PC Connection → set to 'Enable'")
        print("  Then reboot the device.")
