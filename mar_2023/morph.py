import cv2
import numpy as np
from lib import *
import os, subprocess

MIN_VALUE = 891

# para operação de dilatação:
inpath = 'MDS_Pegasus_registrada_1m.tif'

outpath = 'filled_pegasus_1m_x10.tiff'

out_morph = 'pegasus_morph_filtered_1m_x10.tiff'

out_mask = 'mask_filtered_1m_x10.tiff'

out_fillers = 'fillers_1m_x10.tiff'

inpainted_outpath = 'inpainted_1m_x10.tiff'

four_m_degrees = 0.000039718427608012104

for path in[outpath,out_morph,out_mask,out_fillers,inpainted_outpath]:
    remove_if_exists2(path)


# img = cv2.imread(path_im1,cv2.IMREAD_UNCHANGED)
img,mdata_dict = gdal_to_np(inpath)#,print_dict=True)


img = img.astype(np.float32)

# mask:
mask = cv2.inRange(img, 0, MIN_VALUE)

'''
    inpaint: https://docs.opencv.org/4.x/d7/d8b/group__photo__inpaint.html#gaedd30dfa0214fec4c88138b51d678085

    cv2.INPAINT_TELEA

    or

    cv2.INPAINT_NS

'''



inpaint = cv2.inpaint(img,mask,10,cv2.INPAINT_NS)


"""

MORPH_ERODE 
MORPH_DILATE
MORPH_CLOSE
MORPH_OPEN

https://docs.opencv.org/4.x/d4/d86/group__imgproc__filter.html#ga7be549266bad7b2e6a04db49827f9f32 

"""
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))

operation = cv2.MORPH_ERODE

dilated_img = cv2.morphologyEx(inpaint,kernel=kernel,op=operation)

only_filled = cv2.bitwise_and(dilated_img,dilated_img,mask=mask)

out_img = cv2.max(img,only_filled)

for matrix,outpath in ((out_img,outpath),
                     (dilated_img,out_morph),
                     (mask,out_mask),
                     (only_filled,out_fillers),
                     (inpaint,inpainted_outpath),
                     ):
    

    
    matrix = np.int16(matrix*10)

    np_to_gdal(matrix,mdata_dict,outpath,use_zero_nodata=True)

    outpath_4326 = outpath.replace('.tiff','_4326.tiff')
    subprocess.run(f'gdalwarp -r cubic -overwrite -srcnodata 890 -t_srs EPSG:4326 {outpath} {outpath_4326}',shell=True)

    outpath_4m = outpath_4326.replace('.tiff','_4m.tiff')
    subprocess.run(f'gdalwarp -r cubic -overwrite -srcnodata 890 -tr {four_m_degrees} {four_m_degrees} {outpath_4326} {outpath_4m}',shell=True)
# np_to_gdal(out_img,mdata_dict,outpath,use_zero_nodata=True)
# np_to_gdal(dilated_img,mdata_dict,out_morph,use_zero_nodata=True)
# np_to_gdal(mask,mdata_dict,out_mask,use_zero_nodata=True)
# np_to_gdal(only_filled,mdata_dict,out_fillers,use_zero_nodata=True)
# np_to_gdal(inpaint,mdata_dict,inpainted_outpath,use_zero_nodata=True)

