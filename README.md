# zkteco-linux-toolkit

Python scripts for ZKTeco biometric terminals on **Linux and macOS** — attendance extraction, door unlock, time sync, and Zoho People integration. No Windows required.

## Tested on

| Device | Firmware | Pull (4370) | Notes |
|--------|----------|-------------|-------|
| ZKTeco X2008 | ZEM510 / ZLM30_TFT | ✅ | Comm Server must be enabled first |

> **Device has Pull disabled?** (ESSL X2008, SpeedFace-V5L, ZAM180 firmware) — see [`adms-push-server`](https://github.com/Vibhav-Aggarwal/adms-push-server) instead.

## Prerequisites

```bash
pip install pyzk requests
```

Configure your device IP via environment variable or edit `DEVICE_IP` in scripts:
```bash
export ZKTECO_IP=192.168.1.201
export ZKTECO_KEY=0      # comm key from Menu → Comm → PC Connection
```

## Scripts

### Door control

| Script | What it does |
|--------|-------------|
| `scripts/door-control/simple_unlock.py` | One-command door unlock |
| `scripts/door-control/Door Unlock.command` | macOS double-clickable shortcut |

```bash
python3 scripts/door-control/simple_unlock.py
# or: ZKTECO_IP=192.168.1.201 python3 scripts/door-control/simple_unlock.py
```

### Device management

| Script | What it does |
|--------|-------------|
| `scripts/device-management/sync_device_time.py` | Sync clock to server time |
| `scripts/device-management/extract_attendance.py` | Download all records to CSV |
| `scripts/device-management/enable_comm_server.py` | Enable API via telnet (if disabled) |

### Integrations

| Script | What it does |
|--------|-------------|
| `scripts/integrations/zoho_people_sync.py` | Push attendance to Zoho People |

```bash
export ZOHO_CLIENT_ID=...
export ZOHO_CLIENT_SECRET=...
export ZOHO_REFRESH_TOKEN=...
python3 scripts/integrations/zoho_people_sync.py --days 1
```

See [`docs/zoho-people-setup.md`](docs/zoho-people-setup.md) for OAuth setup.

## Troubleshooting

**"Unauthenticated" error from pyzk**: Communication Server is disabled on the device.
Run `enable_comm_server.py` or enable it via the physical menu (`Menu → Comm → PC Connection`).

**pyzk connects but returns empty data**: Your firmware has Pull mode disabled (`0x07f0` error internally).
Switch to ADMS push mode — see [adms-push-server](https://github.com/Vibhav-Aggarwal/adms-push-server).

Full diagnosis: [`docs/pull-vs-push.md`](docs/pull-vs-push.md)

## Related

- [`adms-push-server`](https://github.com/Vibhav-Aggarwal/adms-push-server) — for devices with Pull disabled (ADMS push mode)
- [`realand-bioface-m61-protocol`](https://github.com/Vibhav-Aggarwal/realand-bioface-m61-protocol) — for Secureye/Realand/BIOFACE devices
- [`biometric-oemware-guide`](https://github.com/Vibhav-Aggarwal/biometric-oemware-guide) — identify which repo applies to your device

## License

MIT
