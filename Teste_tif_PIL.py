import os
from PIL import Image


imagem = Image.open('pegasus_1m.tif')

print(imagem.tag)

compressao = imagem.tag[259]  # Código 259 representa a compressão TIFF

if compressao == 5:
    print("A imagem está no formato de compressão LZW, semelhante ao SRTM.")
else:
    print("A imagem não está no mesmo formato de compressão do SRTM.")