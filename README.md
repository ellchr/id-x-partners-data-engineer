# Data Warehouse Design & Automated ETL Pipeline

> **Final Task Project - Project-Based Virtual Internship: Data Engineer at ID/X Partners x Rakamin Academy**

Project ini bertujuan untuk merancang dan membangun **Data Warehouse (`DWH`)** serta mengimplementasikan pipeline **ETL (Extract, Transform, Load)** otomatis dan **Stored Procedure** untuk analisis transaksi perbankan dari berbagai sumber data yang terpisah.

---

## Project Overview

Perusahaan perbankan menghadapi kendala keterlambatan pelaporan dan analisis data karena data transaksi tersimpan secara terpisah di berbagai format sumber data (`SQL Server Database`, `Excel`, dan `CSV`).

Sebagai Data Engineer, solusi yang dibangun dalam project ini meliputi:
1. **Perancangan Database Data Warehouse (`DWH`)** dengan skema *Star Schema* yang terdiri dari 3 Tabel Dimensi (`DimCustomer`, `DimBranch`, `DimAccount`) dan 1 Tabel Fakta (`FactTransaction`) dilengkapi relasi *Primary Key* & *Foreign Key*.
2. **Automated ETL Pipeline (Python & Pandas)** untuk mengekstrak data dari database SQL Server serta file eksternal (Excel & CSV), melakukan pembersihan data (*data cleaning*), standarisasi format (*uppercase & date parsing*), deduplikasi data transaksi, dan memuatnya ke DWH.
3. **Implementasi Stored Procedures (T-SQL)** untuk mempercepat proses pembuatan laporan transaksi harian dan kalkulasi sisa saldo (*Current Balance*) nasabah secara real-time.

---

## Tech Stack & Tools

* **Database Engine**: Microsoft SQL Server Express
* **Database Management GUI**: SQL Server Management Studio (SSMS)
* **Programming Language**: Python 3.11
* **ETL Framework & Libraries**: Pandas, SQLAlchemy, PyODBC, OpenPyXL
* **Version Control**: Git & GitHub

---

## Data Warehouse Architecture & Schema

### Tables & Relationships

1. **`DimCustomer`**: Memuat data nasabah hasil penggabungan tabel `customer`, `city`, dan `state`.
* *Transformation Logic*: Format teks pada nama, alamat, kota, provinsi, dan gender diubah menjadi **UPPERCASE**.


2. **`DimBranch`**: Memuat data kantor cabang bank (`BranchID`, `BranchName`, `BranchLocation`).
3. **`DimAccount`**: Memuat data rekening nasabah (`AccountID`, `CustomerID`, `AccountType`, `Balance`, `Status`).
4. **`FactTransaction`**: Memuat seluruh data transaksi terintegrasi dari 3 sumber data.
* *Transformation Logic*: Penggabungan data DB, Excel, CSV, penghapusan duplikasi berdasarkan `TransactionID`, serta penyelarasan format tanggal `DD-MM-YYYY` ke `Datetime`.

---

## Stored Procedures

Terdapat dua Stored Procedure di database `DWH` untuk analisis bisnis cepat:

### 1. `DailyTransaction`

Menghitung total banyaknya transaksi dan akumulasi nominal (*TotalAmount*) per hari dalam rentang tanggal tertentu.

* **Parameters**: `@start_date DATE`, `@end_date DATE`
* **Execution Example**:
```sql
EXEC DailyTransaction @start_date = '2024-01-18', @end_date = '2024-01-20';

```

### 2. `BalancePerCustomer`

Menghitung sisa saldo akhir (*Current Balance*) nasabah berstatus `active` berdasarkan perhitungan otomatis:


$$\text{CurrentBalance} = \text{Balance} + \sum(\text{Deposit}) - \sum(\text{Withdrawal/Transfer/Payment})$$

* **Parameters**: `@name VARCHAR(100)`
* **Execution Example**:
```sql
EXEC BalancePerCustomer @name = 'Shelly';

```

---

## Getting Started & How to Run

### Prerequisites

* Python 3.8+
* SQL Server Express & SSMS terinstall di komputer lokal.
* File `sample.bak` sudah di-restore ke SQL Server sebagai database source `sample`.

### Step-by-Step Execution

1. **Clone Repository**
```bash
git clone [https://github.com/USERNAME/id-x-partners-data-engineer.git](https://github.com/USERNAME/id-x-partners-data-engineer.git)
cd id-x-partners-data-engineer

```


2. **Setup Database & Tables DWH**
* Buka SSMS, jalankan script `sql/01_ddl_dwh.sql` untuk membuat database `DWH` dan struktur tabelnya.


3. **Install Dependensi Python**
```bash
pip install -r requirements.txt

```


4. **Jalankan Pipeline ETL**
* Pastikan file `transaction_excel.xlsx` dan `transaction_csv.csv` berada di folder project.
* Jalankan script ETL:
```bash
python etl_process.py

```




5. **Deploy & Test Stored Procedures**
* Buka SSMS, eksekusi script `sql/02_stored_procedures.sql`.
* Jalankan query pengujian `EXEC DailyTransaction ...` dan `EXEC BalancePerCustomer ...`.



---

## Author

* **Nama**: Otniel Chresto Purwandi
* **Program**: Virtual Internship Experience (VIX) Data Engineer - ID/X Partners x Rakamin Academy

```

## 📁 Repository Structure

```text
id-x-partners-data-engineer/
│
├── sql/
│   ├── 01_ddl_dwh.sql              # Script DDL Pembuatan Database & Tabel DWH
│   └── 02_stored_procedures.sql    # Script Stored Procedures (DailyTransaction & BalancePerCustomer)
│
├── data/                           # (Optional) Source files
│   ├── transaction_excel.xlsx
│   └── transaction_csv.csv
│
├── etl_process.py                  # Script Utama Automated Pipeline ETL (Python + Pandas)
├── requirements.txt                # Dependensi Library Python
└── README.md                       # Dokumentasi Project

