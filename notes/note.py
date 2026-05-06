import sys

def process():
    if len(sys.argv)==1:
        print("没有检测到指令诶")
    if sys.argv[1]=="--list":
        list()
    if sys.argv[1]=="--add":
        content=sys.argv[2]
        add(content)
    if sys.argv[1]=="--delete":
        delete(sys.argv[2])
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
        enumerate(lines,start=1)
        print(enumerate)


if __name__ == "__main__":
    process()