# Pull (port 4370) vs Push (ADMS) — which does your device support?

## Quick test

```python
from zk import ZK
zk = ZK('<device-ip>', port=4370, timeout=5, password=0)
conn = zk.connect()
if conn:
    users = zk.get_users()
    print(f"Pull mode works — {len(users)} users")
    zk.disconnect()
else:
    print("Connection failed or returns empty — try ADMS push instead")
```

## Decision table

| Symptom | Diagnosis | Solution |
|---------|-----------|---------|
| `pyzk` connects, returns real data | Pull mode enabled | Use scripts in this repo |
| `pyzk` connects but all calls return `[]` | Pull protocol disabled (0x07f0) | Switch to ADMS push — see `adms-push-server` |
| `pyzk` raises "Unauthenticated" | Comm Server disabled on device | Run `enable_comm_server.py` or use device menu |
| `pyzk` raises "Unauthenticated" after enabling | Wrong comm key | Try key=0, then key=123456 |
| Device port 4370 not reachable at all | Network issue or service not running | Check firewall, try `nmap -p 4370 <ip>` |

## Which ZKTeco firmware supports Pull?

| Firmware family | Platform | Pull (4370) | Notes |
|-----------------|----------|-------------|-------|
| ZEM510 (X2008 genuine) | MIPS, ZLM30_TFT | ✅ | Needs Comm Server enabled first |
| ZAM180 (SpeedFace-V5L, eSSL X2008) | ARM, ZAM180_TFT | ❌ 0x07f0 | Use ADMS push |
| ZEM800 (newer models) | — | ✅ usually | Check `pyzk` output |

The `0x07f0` error is not a bug in pyzk — it is the device's firmware actively rejecting all Pull commands. There is no workaround short of firmware downgrade.

## Enabling the Comm Server (ZEM510 / X2008 genuine)

On genuine ZKTeco X2008 (ZEM510 firmware), the Communication Server starts disabled. Symptom: `Unauthenticated` even with correct key.

**Via device menu**: `Menu → Comm → PC Connection` → set to Enabled  
**Via script**: `python3 scripts/device-management/enable_comm_server.py`

After enabling, the device's port 4370 becomes accessible.
