from PIL import TiffImagePlugin
TiffImagePlugin.DEBUG = True
with open('pegasus_1m.tif', 'rb') as f:
    TiffImagePlugin.TiffImageFile(f)