# class for images
from PyQt5.QtGui import QPixmap
from typing import List
from sqlitehandler import SQLiteHandler


class Image:

    def __init__(self, name: str,
                 pixmap: QPixmap,
                 isMarkscheme: bool = False,
                 format: str = "png"):
        self.name = name
        self.pixmap = pixmap
        self.isMarkscheme = isMarkscheme
        self.format = format


def AreImagesAvailable(questionids: List[str], isMarkscheme=False) -> bool:
    """
    Checks if there are images available for the given questionids.
    If there is at least 1, return True, else False
    if markscheem is True, check for markscheme images,
    else check for normal images
    """
    if not questionids:
        return False
    for questionid in questionids:
        # check if the image is in the sqlite server
        sqlitehandler = SQLiteHandler()
        query = f"""
        SELECT * FROM Images
        WHERE QuestionID = '{questionid}'
        AND IsPartOfMarkscheme = {int(isMarkscheme)}
        """
        result = sqlitehandler.queryDatabase(query)
        if result:
            # if there is at least 1 image, return True
            return True

    return False
