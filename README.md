# UsefulWindowsUtils

UsefulWindowsUtils is a comprehensive Windows utility application that combines software installation, system tuning, optional feature management, security triage, threat intelligence querying, PATH environment variable management, ISO patching, and file organization into a single, intuitive desktop user interface.

Current version: **1.0.1**

## 🚀 Key Features

### 📦 App Store (Package Manager UI)
- **Bundled Catalog:** Includes **265 app entries** across **21 categories**, sourced from `config/applications.json` plus built-in additions.
- **Multi-Source Installation:** Seamlessly install or upgrade selected Windows applications using integrated **Winget** and **Chocolatey** package-manager backends.
- **Package Manager Bootstrap:** Install or repair Winget and Chocolatey directly from the App Store toolbar.
- **Intelligent Search:** Query Winget and Chocolatey directly by application name or package ID to locate and install the best match.
- **Visual Indicators:** Open-source applications are highlighted in green for clear licensing visibility.
- **Convenience Controls:** Includes "Select All", "Clear Selection", package-manager bootstrap, and a live compilation log.
- **Portable App Support:** Displays download and extraction progress indicators for portable ZIP-based utilities.
- **Supported Categories:** Browsers, Communications, Customization, Development, Downloads, Games, Microsoft Tools, Multimedia Tools, Pro Tools, Productivity, Security, SOC & Detection, Malware Analysis, AI & Design, AI Tools, Business & Finance, Business & Productivity, Creative Tools, IT & DevOps, Selfhosted Tools, and Utilities.

### 💻 Installed Apps Manager
- **Registry Inventory:** Scans and lists all installed desktop applications extracted from Windows uninstall registry keys.
- **Auto-Loading Inventory:** Installed apps load automatically on startup; use `Refresh` to rescan.
- **Multi-Select Uninstall:** Select installed apps with the tick column or by clicking an app row, then uninstall multiple apps in one action.
- **Windows Debloater:** Bundles **140 removable app entries**, Win11Debloat-style app removal, and ChrisTitusTech app-removal actions under the Installed tab.
- **Package Management:** Perform targeted upgrades, bulk upgrades (`Upgrade All`), or trigger uninstalls utilizing Winget.
- **Smart Elevation Bypass:** Automatically retries user-scope Winget uninstalls without elevation if administrative mode blocks software removal.
- **Live Output:** Offers full real-time console logging for all execution blocks.

### 🔧 Windows Tweaks & Optimizations
- **System Tuning:** Safely applies registry modifications, service adjustments, and specialized PowerShell performance configurations defined in `config/tweaks.json`.
- **Preset Tiers:** Offers standard preset recommendations via `config/presets.json`:
  - `Minimal` — Essential changes with lowest risk profile.
  - `Standard` — Balanced optimizations for power users.
- **Risk Mitigation:** Visually flags high-risk system tweaks in red and forces optional system restore point creation prior to application.
- **Preference Toggles:** Fully supports interactive toggle switches for localized UI and system behavioral options.
- **Start Menu Cleanup:** Includes a bundled blank Windows 11 `start2.bin` layout to clear pinned Start menu apps after backing up the current layout.

### 🛡️ Windows Features & System Fixes
Allows direct management and troubleshooting of native operating system components via `config/feature.json`:
- **Core Components:** Toggle features like `.NET Framework`, `Hyper-V`, `Windows Sandbox`, `Windows Subsystem for Linux (WSL)`, `Network File System (NFS)`, and legacy media components.
- **System Automation:** Deploy or remove personalized PowerShell profiles.
- **System Repairs:** Execute a native system corruption scan (`SFC` / `DISM`), reset network stacks, or clear/reset a broken Windows Update configuration.
- **Quick Links:** Quick access to legacy Windows control panels.

### 🔒 Security Analysis & Triage
- **Subsections:** Security groups System, VirusTotal, and C2 Collector workflows in one tab with consistent rounded section controls.
- **Signature Updates:** Trigger manual definition updates for Microsoft Defender Antivirus.
- **Malware Scanning:** Run quick or comprehensive full system scans via command line.
- **Cryptographic Hashing:** Instantly compute the SHA256 hash of any file, or generate a full cryptographic folder manifest exported directly to CSV.
- **System Visibility:** Export active process inventories and examine established TCP network connections.

### 🔍 VirusTotal Integration
- **Multi-IOC Lookup:** Query cryptographic hashes, public IP addresses, domain names, and URLs through the official VirusTotal API.
- **File Submission:** Directly upload suspicious files to VirusTotal with inline file selection monitoring.
- **Analysis Polling:** Automatically monitors processing state and routes users to a rich local analysis page upon completion.
- **Deep Telemetry Reports:** Renders comprehensive details including alternate file names, type metadata, ingestion dates, global engine detections, precise threat labels/families, YARA/IDS/Sigma matches, detailed execution behavior, and structural entity relationships.

### 🛣️ PATH Manager
- **Environment Editing:** View existing User/System PATH entries, enable or disable entries with checkboxes, and append frequently used tool paths.
- **Custom Mapping:** Browse and select any local folder to map to the environment path variable.
- **Safety Warnings:** Dispatches desktop instructions alerting you to restart active terminal windows or applications to inherit changes.

### 💿 ISO Toolset
- **Windows Deployment:** Modify custom or official Windows installation images.
- **Edition Unlocking:** Write and inject `ei.cfg` configurations to open hidden setup channels and target edition menus.
- **Image Handling:** Dynamically mount or extract ISO structures, and patch/compile clean ISO images back together when `oscdimg.exe` is present.

### 📂 File Mover & Organizer
- **Batch Processing:** Relocate bulk groupings of files using fine-grained filtering by name string, file extension, or matching both.
- **Advanced Logic:** Supports partial string matches, explicit case sensitivity, target file overwriting, and a non-destructive `Dry-Run Mode` to safely preview file operations.
- **External Lists:** Capable of reading explicit target lists from standard text files.

### 📊 C2 Threat Intelligence
- **Indicator Harvesting:** Gathers known malicious IP or file hash indicators from threat intelligence platforms (ThreatFox, URLhaus, MalwareBazaar, AlienVault OTX, Pulsedive, or Hybrid Analysis).
- **Sanitization Filters:** Enforces stringent parsing constraints (e.g., separating public IPv4 indicators from structural hash syntax).
- **Enrichment Engine:** Automatically pairs incoming results with the VirusTotal API to pull structural risk categorization metadata.
- **Visible Logs:** Keeps C2 collection logs visible below the results table with compact top controls.
- **Reporting System:** Compiles flat-file records (`c2_intelligence_YYYYMMDD_HHMM.txt`) alongside styled Excel analytical spreadsheets (`c2_intelligence_YYYYMMDD_HHMM.xlsx`) complete with risk coloring, fixed layouts, and hyperlinked references.

### ⚙️ Settings & Customization
- **Themes:** Pick from `Light`, `Dark`, `AMOLED`, or `Cyberpunk`.
- **Modern UI:** Uses rounded theme-aware buttons, tick boxes, radio controls, toggles, scrollbars, search fields, logs, and progress bars.
- **Accessibility:** Scale interfaces with custom font metrics and improved text fitting for longer labels.
- **Localization:** Multi-language interface translations update immediately where supported.
- **API Store:** Secure, persistent fields to enter and manage threat intel and VirusTotal service tokens.

---

## Version 1.0.1

- Shortened app branding to `UsefulWindowsUtils` across the app and docs.
- Added modern theme-aware canvas controls for buttons, tick boxes, radio buttons, toggles, progress bars, scrollbars, and search fields.
- Added multi-select uninstall in Installed Apps.
- Added fixed Uninstaller/Debloater section controls under Installed.
- Improved C2 Collector layout so logs stay visible.
- Improved live language switching for navigation and primary app actions.
- Removed obsolete runtime image-control assets and the old bundled font.

---

## 📋 System Requirements

- **Operating System:** Windows 10 or Windows 11.
- **Runtime Environment:** Python 3.x with `Tkinter` installed.
- **Package Managers (Optional):** `winget` and/or `chocolatey` command-line interfaces for app installation modules.
- **Privileges:** Administrator/Elevated privileges are strictly required to adjust system services, modify registry entries, handle system PATHs, mount ISO files, or toggle core Windows Features.

---

## 🛠️ Usage

See **First-Time Setup From GitHub** above for download and launch steps. Run from an Administrator PowerShell session when using system-level tools.

## First-Time Setup From GitHub

1. Install **Python 3** from [python.org](https://www.python.org/downloads/windows/) or the Microsoft Store.
2. Download the project:
   - Git users:
     ```powershell
     git clone https://github.com/<your-username>/UsefulWindowsUtils.git
     cd UsefulWindowsUtils
     ```
   - Non-Git users: open the GitHub repo, click **Code > Download ZIP**, extract it, then open PowerShell in the extracted folder.
3. Start the app:
   ```powershell
   python app.py
   ```
4. For system tweaks, debloating, PATH changes, Windows Features, Defender actions, ISO work, or app uninstall operations, run PowerShell **as Administrator** before launching:
   ```powershell
   cd path\to\UsefulWindowsUtils
   python app.py
   ```
5. In the App Store tab, use **Install Winget/Choco** if the machine does not already have Winget or Chocolatey ready.

No `pip install` step is required for the core desktop app.

---

## Project Highlights

- **265 bundled app entries** across **21 major categories**.
- **140 debloater entries** for removable Windows inbox/provisioned apps.
- **Major app categories:** AI & Design, AI Tools, Browsers, Business & Finance, Business & Productivity, Communications, Creative Tools, Customization, Development, Downloads, Games, IT & DevOps, Malware Analysis, Microsoft Tools, Multimedia Tools, Pro Tools, Productivity, SOC & Detection, Security, Selfhosted Tools, and Utilities.
- **Security tools:** Defender panel, VirusTotal lookups/uploads, C2 IP/hash intelligence collection, C2 report export, process export, TCP connection review, SHA256 hashing, and folder hash manifests.
- **System cleanup tools:** Windows debloater, batch app uninstaller, Windows tweaks, Windows Features/fixes, PATH manager, ISO toolset, and mass file mover.

---

The application is intentionally designed to be dependency-light, relying on the Python standard library, Tkinter, native Windows tools, package-manager CLIs, and configured threat-intelligence APIs.

---

## ⚠️ Important Safety Notice

This utility is a powerful system administration tool capable of modifying system settings, registry keys, Windows services, installed software, Windows optional features, system PATH entries, and ISO contents.

- **Environment:** Run this tool only on systems you own or have explicit administrative authorization to manage.
- **Safety Best Practices:** Always create a system restore point and comprehensive backups before applying system tweaks or performance optimizations.
- **Liability:** This software is provided "as is" without warranty of any kind. The authors and contributors are not responsible for any data loss, system downtime, broken installations, unexpected API credit consumption, security exposure, or policy violations.
- **Defensive Research Only:** Threat intelligence and VirusTotal integration features are built strictly for defensive research, triage, and security analysis. The application queries provider APIs securely and never establishes direct connections to suspicious or malicious infrastructure.

For more information, please see `DISCLAIMER.md`, `PRIVACY.md`, `SECURITY.md`, and `docs/COMPLIANCE.md`.

---
