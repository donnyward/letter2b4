import fitz  # PyMuPDF
import sys
import os

def process_pdf(input_path, output_path):
    # Define dimensions in points (1 inch = 72 points, 1 mm ≈ 2.83465 points)
    us_letter_width = 8.5 * 72   # 612 points
    us_letter_height = 11 * 72   # 792 points
    b4_width = 250 * 2.83465     # ≈708.66 points
    b4_height = 353 * 2.83465    # ≈1000.63 points
    
    # Calculate margins to center US Letter content on B4
    margin_x = (b4_width - us_letter_width) / 2   # ≈48.33 points
    margin_y = (b4_height - us_letter_height) / 2 # ≈104.315 points
    
    # Open the input PDF
    doc = fitz.open(input_path)
    # Create a new PDF document for flattened and scaled output
    new_doc = fitz.open()
    
    # Process each page
    for page_num in range(len(doc)):
        page = doc[page_num]
        # Flatten: Render the page with annotations into a pixmap
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), annots=True)  # 2x resolution for clarity
        
        # Create a new B4-sized page
        new_page = new_doc.new_page(width=b4_width, height=b4_height)
        
        # Define the rectangle for the US Letter content
        content_rect = fitz.Rect(margin_x, margin_y, margin_x + us_letter_width, margin_y + us_letter_height)
        
        # Insert the flattened image into the centered US Letter area
        new_page.insert_image(content_rect, pixmap=pix)
        
        # Draw crop marks (10-point lines) at the corners of the US Letter area
        crop_mark_length = 10
        # Top-left corner
        new_page.draw_line((margin_x, margin_y), (margin_x + crop_mark_length, margin_y))  # Horizontal
        new_page.draw_line((margin_x, margin_y), (margin_x, margin_y + crop_mark_length))  # Vertical
        # Top-right corner
        new_page.draw_line((margin_x + us_letter_width - crop_mark_length, margin_y), (margin_x + us_letter_width, margin_y))  # Horizontal
        new_page.draw_line((margin_x + us_letter_width, margin_y), (margin_x + us_letter_width, margin_y + crop_mark_length))  # Vertical
        # Bottom-left corner
        new_page.draw_line((margin_x, margin_y + us_letter_height), (margin_x + crop_mark_length, margin_y + us_letter_height))  # Horizontal
        new_page.draw_line((margin_x, margin_y + us_letter_height - crop_mark_length), (margin_x, margin_y + us_letter_height))  # Vertical
        # Bottom-right corner
        new_page.draw_line((margin_x + us_letter_width - crop_mark_length, margin_y + us_letter_height), (margin_x + us_letter_width, margin_y + us_letter_height))  # Horizontal
        new_page.draw_line((margin_x + us_letter_width, margin_y + us_letter_height - crop_mark_length), (margin_x + us_letter_width, margin_y + us_letter_height))  # Vertical
    
    # Save the output PDF
    new_doc.save(output_path)
    new_doc.close()
    doc.close()
    print(f"Processed PDF saved as {output_path}")

def main():
    # Check if at least one PDF file is provided
    if len(sys.argv) < 2:
        print("Usage: python flatten_and_scale_to_b4.py file1.pdf [file2.pdf ...]")
        sys.exit(1)
    
    # Process each input PDF
    for input_pdf in sys.argv[1:]:
        # Validate file exists and is a PDF
        if not os.path.isfile(input_pdf) or not input_pdf.lower().endswith('.pdf'):
            print(f"Skipping {input_pdf}: Not a valid PDF file")
            continue
        
        # Generate output filename
        base_name = os.path.splitext(input_pdf)[0]
        output_pdf = f"{base_name}_flattened_b4_with_guides.pdf"
        
        try:
            process_pdf(input_pdf, output_pdf)
        except Exception as e:
            print(f"Error processing {input_pdf}: {str(e)}")

if __name__ == "__main__":
    main()
