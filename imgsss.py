from PIL import Image
import os
mpath = './user/screenshot.png'
print(mpath)
im = Image.open(mpath)
im = im.crop((291, 177, 713, 599))
im.save('./user/QRCode.png','png')
im.show()


