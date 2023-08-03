try:
    from osgeo import gdal
except:
    import gdal

import os

def gdal_to_np(inputpath,band=1,print_dict=False):
    img = gdal.Open(inputpath)

    data = img.GetRasterBand(band)
    mat = data.ReadAsArray()

    infos_dict = {}
    infos_dict["NoData"] = data.GetNoDataValue()   
    infos_dict["nBands"] = img.RasterCount      
    infos_dict["nRows"] = img.RasterYSize      
    infos_dict["nCols"] = img.RasterXSize      
    infos_dict["dType"] = data.DataType       
    infos_dict["GeoTransform"] = img.GetGeoTransform()
    infos_dict["Projection"] = img.GetProjection()

    img = None

    if print_dict:
        print(infos_dict)

    return mat,infos_dict

#   GDT_Unknown = 0, GDT_Byte = 1, GDT_UInt16 = 2, GDT_Int16 = 3,
#   GDT_UInt32 = 4, GDT_Int32 = 5, GDT_Float32 = 6, GDT_Float64 = 7,
#   GDT_CInt16 = 8, GDT_CInt32 = 9, GDT_CFloat32 = 10, GDT_CFloat64 = 11,
#   GDT_TypeCount = 12

def np_to_gdal(data,infos_dict,outpath,band=1,use_zero_nodata=False,new_dtype=3):
    driver = gdal.GetDriverByName('GTiff')

    if new_dtype:
        infos_dict["dType"] = new_dtype

    outDs = driver.Create(outpath, infos_dict["nCols"], infos_dict["nRows"], infos_dict["nBands"], infos_dict["dType"])
    outBand = outDs.GetRasterBand(band)
    outBand.WriteArray(data, 0, 0)
    if infos_dict["NoData"]:
        outBand.SetNoDataValue(infos_dict["NoData"])
    else:
        if use_zero_nodata:
            outBand.SetNoDataValue(0)
    outDs.SetGeoTransform(infos_dict["GeoTransform"])
    outDs.SetProjection(infos_dict["Projection"])
    outBand.FlushCache()

    outDs = None

def remove_if_exists(filepath):
    if os.path.exists(filepath):
        os.remove(filepath)

def remove_if_exists2(filepath,ending='.aux.xml'):
    remove_if_exists(filepath)
    remove_if_exists(filepath+ending)

