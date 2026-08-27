# Security Policy & Door Control Safety

## 1. Physical Access Control Safety
Scripts in `scripts/door-control/` send direct relay trigger commands over port 4370:
- Do not execute unlock commands on active physical security barriers without an independent physical manual key override.
- Port 4370 communicates over UDP/TCP with lightweight or zero authentication by default; keep device networks isolated on a secure VLAN.

## 2. Vulnerability Reporting
Please report any security issues to `vibhav.aggarwal2@gmail.com`.
