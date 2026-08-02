import os
import urllib
import pandas as pd
from sqlalchemy import create_engine, text

# ini untuk setup path & koneksi database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SERVER = r'localhost\SQLEXPRESS'
DRIVER = 'ODBC Driver 17 for SQL Server'

conn_str_src = f"DRIVER={{{DRIVER}}};SERVER={SERVER};DATABASE=sample;Trusted_Connection=yes;TrustServerCertificate=yes"
conn_str_dwh = f"DRIVER={{{DRIVER}}};SERVER={SERVER};DATABASE=DWH;Trusted_Connection=yes;TrustServerCertificate=yes"

src_engine = create_engine(f"mssql+pyodbc:///?odbc_connect={urllib.parse.quote_plus(conn_str_src)}")
dwh_engine = create_engine(f"mssql+pyodbc:///?odbc_connect={urllib.parse.quote_plus(conn_str_dwh)}")

print("Starting ETL pipeline...")

# ini untuk reset isi tabel DWH sebelum diload ulang (buat cegah error duplicate PK)
with dwh_engine.connect() as conn:
    conn.execute(text("DELETE FROM FactTransaction;"))
    conn.execute(text("DELETE FROM DimAccount;"))
    conn.execute(text("DELETE FROM DimBranch;"))
    conn.execute(text("DELETE FROM DimCustomer;"))
    conn.commit()
    print("[INIT] Tabel DWH lama berhasil dibersihkan.")


# etl DimCustomer
print("[LOG] Processing DimCustomer...")
query_customer = """
    SELECT 
        c.customer_id AS CustomerID,
        c.customer_name AS CustomerName,
        c.address AS Address,
        ci.city_name AS CityName,
        st.state_name AS StateName,
        c.age AS Age,
        c.gender AS Gender,
        c.email AS Email
    FROM customer c
    LEFT JOIN city ci ON c.city_id = ci.city_id
    LEFT JOIN state st ON ci.state_id = st.state_id
"""
df_customer = pd.read_sql(query_customer, src_engine)

# format nama, alamat, kota, provinsi, gender aku ubah ke UPPERCASE
upper_cols = ['CustomerName', 'Address', 'CityName', 'StateName', 'Gender']
for col in upper_cols:
    df_customer[col] = df_customer[col].astype(str).str.upper()

df_customer.to_sql('DimCustomer', dwh_engine, if_exists='append', index=False)
print("[OK] DimCustomer loaded.")


# etl DimBranch & DimAccount
print("[LOG] Processing DimBranch & DimAccount...")

df_branch = pd.read_sql("""
    SELECT 
        branch_id AS BranchID, 
        branch_name AS BranchName, 
        branch_location AS BranchLocation 
    FROM branch
""", src_engine)
df_branch.to_sql('DimBranch', dwh_engine, if_exists='append', index=False)

df_account = pd.read_sql("""
    SELECT 
        account_id AS AccountID, 
        customer_id AS CustomerID, 
        account_type AS AccountType, 
        balance AS Balance, 
        date_opened AS DateOpened, 
        status AS Status 
    FROM account
""", src_engine)
df_account.to_sql('DimAccount', dwh_engine, if_exists='append', index=False)

print("[OK] DimBranch & DimAccount loaded.")


# etl FactTransaction (DB + Excel + CSV)
print("[LOG] Processing FactTransaction from all sources...")

# data dari database
df_tx_db = pd.read_sql("""
    SELECT 
        transaction_id AS TransactionID, 
        account_id AS AccountID, 
        transaction_date AS TransactionDate,
        amount AS Amount, 
        transaction_type AS TransactionType, 
        branch_id AS BranchID
    FROM transaction_db
""", src_engine)

# mapping nama kolom untuk file eksternal
column_mapping = {
    'transaction_id': 'TransactionID',
    'account_id': 'AccountID', 
    'transaction_date': 'TransactionDate',
    'amount': 'Amount', 
    'transaction_type': 'TransactionType',
    'branch_id': 'BranchID'
}

excel_file = os.path.join(BASE_DIR, 'transaction_excel.xlsx')
csv_file = os.path.join(BASE_DIR, 'transaction_csv.csv')

df_tx_excel = pd.read_excel(excel_file).rename(columns=column_mapping)
df_tx_csv = pd.read_csv(csv_file).rename(columns=column_mapping)

# ini buat merge, hapus duplikat, dan atur parsing tanggal
df_fact = pd.concat([df_tx_db, df_tx_excel, df_tx_csv], ignore_index=True)
df_fact = df_fact.drop_duplicates(subset=['TransactionID'], keep='first')
df_fact['TransactionDate'] = pd.to_datetime(df_fact['TransactionDate'], dayfirst=True)

df_fact.to_sql('FactTransaction', dwh_engine, if_exists='append', index=False)
print("[OK] FactTransaction loaded.")

print("\nETL pipeline sudah berhasil coy")