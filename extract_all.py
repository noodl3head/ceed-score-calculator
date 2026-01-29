from pypdf import PdfReader

def extract_text(filename, out_file):
    reader = PdfReader(filename)
    with open(out_file, "w", encoding="utf-8") as f:
        for i, page in enumerate(reader.pages):
            f.write(f"--- Page {i+1} ---\n")
            f.write(page.extract_text())
            f.write("\n\n")

extract_text("CEED_2026_Answer_Key (1).pdf", "answer_key_text.txt")
extract_text("response.pdf", "response_text.txt")
