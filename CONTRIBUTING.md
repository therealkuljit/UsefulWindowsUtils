# Contributing

Thanks for helping improve UsefulWindowsUtils Python.

## Development Rules

- Keep the app dependency-light.
- Prefer Python standard library and Tkinter.
- Do not hardcode local machine paths.
- Do not commit API keys, local settings, logs, generated reports, or malware samples.
- Keep dangerous actions behind clear UI controls and logs.
- Do not add code that connects directly to collected C2 indicators.

## Checks

Run before opening a pull request:

```powershell
python -m py_compile app.py
python app.py --self-test
```

## Documentation

Update README and relevant docs when changing:

- App catalog behavior.
- Tweaks.
- Feature actions.
- Threat-intelligence collection/enrichment.
- Export formats.
- Security or privacy behavior.

