# inspired by https://gist.github.com/franquis/9fcfa3676a53ddfc698005d8f93e0d82
# source (reverse): https://stackoverflow.com/a/5425501
# source (merge): https://stackoverflow.com/a/37945454

from pypdf import PdfWriter, PdfReader, PdfMerger
from pathlib import Path

# pdfs = ['file1.pdf', 'file2.pdf', 'file3.pdf', 'file4.pdf']
# pdfList = ['reversed_Bild (3).pdf','reversed_Bild (2).pdf'] # absteigend sortieren, weil neuester Scan älteste Einträge enthält


def findByCriterions(*criterions, dirPath=Path.cwd()): # derived from verticalHighlightMaker.py: https://github.com/Sammeeey/verticalHighlightMaker/blob/f9f17c57b90cd36e1ccf9ce54724ac880f707ffa/verticalHighlightMaker.py#LL83C1-L103C24
    """
    - dirPath: takes pathlib.Path path for directory
    - criterions: takes glob pattern(s) (unix filename pattern): https://docs.python.org/3/library/fnmatch.html#module-fnmatch
    - finds files in specified directory (dirPath) based on certain glob pattern (criterions) & saves them in one list

    returns (possibly empty) list of pathlib.Path file-paths, which match specified criterion(s) inside specified directory

    example:
    resultList = findByCriterion(fr'*nterview.mp4', dirPath=p)
    print(resultList)
    """

    # identify all files in target directory, which match certain criterion (originally all those which match glob pattern)
    dirPath = Path(dirPath)
    filePathList = []
    for criterion in criterions:
        print(f'Finding all files in...\n{dirPath}\n...which match this criterion:{criterion}\n')
        # filePathList = list(dirPath.glob(criterion))
        filePathList += sorted(dirPath.glob(criterion))    # build ascending list: https://docs.python.org/3/library/pathlib.html#pathlib.Path.glob & https://docs.python.org/3/howto/sorting.html#sorting-basics
        print(filePathList)

    return filePathList


def reverse(pdfFileName):
    output_pdf = PdfWriter()

    with open(pdfFileName, 'rb') as readfile:
        input_pdf = PdfReader(readfile)
        total_pages = len(input_pdf.pages)
        for page in range(total_pages, 0, -1): # used like in comment here: https://stackoverflow.com/a/5425501/12946000
            # print(input_pdf)
            # print(input_pdf.pages)
            # print(page)
            output_pdf.add_page(input_pdf.pages[page-1])
        reversedName = f"reversed_{pdfFileName}.pdf"
        with open(reversedName, "wb") as writefile:
            output_pdf.write(writefile)

        return reversedName


def merge(pdfs: list):
    merger = PdfMerger()

    for pdf in pdfs:
        merger.append(pdf)

    resultName = 'merged.pdf'
    merger.write(resultName)
    merger.close()

    return resultName