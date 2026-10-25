CREATE TABLE InterviewHistory (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    Category NVARCHAR(50),
    Score INT,
    InterviewDate DATETIME DEFAULT GETDATE()
);

SELECT COUNT(*) FROM Users;
SELECT * FROM Users;