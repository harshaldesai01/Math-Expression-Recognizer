import os
from inkml2img import inkml2img

path = os.getcwd()

# path = os.getcwd()
files = os.listdir(path+'/data/train')
for file in tqdm(files):
    inkml2img(path+'/data/train/'+file, './Image_data/finaltrain/')
