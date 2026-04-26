import shutil
from pathlib import Path

source_file=Path("D:/testfile")

categories={
  "Images":{".jpg",".jpeg",".png",".gif"},
  "Documents":{".pdf",".docx",".txt",".xlsx"},
  "Archives":{".zip",".tar",".gz"},
}

dir_path={
    "Images":Path("C:/Users/liu'miao/Pictures"),
    "Documents":Path("D:/Miao/Documents"),
    "Archives":Path("D:/Miao/Archives"),
}

for item in source_file.iterdir():
    if item.is_file() and not item.name.startswith("."):
        ext=item.suffix.lower()
        for folder_name,ext_set in categories.items():
            if ext in ext_set:
                dest_folder=dir_path[folder_name]/ folder_name
                dest_folder.mkdir(exist_ok=True)
                shutil.move(str(item),str(dest_folder / item.name))
                print(f"already move:{item.name} to {dest_folder}/")
                break


