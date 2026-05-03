# Zoho People Integration Setup

## Prerequisites

1. Zoho People account with attendance module enabled
2. Zoho API Console access at https://api-console.zoho.in/ (India) or https://api-console.zoho.com/

## Step 1 — Create OAuth client

1. Go to https://api-console.zoho.in/ → Add Client → Server-based Application
2. Note your **Client ID** and **Client Secret**
3. Set Redirect URI to `http://localhost:8080/callback`

## Step 2 — Get a refresh token

```bash
# Build authorization URL (replace CLIENT_ID)
open "https://accounts.zoho.in/oauth/v2/auth?scope=ZohoPeople.attendance.CREATE&client_id=CLIENT_ID&response_type=code&redirect_uri=http://localhost:8080/callback&access_type=offline"
```

After authorizing, you get a `code=...` in the redirect URL. Exchange it:

```bash
curl -X POST https://accounts.zoho.in/oauth/v2/token \
  -d "grant_type=authorization_code&client_id=CLIENT_ID&client_secret=CLIENT_SECRET&redirect_uri=http://localhost:8080/callback&code=CODE"
```

Save the `refresh_token` from the response. This token is long-lived.

## Step 3 — Run the sync

```bash
export ZKTECO_IP=192.168.1.201
export ZOHO_CLIENT_ID=your-client-id
export ZOHO_CLIENT_SECRET=your-client-secret
export ZOHO_REFRESH_TOKEN=your-refresh-token

python3 scripts/integrations/zoho_people_sync.py --days 1
```

## Zoho employee ID mapping

Zoho People uses a string `employeeId`. The sync script sends the ZKTeco `user_id` as-is. You may need to adjust this mapping if your Zoho employee IDs differ from the device enrollment IDs.
