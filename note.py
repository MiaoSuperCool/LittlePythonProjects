import argparse


parser=argparse.ArgumentParser(description="命令行便签本")
parser.add_argument("--list",action="store_true")
parser.add_argument("--add",nargs="?")
parser.add_argument("--delete",type=int,nargs="?")

def process():

    args=parser.parse_args()

    if args.list:
        list_notes()
    elif args.add is not None:
        add_notes(args.add)
    elif args.delete is not None:
        delete_notes(args.delete)
    else:
        print("指令有误或者未输入内容，请再试一下吧")


def delete_notes(index):
    with open("note.txt","r") as f:
        lines=f.readlines()
        del lines[index]
    with open("note.txt","w") as f:
        f.writelines(lines)
        print("删除成功")


def add_notes(content):
    with open("note.txt","a") as f:
        f.write(f"{content}\n")
        print("添加成功")


def list_notes():
    with open("note.txt","r") as f:
        lines=f.readlines()
        for i,line in enumerate(lines,start=1):
            print(f"{i}:{line}",end="")


if __name__ == "__main__":
    process()