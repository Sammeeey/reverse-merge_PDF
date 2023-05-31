# rmPDF
> built & *tested* using Python 3.11.3

Reverses order of pages in multiple PDFs in working directory.
Then merges them into one large PDF & saves it to working directory.


## Installation (on windows 10)
1. clone repo
2. enter repo directory: `cd rmPDF`
3. create virtual environment: `py -m venv venv`
4. activate virtual environment: `venv\Scripts\activate.bat`
5. update pip: `py -m pip install --upgrade pip`
6. install requirements: `pip install -r requirements.txt`
7. run program as described below (*Usage*)

## Usage (on windows 10)
1.  have multuiple multi-pages PDFs in working directory
2. run `py rmPDF.py`

## Quickstart
<!-- 1. run `py ocr.py`
1. press Enter to use sample PDFs in `./samplePDFs` subdirectory by default -->
- (see **Usage** above)

## What happens
1. Finds all files based on certain criterion in directory (currently `Bild*.pdf`) 
2. Reverses order of pages in PDFs
3.  Merges reverse-ordered PDFs into one final PDF (currently `merged.pdf`)

## Resources
- [reverse](https://stackoverflow.com/a/5425501)
- [merge](https://stackoverflow.com/a/37945454)

### sample PDFs
- https://www.africau.edu/images/default/sample.pdf
- https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf
- https://www.adobe.com/support/products/enterprise/knowledgecenter/media/c4611_sample_explain.pdf
- https://unec.edu.az/application/uploads/2014/12/pdf-sample.pdf
- https://file-examples.com/index.php/sample-documents-download/sample-pdf-download/
- https://www.orimi.com/pdf-test.pdf

## Limitations / Known Issues
- **highly spicific use case** (basically function-based script)
  - expects `*Bild (integer).pdf` files and one `*Bild.pdf` file
  - saves reversed PDFs in directory
  - saves final file as `merged.pdf`
<!-- - potentially inaccurate - depending on quality, structure & content of input PDFs (images, charts, ...) -->

## Potential Improvements
<!-- - adjust OCR settings to *real world* input PDFs (to achieve best results for expected input)
- create REST API to get share results with clients (long-term?)
  - authentication & encryption (e.g. using JSON Web Token) -->