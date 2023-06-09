import sys
from pathlib import Path

def main():
    try:
        path = Path(sys.argv[1])
    except IndexError:
        return "No path to folder"
    
    if not path.exists():
        return f"Folder with path {path} dos not exists."
    
    return "All ok"

if __name__ == "__main__":
    print(main())
