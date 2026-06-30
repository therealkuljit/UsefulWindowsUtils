# Security Policy

## Supported Versions

This repository currently tracks the latest source version only.

## Reporting Security Issues

Do not open a public issue for exploitable security problems.

Report privately to the maintainer with:

- A clear summary.
- Affected file/function.
- Reproduction steps.
- Potential impact.
- Any suggested fix.

## Threat-Intelligence Safety

The app must not directly connect to collected C2 indicators or user-submitted suspicious infrastructure. Lookups should go through provider APIs such as VirusTotal and configured threat-intelligence sources.

## Secret Handling

API keys are stored locally in ignored JSON files:

- `api_keys.json`
- `settings.json`

Do not commit real API keys, generated logs, or investigation outputs.

## Malware Handling

If using file upload or malware-analysis workflows:

- Work inside an isolated lab.
- Do not execute unknown samples.
- Do not upload files you are not allowed to share with third-party services.
- Follow organization policy and applicable law.

