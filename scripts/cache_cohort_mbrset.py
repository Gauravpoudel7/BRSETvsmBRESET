import sys; sys.path.insert(0,'.'); sys.path.insert(0,'scripts')
import pandas as pd
from pathlib import Path
from PIL import Image
from build_image_cache import resize_short_side
from src.data import cache_filename
d=pd.read_csv('data/splits/cohorts/ext_mbrset_steep.csv'); out=Path('C:/data/cache_256/mbrset'); n=0
for f in d.file:
    dst=out/cache_filename(f)
    if dst.exists(): continue
    im=Image.open(Path('C:/data/brset_mbrset/mbrset/1.0/images')/f).convert('RGB'); resize_short_side(im).save(dst,quality=95); n+=1
print('cached new',n)
