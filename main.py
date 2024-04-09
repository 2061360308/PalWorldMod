import os
from filecmp import cmp as filecmp_cmp
from os import listdir as os_listdir, makedirs as os_makedirs, path as os_path
from os.path import exists as os_path_exists, splitext as os_path_splitext, join as os_path_join
from shutil import move as shutil_move, copy2 as shutil_copy2

from json import loads as json_loads, dumps as json_dumps
from modResource import ReleaseModResource

mods = os_listdir('./mods')


# 读取配置文件
pal_server_path = None
pal_world_path = None

with open('settings', 'r', encoding='utf-8') as f:
    content = f.read()
lines = content.split("\n")
for line in lines:
    if line.startswith("#"):
        continue
    elif line.startswith("pal_server_path"):
        pal_server_path = line.split('=')[1].strip()
    elif line.startswith("pal_world_path"):
        pal_world_path = line.split('=')[1].strip()

print(f"pal_server_path: {pal_server_path}")
print(f"pal_world_path: {pal_world_path}")


def copy_with_backup(src, dst, mod_name):
    if os_path_exists(dst) and not filecmp_cmp(src, dst, False):
        backup_dst = dst + f'.{mod_name}.backup'
        shutil_move(dst, backup_dst)

    # 如果文件夹不存在，创建文件夹
    if not os_path_exists(os_path.dirname(dst)):
        os_makedirs(os_path.dirname(dst))

    print(f"复制文件：{src} -> {dst}")
    shutil_copy2(src, dst)


print("选择以下命令：\n【1】添加mod\n【2】删除mod\n【3】退出")
cmd = input("请输入命令：")
if cmd == '1':
    if os_path_exists('config.json'):
        with open('config.json', 'r') as f:
            config = json_loads(f.read())
    else:
        config = {'mods': []}

    print("当前可用mod为：")
    j = 1
    for i in mods:
        if i in config['mods']:
            j += 1
            continue
        print(f'【{j}】：', i)
        j += 1

    mod_index = input("输入序号添加mod：")
    mod_name = mods[int(mod_index) - 1]
    mod_path = f'./mods/{mod_name}'
    ReleaseModResource.release_mod_resource(mod_path)
    # 使用os.walk遍历mod_files/mod_name/Pal文件夹，将文件复制到Pal文件夹
    mod_files_path = f'.\\mod_files\\{os_path_splitext(mod_name)[0]}\\Pal\\'
    # print(mod_files_path)
    for root, dirs, files in os.walk(mod_files_path):
        for file in files:
            file_path = os_path_join(root, file).replace('/', '\\')
            # 计算相对路径
            relative_path = file_path.replace(mod_files_path, '')
            # 计算游戏中的路径
            # 复制文件
            if pal_server_path:
                server_path = os_path_join(pal_server_path, relative_path)
                copy_with_backup(file_path, server_path, os_path_splitext(mod_name)[0])

            if pal_world_path:
                game_path = os_path_join(pal_world_path, relative_path)
                copy_with_backup(file_path, game_path, os_path_splitext(mod_name)[0])

    print("添加mod成功")
    config['mods'].append(mod_name)
    with open('config.json', 'w') as f:
        f.write(json_dumps(config, indent=4))

elif cmd == '2':
    with open('config.json', 'r') as f:
        config = json_loads(f.read())
    j = 1
    for i in config['mods']:
        print(f'【{j}】：', i)
        j += 1

    mod_index = input("输入序号删除mod：")
    mod_name = config['mods'][int(mod_index) - 1]
    mod_path = f'./mods/{mod_name}'
    ReleaseModResource.release_mod_resource(mod_path)
    # 使用os.walk遍历mod_files/mod_name/Pal文件夹，删除这些文件
    mod_files_path = f'.\\mod_files\\{os_path_splitext(mod_name)[0]}\\Pal\\'
    # print(mod_files_path)
    for root, dirs, files in os.walk(mod_files_path):
        for file in files:
            file_path = os_path_join(root, file).replace(mod_files_path, '').replace('/', '\\')
            # 计算相对路径
            relative_path = file_path.replace(mod_files_path, '')
            # 计算游戏中的路径
            # 计算游戏中的路径
            # 复制文件
            if pal_server_path:
                server_path = os_path_join(pal_server_path, relative_path)
                if os_path.exists(server_path):
                    os.remove(server_path)

                # 判断是否有备份文件
                backup_path = server_path + f'.{os_path_splitext(mod_name)[0]}.backup'
                if os_path.exists(backup_path):
                    shutil_move(backup_path, server_path)
            if pal_world_path:
                game_path = os_path_join(pal_world_path, relative_path)
                if os_path.exists(game_path):
                    os.remove(game_path)

                # 判断是否有备份文件
                backup_path = game_path + f'.{os_path_splitext(mod_name)[0]}.backup'
                if os_path.exists(backup_path):
                    shutil_move(backup_path, game_path)
    print("删除mod成功")
    config['mods'].remove(mod_name)
    with open('config.json', 'w') as f:
        f.write(json_dumps(config, indent=4))

elif cmd == '3':
    print("退出")
    exit(0)
