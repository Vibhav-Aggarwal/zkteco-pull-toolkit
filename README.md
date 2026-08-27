# zkteco-pull-toolkit

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Schema.org](https://img.shields.io/badge/Schema.org-CodeMeta_JSON--LD-orange.svg)](codemeta.json)
[![Citation](https://img.shields.io/badge/Citation-CITATION.cff-green.svg)](CITATION.cff)
[![Author](https://img.shields.io/badge/ORCID-0009--0000--7686--7119-green.svg)](https://orcid.org/0009-0000-7686-7119)
[![Atlas Hub](https://img.shields.io/badge/Ecosystem-Terminal_Firmware_Atlas-blue.svg)](https://github.com/Vibhav-Aggarwal/terminal-firmware-atlas)

Clean Python CLI scripts for ZKTeco and OEM biometric terminals on **Linux and macOS** — attendance CSV extraction, door unlock triggers, device time synchronization, and Zoho People integration.

No Windows required.

---

## 📋 Tested Hardware

| Device Model | Firmware / Platform | Port 4370 Pull | Status |
| :--- | :--- | :--- | :--- |
| **ZKTeco X2008** | `ZEM510` / `ZLM30_TFT` | ✅ Enabled | Verified (Comm Server enabled) |
| **ZKTeco F22 / UA300** | `ZEM` Series | ✅ Enabled | Verified |
| **eSSL X990 / MB160** | Older ZEM | ✅ Enabled | Verified |

> **Is port 4370 Pull disabled on your device?** (Common on newer face devices like SpeedFace-V5L / eSSL X2008 with ZAM180 firmware)  
> 👉 Use **[zkteco-adms-server](https://github.com/Vibhav-Aggarwal/zkteco-adms-server)** instead.

---

## 🚀 Quick Start

```bash
# 1. Clone repository
git clone https://github.com/Vibhav-Aggarwal/zkteco-pull-toolkit.git
cd zkteco-pull-toolkit

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set environment variable or configure device IP
export ZKTECO_IP=192.168.1.201
export ZKTECO_KEY=0

# 4. Extract attendance to CSV
python3 scripts/device-management/extract_attendance.py
```

---

## 🛠️ Included Tools

### 1. Door Control
- `scripts/door-control/simple_unlock.py`: Instant one-shot door unlock trigger.
- `scripts/door-control/Door Unlock.command`: Double-clickable macOS launcher script.

### 2. Device Management
- `scripts/device-management/extract_attendance.py`: Dump attendance logs to structured CSV.
- `scripts/device-management/sync_device_time.py`: Synchronize terminal clock with system NTP time.
- `scripts/device-management/enable_comm_server.py`: Diagnostic helper to enable communication socket.

### 3. Integrations
- `scripts/integrations/zoho_people_sync.py`: Automated push of daily punches to Zoho People API.

---

## 📄 License & Attribution

- **License:** [Apache-2.0 License](LICENSE)
- **Author:** Vibhav Aggarwal ([ORCID: 0009-0000-7686-7119](https://orcid.org/0009-0000-7686-7119))
- **Citation:** See [`CITATION.cff`](CITATION.cff)
