#!/usr/bin/env python3
"""
Sync ZKTeco attendance to Zoho People (India region).

Setup:
  1. Create a Zoho OAuth client at https://api-console.zoho.in/
  2. Get a refresh token (see docs/zoho-people-setup.md)
  3. Set environment variables below

Usage:
    ZOHO_CLIENT_ID=... ZOHO_CLIENT_SECRET=... ZOHO_REFRESH_TOKEN=... \\
      python3 zoho_people_sync.py [--days 1]

Requires: pip install pyzk requests
"""

import argparse
import os
from datetime import datetime, timedelta
from zk import ZK
import requests

# ── Configuration ── set via environment, never hardcode credentials ──
DEVICE_IP      = os.getenv("ZKTECO_IP",            "192.168.1.201")
DEVICE_PORT    = int(os.getenv("ZKTECO_PORT",       "4370"))
COMM_KEY       = int(os.getenv("ZKTECO_KEY",        "0"))

ZOHO_DOMAIN    = os.getenv("ZOHO_DOMAIN",           "zoho.in")   # or zoho.com
CLIENT_ID      = os.getenv("ZOHO_CLIENT_ID",        "")
CLIENT_SECRET  = os.getenv("ZOHO_CLIENT_SECRET",    "")
REFRESH_TOKEN  = os.getenv("ZOHO_REFRESH_TOKEN",    "")

def get_access_token() -> str:
    resp = requests.post(
        f"https://accounts.{ZOHO_DOMAIN}/oauth/v2/token",
        data={
            "grant_type":    "refresh_token",
            "client_id":     CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "refresh_token": REFRESH_TOKEN,
        },
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()["access_token"]


def fetch_attendance(days_back: int) -> list:
    zk = ZK(DEVICE_IP, port=DEVICE_PORT, timeout=10, password=COMM_KEY, force_udp=True)
    conn = zk.connect()
    if not conn:
        raise RuntimeError(f"Could not connect to device at {DEVICE_IP}:{DEVICE_PORT}")
    records = zk.get_attendance()
    zk.disconnect()
    cutoff = datetime.now() - timedelta(days=days_back)
    return [r for r in records if r.timestamp >= cutoff]


def push_to_zoho(records: list, access_token: str):
    headers = {
        "Authorization": f"Zoho-oauthtoken {access_token}",
        "Content-Type":  "application/json",
    }
    url = f"https://people.{ZOHO_DOMAIN}/people/api/attendance/checkinout"
    ok = err = 0
    for r in records:
        data = {
            "employeeId": str(r.user_id),
            "checkTime":  r.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "checkType":  "IN" if r.status in (0, 4) else "OUT",
        }
        resp = requests.post(url, headers=headers, json=data, timeout=10)
        if resp.status_code == 200:
            ok += 1
        else:
            err += 1
            print(f"  failed user={r.user_id} status={resp.status_code}: {resp.text[:100]}")
    print(f"Zoho sync: {ok} OK, {err} errors")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int, default=1)
    args = parser.parse_args()

    if not CLIENT_ID or not REFRESH_TOKEN:
        raise SystemExit("Set ZOHO_CLIENT_ID, ZOHO_CLIENT_SECRET, ZOHO_REFRESH_TOKEN env vars")

    print(f"Fetching attendance from {DEVICE_IP} (last {args.days} day(s))...")
    records = fetch_attendance(args.days)
    print(f"  {len(records)} records found")
    if not records:
        return

    print("Refreshing Zoho access token...")
    token = get_access_token()

    print("Pushing to Zoho People...")
    push_to_zoho(records, token)


if __name__ == "__main__":
    main()
