# python tiff to pdf inspired by https://stackoverflow.com/a/68336325

from PIL import Image, ImageSequence
import os

def tiff_to_pdf(tiff_path: str) -> str:
    # check if file extension with 1 or 2 ff in .tiff
    twoF = '.tiff' in tiff_path
    # print(f'tiff in path? {twoF}')
    oneF = '.tif' in tiff_path
    # print(f'tif in path? {oneF}')

    if twoF:
        tiffExtension = '.tiff'
    elif oneF:
        tiffExtension = '.tif'

    pdf_path = tiff_path.replace(tiffExtension, '.pdf')
    if not os.path.exists(tiff_path): raise Exception(f'{tiff_path} does not find.')
    image = Image.open(tiff_path)

    images = []
    for i, page in enumerate(ImageSequence.Iterator(image)):
        page = page.convert("RGB")
        images.append(page)
    if len(images) == 1:
        images[0].save(pdf_path)
    else:
        images[0].save(pdf_path, save_all=True,append_images=images[1:])

    # print(images)
    return pdf_path


# --- get input
tiffPath = input('.tiff path?')
tiff_to_pdf(tiffPath)