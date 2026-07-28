# National Occupational Standard (NOS) Framework

Converts the Nigerian National Board for Technical Education (NBTE) National Occupational Standard PDFs into structured **JSON** and plain **text** formats for developers building skills platforms, LMS, assessment tools, and skills registries.

📥 Download NOS PDFs from: [NBTE Public Dashboard](https://www.digitalnbte.nbte.gov.ng/Public/PUCDashboard)

---

## Project Structure

```
├── implement-tojson.py    # PDF → JSON converter (auto-detects NSQ level)
├── CONTRIBUTING.md        # Guide for contributors
├── worker/                # Place new NOS PDFs here for extraction
├── extracted_json/        # JSON output
│   ├── level-1/
│   ├── level-2/
│   ├── level-3/
│   ├── level-4/
│   └── level-5/
```

## Data Model

```json
{
  "trade_name": "PAINTING AND DECORATION",
  "level": 2,
  "units": [
    {
      "code": "CON/PD/004/L2",
      "title": "Handling and Storage of Painting and decorating materials",
      "learning_outcomes": [
        {
          "lo_num": "1",
          "description": "Handle Painting and Decorating materials",
          "performance_criteria": [
            { "pc_code": "1.1", "description": "Identify methods of safe handling..." }
          ]
        }
      ]
    }
  ]
}
```

## Quick Start

```bash
# Clone and set up
git clone <repo-url>
cd national-occupational-standard-framework
python3 -m venv venv
source venv/bin/activate
pip install pdfplumber

# Add a NOS PDF to worker/
cp ~/Downloads/"NOS Course Name.pdf" ./worker/

# Extract
python implement-tojson.py --dir ./worker

# Output goes to extracted_json/ and extracted_text/
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed instructions on adding new NOS trades, verifying output, and submitting pull requests.

## Contact

- muhammadjibrildauda@gmail.com
- mdjbinary@gmail.com
- mdjibril.essa@gmail.com
