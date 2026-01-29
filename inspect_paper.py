from pypdf import PdfReader

reader = PdfReader("CEED_2026_Answer_Key (1).pdf")
with open("paper_text.txt", "w", encoding="utf-8") as f:
    for i in range(min(10, len(reader.pages))):
        f.write(f"--- Page {i+1} ---\n")
        f.write(reader.pages[i].extract_text())
        f.write("\n\n")
