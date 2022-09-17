import os

def get_file_list(path:str,ftype:str):
    '''
    读取文件夹下所有指定类型文件
    '''
    import os
    file_list = []
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            name = root+'/'+name
            # 指定类型
            if name.endswith(ftype):
                file_list.append(name)
    return file_list