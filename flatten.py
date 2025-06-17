# Take input PDFs and rasterize them, so that they can be scaled onto B4 paper without issues
import fitz  # PyMuPDF
import sys
import os

def flatten_pdf_with_pymupdf(input_path, output_path):
    # Open the original PDF
    doc = fitz.open(input_path)
    # Create a new PDF document
    new_doc = fitz.open()
    
    # Process each page
    for page_num in range(len(doc)):
        page = doc[page_num]
        # Render the page with annotations into a pixmap (image)
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), annots=True)  # 2x resolution for clarity
        
        # Create a new page in the output PDF with the same dimensions
        new_page = new_doc.new_page(width=page.rect.width, height=page.rect.height)
        # Insert the rendered image into the new page
        new_page.insert_image(new_page.rect, pixmap=pix)
    
    # Save the new PDF
    new_doc.save(output_path)
    new_doc.close()
    doc.close()
    print(f"Flattened PDF saved as {output_path}")

def main():
    # Check if at least one PDF file is provided
    if len(sys.argv) < 2:
        print("Usage: python flatten_multiple_pdfs.py file1.pdf [file2.pdf ...]")
        sys.exit(1)
    
    # Process each input PDF
    for input_pdf in sys.argv[1:]:
        # Validate file exists and is a PDF
        if not os.path.isfile(input_pdf) or not input_pdf.lower().endswith('.pdf'):
            print(f"Skipping {input_pdf}: Not a valid PDF file")
            continue
        
        # Generate output filename
        base_name = os.path.splitext(input_pdf)[0]
        output_pdf = f"{base_name}_flattened.pdf"
        
        try:
            flatten_pdf_with_pymupdf(input_pdf, output_pdf)
        except Exception as e:
            print(f"Error processing {input_pdf}: {str(e)}")

if __name__ == "__main__":
    main()
