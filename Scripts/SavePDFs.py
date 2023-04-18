# save all PDFs in the PDFs folder to the database
from ParsingOfData.pdfreader import PDFReading
from pathlib import Path
from sqlitehandler import SQLiteHandler
import getmarkschemes


def main():
    sqlsocket = SQLiteHandler()
    files = list((Path.cwd() / "pdfs").rglob('*.pdf'))
    print("processing markschemes...")
    markschemes = getmarkschemes.main()

    for file in files:
        print("processing " + str(file))
        reader = PDFReading(file)
        questions = reader.questionspartsindex
        # add the header information for the paper first
        paperid = f"{reader.level}-{reader.component}-{reader.year}"
        markschemeparser = markschemes[paperid]
        headerquery = f"""INSERT INTO PAPER VALUES(
        '{paperid}',
        '{reader.component}',
        '{reader.year}',
        '{reader.level}'
        )"""
        sqlsocket.addToDatabase(headerquery)
        for question in questions:
            # create the SQL query
            questionobj = questions[question]

            # get markscheme contents if possible, but otherwise
            # leave blank
            try:
                mstext = markschemeparser.answerindex[str(question)].contents
            except KeyError:
                mstext = ""

            # get the next max question id
            questionidquery = f"""
            SELECT IFNULL(MAX(QuestionID), 0) FROM QUESTION"""
            questionid = sqlsocket.queryDatabase(questionidquery)[0][0] + 1
            totalmarks = questionobj.marks + sum(
                i.marks for i in questionobj.parts)
            mstext = mstext.replace("\n", r"\n").replace("'", r"''")
            questionobj.contents = questionobj.contents.replace("'", r"''")
            # first add the question itself
            questioninsert = f"""
            INSERT INTO QUESTION VALUES(
            {questionid},
            '{paperid}',
            {questionobj.number},
            '{questionobj.contents}',
            {totalmarks},
            '{mstext}'
            )
            """
            sqlsocket.addToDatabase(questioninsert)
            for topic in questionobj.topics:
                # get next questiontopic id
                questiontopicid = f"""
                SELECT IFNULL(MAX(QuestionTopicID), 0) FROM QUESTIONTOPIC
                """
                questiontopicid = sqlsocket.queryDatabase(
                    questiontopicid)[0][0] + 1
                topicquery = f"""
                INSERT INTO QUESTIONTOPIC VALUES(
                {questiontopicid},
                {questionid},
                '{topic}'
                )
                """
                sqlsocket.addToDatabase(topicquery)
            for part in questionobj.parts:
                if part.marks == 0:
                    continue
                # get next part id
                partidquery = f"""
                SELECT IFNULL(MAX(PartID), 0) FROM PARTS"""
                partid = sqlsocket.queryDatabase(partidquery)[0][0] + 1
                try:
                    msobj = markschemeparser.answerindex[part.section]
                    mstext = msobj.contents
                    mstext = mstext.replace("\n", r"\n").replace("'", r"''")
                except KeyError:
                    # set breakpoint here to see errors
                    # for a list of known question skips
                    # see the questionskips.txt
                    print("Skipping part: " + part.section)
                    continue
                partinsert = f"""
                INSERT INTO PARTS VALUES(
                {partid},
                {questionid},
                '{part.section}',
                '{part.contents.strip()}',
                {part.marks},
                '{mstext}'
                )
                """
                sqlsocket.addToDatabase(partinsert)


if __name__ == "__main__":
    main()
    print("done")
