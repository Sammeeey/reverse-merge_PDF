from rmPDF import *

pdfList = findByCriterions("Bild*.pdf")
print(f'pdfList: {pdfList}')

pdfNameList = []
for path in pdfList:
    pathName = path.name
    pdfNameList.append(pathName)
print(f'pdfNameList: {pdfNameList}')

# sort names of pdf files inside list descending (based on integer in file format `Bild (10).pdf` if(!) integer available, else ignore respective item (Bild.pdf)!?)
sortedNameList = sorted(pdfNameList, key=lambda x: int(x.split('(')[-1].split(')')[0]) if '(' in x else float('inf'), reverse=True)
# move `Bild.pdf` to end of sorted list manually: https://www.geeksforgeeks.org/python-move-element-to-end-of-the-list/
sortedNameList.append(sortedNameList.pop(sortedNameList.index('Bild.pdf')))
print(f'sortedNameList: {sortedNameList}')

reversedNameList = []
# reverse order of every single pdf
for pdf in sortedNameList:
    reversedPdf = reverse(pdf)
    print(f"Reversed file {pdf} into {reversedPdf}")
    reversedNameList.append(reversedPdf)
print(f"Reversed files: {reversedNameList}")

mergedPdf = merge(reversedNameList)
print(f"Merged files {reversedNameList} into {mergedPdf}")