-- pertama tama, membuat database DWH
CREATE DATABASE DWH;
GO

USE DWH;
GO

-- yang kedua membuat tabel DimCustomer
CREATE TABLE DimCustomer (
    CustomerID INT PRIMARY KEY,
    CustomerName VARCHAR(100) NOT NULL,
    Address VARCHAR(255),
    CityName VARCHAR(100),
    StateName VARCHAR(100),
    Age INT,
    Gender VARCHAR(20),
    Email VARCHAR(100)
);

-- yang ketiga membuat tabel DimBranch
CREATE TABLE DimBranch (
    BranchID INT PRIMARY KEY,
    BranchName VARCHAR(100) NOT NULL,
    BranchLocation VARCHAR(255)
);

-- yang keempat membuat tabel DimAccount
CREATE TABLE DimAccount (
    AccountID INT PRIMARY KEY,
    CustomerID INT NOT NULL,
    AccountType VARCHAR(50),
    Balance DECIMAL(18, 2),
    DateOpened DATETIME,
    Status VARCHAR(20),
    CONSTRAINT FK_DimAccount_DimCustomer FOREIGN KEY (CustomerID) 
        REFERENCES DimCustomer(CustomerID)
);

-- yang kelima membuat Tabel FactTransaction
CREATE TABLE FactTransaction (
    TransactionID INT PRIMARY KEY,
    AccountID INT NOT NULL,
    TransactionDate DATETIME NOT NULL,
    Amount DECIMAL(18, 2) NOT NULL,
    TransactionType VARCHAR(50) NOT NULL,
    BranchID INT NOT NULL,
    CONSTRAINT FK_FactTransaction_DimAccount FOREIGN KEY (AccountID) 
        REFERENCES DimAccount(AccountID),
    CONSTRAINT FK_FactTransaction_DimBranch FOREIGN KEY (BranchID) 
        REFERENCES DimBranch(BranchID)
);
GO