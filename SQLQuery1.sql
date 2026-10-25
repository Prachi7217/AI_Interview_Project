USE AI_Interview;
GO

CREATE TABLE Questions (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    QuestionText NVARCHAR(500)
);
GO

ALTER TABLE Questions
ADD Category NVARCHAR(50);

INSERT INTO Questions (QuestionText)
VALUES
('Tell me about yourself'),
('What are your strengths?'),
('Why should we hire you?'),
('What is Python?'),
('Explain Object Oriented Programming');

INSERT INTO Questions (QuestionText, Category)
VALUES
('Tell me about yourself', 'HR'),
('Why should we hire you?', 'HR'),
('What is Python?', 'Python'),
('Explain OOP concepts', 'Python'),
('What is JVM?', 'Java'),
('Explain Inheritance', 'Java');

SELECT * FROM Questions;