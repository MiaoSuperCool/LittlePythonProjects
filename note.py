import sys

def process():
    if len(sys.argv)==1:
        print("没有检测到指令诶")
    elif sys.argv[1]=="--list":
        list_notes()
    elif sys.argv[1]=="--add":
        if len(sys.argv)<3:
            print("请提供便签内容")
        else:
            add_notes(sys.argv[2])
    elif sys.argv[1]=="--delete":
        if len(sys.argv) < 3:
            print("请输入要删除的便签序号")
        else:
            delete_notes(int(sys.argv[2]))
    else:
        print("暂无这样的指令，再试一下其他的吧")


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