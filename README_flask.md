## algo
- upload multiple pdfs -> give back as one reverse-merged pdf


## steps
- [ ] upload & handle pdf(s)
  - [x] save pdfs on server (temporarily)
  - [ ] reverse-merge pdfs using existing modification files
    - [ ] create folder inside `/uploads` for uploaded files - named with unique hash
      - [x] if tif/tiff: convert to pdf (`tiff2pdf.py`)
      - [x] use `rmPDF.py` features to reverse-merge pdfs in folder
        - [x] `Bild*` as default file stem, `merged.pdf` as default final file
- [x] give back 1 downloadable reverse-merged pdf file
- [x] delete pdfs after download

## todo
- [ ] put imports at beginning of app.py
- [ ] deploy
- [ ] use internal tools (`Flask.request.files`) to handle files & lists of files instead of using Python built-in library