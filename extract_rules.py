from pypdf import PdfReader

reader = PdfReader("CEED_2026_Question_Paper.pdf")
page = reader.pages[1] # Page 2 is index 1
print(page.extract_text())
