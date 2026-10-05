# PROJECT 2: Data Cleaner and Transformer

A robust, modular data cleaning and transformation pipeline built in Python. Designed to systematically identify data quality issues, handle inconsistencies, and prepare messy raw datasets for downstream analytics and engineering workflows.

---

## 🛠️ Project Overview

Raw data from source systems is rarely analysis-ready. This project implements a reusable data processing layer that tackles common data hygiene problems:
* **Inconsistent Date Parsing:** Standardizes multiple messy date string formats into a uniform `YYYY-MM-DD` layout.
* **Configurable Null Handling:** Dynamically fills or manages missing values using dictionary configurations rather than rigid hardcoded logic.
* **Type Conversion & Normalization:** Cleans numeric strings containing formatting artifacts (like commas) and standardizes categorical string formatting (trimming, casing).
* **Audit & Observability:** Logs execution stages using Python's `logging` module and generates a detailed post-cleaning quality report.

---

## 📂 Folder Structure

```text
project_02_data_cleaner/
├── data/
│   └── raw_input.csv
├── output/
│   ├── output_clean.csv
│   └── quality_report.csv
├── cleaner.py
├── config.py
└── README.md
```

---

## 🚀 Key Features

1. **Pre-Cleaning Quality Assessment:** Scans the raw dataset to report total rows, missing value distribution, duplicate counts, and unique value frequencies per column.
2. **Configurable Strategy Map (`config.py`):** Define column-specific type transformations and null handling behaviors (mean imputation, default values, or dropping) via clean dictionary mappings.
3. **Pipeline Observability:** Replaces basic print statements with structured runtime logging (`INFO`, `WARNING`, `ERROR`) to trace pipeline health step-by-step.

---

## ⚙️ Getting Started

### Prerequisites
* Python 3.8+ installed on your machine.

### Installation & Execution

1. Clone the repository:
   ```bash
   git clone https://github.com/WardaRashid07/PROJECT-2-Based-Data-Cleaner-and-Transformer.git
   cd PROJECT-2-Based-Data-Cleaner-and-Transformer
   ```

2. Place your raw input CSV file inside the `data/` folder as `raw_input.csv`.

3. Run the cleaning pipeline:
   ```bash
   python cleaner.py
   ```

4. Check your processed data and execution metrics inside the `output/` directory.

---

## 📊 Sample Output & Quality Report

### Processed Record Example
* **Raw Input:** `1001 | "jan 15 2024" | " typeA " | subB | "1,500.00" | null | null`
* **Cleaned Output:** `1001 | 2024-01-15 | Type A | Sub B | 1500.00 | <mean_filled> | UNKNOWN`

### Sample Quality Metrics (`quality_report.csv`)
```csv
Metric,Value
Total rows read,1000
Duplicates removed,52
Nulls filled (metric_2),110
Nulls filled (label),85
Rows written (clean),948
```

---

## 🧠 Concepts Covered
* **Modular Design:** Separation of pipeline execution logic (`cleaner.py`) from configuration settings (`config.py`).
* **Robust Error Handling:** `try/except` blocks during type casting and date parsing.
* **String Manipulation:** Python string methods (`strip`, `lower`, `upper`, `replace`) for data standardization.
* **File I/O:** Native Python `csv` module operations.

---

## 💡 Future Enhancements (Stretch Goals)
* [ ] Accept null handling strategies via an external JSON configuration file.
* [ ] Add a column-level validation step to flag out-of-bounds or unexpected values.
* [ ] Generate HTML-formatted diagnostic reports alongside CSV files.
