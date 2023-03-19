# convert markschemes from pdf to word.
import aspose.words as aw
from pathlib import Path


def main():
    files = list((Path.cwd() / "markschemes").rglob('*.pdf'))
    for file in files:
        print("processing " + str(file.name))
        doc = aw.Document(str(file))
        doc.save("markschemes/" + file.name + ".docx")


if __name__ == "__main__":
    main()
