import sys

def process():
    if len(sys.argv)==1:
        print("没有检测到指令诶")
    elif sys.argv[1]=="--list":
        list()
    elif sys.argv[1]=="--add":
        content=sys.argv[2]
        add(content)
    elif sys.argv[1]=="--delete":
        delete(int(sys.argv[2]))
    else:
        print("暂无这样的指令，再试一下其他的吧")

def delete(count):
    with open("note.txt","r") as f:
        lines=f.readlines()
        del lines[count]
    with open("note.txt","w") as f:
        f.writelines(lines)
        print("删除成功")


def add(content):
    with open("note.txt","a") as f:
        f.write(f"{content}\n")
        print("添加成功")


def list():
    with open("note.txt","r") as f:
        lines=f.readlines()
        for i,line in enumerate(lines,start=1):
            print(f"{i}:{line}",end="")


if __name__ == "__main__":
    process()