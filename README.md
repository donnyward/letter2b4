# Dependencies

Setup a Python virtual environment and install dependencies.

`python3 -m venv env`
`cd env`
`source bin/activate.fish`
`pip install pymupdf`

# Usage

1. Rasterize the PDF, scale to print on B4, and add cutting guides.

`python letter2b4.py file.pdf`

2. Rasterization balloons the file size. Use Ghostscript to compress.

# Ghostscript commands to compress the output PDF

## Low quality

`gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/screen -dColorImageDownsampleType=/Bicubic -dColorImageResolution=72 -dGrayImageDownsampleType=/Bicubic -dGrayImageResolution=72 -dMonoImageDownsampleType=/Subsample -dMonoImageResolution=72 -sOutputFile=output.pdf input.pdf`

## Medium quality

`gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/ebook -dColorImageDownsampleType=/Bicubic -dColorImageResolution=150 -dGrayImageDownsampleType=/Bicubic -dGrayImageResolution=150 -dMonoImageDownsampleType=/Subsample -dMonoImageResolution=150 -dJPEGQ=90 -sOutputFile=output_medium.pdf input.pdf`

## High quality

`gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/prepress -dColorImageDownsampleType=/Bicubic -dColorImageResolution=300 -dGrayImageDownsampleType=/Bicubic -dGrayImageResolution=300 -dMonoImageDownsampleType=/Subsample -dMonoImageResolution=300 -dJPEGQ=95 -sOutputFile=output_high.pdf input.pdf`

# Optional resizing

Rename your PDF to `existing.pdf` and run `pdflatex resize.tex` to resize it to
8.5 x 11 inches.
