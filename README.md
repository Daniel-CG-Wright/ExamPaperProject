# ExamPaperProject
This collated all the exam questions into a database.
It also provides a UI with some options to help with revision, such as random question generation, exam paper generation
and a question bank containing all the questions, and allowing them to be filtered.

## Important
This program runs a subprocess call to run pip if the required dependencies are not found on the Python environment.
They are found in RunFrontend.py
If you wish, you may delete these if you are scared of them. However, the program will still not run without the dependencies.

## Acknowledgements:
- Thank you very much to Muhie for having the idea of converting markschemes from PDFs to Word docs, this allowed for markscheme processing.
He also developed the Anki conversion to allow for Anki decks, and also suggeted using SQLite, making the program a lot easier
to use and more portable. He also helped test on Linux.

- Also thank you to Tamsin for giving me the idea of generating random exam papers after I complained of severe boredom too many times.
It also helped me come up with the idea for this program.

- Thank you to Evan for helping me test the program before release.

- Thank you to Oscar Detnon for the suggestion of placing an automatic pip call to try installing PyQt5 automatically if it could not be found.


## Dependencies:
- PyQT5
- python-docx

To run the pdf parsing (not for end user use):
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
