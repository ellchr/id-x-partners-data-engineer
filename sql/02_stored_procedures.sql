USE DWH;
GO

-- ini untuk stored procedure pertama: DailyTransaction
CREATE PROCEDURE DailyTransaction
    @start_date DATE,
    @end_date DATE
AS
BEGIN
    SET NOCOUNT ON;

    SELECT 
        CAST(TransactionDate AS DATE) AS [Date],
        COUNT(TransactionID) AS TotalTransactions,
        SUM(Amount) AS TotalAmount
    FROM FactTransaction
    WHERE CAST(TransactionDate AS DATE) BETWEEN @start_date AND @end_date
    GROUP BY CAST(TransactionDate AS DATE)
    ORDER BY [Date] ASC;
END;
GO

-- ini untuk stored procedure kedua: BalancePerCustomer
CREATE PROCEDURE BalancePerCustomer
    @name VARCHAR(100)
AS
BEGIN
    SET NOCOUNT ON;

    SELECT 
        c.CustomerName,
        a.AccountType,
        a.Balance,
        a.Balance + ISNULL(
            SUM(
                CASE 
                    WHEN LOWER(t.TransactionType) = 'deposit' THEN t.Amount
                    ELSE -t.Amount
                END
            ), 0
        ) AS CurrentBalance
    FROM DimAccount a
    INNER JOIN DimCustomer c ON a.CustomerID = c.CustomerID
    LEFT JOIN FactTransaction t ON a.AccountID = t.AccountID
    WHERE LOWER(c.CustomerName) LIKE '%' + LOWER(@name) + '%'
      AND LOWER(a.Status) = 'active'
    GROUP BY 
        c.CustomerName,
        a.AccountID,
        a.AccountType,
        a.Balance;
END;
GO