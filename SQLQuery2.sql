USE AI_Interview;
GO

CREATE TABLE Answers (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    QuestionId INT,
    UserAnswer NVARCHAR(MAX)
);
GO

SELECT * FROM Answers;


