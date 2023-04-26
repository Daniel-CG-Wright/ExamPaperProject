# ExamPaperProject - Staff View
This collated all the exam questions into a database.
The UI provided with this version is for teaching use.
It provides the question bank view available to students, as well as the ability
to add new exam papers to the database. It also gives the ability to add questions
manually, or edit or delete them.
It does not have the capability to generate a random question or exam paper. This is
only available in the student (ExamPaperProject) version.
This version = 1.2

## Important
This program runs a subprocess call to run pip if the required dependencies are not found on the Python environment.
They are found in RunFrontend.py
If you wish, you may delete these subprocess calls if you are scared of them. However, the program will still not run without the dependencies.

## Acknowledgements:
- Thank you very much to Muhie for having the idea of converting markschemes from PDFs to Word docs, this allowed for markscheme processing.
He also developed the Anki conversion to allow for Anki decks, and also suggeted using SQLite, making the program a lot easier
to use and more portable. He also helped test on Linux.

- Also thank you to Tamsin for giving me the idea of generating random exam papers after I complained of severe boredom too many times.
It also helped me come up with the idea for this program.

- Thank you to Evan for helping me test the program before release.

- Thank you to Oscar Detnon for the suggestion of placing an automatic pip call to try installing PyQt5 automatically if it could not be found.

- Thank you to Kian for the line to correct for high DPI screens.

## Dependencies (already installed on school PCs):
- PyQT5
- python-docx
- PyPDF2

Made with Python 3.10, but should be backward compatible for a few versions.


## Use:
Run the RunFrontend.py file. Don't move it from its initial directory.
For help on using the program itself see the HowToUse.txt file


## FAQs/troubleshooting
**Fatal Python Error**
- From reports I have heard, it can be caused by multiple versions of Python conflicting. Try uninstalling all versions of Python and reinstalling the latest one, then reinstalling dependencies.

**Could not find ExamQuestions.db**
- Make sure your current working directory is in Scripts. If using VScode, then closing it and reopening it by opening the RunFrontend.py file should work.

Please note there are likely issues with the following features in non-Windows environments:
- Saving markschemes and papers to .txt / Word docx

This is due to not having implemented cross-platform capabilities fully yet. This is a low priority as it does not affect most features.


Github (contains the PDF parser, .ui files etc):
https://github.com/Daniel-CG-Wright/ExamPaperProject

Created by Daniel Wright
