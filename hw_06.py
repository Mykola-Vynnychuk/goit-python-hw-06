import sys
from pathlib import Path
import uuid
import shutil


CATEGORIES = {"Archives": [".zip", ".gz", ".tar", ".rar"],
              "Audio": [".mp3", ".ogg", ".wav", ".amr"],
              "Documents": [".doc", ".docx", ".txt", ".pdf", ".xlsx", ".pptx"],
              "Images": [".jpeg", ".png", ".jpg", ".svg"],
              "Video": [".avi", ".mp4", ".mov", ".mkv"]}

CYRILLIC_SYMBOLS = "абвгґдеёєжзиіїйклмнопрстуфхцчшщъыьэюя"

TRANSLATION = ("a", "b", "v", "h", "g", "d", "e", "e", "ie", "zh", 
               "z", "y", "i", "i", "i", "k", "l", "m", "n", "o", "p", 
               "r", "s", "t", "u", "f", "kh", "ts", "ch", "sh", "shch", 
               "", "y", "", "e", "iu", "ia")

BAD_SYMBOLS = ("%", "*", " ", "-")

TRANS = {}

for c, t in zip(list(CYRILLIC_SYMBOLS), TRANSLATION):
    TRANS[ord(c)] = t
    TRANS[ord(c.upper())] = t.upper()

for i in BAD_SYMBOLS:
    TRANS[ord(i)] = "_"

def normalize(name: str) -> str:
    return name.translate(TRANS)
    
def move_file(file: Path, root_dir: Path, categorie: str) -> None:
    target_dir = root_dir.joinpath(categorie)
    if not target_dir.exists():
        target_dir.mkdir()
    new_name = target_dir.joinpath(f"{normalize(file.stem)}{file.suffix}")
    if new_name.exists():
        new_name = new_name.with_name(f"{new_name.stem}-{uuid.uuid4()}{file.suffix}")
    file.rename(new_name)

def get_categories(file: Path) -> str:
    ext = file.suffix
    for cat, exts in CATEGORIES.items():
        if ext in exts:
            return cat
    return "Other"

def delete_empty_folder(path: Path) -> None:
    for item in path.iterdir():
        if item.is_dir():
            delete_empty_folder(item)
            if not any(item.iterdir()):
                item.rmdir()

def unpack_archive(path: Path) -> None:
    archives_folder = path / "Archives"
    for file_path in archives_folder.iterdir():
        if file_path.is_file():
            try:
                shutil.unpack_archive(str(file_path), str(archives_folder / file_path.stem))
                file_path.unlink()
            except:
                continue

def sort_folder(path: Path) -> None:
    path_list = []
    for item in path.glob("**/*"):
        path_list.append(item)
    for i in path_list[::-1]:
        if i.is_file():
            move_file(i, path, get_categories(i))
        else: 
            delete_empty_folder(path)

def main():
    try:
        path = Path(sys.argv[1])
    except IndexError:
        return "No path to folder"
    
    if not path.exists():
        return f"Folder with path {path} dos not exists."
    
    sort_folder(path)
    unpack_archive(path)
    return "All ok"

if __name__ == "__main__":
    print(main())
