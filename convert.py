import os
import re
import glob
import shutil
from pathlib import Path
from zipfile import ZipFile

source_path = './_markdowns/raw'
target_path = './_markdowns'

try:
    
    list_of_files = glob.glob(os.path.join(source_path,'*.zip'))
    latest_file = max(list_of_files, key=os.path.getctime)

    with ZipFile(latest_file, 'r') as zipobj:
        zipobj.extractall(source_path)
        
    image_paths = []
    for path in Path(source_path).rglob('*.png'):
        image_paths.append(path)
        
    def clean_path(x):
        x = ' '.join(x.split('\\'))
        x = re.sub(r'\S+\d+\S*', ' ', x)
        x = '-'.join(x.lower().split())
        return x

    for p in image_paths:
        newname = clean_path(str(p))
        os.rename(p, Path(os.path.join(p.parent,newname)))

    renamed_image_paths = []
    for path in Path(source_path).rglob('*.png'):
        renamed_image_paths.append(path)

    for p in renamed_image_paths:
        shutil.move(str(p), os.path.join(target_path,'img'))
        
    for opath, npath in zip(image_paths, renamed_image_paths):
        fin = open(str(opath.parent)+'.md', 'rt')
        data = fin.read()
        data = re.sub(r'!\[[^\]]*\]\((.*?)\s*("(?:.*[^"])")?\s*\)',
        f'![img/{npath.name}](img/{npath.name})', data)
        fin.close()
        fin = open(str(opath.parent)+'.md', "wt")
        fin.write(data)
        fin.close()
        
    md_paths = []
    for path in Path(source_path).rglob('*.md'):
        md_paths.append(path)

    for p in md_paths:
        newname = clean_path(p.name)+'.md'
        os.rename(p, Path(os.path.join(p.parent,newname)))
        
    for path in Path(source_path).rglob('*.md'):
        with open(path, 'r') as fin:
            data = fin.read().splitlines(True)
        with open(path, 'w') as fout:
            fout.writelines(data[2:])
        shutil.move(str(path), target_path)

    print('Done!')
    
except: 
    pass