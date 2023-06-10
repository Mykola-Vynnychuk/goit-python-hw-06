import sys
from pathlib import Path


CATEGORIES = {"Audio": [".mp3", ".aiff"],
              "Documents": [".docx", ".txt", ".pdf"]}

def get_categories(path: Path) -> str:
    ext = path.suffix
    for cat, exts in CATEGORIES.items():
        if ext in exts:
            return cat
    return "Other"

def sort_folder(path: Path) -> None:
    for item in path.glob("**/*"):
        if item.is_file:
            print(get_categories(item))

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
