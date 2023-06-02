import os

import count

if __name__ == '__main__':
    path = input('请输入文件路径或直接将文件拖拽到此窗口 > ')
    if '"' in path:
        path = path[1:-1]
    is_exit = False
    os.system('cls')
    while not is_exit:
        is_exit = count.count(path)
