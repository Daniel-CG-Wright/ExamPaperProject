
# importing required modules
import PyPDF2
  
# creating a pdf file object
pdfFileObj = open('Component 2 Eduqas.pdf', 'rb')
  
# creating a pdf reader object
pdfReader = PyPDF2.PdfReader(pdfFileObj)
  
# printing number of pages in pdf file
print(len(pdfReader.pages))
  
# creating a page object
pageObj = pdfReader.pages[4]
  
# extracting text from page
print(pageObj.extract_text())
  
# closing the pdf file object
pdfFileObj.close()