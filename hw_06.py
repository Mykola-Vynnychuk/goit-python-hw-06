import sys
from pathlib import Path


CATEGORIES = {"Audio": ["mp3", "aiff"],
              "Documents": ["docx", "txt", "pdf"]}

def sort_folder(path: Path) -> None:
    for item in path.glob("**/*"):
        print (item)

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
