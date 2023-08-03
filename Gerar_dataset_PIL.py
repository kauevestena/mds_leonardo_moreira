import rasterio
from rasterio.windows import Window
import numpy as np
from rasterio.crs import CRS

def split_images(src_path_hr, src_path_lr, dst_path_hr, dst_path_lr, tile_size_hr, tile_size_lr, overlap):
    crs_hr = CRS.from_epsg(4326)  # Defina o EPSG correto para o CRS da imagem de alta resolução
    crs_lr = CRS.from_epsg(4326)  # Defina o EPSG correto para o CRS da imagem de baixa resolução

    with rasterio.open(src_path_hr, crs=crs_hr) as src_hr, rasterio.open(src_path_lr, crs=crs_lr) as src_lr:
        profile_hr = src_hr.profile
        profile_lr = src_lr.profile
        tile_size_x_hr = tile_size_y_hr = tile_size_hr
        tile_size_x_lr = tile_size_y_lr = tile_size_lr
        overlap_x_hr = overlap_y_hr = int(overlap * tile_size_hr)
        overlap_x_lr = overlap_y_lr = int(overlap * tile_size_lr)

        for i_hr in range(0, src_hr.width, tile_size_x_hr - overlap_x_hr):
            for j_hr in range(0, src_hr.height, tile_size_y_hr - overlap_y_hr):
                # Calculate the corresponding position in the low-resolution image
                i_lr = i_hr // 4
                j_lr = j_hr // 4

                # Calculate the tile size and overlap for the low-resolution image
                tile_size_x_lr = tile_size_y_lr = tile_size_hr // 4
                overlap_x_lr = overlap_y_lr = int(overlap * tile_size_lr) // 4

                window_hr = Window(i_hr, j_hr, tile_size_x_hr, tile_size_y_hr)
                transform_hr = src_hr.window_transform(window_hr)
                data_hr = src_hr.read(window=window_hr)

                window_lr = Window(i_lr, j_lr, tile_size_x_lr, tile_size_y_lr)
                transform_lr = src_lr.window_transform(window_lr)
                data_lr = src_lr.read(window=window_lr)

                # Check if tile is completely contained within the image bounds
                if i_hr + tile_size_x_hr > src_hr.width:
                    width_hr = src_hr.width - i_hr
                    width_lr = width_hr // 4
                else:
                    width_hr = tile_size_x_hr
                    width_lr = tile_size_x_lr
                if j_hr + tile_size_y_hr > src_hr.height:
                    height_hr = src_hr.height - j_hr
                    height_lr = height_hr // 4
                else:
                    height_hr = tile_size_y_hr
                    height_lr = tile_size_y_lr

                # Create destination profiles
                dst_profile_hr = profile_hr.copy()
                dst_profile_hr.update({
                    'height': height_hr,
                    'width': width_hr,
                    'transform': transform_hr,
                    'driver': 'GTiff',
                    'compress': 'lzw'
                })
                dst_profile_lr = profile_lr.copy()
                dst_profile_lr.update({
                    'height': height_lr,
                    'width': width_lr,
                    'transform': transform_lr,
                    'driver': 'GTiff',
                    'compress': 'lzw'
                })

                # Write tiles to disk
                with rasterio.open(dst_path_hr.format(i_hr, j_hr), 'w', **dst_profile_hr) as dst_hr, \
                     rasterio.open(dst_path_lr.format(i_hr, j_hr), 'w', **dst_profile_lr) as dst_lr:
                    dst_hr.write(data_hr)
                    dst_lr.write(data_lr)

# Example usage
src_path_hr = 'rasteres_finais_kaue/pegasus_1m.tif'
src_path_lr = 'rasteres_finais_kaue/pegasus_4m.tif'
dst_path_hr = 'hr/high_{}_{}.tif'
dst_path_lr = 'lr/low_{}_{}.tif'
tile_size_hr = 156 # for high resolution, 39 for low resolution
tile_size_lr = 39
overlap = 0.0 # 80% overlap

#import os
#os.environ["GDAL_DATA"] = "C:/Program Files/PostgreSQL/13/share/contrib/postgis-3.1/proj"

split_images(src_path_hr, src_path_lr, dst_path_hr, dst_path_lr, tile_size_hr, tile_size_lr, overlap)