import skimage.io as skio
import numpy as np

# Ler a imagem TIFF
imagem_tiff = skio.imread('D:/dataset_nuvem_pontos_Pegasus_1m_4m/pegasus_morph_filtered_4m.tif')

# Converter para int16
imagem_int16 = imagem_tiff.astype(np.int16)

# Salvar como arquivo TIFF
skio.imsave('D:/dataset_nuvem_pontos_Pegasus_1m_4m/pegasus_morph_filtered_4m_16.tif', imagem_int16)