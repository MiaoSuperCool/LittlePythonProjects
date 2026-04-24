import shutil
from pathlib import Path

source_file=Path("D:/testfile")

categories={
  "Images":{".jpg",".jpeg",".png",".gif"},
  "Documents":{".pdf",".docx",".txt",".xlsx"},
  "Archives":{".zip",".tar",".gz"},
}

for item in source_file.iterdir():
    if item.is_file() and not item.name.startswith("."):
        ext=item.suffix.lower()
        for folder_name,ext_set in categories.items():
            if ext in ext_set:
                dest_folder=source_file / folder_name
                dest_folder.mkdir(exist_ok=True)
                shutil.move(str(item),str(dest_folder / item.name))
                print(f"already move:{item.name} to {folder_name}/")
                break


