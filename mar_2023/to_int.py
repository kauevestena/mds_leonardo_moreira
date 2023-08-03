import cv2
import numpy as np
from lib import *

inpath = 'MDS_ALTM_fusao_4m.tif'

outpath = 'MDS_ALTM_fusao_4m_int.tif'


img,mdata_dict = gdal_to_np(inpath)

img = np.int16(img)


np_to_gdal(img,mdata_dict,outpath)