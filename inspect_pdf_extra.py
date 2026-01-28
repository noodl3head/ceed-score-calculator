from pypdf import PdfReader

def inspect_pdf(filename):
    print(f"--- Inspecting {filename} ---")
    reader = PdfReader(filename)
    
    # Check for annotations
    has_annots = False
    for i, page in enumerate(reader.pages):
        if "/Annots" in page:
            has_annots = True
            print(f"Page {i+1} has annotations.")
            annots = page["/Annots"]
            for annot in annots:
                obj = annot.get_object()
                print(f"  Annot: {obj.get('/Subtype')}, Contents: {obj.get('/Contents')}")
    
    if not has_annots:
        print("No annotations found.")

    # Check for form fields
    fields = reader.get_fields()
    if fields:
        print("Form fields found:")
        for name, field in fields.items():
            print(f"  {name}: {field.get('/V')}")
    else:
        print("No form fields found.")

inspect_pdf("CEED_2026_Answer_Key.pdf")
