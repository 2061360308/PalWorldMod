from os.path import isfile as os_path_isfile, basename as os_path_basename, join as os_path_join, isdir as os_path_isdir
from os import makedirs as os_makedirs, listdir as os_listdir
from hashlib import md5 as hashlib_md5
from json import dumps, loads
from shutil import copy2

resource_dir = './resource'


class Node:
    def __init__(self, name, hash, children=None):
        self.name = name
        self.hash = hash
        self.children = children or []

    def to_dict(self):
        return {
            'name': self.name,
            'hash': self.hash,
            'children': [child.to_dict() for child in self.children],
        }


class CreateModResource:
    resource_dir = './resource'

    @staticmethod
    def get_hash(path):
        if os_path_isfile(path):
            with open(path, 'rb') as f:
                bytes = f.read()
                data = os_path_basename(path).encode() + bytes
                hash_value = hashlib_md5(data).hexdigest()
                CreateModResource.copy_to_resource(path, hash_value)
                return hash_value
        else:
            return '0' * 32

    @staticmethod
    def copy_to_resource(path, hash_value):
        new_dir = os_path_join(CreateModResource.resource_dir, hash_value[:2])
        new_path = os_path_join(new_dir, hash_value[2:])
        if not os_path_isdir(new_dir):
            os_makedirs(new_dir, exist_ok=True)
        copy2(path, new_path)

    @staticmethod
    def __create_node_structure(root_dir):
        """
        创建mod文件的结构

        :param root_dir:
        :return:
        """
        if os_path_isfile(root_dir):
            return Node(os_path_basename(root_dir), CreateModResource.get_hash(root_dir))
        else:
            node = Node(os_path_basename(root_dir), CreateModResource.get_hash(root_dir))
            for child in os_listdir(root_dir):
                child_path = os_path_join(root_dir, child)
                node.children.append(CreateModResource.__create_node_structure(child_path))
            return node

    @staticmethod
    def create_node_structure(mod_dir):
        node_structure = CreateModResource.__create_node_structure(mod_dir)

        node_structure_dict = node_structure.to_dict()
        jsonStr = dumps(node_structure_dict, indent=4, ensure_ascii=False)
        node_structure_hash = hashlib_md5(jsonStr.encode()).hexdigest()

        return node_structure_dict, node_structure_hash

    @staticmethod
    def create_mod_resource(mod_dir, name: str, version: str, author: str,
                            description: str, tags: list, adapt_version: list):
        """
        创建mod资源

        :param mod_dir:
        :param name:
        :param version:
        :param author:
        :param description:
        :param tags:
        :param adapt_version:
        :return:
        """

        # 适用版本
        jsonStr, node_structure_hash = CreateModResource.create_node_structure(mod_dir)

        mod_resource = {
            'node_structure': jsonStr,
            'node_structure_hash': node_structure_hash,
            'name': name,
            'version': version,
            'author': author,
            'description': description,
            'tags': tags,
            'adapt_version': adapt_version,
        }

        with open(f"./mods/{name}.mod", 'w', encoding='utf-8') as f:
            f.write(dumps(mod_resource, indent=4, ensure_ascii=False))


# 释放资源类
class ReleaseModResource:
    @staticmethod
    def release_mod_resource(mod_path):
        print(f"释放资源: {mod_path}")
        with open(mod_path, 'r', encoding='utf-8') as f:
            mod_resource = loads(f.read())
        node_structure = mod_resource['node_structure']
        node_structure_hash = mod_resource['node_structure_hash']
        name = mod_resource['name']
        version = mod_resource['version']
        author = mod_resource['author']
        description = mod_resource['description']
        tags = mod_resource['tags']
        adapt_version = mod_resource['adapt_version']

        # 释放资源
        ReleaseModResource.__release_node_structure(node_structure, node_structure_hash)
        print(f"释放资源: {name}  成功")

    @staticmethod
    def __release_node_structure(node_structure, node_structure_hash):
        # 验证hash
        jsonStr = dumps(node_structure, indent=4, ensure_ascii=False)
        hash_value = hashlib_md5(jsonStr.encode()).hexdigest()
        if hash_value != node_structure_hash:
            print('资源hash验证失败')
            return

        # 释放资源
        # 遍历每一个节点，如果hash是0*32，说明是文件夹，否则是文件
        # 如果是文件夹，创建文件夹，如果是文件，从resource中复制到mod文件夹中

        mod_files_path = './mod_files'
        ReleaseModResource.create_node(node_structure, mod_files_path)

    @staticmethod
    def create_node(node, parent_path):
        path = os_path_join(parent_path, node['name'])
        if node['hash'] == '0' * 32:
            os_makedirs(path, exist_ok=True)
            for child in node['children']:
                ReleaseModResource.create_node(child, path)
        else:
            resource_path = os_path_join(resource_dir, node['hash'][:2], node['hash'][2:])
            copy2(resource_path, path)


if __name__ == '__main__':
    def make_mod_resource():
        root_dir = r"D:\LUAO\Desktop\帕鲁mod\幻兽帕鲁MOD合集（新增宝可梦MOD）\1-功能性MOD\服务器MOD一键安装\单独一键安装"
        for i in os_listdir(
                r"D:\LUAO\Desktop\帕鲁mod\幻兽帕鲁MOD合集（新增宝可梦MOD）\1-功能性MOD\服务器MOD一键安装\单独一键安装"):
            CreateModResource.create_mod_resource(os_path_join(root_dir, i),
                                                  i, '1.0', '未知',
                                                  '100%稀有掉落', ['游戏作弊'], ['1.0.0']
                                                  )


    def release_mod_resource():
        for i in os_listdir('./mods'):
            ReleaseModResource.release_mod_resource(os_path_join('./mods', i))

    make_mod_resource()


