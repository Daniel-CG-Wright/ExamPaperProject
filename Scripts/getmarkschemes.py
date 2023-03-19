from ParsingOfData.markschemereader import MarkschemeParser
from pathlib import Path
from typing import Dict


# return the dictionary of markschemes for each paper
def main() -> Dict[str, MarkschemeParser]:
    dictionary: Dict[str, MarkschemeParser] = {}

    files = list((Path.cwd() / "markschemes").rglob('*.docx'))
    for file in files:
        print("Markscheme processing: " + str(file))
        filename = str(file).rpartition(".docx")[0]
        reader = MarkschemeParser(filename)
        paperid = f"{reader.level}-{reader.component}-{reader.year}"
        dictionary[paperid] = reader
    return dictionary
