from skimage import io
from skimage.util import view_as_windows

def create_image_pairs(high_res_path, low_res_path, high_res_size, low_res_size):
    high_res_image = io.imread(high_res_path)
    low_res_image = io.imread(low_res_path)

    high_res_height, high_res_width = high_res_image.shape[:2]
    low_res_height, low_res_width = low_res_image.shape[:2]

    if high_res_height % high_res_size != 0 or high_res_width % high_res_size != 0:
        raise ValueError("O tamanho da janela não é compatível com a forma da imagem de alta resolução.")

    high_res_patches = view_as_windows(high_res_image, (high_res_size, high_res_size, 3), high_res_size)
    low_res_patches = view_as_windows(low_res_image, (low_res_size, low_res_size, 3), low_res_size)

    pairs = []

    for i in range(high_res_patches.shape[0]):
        for j in range(high_res_patches.shape[1]):
            high_res_crop = high_res_patches[i, j, 0]

            low_res_x = j * (high_res_size // low_res_size)
            low_res_y = i * (high_res_size // low_res_size)
            low_res_crop = low_res_patches[i, j, 0]

            pair = {
                'high_res_crop': high_res_crop,
                'low_res_crop': low_res_crop,
                'name': f'{i}_{j}'  # Nome do recorte
            }

            pairs.append(pair)

    return pairs

# Exemplo de uso
high_res_path = 'D:\\dataset_nuvem_pontos_Pegasus_1m_4m\\pegasus_morph_filtered_1m_4326.tif'
low_res_path = 'D:\\dataset_nuvem_pontos_Pegasus_1m_4m\\pegasus_morph_filtered_4m_4326.tif'
high_res_size = 156
low_res_size = 39

pairs = create_image_pairs(high_res_path, low_res_path, high_res_size, low_res_size)

# Iterando pelos pares de recortes
for pair in pairs:
    high_res_crop = pair['high_res_crop']
    low_res_crop = pair['low_res_crop']
    name = pair['name']

    # Faz algo com os recortes ou o nome...
    # Por exemplo, salvar os recortes em arquivos:
    io.imsave(f'D:\\dataset_nuvem_pontos_Pegasus_1m_4m\\recortes\\alta\\{name}.tif', high_res_crop)
    io.imsave(f'D:\\dataset_nuvem_pontos_Pegasus_1m_4m\\recortes\\baixa\\{name}.tif', low_res_crop)