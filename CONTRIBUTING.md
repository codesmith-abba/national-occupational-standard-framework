# Contributing to the NOS Framework

This project converts the Nigerian National Board for Technical Education (NBTE) National Occupational Standard (NOS) PDFs into structured JSON and plain text formats. Developers consuming these NOS datasets for web applications, LMS platforms, assessment tools, or skills registries depend on accurate extraction — your contribution helps make that possible.

---

## Setup

```bash
# Clone the repository
git clone https://github.com/<your-org>/national-occupational-standard-framework.git
cd national-occupational-standard-framework

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate      # Linux / macOS
# venv\Scripts\activate       # Windows

# Install the only dependency
pip install pdfplumber
```

---

## Contribution Workflow

At a high level the process is:

1. **Pick a NOS PDF** — find one on the NBTE portal (or elsewhere) that is not yet in the repo.
2. **Place it in `worker/`**.
3. **Convert** to JSON and text with the extraction scripts.
4. **Verify** every unit, learning outcome, and performance criteria against the PDF.
5. **Fix any extraction gaps** in `implement-tojson.py` if the script misses data.
6. **Submit a pull request** when the output is clean.

---

## Step‑by‑Step Guide

### 1. Add your PDF

Copy the NOS PDF you want to contribute into the `worker/` directory:

```bash
cp ~/Downloads/NOS-NSQ\ New\ Trade\ Levels\ 2.pdf ./worker/
```

### 2. Run the extraction scripts

```bash
# Convert PDF → JSON (auto‑detects NSQ level and splits into appropriate level‑N/ folders)
python implement-tojson.py --dir ./worker

# Convert PDF → plain text
python implement-totext.py --dir ./worker
```

Output is written to:

```
extracted_json/
  level-1/
  level-2/
  level-3/

extracted_text/
  level-1/
  level-2/
  level-3/
```

A single PDF that spans multiple NSQ levels (common for masonry and other trades) will produce one file per level, each containing only the units belonging to that level.

### 3. Verify the JSON output

Open the generated JSON and the original PDF side by side. For **every unit** check:

- **Unit code** — matches `Unit Reference Number` in the PDF.
- **Unit title** — matches the title in the PDF.
- **Learning outcomes** — every LO from the PDF is present with the correct number.
- **Performance criteria** — every PC (e.g., `1.2`, `3.4`) is present under the correct LO with a complete description.
- **PC descriptions** — no truncated text, no mixed‑up columns, no garbage from table headers.

A quick way to count PCs in your output:

```bash
python -c "
import json
with open('extracted_json/level-2/NOS-NSQ New Trade Levels 2.json') as f:
    data = json.load(f)
for u in data['units']:
    pcs = sum(len(lo['performance_criteria']) for lo in u['learning_outcomes'])
    print(f'{u[\"code\"]}: {len(u[\"learning_outcomes\"])} LOs, {pcs} PCs')
"
```

If any unit, LO, or PC is missing, move to step 4. If everything checks out, skip to step 5.

### 4. What to do when extraction misses data

The extraction script (`implement-tojson.py`) handles the most common PDF layouts, but NBTE PDFs vary in formatting. Common issues you may encounter:

| Problem | Likely cause | Where to look |
|---|---|---|
| Entire unit missing | `Unit Reference Number` format not recognised | `unit_code_pattern` regex (line ~9) |
| Unit title is "Unknown Title" | `Unit Title:` line uses a different delimiter | `unit_title_pattern` regex or text processing loop |
| Learning outcomes not detected | Table layout differs from expected columns | Table processing logic (line ~130+) |
| Some PCs end up under the wrong LO | PC code prefix auto‑switch not working | `get_or_create_lo()` call in PC section |
| Multi‑page tables lose data | Table extraction doesn't carry state across pages | The `current_lo` / `current_pc` variables |

If you are comfortable with Python regex and `pdfplumber`, please include the fix in your PR. If not, open an issue describing what is missing and attach the PDF — someone else can work on the extraction logic.

### 5. Clean up and PR

- Remove the source PDF from `worker/` — only the extracted JSON and text files should be committed.
- Delete any stale files in `worker/extracted_json/` left over from earlier runs.

```bash
rm worker/NOS-NSQ\ New\ Trade\ Levels\ 2.pdf
rm -rf worker/extracted_json/ worker/extracted_text/
```

- Commit only the new `extracted_json/` and `extracted_text/` files:

```bash
git add extracted_json/ extracted_text/
git commit -F - <<'EOF'
Add NOS extraction for New Trade Level 2

Co-authored-by: CommandCodeBot <noreply@commandcode.ai>
EOF
```

- Push your branch and open a pull request. In the PR description, mention which PDF you processed and confirm that you verified all units, LOs, and PCs manually.

---

## Script Reference

### `implement-tojson.py`

- **What it does** — Parses NOS PDFs with `pdfplumber`, extracting trade names, unit codes/titles, learning outcomes, and performance criteria into structured JSON.
- **CLI flags**:
  - `--dir` — Directory containing the PDFs (default: `./worker`).
  - `--trade` — Override the auto‑detected trade name.
- **Level detection** — Units are split by the `/L1`, `/L2`, `/L3` suffix in their reference codes. A multi‑level PDF produces a separate JSON file for each level.

### `implement-totext.py`

- **What it does** — Extracts raw text from every page of a NOS PDF and writes it to a `.txt` file for manual inspection or alternate parsing.
- **CLI flags**:
  - `--dir` — Directory containing the PDFs (default: `./nosall`).

---

## Data Model

The JSON follows this hierarchy:

```
{
  "trade_name": "PAINTING AND DECORATION",
  "units": [
    {
      "code": "CON/PD004/L2",
      "title": "Handling and Storage of Painting and decorating materials",
      "learning_outcomes": [
        {
          "lo_num": "1",
          "description": "Handle Painting and Decorating materials",
          "performance_criteria": [
            {
              "pc_code": "1.1",
              "description": "Identify methods of safe handling..."
            }
          ]
        }
      ]
    }
  ]
}
```

---

## Avoiding Common Mistakes

- **Do not guess levels**. Let the script auto‑detect — each unit's code contains its NSQ level.
- **Do not hand‑edit JSON**. If the output is wrong, fix the extraction script, re‑run it, and re‑verify.
- **Small hand‑edits are okay for edge cases**. Things like a missing slash in a unit code (`CONPD004L2` → `CON/PD004/L2`) or a malformed code pattern the regex genuinely cannot handle are fine to fix manually. Always note these edits in your PR description.
- **Check empty descriptions**. Some PDF layouts put LO descriptions on separate lines or interleaved with PC text. A few empty LO descriptions are acceptable when the PDF layout makes clean extraction impossible — PCs are what really matter.
- **Do not skip the text output**. The `.txt` files are useful for debugging extraction issues — compare them against the JSON to find gaps.
- **One trade per PDF**. Most NOS PDFs contain a single trade. If your PDF covers multiple trades, split it or note it in your PR.
