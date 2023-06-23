## flask [on PythonAnywhere](http://sammeeey.pythonanywhere.com/)
> https://flask.palletsprojects.com/en/2.3.x/deploying/
- works to some extend
  - works when uploading 1-2 files
  - fails when uploading more than 1-2 files (*The connection was reset*-error)
- **stopped** working on it intentionally
  - rather focus on improving fundamental JS, CSS, HTML skills & build up language- & hosting tech stack that works for real world projects long-term instead of tinkering with so-so-tech-stack/hosting
### [setup steps on PythonAnywhere](https://help.pythonanywhere.com/pages/Flask/)
- create new flask project on pythonanywhere
- put `app.py` and other files (`requirements.txt`, `rmPDF.py`, `tiff2pdf.py`, `/venv`) into root directory (`/home/Sammeeey/`) of flask project on pythonanywhere
- go to `Web` tab in navigation of pythonanywhere & add path to venv directory into *Virtualenv* section

---
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