from rmPDF import reverse
import os
from pathlib import Path

reversePdfPath = input(f'full path to PDF file to reverse? ')
reversePdfPath = Path(reversePdfPath)
print(reversePdfPath)
print(type(reversePdfPath))

reverseDir = reversePdfPath.parent
print(f'reverseDir: {reverseDir}')
reverseFilename = reversePdfPath.name
print(f'reverseFilename: {reverseFilename}')

os.chdir(reverseDir)
reverse(reverseFilename)