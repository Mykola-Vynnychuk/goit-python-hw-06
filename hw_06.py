import sys
from pathlib import Path


CATEGORIES = {"Archives": [".zip", ".gz", ".tar"],
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
    file.replace(target_dir.joinpath(f"{normalize(file.stem)}{file.suffix}"))

def get_categories(file: Path) -> str:
    ext = file.suffix
    for cat, exts in CATEGORIES.items():
        if ext in exts:
            return cat
    return "Other"

def delete_empty(path: Path) -> None:
    for item in path.iterdir():
        if item.is_dir():
            delete_empty(item)
            if not any(item.iterdir()):
                item.rmdir()

def sort_folder(path: Path) -> None:
    path_list = []
    for item in path.glob("**/*"):
        path_list.append(item)
    for i in path_list[::-1]:
        if i.is_file():
            move_file(i, path, get_categories(i))
        else: 
            delete_empty(path)

def main():
    try:
        path = Path(sys.argv[1])
    except IndexError:
        return "No path to folder"
    
    if not path.exists():
        return f"Folder with path {path} dos not exists."
    
    sort_folder(path)
    return "All ok"

if __name__ == "__main__":
    print(main())
