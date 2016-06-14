import os
import sys
import math
from selenium import webdriver
from PIL import Image
from tqdm import trange


def process_latlng(north, west, south, east, zoom, output='output/mosaic.png'):
    """
    download and mosaic by latlng
    """
    left, top = latlng2tilenum(north, west, zoom)
    right, bottom = latlng2tilenum(south, east, zoom)
    process_tilenum(left, right, top, bottom, zoom, output)


def process_tilenum(left, right, top, bottom, zoom, output='output/mosaic.png'):
    """
    download and mosaic by tile number 
    """
    for x in trange(left, right + 1):
        for y in trange(top, bottom + 1):
            path = './tiles/%i/%i/%i.png' % (zoom, x, y)
            if not os.path.exists(path):
                _download(x, y, zoom)
    _mosaic(left, right, top, bottom, zoom, output)


def _download(x, y, z):
    url = "http://mt1.google.cn/maps/vt?lyrs=s%40690&hl=zh-CN&gl=CN&&x={x}&y={y}&z={z}".format(x=x, y=y, z=z)

    path = './tiles/%i/%i' % (z, x)
    if not os.path.isdir(path):
        os.makedirs(path)
    driver = webdriver.PhantomJS()
    driver.get(url)
    name = '%s/%i.png' % (path, y)
    driver.save_screenshot(name)
    img = Image.open(name)
    img.crop((0, 0, 256, 256)).save(name, "png")
    driver.close()


def _mosaic(left, right, top, bottom, zoom, output):
    print('log')
    size_x = (right - left + 1) * 256
    size_y = (bottom - top + 1) * 256
    output_im = Image.new("RGB", (size_x, size_y))

    for x in trange(left, right + 1):
        for y in trange(top, bottom + 1):
            path = './tiles/%i/%i/%i.png' % (zoom, x, y)
            target_im = Image.open(path)
            output_im.paste(target_im, (256 * (x - left), 256 * (y - top)))
    output_path = os.path.split(output)
    if len(output_path) > 1 and len(output_path) != 0:
        if not os.path.isdir(output_path[0]):
            os.makedirs(output_path[0])
    output_im.save(output)


def latlng2tilenum(lat_deg, lng_deg, zoom):
    """
    referencing http://www.cnblogs.com/Tangf/archive/2012/04/07/2435545.html
    """
    n = math.pow(2, int(zoom))
    xtile = ((lng_deg + 180) / 360) * n
    lat_rad = lat_deg / 180 * math.pi
    ytile = (1 - (math.log(math.tan(lat_rad) + 1 / math.cos(lat_rad)) / math.pi)) / 2 * n
    return math.floor(xtile), math.floor(ytile)


def test():
    process_latlng(22.8203395702, 115.134878259, 22.8016510269, 115.1763224812, 18, 'output/houmen.png')


def cml():
    if not len(sys.argv) in [6, 7]:
        print('input 6 parameter northeast latitude,northeast longitude, southeast latitude, southeast longitude,zoom, output file')
        return
    process_latlng(float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5]), str(sys.argv[6]))

if __name__ == '__main__':
    test()
    # cml()
