CREATE TABLE PAPER(PaperID varchar(40) PRIMARY KEY NOT NULL,
PaperComponent varchar(15),
PaperYear varchar(4),
PaperLevel varchar(10));
CREATE TABLE QUESTION(QuestionID varchar(50) PRIMARY KEY NOT NULL,
PaperID varchar(40),
QuestionNumber int,
QuestionContents varchar(max));
CREATE TABLE IMAGES(ImageID int PRIMARY KEY NOT NULL,
QuestionID varchar(50),
ImageData varbinary(max));
CREATE TABLE PARTS(PartID varchar(60) PRIMARY KEY NOT NULL,
QuestionID varchar(50),
PartNumber varchar(10),
PartContents varchar(max));
CREATE TABLE QUESTIONTOPIC(QuestionTopicID varchar(150),
QuestionID varchar(50),
TopicID varchar(100))