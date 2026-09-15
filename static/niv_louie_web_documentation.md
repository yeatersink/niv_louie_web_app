# Niv Louie Web — User Guide

It follows the same topics as the original Niv Louie documentation, updated for how the web app works now.

Spell the braille library **Liblouis** (one word). Generated tables use the extension **`.utb`**.

---

## Table of contents

1. [Introduction to Niv Louie](#1-introduction-to-niv-louie)
2. [Building your spreadsheet](#2-building-your-spreadsheet)
3. [Signing in and the dashboard](#3-signing-in-and-the-dashboard)
4. [Creating a new project](#4-creating-a-new-project)
5. [Editing or removing a project](#5-editing-or-removing-a-project)
6. [Creating a braille document](#6-creating-a-braille-document)
7. [Creating an NVDA add-on](#7-creating-an-nvda-add-on)
8. [Creating a Liblouis table](#8-creating-a-liblouis-table)
9. [Creating a YAML test for Liblouis](#9-creating-a-yaml-test-for-liblouis)
10. [Collaborate](#10-collaborate)
11. [Where your files live](#11-where-your-files-live)

---

## 1. Introduction to Niv Louie

Niv Louie lets anyone who can build a spreadsheet create access to Unicode with **speech** and **braille**.

- **Speech** comes from **NVDA**, a free open-source screen reader. Niv Louie builds an NVDA add-on from your spreadsheet so NVDA can speak the names you assigned.
- **Braille** comes from Niv Louie itself (braille documents) and from **Liblouis**, the open-source translator used by most braille software. Niv Louie builds a Liblouis table and a YAML test file from the same spreadsheet.

### What Niv Louie does

From the dashboard, after you save a project, you can:

1. Create and manage projects (upload a CSV, map columns, save).
2. Build a Liblouis braille table (`.utb`), with or without catalog metadata.
3. Build a Liblouis YAML test file, with or without header metadata.
4. Build an NVDA add-on (`.nvda-addon`).
5. Convert a print document into a custom braille document.

### How Niv Louie works (home page order)

1. **Project Manager** — upload a CSV, map columns, save the project.
2. **Liblouis Table Builder** — generate a table ready to publish.
3. **Liblouis Test Builder** — generate a YAML test from a one-column `Text` CSV.
4. **NVDA Add-on Builder** — generate an add-on for speech (and related character data).
5. **Custom Braille Document Builder** — convert `.txt`, `.docx`, or `.pdf` using your project rules.

If you can put a Unicode symbol in a spreadsheet, you can make it accessible with speech and braille.

The public home page explains this and offers **example files** to download. It does not send guests into the builders. Builders are on the dashboard after you sign in.

---

## 2. Building your spreadsheet

Niv Louie needs **at least five columns**. You may name them as you like; when you save the project you will map each list to what Niv Louie expects.

Suggested headers:

1. **Character** — the print character or the whole word you want contracted (for example `day`).
2. **Name** — spoken name for NVDA, and the comment in the Liblouis table.
3. **Unicode** (or **Hex**) — code point(s). One character is four hex digits (`0064`). A contraction joins parts with `+` (`0064+0061+0079` for d+a+y).
4. **Type** — the Liblouis opcode (`letter`, `punctuation`, `always`, `word`, and so on). Use the official Liblouis opcode list.
5. **Braille** — **Unicode braille cells**, not the digits `5-145` and not the letters `day`.

For the word *day* as a contraction (dot 5 + dots 1-4-5):

| Character | Unicode | Type | Name | Braille |
|---|---|---|---|---|
| day | 0064+0061+0079 | always | day | ⠐⠙ |

Important rules (these caused real failures in the web app when they were wrong):

- Character must match the test text **exactly**, including case. `Day` will not match `day`.
- Do not put a leading or trailing space in Character, Type, Hex, or Braille. A cell like `" ⠐⠙"` is wrong.
- Type `always` is copied into the `.utb` as the opcode. Niv Louie does not invent English grade-2 rules. If the word is not a row in the sheet, it will be translated letter by letter.
- Save as **`.csv`**. Only CSV is accepted for projects.
- First row must be headers. Avoid a BOM or a space before the first header (` Character`).

On the home page you can download **example of Csv.csv** and open it in Microsoft Excel as a template.

---

## 3. Signing in and the dashboard

### Local development

From the project folder:

```text
python gui.py
```

Then open `http://127.0.0.1:8080`.

### Account

- **New user:** choose a nickname. Niv Louie creates a private User ID and folders.
- **Existing user:** paste your User ID.

Save the User ID. That is how you open the same projects on another device. Sync codes are no longer used.

### Dashboard

After login you see:

- **Show my projects** — lists saved project names for this account.
- **Go to Project Manager**
- **Go to Braille Document Builder**
- **Go to NVDA Extension Builder**
- **Go to Liblouis Table Builder**
- **Go to Liblouis Test Builder**

Tool pages use **Go to Dashboard** (not Home) so you stay signed in.

---

## 4. Creating a new project

1. Open **Project Manager**.
2. Choose **Create a project** (or the create flow on that page).
3. Upload your `.csv` from this computer.
4. Continue to **Project information**.

### Liblouis metadata

These fields become the header of the `.utb` (and related YAML metadata):

- Project name
- Language ISO code (this also becomes the `.utb` / `.yaml` file name, for example `eng.utb`)
- Language system
- Display name
- Index name
- Supported languages
- Explanation
- Contributors
- Other tables to include
- Translation direction / test display (used by the YAML test, not the table header)
- Replace list (used when filtering the CSV)

### Column matching

Each combo box is a column from **your** file. Pick:

- Character column
- Character name column
- Unicode / Hex column
- Type column
- Braille column

If a saved name is not in the file, the list stays empty rather than crashing. If the CSV cannot be read, a dialog explains the error and how to fix it. Use **Refresh project manager** to return to upload.

### Save

Press **Save project**.

Niv Louie writes the filtered spreadsheet and a **CSV quality report**, then downloads:

`{project name}_csv_report.txt`

The report lists each problem with **row number**, **column name**, the **exact value in quotes**, and what is wrong. Examples:

- `row 2, column Braille: leading space in " ⠐⠙"`
- `row 3, column Hex: leading space in " 0064"`
- `row 4, column Hex: part "1208D" is 5 characters, expected 4`

Save still succeeds when the report has warnings. Fix the sheet, upload or edit, and Save again.

You should hear: **Your project is saved successfully.** Then you return to the **dashboard**.

---

## 5. Editing or removing a project

In Project Manager, choose a project in the list.

### Edit

You can change metadata, remap columns, and use the generate checkboxes from the original product:

- Generate Unicode / Hex from the Character column.
- Generate Character from the Unicode / Hex column (for example `0064+0061+0079` → `day`).

Save again. A new filtered CSV and a new report download.

### Remove

Confirm when asked. Niv Louie removes:

- the project entry
- `filtered_{name}.csv`
- `filtered_{name}_updated.csv` if present
- `{name}_csv_report.txt` if present
- `source/{name}.csv` if present

You should hear **Project removed successfully.** Then you return to **Project Manager**.

---

## 6. Creating a braille document

1. Open **Braille Document Builder**.
2. Upload a **`.txt`**, **`.docx`**, or **`.pdf`**.
3. Select one or more projects. Order matters: earlier projects are applied first.
4. Optional: general English letter rules after your project rows.
5. Convert, then choose output: **`.txt`**, **`.brf`**, or **`.docx`**.

Niv Louie replaces print strings from your Character column with the Braille cells from that row. Longer matches should win over shorter ones (so `day` is applied before `d`). Type/`always` is not used here; only the Character → Braille pairs.

The file downloads to your browser Downloads folder. A copy is also stored under this account’s documents folder (see [Where your files live](#11-where-your-files-live)).

---

## 7. Creating an NVDA add-on

The builder has two sections.

### Create an NVDA add-on

Short instructions, then **Create NVDA add-on**. That opens the create form: pick projects, name the add-on, save. The `.nvda-addon` is written to this account’s `nvda_extensions` folder.

### Saved add-ons

Choose an add-on in the list, then:

- **Edit selected add-on**
- **Download Addon** — sends the **existing** file. It does not rebuild. If the file is missing, create the add-on first.
- **Remove selected add-on** — confirm, then delete.

### Install in NVDA

1. Open the downloaded `.nvda-addon` while NVDA is running.
2. NVDA menu (Insert or Caps Lock + N) → Preferences → Settings.
3. Speech → Extra dictionaries for symbol and characters.
4. Check your add-on → Apply.

Your CSV names are then used when NVDA speaks those characters.

---

## 8. Creating a Liblouis table

1. Open **Liblouis Table Builder**.
2. Select a project.
3. Choose one:

- **Generate and download table** — full `.utb` with catalog metadata.
- **Generate table without metadata** — rules only (`{language code}_nometa.utb`).

### What the full table contains

From project information:

- `# liblouis:` project name
- `#-display-name:`
- `#-index-name:`
- `#+language:`
- `#+type:literary`
- `#+contraction:no`
- `#+system:`
- `#+dots:6`
- `#-license: lgpl-2.1` and the LGPL comment block
- explanation and contributors
- one rule per CSV row: `Type  Character  dot-numbers  # Name`
- `include` lines for other tables you listed

Braille cells are converted from Unicode braille to Liblouis dot numbers (`⠐⠙` → `5-145`).

The no-metadata file is the opcode lines (and includes, if you listed extra tables). Use the full file when you submit a table; use the short file when you only want the rules.

---

## 9. Creating a YAML test for Liblouis

Liblouis needs a YAML test to publish a table. Niv Louie builds it from your project plus a **test document**.

1. Make a spreadsheet with one column named **`Text`**. Each row is a print sample (`d`, `day`, a sentence).
2. Save as CSV. The home page offers **example of test.csv**.
3. Open **Liblouis Test Builder**.
4. Upload that CSV.
5. Select one or more projects.
6. Choose one:

- **Generate and download YAML test** — `{code}.yaml` with display, table, flags, and tests.
- **Generate test without metadata** — `{code}_nometa.yaml` with only the `tests:` pairs.

The expected braille side is built by applying your Character → Braille rows, longest match first. If `day` does not appear as a row, or the letters do not match exactly, you will see letter-by-letter braille instead of the contraction.

`display` comes from the project’s test display field, or `unicode.dis` if that field is empty. Do not put `forward` in display unless that is a real Liblouis display file name. Forward/backward belongs under `flags: { testmode: forward }`.

---

## 10. Collaborate

Open **Collaborate** while signed in.

- Your **User ID** is shown in a read-only field. Use it to sign in on another device.
- For live editing of Python, use **VS Code Live Share**.
- For the spreadsheet itself, use **Microsoft 365 / Excel**, then save as CSV and upload again.

Real-time co-editing inside Niv Louie is not provided.

---

## 11. Where your files live

The web app does **not** use the old desktop path `%LOCALAPPDATA%\Niv_Louie` as the main store.

On Windows, files for an account look like:

```text
C:\Users\<you>\niv_louie_data\users\<user-id>\
  projects\
    languages_file.json
    filtered_<project>.csv
    <project>_csv_report.txt
    source\<project>.csv
  nvda_extensions\
    <name>.nvda-addon
    extentions_file.json
  braille_tests\
    <language>.csv
    <language>.yaml
  documents\
```

Downloads from the browser go to your usual Downloads folder. Use **Download Addon** or the generate buttons rather than copying by hand unless you are debugging.

Example files on the home page:

- `/static/example of Csv.csv`
- `/static/example of test.csv`

They should download with those names, not as a file called `true`.

---

## Quick checks when something looks wrong

| Symptom | Usual cause |
|---|---|
| YAML shows three cells for `day` | Character is `Day`, or Braille is not `⠐⠙`, or `d` is applied first |
| Report says extra spaces | Leading space in Hex, Type, or Braille, even if Character looks clean |
| Hex part is not 4 characters | Five-digit codes such as `1208D` — warning only |
| Select crashes “Invalid value” | Saved column name is not in the uploaded headers |
| Download Addon does nothing useful | File was never created; use Create first |
| Table has `d-a-y` instead of `5-145` | Braille column was letters, not Unicode braille cells |
| 404 for images or examples | Static folder not mounted; the app should serve the repo `static` directory |

---

© 2026 Niv Louie — Free and Open Source (GPL-3.0)
