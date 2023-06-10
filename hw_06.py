import sys
from pathlib import Path


CATEGORIES = {"Audio": [".mp3", ".aiff"],
              "Documents": [".docx", ".txt", ".pdf"]}

def move_file(path: Path, root_dir: Path, categorie: str) -> None:
    target_dir = root_dir.joinpath(categorie)
    if not target_dir.exists():
        print(f"Make {target_dir}")
        target_dir.mkdir()
    print(f"Exist {target_dir}")

def get_categories(path: Path) -> str:
    ext = path.suffix
    for cat, exts in CATEGORIES.items():
        if ext in exts:
            return cat
    return "Other"

def sort_folder(path: Path) -> None:
    for item in path.glob("**/*"):
        if item.is_file:
            cat = get_categories(item)
            move_file(item, path, cat)

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
