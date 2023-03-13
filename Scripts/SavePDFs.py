# save all PDFs in the PDFs folder to the database
from pdfreader import PDFReading
from sqlhandler import SQLHandler
from pathlib import Path

SERVER = "DESKTOP-QG36584\SQLEXPRESS"
DATABASE = "ExamQuestions"


def main():
    sqlsocket = SQLHandler(SERVER, DATABASE)
    files = list((Path.cwd() / "pdfs").rglob('*.pdf'))
    for file in files:
        reader = PDFReading(file)
        questions = reader.questions
        for question in questions:
            query = 

if __name__ == "__main__":
    main()
