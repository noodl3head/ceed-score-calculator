from pypdf import PdfReader

reader = PdfReader("CEED_2026_Answer_Key (1).pdf")
page = reader.pages[1] # Page 2 is index 1
print(page.extract_text())
