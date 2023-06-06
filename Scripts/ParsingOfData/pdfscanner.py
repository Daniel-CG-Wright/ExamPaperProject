# used to scan pdf files into a list of images for each question
# NOTE remove __main__ code when finished
# using pydf2
import PyPDF2
# and fitz
import fitz
# and re
import re
# typing
from typing import List, Dict


# function to scan pdf files into a list of images for each question
def ExtractQuestionSnapshots(pdfPath: str) -> Dict[str, List[str]]:
    """
    Takes a snapshot of each question in the pdf file
    and returns a dictionary of question numbers and image data.
    The questions are kept whole (not split into parts)

    Args:
        pdfPath (str): path to the pdf file

    Returns:
        Dict[str, List]: dictionary of question numbers and list
        of image data
    """
    try:
        with open(pdfPath, 'rb') as pdfFile:
            reader = PyPDF2.PdfReader(pdfFile)
            output = {}
            # Get the pages' content as PyMuPDF Document objects
            pdfDocument = fitz.open(pdfPath)
            # iterate over question numbers - keep going
            # until we find a question that doesn't exist
            # this adds robustness by not picking up on numbers
            # like "100." in a question which get misinterpreted.
            questionFound = True
            questionNumber = 1
            # track the page the last question ended on so we can start from
            # there in the next question
            lastPage = 0

            while questionFound:
                questionFound = False
                startPage = None
                endPage = None

                # start char is the question number followed by a full stop
                # this is the regex pattern to find the start of the question
                startCharPattern = re.compile(
                    r"{0}\.\s".format(questionNumber), re.DOTALL)
                startChar = f"{questionNumber}. "
                # end char is the next question number followed by a full stop
                # this is the regex pattern to find the end of the question
                endCharPattern = re.compile(
                    r"{0}\.\s".format(questionNumber + 1), re.DOTALL)
                # instead of using a pattern we can just look for the
                # next question number
                # pattern = r"{0}\..*?(?={1}\.)".format(
                #         questionNumber, questionNumber + 1)

                # if the end of exam page is reached
                isEndOfExam = False
                for index in range(lastPage, len(reader.pages), 1):
                    page = reader.pages[index]
                    text = page.extract_text()
                    if "end of paper" in text.lower():
                        isEndOfExam = True

                    # search for the start of the question
                    searchresult = re.search(startCharPattern, text)
                    if searchresult and not startPage:
                        startPage = index

                    # get the text with the square bracket before
                    # the next question number

                    # searchresult = re.search(pattern, text, re.DOTALL)

                    # search for the end of the question
                    searchresult = re.search(
                        endCharPattern, text)

                    if (searchresult or isEndOfExam) and not endPage:
                        endPage = index

                    if startPage and endPage:
                        questionFound = True
                        break

                if startPage and endPage:
                    questionFound = True

                if questionFound:
                    images = []
                    startPos: int = -1
                    endPos: int = -1
                    startPoint: int = -1
                    endPoint: int = -1
                    for pageNumber in range(startPage, endPage + 1):
                        page = pdfDocument.load_page(pageNumber)
                        # get the bounding box of the page
                        pageRect = fitz.Rect(
                            0,
                            0,
                            page.mediabox_size.x,
                            page.mediabox_size.y
                            )
                        # get the text on the page
                        text: str = page.get_text("text")

                        # get the bounding box of the area based on start
                        # and end characters.
                        searchResult = re.search(
                            startCharPattern, text)
                        if searchResult:
                            startPos = searchResult.start()

                        # searchresult = re.search(pattern, text, re.DOTALL)
                        searchResult = re.search(
                            endCharPattern, text)
                        if searchResult:
                            endPos: int = searchResult.end()
                        elif isEndOfExam:
                            endPos = len(text)
                        # count number of square brackets
                        # this is used to find the end of the question
                        # and therefore the end of the snapshot
                        numberOfSquareBrackets = len(re.findall(
                            r"\s\[\d+]", text[:endPos+1]
                        ))

                        if startPos == -1 and endPos == -1:
                            # neither start nor end are on this page
                            # so take a snapshot of the whole page
                            images.append(page.get_pixmap())
                            continue

                        # use the searchFor method to find the bounding box
                        # of the desired area.

                        searchRect = fitz.Rect(pageRect.tl, pageRect.br)
                        if startPos != -1:
                            searchResults = page.search_for(
                                startChar,
                                hit_max=1,
                                quads=True,
                                rect=searchRect
                                )
                            if not searchResults:
                                continue

                            startPoint = searchResults[0].ul

                        else:
                            startPoint = pageRect.tl

                        if endPos != -1:
                            searchResults = page.search_for(
                                "]",
                                hit_max=1,
                                quads=True,
                                rect=searchRect
                                )
                            if not searchResults:
                                continue

                            # final square bracket should be used
                            # as the end point
                            endPoint = searchResults[
                                numberOfSquareBrackets-1].lr
                        else:
                            endPoint = pageRect.br

                        # taking a snapshot of the area
                        # and appending it to the list of images
                        x0, y0 = startPoint[:2]
                        x1, y1 = endPoint[:2]

                        # make the snapshot rectangle, and add a small
                        # margin on all sides
                        snapshotRect = fitz.Rect(
                            x0 - 5,
                            y0 - 5,
                            x1 + 5,
                            y1 + 5
                            )

                        image = page.get_pixmap(
                            matrix=fitz.Matrix(2, 2),
                            clip=snapshotRect
                        )
                        images.append(image)

                    # add the images to the output dictionary
                    output[f"{questionNumber}"] = images
                    questionNumber += 1
                    lastPage = endPage
                else:
                    break
        return output
    except FileNotFoundError as e:
        print(e)
        return None


if __name__ == "__main__":
    # test the function
    path = r"C:\Users\danie\OneDrive\Projects\ExamProject V2\Questions\Scripts\pdfs\2017 Component 1.pdf"
    output = ExtractQuestionSnapshots(path)
    print(output)
    for key in output.keys():
        print(key)
        for image in output[key]:
            # save image
            image.save("snapshot{}.png".format(key), "PNG")
