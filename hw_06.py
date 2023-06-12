import sys
from pathlib import Path


CATEGORIES = {"Audio": [".mp3", ".aiff"],
              "Documents": [".docx", ".txt", ".pdf"]}

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
    
def move_file(path: Path, root_dir: Path, categorie: str) -> None:
    target_dir = root_dir.joinpath(categorie)
    if not target_dir.exists():
        print(f"Make {target_dir}")
        target_dir.mkdir()
    path.replace(target_dir.joinpath(f"{normalize(path.stem)}{path.suffix}"))

def get_categories(path: Path) -> str:
    ext = path.suffix
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
    for item in path.glob("**/*"):
        if item.is_file:
            cat = get_categories(item)
            move_file(item, path, cat)
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
