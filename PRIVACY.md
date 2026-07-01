# Privacy

UsefulWindowsUtils stores settings and API keys locally in JSON files.

## Local Data

The app may create or use:

- `settings.json`
- `api_keys.json`
- `outputs/`
- exported logs
- exported CSV/XLSX/TXT reports

These files can contain hostnames, file paths, hashes, IP addresses, domains, API responses, and operational logs. Do not publish them without review.

## Third-Party Services

When you use VirusTotal or other configured threat-intelligence APIs, submitted values/files and returned metadata are handled by those providers under their own terms and privacy policies.

Do not submit confidential, personal, customer, proprietary, or regulated data unless you are authorized to do so.

## Network Behavior

C2 enrichment should query provider APIs only. The app must not directly connect to collected C2 IPs, domains, or URLs.
