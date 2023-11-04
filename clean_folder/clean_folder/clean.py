import sys
from pathlib import Path
import re
import os
import shutil



CATEGORIES = {"Images": ['.jpeg', '.png', '.jpg', '.svg'],
              "Video": ['.avi', '.mp4', '.mov', '.mkv'],
              "Documents": ['.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'],
              "Audio": ['.mp3', "'.wav'", '.flac', '.wma'],
              "Archives": ['.zip', '.gz', '.tar']}


CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji", "g")


  
def normalize(file):
    TRANS = {}
    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.lower())] = l.lower()


    file = Path(file)
    suff = file.suffix
    file = file.stem
    file = re.sub(r'\W', '_', file)
    file = file.translate(TRANS) + suff

    return file



#-------------------------------------------------


def move_file(file: Path, category: str, root_dir: Path) -> None:
    target_dir = root_dir.joinpath(category)
    if not target_dir.exists():
        target_dir.mkdir()
    file.replace(target_dir.joinpath(normalize(file)))


#------------------------------------------------


def un_zip(path: Path):
    for element in path.glob('**/*'):
        if element.suffix.lower() in CATEGORIES['Archives']:
            new_dir = element.parent.joinpath(rf'{element.stem}')
            shutil.unpack_archive(element, new_dir)
            os.remove(element)

          
#-------------------------------------------------


def get_categories(file: Path) -> str:
    ext = file.suffix.lower()
    for cat, exts in CATEGORIES.items():
        if ext in exts:
            return cat
    return 'Other'


#-------------------------------------------------



def sort_folder(path: Path) -> None:
    for element in path.glob('**/*'):
        if element.is_file():
            category = get_categories(element)
            move_file(element, category, path)
        if element.is_dir():
            if len(os.listdir(element)) == 0:
                element.rmdir()
    un_zip(path)    


#-------------------------------------------------


def main() -> str:
    try:
        path = Path(sys.argv[1])
    except IndexError:
        return 'No path to folder'

    if not path.exists():
        return 'Folder dos not exists'

    sort_folder(path)

    return 'All Ok'


if __name__ == '__main__':
    #print(main())
    main()

# py dz_6.py D:\hlam
