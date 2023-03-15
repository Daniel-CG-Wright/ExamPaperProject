CREATE TABLE PAPER(PaperID varchar(25) PRIMARY KEY NOT NULL,
PaperComponent varchar(15),
PaperYear varchar(4),
PaperLevel varchar(2));
CREATE TABLE QUESTION(QuestionID varchar(35) PRIMARY KEY NOT NULL,
PaperID varchar(25),
QuestionNumber int,
QuestionContents varchar(max));
CREATE TABLE IMAGES(ImageID int PRIMARY KEY NOT NULL,
QuestionID varchar(35),
ImageData varbinary(max));
CREATE TABLE PARTS(PartID varchar(40) PRIMARY KEY NOT NULL,
QuestionID varchar(35),
PartNumber varchar(10),
PartContents varchar(max));
CREATE TABLE QUESTIONTOPIC(QuestionTopicID varchar(65),
QuestionID varchar(35),
TopicID varchar(30))