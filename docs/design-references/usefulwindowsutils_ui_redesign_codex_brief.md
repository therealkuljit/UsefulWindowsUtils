# UsefulWindowsUtils UI Redesign Brief for Codex

## Objective

Redesign the existing **UsefulWindowsUtils Python** desktop app so it looks modern, minimal, polished, and Windows 11-inspired while keeping the current application layout and functionality intact.

This is a **visual/UI system redesign only**. Do **not** rewrite the app architecture, do **not** change the navigation model, do **not** remove any existing features, and do **not** reorganize the user flow unless absolutely required for styling consistency.

The current app is a dependency-light Python/Tkinter Windows utility that combines app installation, installed-app management, system tuning, Windows feature management, security triage, VirusTotal/threat-intel workflows, PATH management, ISO patching, file organization, and settings/theme customization. Preserve all existing behavior.

The reference images supplied with this brief define the target visual direction:
1. Light theme design language board
2. Dark mode design language board
3. AMOLED mode design language board
4. Cyberpunk mode design language board
5. UsefulWindowsUtils logo reference

Use those images as the visual source of truth.

---

## Non-Negotiable Constraints

### 1. Preserve existing layout

The app layout must remain the same.

Do not:
- Move major tabs to a different structure.
- Convert the app into a sidebar-first layout if it is currently tab-first.
- Reorder major feature areas.
- Rename existing functional sections.
- Remove existing controls.
- Hide advanced functionality behind extra screens.
- Change workflows for install, uninstall, scan, lookup, export, PATH editing, ISO patching, or file moving.

You may:
- Improve spacing inside existing sections.
- Add visual grouping through cards/panels.
- Improve button hierarchy.
- Replace outdated Tkinter-looking widgets with themed equivalents.
- Add better section headers.
- Add subtle helper text where it improves clarity.
- Improve status/error/progress presentation.
- Add icons only if they do not disturb the existing layout.

### 2. Keep the app dependency-light

The existing project is intentionally based around Python standard library, Tkinter, native Windows tools, package manager CLIs, and configured APIs. Avoid adding heavy dependencies.

Preferred implementation:
- `tkinter`
- `ttk`
- `tkinter.font`
- `tkinter.Canvas` for custom controls
- Existing project modules
- Existing config files
- Standard library only

Avoid unless already present:
- PyQt
- PySide
- Electron
- Kivy
- DearPyGui
- CustomTkinter
- Large icon/font frameworks
- Webview-based full rewrite

If an external dependency is truly necessary, explain the tradeoff in code comments and keep it optional.

### 3. No business logic rewrite

Do not rewrite system-level logic. The app performs sensitive administrative tasks including registry changes, service changes, optional feature toggles, Defender operations, package manager execution, PATH edits, ISO handling, file operations, and threat-intelligence API calls.

Only refactor UI code when needed to apply:
- Theme tokens
- Widget wrappers
- Shared styles
- Consistent layout helpers
- Component state styling
- Better status/progress surfaces

### 4. Safety-sensitive actions must be visually obvious

Any action that can modify the system, registry, services, PATH, installed apps, Windows features, ISO contents, files, or security settings must be visually classified.

Use:
- Primary button for safe/expected forward actions.
- Destructive red button for delete, uninstall, remove, reset, clear, wipe, disable risky services, or overwrite operations.
- Warning badge or panel for high-risk tweaks.
- Confirmation modal for irreversible or high-risk actions.
- Disabled state while operations are running.
- Clear progress/status feedback during long-running commands.

---

## Visual Direction

The UI should feel like a serious Windows 11-era utility tool:

- Minimal
- Clean
- Productive
- Calm
- Trustworthy
- Modern
- Slightly technical
- Not gamer-ish except the optional Cyberpunk theme
- Not cluttered
- Not glossy
- Not skeuomorphic
- Not loud by default

Use a Fluent-inspired design language:
- Rounded corners
- Soft surfaces
- Thin borders
- Subtle elevation
- High contrast text
- Consistent spacing
- Clear control states
- Clean typography
- Minimal iconography
- Polished focus/hover states

The app should feel like it belongs on Windows 11 without copying Microsoft branding directly.

---

## Brand Identity

### App name

Use:

```text
UsefulWindowsUtils
```

Avoid showing `Python` in the main UI branding unless it already appears in an About screen or technical footer. The latest logo direction removed the `Python` subtitle.

### Logo usage

Use the supplied logo reference.

Logo characteristics:
- Four-pane rounded-square icon
- Blue, teal, violet, and cobalt/royal-blue panes
- White utility glyphs:
  - gear
  - shield
  - terminal prompt
  - folder
- Wordmark:
  - `Useful` in dark navy or theme foreground
  - `Windows` in bright blue
  - `Utils` in dark navy or theme foreground

In the app:
- Header logo should be compact.
- Use icon-only version for window icon if available.
- Use wordmark in splash/about/header only, not repeated on every small panel.
- Keep logo away from cluttered control zones.

---

## Theme System

Implement a centralized theme system instead of hardcoding colors across the app.

Create or refactor into something equivalent to:

```text
ui/
  theme.py
  styles.py
  widgets.py
  icons.py
  layout.py
```

If the project already has a UI/theme structure, extend it instead of creating duplicate systems.

### Theme manager requirements

Implement a `ThemeManager` or equivalent that exposes:

```python
theme.get("color.background")
theme.get("color.surface")
theme.get("color.surface_elevated")
theme.get("color.text")
theme.get("color.text_muted")
theme.get("color.border")
theme.get("color.primary")
theme.get("color.danger")
theme.get("radius.md")
theme.get("spacing.3")
```

Required behavior:
- Load the active theme from existing settings if available.
- Support runtime switching between Light, Dark, AMOLED, and Cyberpunk.
- Apply theme to root window, frames, ttk styles, custom canvas widgets, Treeviews, menus, dialogs, scrollbars, and log panels.
- Keep font scaling/accessibility support intact.
- Do not require app restart for basic theme switching if current architecture allows live refresh.

---

## Color Tokens

Use these as the implementation baseline. Slight adjustments are allowed only if needed for readability.

### Shared semantic colors

```python
SEMANTIC = {
    "primary": "#0A84FF",
    "teal": "#00B8A9",
    "violet": "#7C3AED",
    "success": "#10B981",
    "warning": "#F59E0B",
    "danger": "#EF4444",
    "info": "#38BDF8",
}
```

---

### Light theme

Use this for the default clean Windows 11-inspired mode.

```python
LIGHT = {
    "background": "#F8FAFC",
    "surface": "#FFFFFF",
    "surface_subtle": "#F1F5F9",
    "surface_elevated": "#FFFFFF",
    "surface_pressed": "#EAF2FF",
    "text": "#0F172A",
    "text_muted": "#64748B",
    "text_subtle": "#94A3B8",
    "border": "#E2E8F0",
    "border_strong": "#CBD5E1",
    "primary": "#0A84FF",
    "primary_hover": "#0072E5",
    "primary_pressed": "#005FBF",
    "primary_soft": "#E7F2FF",
    "teal": "#00B8A9",
    "violet": "#7C3AED",
    "success": "#10B981",
    "success_soft": "#E8F8F2",
    "warning": "#F59E0B",
    "warning_soft": "#FFF7E6",
    "danger": "#EF4444",
    "danger_soft": "#FEECEC",
    "disabled_bg": "#F1F5F9",
    "disabled_text": "#A3AAB8",
    "focus_ring": "#0A84FF",
    "shadow": "#0F172A22",
}
```

---

### Dark theme

Use this for a polished, practical dark mode. This is not pure black.

```python
DARK = {
    "background": "#0F141C",
    "surface": "#111827",
    "surface_subtle": "#162032",
    "surface_elevated": "#1B2637",
    "surface_pressed": "#1E3350",
    "text": "#E2E8F0",
    "text_muted": "#94A3B8",
    "text_subtle": "#64748B",
    "border": "#2E3A4C",
    "border_strong": "#3B4A60",
    "primary": "#0D6EFD",
    "primary_hover": "#2384FF",
    "primary_pressed": "#0A58CA",
    "primary_soft": "#102A4D",
    "teal": "#00B8A9",
    "violet": "#7C3AED",
    "success": "#10B981",
    "success_soft": "#0B2A22",
    "warning": "#F59E0B",
    "warning_soft": "#2D2108",
    "danger": "#EF4444",
    "danger_soft": "#2A1010",
    "disabled_bg": "#1A202C",
    "disabled_text": "#64748B",
    "focus_ring": "#0D6EFD",
    "shadow": "#00000066",
}
```

---

### AMOLED theme

Use this for OLED displays. It should be true-black, sharper, and more minimal than dark mode.

```python
AMOLED = {
    "background": "#000000",
    "surface": "#050505",
    "surface_subtle": "#0A0A0A",
    "surface_elevated": "#101010",
    "surface_pressed": "#111A24",
    "text": "#F8FAFC",
    "text_muted": "#A1A1AA",
    "text_subtle": "#71717A",
    "border": "#242424",
    "border_strong": "#383838",
    "primary": "#0A84FF",
    "primary_hover": "#2994FF",
    "primary_pressed": "#006AD6",
    "primary_soft": "#061A33",
    "teal": "#00D1C1",
    "violet": "#8B5CF6",
    "success": "#22C55E",
    "success_soft": "#061A10",
    "warning": "#FBBF24",
    "warning_soft": "#1C1404",
    "danger": "#F43F5E",
    "danger_soft": "#21060B",
    "disabled_bg": "#111111",
    "disabled_text": "#525252",
    "focus_ring": "#0A84FF",
    "shadow": "#000000",
}
```

---

### Cyberpunk theme

Use this as a stylized optional mode. It can glow, but it must remain usable. Do not make every element neon. The theme should feel premium, not childish.

```python
CYBERPUNK = {
    "background": "#050816",
    "surface": "#0B1024",
    "surface_subtle": "#101735",
    "surface_elevated": "#111936",
    "surface_pressed": "#172554",
    "text": "#E2F0FF",
    "text_muted": "#9CA3D6",
    "text_subtle": "#64748B",
    "border": "#22304A",
    "border_strong": "#334155",
    "primary": "#00C8FF",
    "primary_hover": "#33D6FF",
    "primary_pressed": "#0099CC",
    "primary_soft": "#06283A",
    "teal": "#00E8D1",
    "violet": "#9D4EDD",
    "magenta": "#FF2BD6",
    "success": "#00E8A2",
    "success_soft": "#04251C",
    "warning": "#FFB020",
    "warning_soft": "#2A1700",
    "danger": "#FF3B5C",
    "danger_soft": "#2A0610",
    "disabled_bg": "#111827",
    "disabled_text": "#4B5563",
    "focus_ring": "#00C8FF",
    "glow_cyan": "#00C8FF88",
    "glow_magenta": "#FF2BD688",
    "shadow": "#00000099",
}
```

Cyberpunk usage rules:
- Primary actions can glow subtly.
- Focus rings can glow.
- Panel borders can use faint cyan/purple.
- Avoid large glowing backgrounds.
- Keep text white or soft blue-gray for readability.
- Destructive actions stay red, not magenta.

---

## Typography

Use Windows-native typography.

Preferred:
```text
Segoe UI Variable
```

Fallbacks:
```text
Segoe UI
Arial
sans-serif
```

### Type scale

```python
TYPOGRAPHY = {
    "display":  {"size": 28, "line": 36, "weight": "semibold"},
    "heading1": {"size": 20, "line": 28, "weight": "semibold"},
    "heading2": {"size": 16, "line": 24, "weight": "semibold"},
    "body":     {"size": 12, "line": 16, "weight": "regular"},
    "caption":  {"size": 11, "line": 14, "weight": "regular"},
    "small":    {"size": 10, "line": 12, "weight": "regular"},
}
```

### Usage

- App title: display or heading1.
- Section titles: heading2.
- Control labels: caption or body semibold.
- Button text: body semibold.
- Table/list text: body.
- Helper text: caption.
- Warning/legal/helper notices: caption/body depending on importance.
- Log output: monospace fallback such as `Consolas`, size 11 or 12.

Do not use oversized fonts everywhere. The app is a utility app, so density matters.

---

## Spacing System

Use a consistent 4px base grid.

```python
SPACING = {
    "0": 0,
    "1": 4,
    "2": 8,
    "3": 12,
    "4": 16,
    "5": 24,
    "6": 32,
    "7": 40,
    "8": 48,
    "9": 64,
}
```

### Layout rules

- Outer window padding: 16-24px.
- Section/card padding: 16px.
- Dense row padding: 8-12px.
- Button horizontal padding: 14-18px.
- Gap between related controls: 8px.
- Gap between unrelated groups: 16-24px.
- Keep existing panel ordering and tab order.
- Add whitespace only where it improves readability without bloating the app.

---

## Radius System

```python
RADIUS = {
    "xs": 4,
    "sm": 8,
    "md": 12,
    "lg": 16,
    "xl": 24,
    "pill": 999,
}
```

### Usage

- Small inputs/buttons: 8px.
- Cards/panels: 12-16px.
- Modals: 16px.
- Pills/chips: 999px.
- Icon buttons: 8-12px.
- Segmented controls: 999px outer radius.

Tkinter does not natively support rounded corners for all widgets. Use the best practical approximation:
- ttk styles where possible.
- Canvas-backed custom widgets where needed.
- Avoid brittle hacks that break resizing or accessibility.

---

## Border and Elevation System

### Borders

Use thin 1px borders.

```python
BORDERS = {
    "default": "1px solid border",
    "focus": "1px solid primary",
    "divider": "1px solid border",
    "subtle": "1px solid surface_subtle",
}
```

### Elevation

Tkinter shadow support is limited. Use:
- Slightly different surface colors.
- Thin borders.
- Canvas shadow approximations only where stable.
- Do not overdo shadows.

Light theme:
- Cards can use subtle shadows and borders.

Dark/AMOLED:
- Prefer border contrast over shadow.

Cyberpunk:
- Use glow only on focus, active controls, and selected navigation items.

---

## Component Specifications

### 1. Buttons

Create shared button styles.

Required variants:
- Primary
- Secondary
- Subtle/Ghost
- Destructive
- Icon
- Disabled

#### Primary button

Use for:
- Install
- Run scan
- Search
- Save
- Apply safe/default action
- Confirm positive action

Visual:
- Filled primary background.
- White text.
- Rounded 8px or 10px.
- Height 34-40px.
- Hover state slightly brighter.
- Pressed state slightly darker.
- Disabled state muted.

#### Secondary button

Use for:
- Cancel
- Browse
- Refresh
- Clear non-destructive filters
- Open folder
- View details

Visual:
- Surface background.
- Border.
- Text color.
- Hover surface_subtle.

#### Subtle/Ghost button

Use for:
- Settings
- Expand details
- Small helper actions
- Low-emphasis controls

Visual:
- Transparent or near-transparent background.
- Text color.
- Hover surface_subtle.

#### Destructive button

Use for:
- Delete
- Remove
- Uninstall
- Reset
- Clear system config
- Disable risky item
- Overwrite destination
- Remove PATH entry
- Trash/move file destructive operations

Visual:
- Filled danger for high-risk destructive action.
- Outlined danger for medium-risk destructive action.
- Always use confirmation modal for irreversible changes.

#### Icon button

Use for:
- Refresh
- More menu
- Close
- Browse
- Copy
- Open external link
- Delete row action

Visual:
- Square 32-36px.
- 16-18px icon.
- Rounded 8px.
- Hover surface_subtle.
- Active/focus uses primary outline.

---

### 2. Toggles / Switches

Use toggles for boolean preferences only.

Examples:
- Theme behavior options
- Enable/disable UI preferences
- Toggle localized options
- Optional safe settings

Do not use toggles for dangerous immediate system changes unless there is confirmation.

States:
- On: primary track, white knob.
- Off: muted track, surface knob.
- Disabled: disabled_bg, disabled_text.

Implementation:
- Prefer custom `Canvas` toggle widget.
- Support keyboard focus and click.
- Expose accessible state through variable binding.

---

### 3. Checkboxes and Radio Buttons

Use checkboxes for:
- Selecting apps to install
- Selecting tweaks
- Selecting files
- PATH entries
- Optional features lists
- Bulk actions

Use radio buttons for:
- Mutually exclusive modes
- Scan type: quick/full/custom
- Package manager preference where mutually exclusive
- Preset choice

States:
- Checked
- Unchecked
- Indeterminate
- Disabled
- Focused

Important:
- High-risk tweak checkboxes should show a red/warning label, warning badge, or warning icon.
- Disabled options should have helper text explaining why disabled where practical.

---

### 4. Input Fields

Create consistent input styles.

Required states:
- Default
- Focused
- Filled
- Error
- Disabled

Types:
- Standard text input
- Search field
- Password/API token field
- Path field with browse button
- Numeric field if applicable
- Multi-line text/log field

Visual:
- Height 34-38px.
- Rounded border.
- Surface background.
- Focus border primary.
- Error border danger.
- Placeholder text muted.
- Clear icon for search fields.

Security/API token fields:
- Mask tokens by default.
- Add eye reveal icon.
- Add copy button only if already safe and intentional.
- Never print tokens into logs.

---

### 5. Dropdown / Select Menus

Use for:
- Theme selection
- Language selection
- Category filters
- Package manager choice
- Presets
- Scan/report options

Visual:
- Surface background.
- 1px border.
- Chevron icon.
- Selected item highlighted with primary_soft.
- Hover row state.

Tkinter implementation:
- Style `ttk.Combobox`.
- If default dropdown styling cannot be fully themed, at minimum style the field and selected state consistently.

---

### 6. Scrollbars

Make scrollbars modern and minimal.

Visual:
- Thin track.
- Rounded thumb if practical.
- Thumb primary or muted depending context.
- Hover state slightly brighter.

Usage:
- Logs
- App lists
- Tables
- Long tweak lists
- Report panes
- File lists

Avoid giant default OS-looking scrollbars if possible.

---

### 7. Sliders and Progress Bars

Use progress bars for:
- Installation progress
- Download/extract progress
- VirusTotal analysis polling
- C2 collection progress
- File moving progress
- ISO extraction/patching
- System scans when measurable

Styles:
- Determinate progress: primary fill.
- Indeterminate progress: animated or striped primary fill.
- Warning progress if operation has caution state.
- Error state if operation fails.

Progress rules:
- Always pair progress with text status.
- Disable conflicting controls while running.
- Do not freeze UI during long operations.
- Preserve existing threading/subprocess behavior.

---

### 8. Tabs / Segmented Controls

Preserve the existing app navigation.

If current app uses tabs:
- Restyle them.
- Do not replace with a new navigation system.
- Active tab gets primary underline or filled subtle background.
- Inactive tabs stay low emphasis.
- Hover state should be visible.

Use segmented controls inside a tab for filters:
- App category filters
- Security subsections
- Installed app filters
- Log/report views
- PATH User/System selection
- VirusTotal IOC type selection

---

### 9. Cards / Panels

Use cards to group content inside existing sections.

Card types:
- Elevated card
- Outlined card
- Subtle panel

Use cards for:
- Feature groups
- Preset groups
- Security workflow groups
- Summary metrics
- Settings blocks
- API configuration blocks
- Risk warnings

Visual:
- Surface background.
- 1px border.
- 12-16px radius.
- 12-16px padding.
- Subtle title and helper text.
- Icons optional and minimal.

Do not over-card everything. Too many boxes create clutter.

---

### 10. Tables / Lists / Treeviews

Important for:
- Installed apps list
- App Store packages
- PATH entries
- Process inventory
- Network connections
- VirusTotal detections
- C2 intelligence results
- File mover results
- Logs/export rows

Style requirements:
- Clean header row.
- Soft row dividers.
- Hover state.
- Selected row state using primary_soft or surface_pressed.
- Checkbox support if currently present.
- Status dots/badges for Enabled, Running, Disabled, Failed, Pending, Complete.
- Right-aligned size/date columns where appropriate.
- Keep columns readable and resizable where current app supports it.

Tkinter:
- Style `ttk.Treeview`.
- Set row height around 30-36px.
- Improve heading style.
- Improve selected row colors per theme.

---

### 11. Pills / Chips / Status Badges

Use badges for metadata and state.

Required badge variants:
- Primary
- Success
- Info
- Warning
- Danger
- Neutral

Examples:
- Open Source
- Installed
- Update Available
- Running
- Disabled
- High Risk
- Admin Required
- API Required
- Portable
- Winget
- Chocolatey
- VirusTotal
- ThreatFox
- URLhaus
- OTX

Visual:
- Pill radius.
- Small text.
- Soft tinted background.
- Border optional.
- High-risk badges should be warning/danger.

---

### 12. Tooltip / Toast

Use tooltips for:
- Explaining risky settings
- Explaining package manager icons
- Explaining API token fields
- Explaining disabled controls
- Explaining high-risk tweaks

Use toast notifications for:
- Install started
- Install complete
- Export saved
- Token saved
- Scan started/completed
- Error summary
- Clipboard copy
- Restore point created

Toast behavior:
- Non-blocking.
- Auto-dismiss after a few seconds unless error/warning.
- Error toasts should remain longer or require dismissal.
- Do not spam toasts for every log line.

---

### 13. Modal / Dialog

Use modal dialogs for:
- Confirming destructive actions
- Confirming high-risk tweaks
- Confirming bulk uninstall
- Confirming PATH modifications
- Confirming reset Windows Update
- Confirming ISO overwrite
- Confirming file overwrite
- Showing important API/security warnings

Dialog design:
- Rounded card.
- Clear title.
- Concise body text.
- Primary/secondary/destructive action buttons.
- Cancel always available.
- Dangerous action should not be the default focused button unless intentional.

---

### 14. Sidebar / Navigation

Only use sidebar styling if the current app already has a sidebar or a left navigation area.

If the app currently uses top tabs or notebook tabs:
- Keep that structure.
- Do not force a sidebar.

If there is an existing sidebar:
- Use selected background.
- Use small icons.
- Use primary left indicator or filled selected state.
- Keep labels readable.
- Avoid overly large navigation.

---

### 15. Color Tokens Panel / Settings Theme Selector

In the app’s Settings tab:
- Keep existing Light, Dark, AMOLED, Cyberpunk theme choices.
- Redesign the theme selector using cards or segmented controls.
- Show a small color preview for each theme.
- Make active theme clearly selected.
- Respect accessibility/font scale settings.

---

## Screen-by-Screen Redesign Guidance

### App Store / Package Manager UI

Preserve:
- Categories
- Search
- Multi-select app list
- Winget/Chocolatey behavior
- Open-source indicators
- Presets
- Select All / Clear Selection
- Live compilation log
- Portable download progress

Improve:
- Use segmented controls or pill filters for categories.
- Use modern search input with clear button.
- Use app rows/cards with name, package ID, source, status badges.
- Make Open Source badge green/success.
- Use primary button for Install/Upgrade.
- Use secondary buttons for Search, Refresh, Clear.
- Use progress bar and toast when operations begin/finish.
- Use log panel with monospace font and dark/surface styling.

### Installed Apps Manager

Preserve:
- Registry inventory scan
- Auto-load behavior
- Refresh
- Debloater actions
- Upgrade All
- Targeted upgrade/uninstall
- Winget retry behavior
- Live output

Improve:
- Use Treeview/table with modern row height.
- Add status badges for Installed, Update Available, Unknown.
- Destructive style for Uninstall/Remove.
- Warning panel for debloat actions.
- Confirmation modal for bulk remove/uninstall.
- Keep logs visually separate from app list.

### Windows Tweaks & Optimizations

Preserve:
- Existing tweak config loading
- Presets from config
- Restore point behavior
- High-risk tweak flagging
- Start menu cleanup

Improve:
- Group tweaks into cards or panels.
- Use badges: Minimal, Standard, High Risk, Admin Required.
- High-risk tweaks must use warning/danger visual treatment.
- Restore point prompt should be a clear modal or prominent panel.
- Toggle switches can represent preference-like tweaks, but risky system changes need explicit Apply button and confirmation.
- Keep current preset behavior.

### Windows Features & System Fixes

Preserve:
- Feature toggling
- .NET, Hyper-V, Sandbox, WSL, NFS, legacy media components
- PowerShell profile actions
- SFC/DISM
- Network reset
- Windows Update reset
- Quick links

Improve:
- Use list rows/cards for each feature.
- Use status badges: Enabled, Disabled, Requires Restart, Admin Required.
- Use primary for Enable/Apply.
- Use secondary for Open/Check.
- Use destructive/warning for Reset actions.
- Add confirmation modals for network reset and Windows Update reset.

### Security Analysis & Triage

Preserve:
- System, VirusTotal, C2 Collector subsections
- Defender updates
- Quick/full scans
- SHA256 hashing
- Folder manifest CSV export
- Process inventory export
- TCP connection inspection

Improve:
- Use segmented controls for System / VirusTotal / C2 Collector if currently nested.
- Use cards for scan actions.
- Use badges: Defensive Only, Admin Required, API Required.
- Use table/list styling for process/network results.
- Use progress and status text for Defender scans and exports.
- Keep security warnings visible but not visually overwhelming.

### VirusTotal Integration

Preserve:
- Multi-IOC lookup
- Hash/IP/domain/URL support
- File submission
- Polling
- Local analysis page
- Detection details
- YARA/IDS/Sigma/behavior/relationships

Improve:
- IOC input should use a large clean input area or grouped fields.
- IOC type selector should be segmented or dropdown.
- Results should use cards/tables with clear severity badges.
- Detection counts should be visually prominent.
- Dangerous/malicious detections use danger badges.
- Suspicious uses warning.
- Clean uses success.
- API token fields should be masked by default.
- Never reveal API tokens in UI logs.

### PATH Manager

Preserve:
- User/System PATH entries
- Enable/disable checkboxes
- Add folder mapping
- Restart terminal/app warning

Improve:
- Use a modern list/table with checkbox rows.
- Use badges for User PATH and System PATH.
- Use Browse button with icon.
- Use warning panel after changes: restart terminal/apps.
- Use confirmation for removing/disabling system PATH entries.
- Use toast for copied/added/saved path actions.

### ISO Toolset

Preserve:
- ISO mounting/extraction
- `ei.cfg` generation/injection
- Edition unlocking
- Patch/compile behavior
- oscdimg handling

Improve:
- Use step-based panels inside current layout if possible.
- Use file picker fields.
- Use status badge for oscdimg availability.
- Use progress bar for extraction/compile.
- Use warning/destructive treatment for overwrite operations.
- Confirmation modal before modifying or overwriting ISO output.

### File Mover & Organizer

Preserve:
- Bulk move logic
- Name/extension/both filtering
- Case sensitivity
- Overwrite option
- Dry-run mode
- External target lists

Improve:
- Make Dry-Run a visually clear safe mode badge/toggle.
- Overwrite must be warning/destructive.
- Use clean input fields for source/destination.
- Use chips for selected extensions/filters.
- Use preview table for matching files.
- Use progress and result summary toast.

### C2 Threat Intelligence

Preserve:
- ThreatFox, URLhaus, MalwareBazaar, AlienVault OTX, Pulsedive, Hybrid Analysis
- Public IPv4/hash parsing constraints
- VirusTotal enrichment
- TXT and XLSX report generation
- Risk coloring
- Hyperlinked references

Improve:
- Use source selection chips/cards.
- Use status badges for API source health.
- Use progress while harvesting/enriching.
- Use table with risk badges.
- Use export success toast.
- Use caution panel explaining defensive-only use.
- Keep links styled but safe.

### Settings & Customization

Preserve:
- Light, Dark, AMOLED, Cyberpunk themes
- Font/accessibility scaling
- Localization
- API store

Improve:
- Theme selection with preview cards.
- Font scale slider or dropdown.
- API token fields masked with reveal icon.
- Save buttons clearly separated.
- Settings grouped into cards:
  - Appearance
  - Accessibility
  - Localization
  - API Keys
  - Safety/Restore behavior
- Use success toast after settings save.

---

## Implementation Architecture

### Recommended file structure

If the repository does not already have this separation, create it carefully:

```text
ui/
  __init__.py
  theme.py        # theme tokens, active theme, persistence bridge
  styles.py       # ttk style configuration
  widgets.py      # custom/themed wrappers
  layout.py       # spacing helpers, card helpers, section header helpers
  dialogs.py      # confirm dialogs, toast manager, tooltip helpers
  icons.py        # lightweight icon helpers if needed
```

Do not break existing imports. If the app is currently single-file, apply this refactor incrementally.

---

## Theme Application Strategy

### Step 1: Identify current UI root

Find:
- Root Tk instance
- Main frames/tabs/notebooks
- Existing style initialization
- Settings persistence for selected theme
- Font scaling logic
- Current theme switching logic if present

### Step 2: Add central theme tokens

Implement the token dictionaries from this document.

Example structure:

```python
THEMES = {
    "Light": LIGHT,
    "Dark": DARK,
    "AMOLED": AMOLED,
    "Cyberpunk": CYBERPUNK,
}
```

### Step 3: Configure ttk styles

Style:
- `TFrame`
- `TLabel`
- `TButton`
- `Primary.TButton`
- `Secondary.TButton`
- `Subtle.TButton`
- `Danger.TButton`
- `TEntry`
- `TCombobox`
- `TCheckbutton`
- `TRadiobutton`
- `TNotebook`
- `TNotebook.Tab`
- `Treeview`
- `Treeview.Heading`
- `TProgressbar`
- `Vertical.TScrollbar`
- `Horizontal.TScrollbar`
- `TLabelframe`

Example concept:

```python
def configure_ttk_styles(root, theme):
    style = ttk.Style(root)

    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    c = theme.colors

    style.configure(".", font=theme.fonts["body"])
    style.configure("App.TFrame", background=c["background"])
    style.configure("Surface.TFrame", background=c["surface"])
    style.configure("Card.TFrame", background=c["surface_elevated"], relief="flat")
    style.configure("App.TLabel", background=c["background"], foreground=c["text"])
    style.configure("Muted.TLabel", background=c["background"], foreground=c["text_muted"])

    style.configure(
        "Primary.TButton",
        background=c["primary"],
        foreground="#FFFFFF",
        borderwidth=0,
        focusthickness=1,
        focuscolor=c["focus_ring"],
        padding=(14, 8),
    )

    style.map(
        "Primary.TButton",
        background=[
            ("active", c["primary_hover"]),
            ("pressed", c["primary_pressed"]),
            ("disabled", c["disabled_bg"]),
        ],
        foreground=[
            ("disabled", c["disabled_text"]),
        ],
    )
```

Adjust for actual Tkinter compatibility.

### Step 4: Replace local hardcoded styles

Search for:
- Hardcoded hex colors
- Direct `bg=`
- Direct `fg=`
- Hardcoded fonts
- Inline padding inconsistencies
- Repeated button styling

Replace with:
- Theme tokens
- Shared style names
- Layout helper constants
- Shared widget wrappers

### Step 5: Add custom widgets only where ttk is insufficient

Implement lightweight custom widgets for:
- Toggle switch
- Toast
- Tooltip
- Card frame with rounded approximation if stable
- Segmented control
- Status badge
- Icon button
- Password entry with reveal button
- Search entry with clear button

Keep them simple and maintainable.

---

## Widget Wrapper Requirements

### ThemedButton

Create a wrapper/helper that standardizes buttons.

```python
create_button(parent, text, variant="primary", icon=None, command=None, disabled=False)
```

Supported variants:
- primary
- secondary
- subtle
- danger
- danger_outline
- icon
- disabled

### Card

```python
Card(parent, title=None, subtitle=None, icon=None, variant="outlined")
```

Variants:
- outlined
- elevated
- subtle
- warning
- danger

### Badge

```python
Badge(parent, text, variant="neutral")
```

Variants:
- primary
- success
- info
- warning
- danger
- neutral

### SearchEntry

Features:
- Placeholder
- Search icon if available
- Clear button
- Focus state
- Bind to existing search variable/callback

### PasswordEntry

Features:
- Masked by default
- Reveal/hide button
- Copy only if existing behavior supports it
- Never log contents

### ToggleSwitch

Features:
- Bound to BooleanVar
- Keyboard accessible if practical
- Disabled state
- Theme-aware redraw

### ToastManager

Features:
- Show success/info/warning/error
- Auto-dismiss
- Close button
- Queue or replace behavior
- Does not block operations

### ConfirmDialog

Features:
- Title
- Message
- Severity: info/warning/danger
- Primary action label
- Cancel action label
- Optional checkbox if existing safety flow needs it
- Return boolean/action result

---

## Control State Rules

Every interactive component should define these states:

```text
default
hover
pressed
focused
disabled
selected
error
success
warning
```

### Focus

Focus must be visible, especially for keyboard navigation.

Light/Dark/AMOLED:
- 1px or 2px primary border.

Cyberpunk:
- Primary border plus subtle cyan glow.

### Disabled

Disabled controls should:
- Reduce contrast.
- Keep layout stable.
- Avoid disappearing.
- Use disabled text and disabled background tokens.
- Avoid looking clickable.

### Error

Error controls should:
- Use danger border.
- Show concise error text.
- Avoid only relying on color if possible.
- Use warning/error icon if already available or simple text fallback.

---

## Icon Direction

Use minimal line icons if icons already exist or can be drawn simply.

Recommended icon concepts:
- Gear: settings/tweaks
- Shield: security
- Terminal prompt: command/system tools
- Folder: file operations
- Download: install
- Refresh: reload/scan
- Trash: remove/uninstall/delete
- Alert triangle: warning
- Check circle: success
- Info circle: info
- External link: open link
- Eye: reveal password/token
- Search: search

Constraints:
- Keep icons 16-20px.
- Use theme foreground or muted colors.
- Do not use colorful icons everywhere.
- Color only high-priority states and badges.

If no icon system exists, use text labels first. Do not block redesign on icons.

---

## Logs and Console Output

Logs are central to this app. Do not hide them.

Style logs as:
- Monospace font: `Consolas`
- Font size: 11 or 12
- Surface/subtle background
- Rounded/outlined panel if practical
- Muted timestamps
- Error lines in danger
- Warning lines in warning
- Success lines in success
- Running/current action in primary/info

Do not change existing log content unless necessary for readability.

---

## Accessibility Requirements

- Preserve keyboard navigation.
- Keep focus rings visible.
- Ensure dark and AMOLED contrast is strong.
- Do not rely only on color for warnings/errors.
- Keep font scaling support.
- Do not use tiny text for critical warnings.
- Keep hit targets at least around 32px high where practical.
- Avoid low-contrast gray text on dark backgrounds.
- Cyberpunk theme must remain readable, not just aesthetic.

---

## Responsive / Resize Behavior

The app is a desktop utility and may be resized.

Requirements:
- Existing layout resize behavior must not regress.
- Tables/lists should expand where they already expand.
- Logs should remain scrollable.
- Buttons should not overlap.
- Long labels should truncate or wrap cleanly.
- Cards should not force unnecessary window expansion.
- Keep minimum window size reasonable.

---

## Theme-Specific Notes

### Light

Default professional theme.

Use:
- White surfaces
- Light gray background
- Blue primary
- Minimal shadows
- Soft borders
- Clean cards

Avoid:
- Excessive color
- Heavy outlines
- Overly large gradients

### Dark

Practical dark mode.

Use:
- Dark slate surfaces
- Blue primary
- Soft contrast
- Thin borders
- Very subtle elevation

Avoid:
- Pure black background
- Neon glow
- Low contrast gray text

### AMOLED

OLED-focused black mode.

Use:
- True black app background
- Near-black surfaces
- Strong text contrast
- Minimal separators
- Minimal shadow
- Electric accent only where necessary

Avoid:
- Large gray panels
- Heavy gradients
- Excessive glow
- Washed-out text

### Cyberpunk

Stylized optional mode.

Use:
- Dark indigo background
- Neon cyan/blue primary
- Violet/magenta accent for selected/focus states
- Subtle glows
- Sharp contrast
- Futuristic but clean controls

Avoid:
- Neon everywhere
- Magenta body text
- Hard-to-read glows
- Distracting animated effects
- Changing layout

---

## Safety and Confirmation UI

Use a consistent confirmation flow for dangerous actions.

Dangerous examples:
- Bulk uninstall
- Debloat
- Registry tweak
- Service modification
- Reset network stack
- Reset Windows Update
- Delete/move/overwrite files
- Modify System PATH
- Overwrite ISO
- Disable security-related features

Dialog copy pattern:

```text
Title: Confirm Action

Message:
You are about to [specific action]. This may affect system behavior and cannot be automatically undone.

Buttons:
Cancel
Continue
```

For high-risk destructive actions:

```text
Title: Confirm Destructive Action

Message:
This action may remove software, change system configuration, or overwrite existing data. Create a restore point or backup before continuing.

Buttons:
Cancel
Continue Anyway
```

Use the danger button for `Continue Anyway`.

---

## Settings Persistence

Ensure theme selection persists.

If a settings file already exists:
- Use it.
- Do not invent a parallel config file.

If no settings persistence exists:
- Add minimal JSON persistence using the standard library.

Example:

```json
{
  "theme": "Light",
  "font_scale": 1.0,
  "language": "en"
}
```

Do not store API tokens in plain JSON unless that is already the current behavior. If token storage already exists, preserve and style its UI only.

---

## Suggested Implementation Order for Codex

Follow this order. Do not jump straight into visual tweaking across random files.

### Phase 1: Discovery

1. Inspect the existing UI entry point.
2. Identify all major tabs/sections.
3. Identify existing theme/settings code.
4. Identify existing widget creation patterns.
5. Identify hardcoded colors/fonts/padding.
6. Identify long-running operation UI states.

### Phase 2: Theme foundation

1. Add central tokens for Light, Dark, AMOLED, Cyberpunk.
2. Add shared spacing/radius/font constants.
3. Add ttk style configuration function.
4. Apply root/background/base label styles.
5. Wire theme setting to theme manager.

### Phase 3: Shared components

1. Add button variants.
2. Add card/panel helper.
3. Add badges/chips.
4. Add themed inputs.
5. Add table/treeview styles.
6. Add progress/log styling.
7. Add toast and confirm dialog if missing.
8. Add toggle/segmented controls only if needed.

### Phase 4: Screen adaptation

Apply the new components to each existing section without changing layout:
1. App Store
2. Installed Apps
3. Tweaks
4. Windows Features
5. Security
6. VirusTotal
7. PATH Manager
8. ISO Toolset
9. File Mover
10. C2 Intelligence
11. Settings

### Phase 5: Theme validation

Verify each theme:
1. Light
2. Dark
3. AMOLED
4. Cyberpunk

Check:
- Text contrast
- Focus visibility
- Disabled state
- Error state
- Long-running operation state
- Treeview readability
- Log readability
- Dialog readability
- High-risk/destructive actions

### Phase 6: Cleanup

1. Remove duplicate styling code.
2. Remove unused color constants.
3. Ensure no layout regression.
4. Ensure no business logic changes.
5. Ensure no broken imports.
6. Add comments where custom widgets are non-obvious.

---

## Acceptance Criteria

The redesign is successful only if all of the following are true:

- Existing app layout is preserved.
- Existing features still work.
- Existing config-driven app/tweak/feature behavior still works.
- The UI clearly matches the supplied design language references.
- All four themes are implemented:
  - Light
  - Dark
  - AMOLED
  - Cyberpunk
- Theme switching works through existing Settings UI.
- Primary, secondary, subtle, destructive, icon, and disabled buttons are visually distinct.
- Inputs have default, focused, filled, error, and disabled states.
- Checkboxes, radio buttons, toggles, tabs, scrollbars, progress bars, cards, tables, badges, dialogs, and logs are styled consistently.
- Destructive and high-risk operations are visually obvious.
- Text remains readable in every theme.
- The app does not gain unnecessary heavy dependencies.
- No administrative/system operation logic is rewritten unnecessarily.
- No API tokens are exposed in logs or visible text unintentionally.
- UI remains usable on Windows 10 and Windows 11.

---

## Direct Codex Task Prompt

Use this prompt when applying the redesign:

```text
Redesign the existing UsefulWindowsUtils Python/Tkinter desktop app using the supplied UI design language reference images.

Preserve the current app layout, tabs, feature order, workflows, and business logic. This is a UI modernization task, not a functional rewrite.

Implement a centralized theme/style system with Light, Dark, AMOLED, and Cyberpunk themes. Use modern Windows 11-inspired styling: clean surfaces, rounded controls, subtle borders, strong typography, consistent spacing, polished buttons, inputs, toggles, checkboxes, tables, cards, badges, modals, scrollbars, progress bars, and logs.

Keep the app dependency-light. Prefer tkinter/ttk/Canvas and the Python standard library. Do not migrate to PyQt, Electron, or another GUI framework.

Apply the visual system across all existing sections: App Store, Installed Apps Manager, Windows Tweaks, Windows Features/System Fixes, Security Analysis, VirusTotal, PATH Manager, ISO Toolset, File Mover, C2 Threat Intelligence, and Settings.

Use destructive styling and confirmation dialogs for risky system actions. Preserve existing safety flows, restore point prompts, logs, threading/subprocess behavior, config loading, API integrations, package manager behavior, file operations, and exports.

Refactor repeated styling into reusable theme tokens, ttk styles, and lightweight widget helpers. Avoid hardcoded colors and one-off styling.

After changes, verify that all four themes are readable, consistent, and usable, and that no existing functionality or layout has regressed.
```

---

## Final Design Principle

UsefulWindowsUtils is not a toy launcher. It is a powerful Windows administration and security utility. The redesign should make it feel safer, clearer, faster, and more trustworthy without making it bloated.

The app should look modern, but the real win is control hierarchy:
- Safe actions should feel easy.
- Dangerous actions should feel deliberate.
- Long-running actions should feel visible.
- Complex tools should feel organized.
- The user should always know what they are about to change.
