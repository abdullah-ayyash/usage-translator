# Usage Translator

![Python CI](https://github.com/abdullah-ayyash/usage-translator/actions/workflows/python-tests.yml/badge.svg)

This script processes account usage data for billing purposes. It reads a usage CSV and a JSON part number map, applies transformation rules, and generates two SQL `INSERT` statements (for `chargeable` and `domains` tables) saved to `output.sql`.

## ✅ Features

- Skips invalid rows (missing PartNumber, zero/negative itemCount)
- Filters by a configurable partner skip list
- Applies unit reduction rules per PartNumber
- Cleans and normalizes `accountGuid` into valid 32-char IDs
- Generates deduplicated domain records
- Logs validation issues and running usage totals per product
- Escapes SQL string values to prevent SQL injection

## 📂 Project Structure

```
usage-translator/
├── data/
│   ├── Sample_Report.csv
│   └── typemap.json
├── src/
│   ├── main.py
│   ├── config.py
│   ├── parser.py
│   ├── transformer.py
│   └── sql_writer.py
├── tests/
│   ├── __init__.py
│   ├── test_sql_writer.py
│   └── test_transformer.py
├── .env
├── .gitignore
├── requirements.txt
└── output.sql
```

## ⚙️ Setup Instructions

1. **Clone the repository**

   ```bash
   git clone https://github.com/abdullah-ayyash/usage-translator.git
   cd usage-translator
   ```

2. **Create a `.env` file**

Copy the example environment file into a real `.env` file:

```bash
cp .env.example .env
```

You can then update the values in `.env` if needed. Example content:

```env
CSV_PATH=./data/Sample_Report.csv
TYPEmap_PATH=./data/typemap.json
SKIP_PARTNERS=26392
UNIT_FACTORS={"EA000001GB0O":1000,"PMQ00005GB0R":5000,"SSX006NR":1000,"SPQ00001MB0R":2000}
```

> 💡 You can customize the skip list and unit factors as needed.

3. **Create a virtual environment**

### 🪟 Windows

```bash
python -m venv .venv
```

### 🐧 WSL / Linux

If you're using WSL or Linux and creating a virtual environment fails, you may need to install the `venv` module first:

```bash
sudo apt update
sudo apt install python3-venv
```

Then create the environment:

```bash
python3 -m venv .venv
```

> 💡 Tip: Use `python3 --version` to check your installed version. If needed, install the matching `python3.x-venv` package (e.g., `python3.10-venv`).

4. **Activate the virtual environment**

### 🪟 Windows

- **On PowerShell**

  ```bash
  .venv\Scripts\Activate.ps1
  ```

- **On Command Prompt**
  ```bash
  .venv\Scripts\activate.bat
  ```

### 🐧 WSL / Linux

```bash
source .venv/bin/activate
```

5. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Running the Script

Once setup is complete, run:

```bash
python src/main.py
```

This will:

- Read the CSV and JSON files
- Process and validate usage entries
- Output `output.sql` containing the SQL insert statements
- Print summary logs to the terminal

## 📤 Output Example

`output.sql` will contain something like:

```sql
-- Chargeable Table Insert
INSERT INTO chargeable (partnerID, product, partnerPurchasedPlanID, plan, usage) VALUES
(1001, 'core.chargeable.adsync', 'ABCD1234XYZ', 'Email Plan', 5);

-- Domains Table Insert
INSERT INTO domains (partnerPurchasedPlanID, domain) VALUES
('ABCD1234XYZ', 'example.com');
```

## 🧪 Running Tests

This project uses `pytest` for unit testing. All test files are located in the `tests/` folder.

### ✅ Run all tests

Make sure your virtual environment is activated, then run:

```bash
pytest
```

> ✅ Tests are automatically run on each push via GitHub Actions CI.

## 🔐 SQL Safety

Although this tool only outputs SQL and does not execute it, precautions were taken to ensure output safety:

- All string values are sanitized using `.replace("'", "''")` to escape single quotes
- No external user input is allowed at runtime
- The script assumes empty target tables, as specified in the requirements

## 📄 License

This project was created as part of a technical assessment. Feel free to review or reuse the code as needed.
