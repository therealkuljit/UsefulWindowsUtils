# UsefulWindowsUtils Python

UsefulWindowsUtils Python is a comprehensive Windows utility application that combines software installation, system tuning, optional feature management, security triage, threat intelligence querying, PATH environment variable management, ISO patching, and file organization into a single, intuitive desktop user interface. 

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

## 🚀 Key Features

### 📦 App Store (Package Manager UI)
- **Multi-Source Installation:** Seamlessly install or upgrade selected Windows applications using integrated **Winget** and **Chocolatey** package-manager backends based on `config/applications.json`.
- **Intelligent Search:** Query Winget and Chocolatey directly by application name or package ID to locate and install the best match.
- **Visual Indicators:** Open-source applications are highlighted in green for clear licensing visibility.
- **Convenience Controls:** Includes preset recommendations, "Select All", "Clear Selection", and a live compilation log.
- **Portable App Support:** Displays download and extraction progress indicators for portable ZIP-based utilities.
- **Supported Categories:** Browsers, Communications, Customization, Development, Downloads, Games, Microsoft Tools, Multimedia Tools, Pro Tools, Productivity, Security, SOC & Detection, Malware Analysis, AI & Design, AI Tools, Business & Finance, Business & Productivity, Creative Tools, IT & DevOps, Selfhosted Tools, and Utilities.

### 💻 Installed Apps Manager
- **Registry Inventory:** Scans and lists all installed desktop applications extracted from Windows uninstall registry keys.
- **Auto-Loading Inventory:** Installed apps load automatically on startup; use `Refresh` to rescan.
- **Debloater:** Bundles a Win11Debloat app catalog and ChrisTitusTech app-removal action under the Installed tab.
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
- **Subsections:** Security groups System, VirusTotal, and C2 Collector workflows in one tab.
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
- **Reporting System:** Compiles flat-file records (`c2_intelligence_YYYYMMDD_HHMM.txt`) alongside styled Excel analytical spreadsheets (`c2_intelligence_YYYYMMDD_HHMM.xlsx`) complete with risk coloring, fixed layouts, and hyperlinked references.

### ⚙️ Settings & Customization
- **Themes:** Pick from `Light`, `Dark`, `AMOLED`, or `Cyberpunk`.
- **Accessibility:** Scale interfaces with custom font metrics.
- **Localization:** Multi-language interface translations.
- **API Store:** Secure, persistent fields to enter and manage threat intel and VirusTotal service tokens.

---

## 📋 System Requirements

- **Operating System:** Windows 10 or Windows 11.
- **Runtime Environment:** Python 3.x with `Tkinter` installed.
- **Package Managers (Optional):** `winget` and/or `chocolatey` command-line interfaces for app installation modules.
- **Privileges:** Administrator/Elevated privileges are strictly required to adjust system services, modify registry entries, handle system PATHs, mount ISO files, or toggle core Windows Features.

---

## 🛠️ Usage

1. Open a PowerShell terminal as an Administrator.
2. Launch the utility main interface:
   ```powershell
   python app.py
