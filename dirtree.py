import os


class DirTree:
    def __init__(self):
        pass

    def buildPath(self, path, file):
        return path + '/' + file

    def buildRecursive(self, path, currDir, ignoreDirs):
        """  列表为主表示文件夹的递归形式
         {
            '.': [
                'README.md',
                {
                    'git': [

                    ]
                },
                'index.json',
                {
                    'linux': [
                        {
                            'tmux': [

                            ]
                        }
                    ]
                },
                {
                    'python': [
                        {
                            'virtualenv': [
                                'readme.md'
                            ]
                        }
                    ]
                }
            ]
        }
        """
        res = []
        lst = os.listdir(path)
        for i in sorted(lst):
            x = self.buildPath(path, i)

            if os.path.isdir(x):
                if i in ignoreDirs:
                    continue

            if os.path.isfile(x):
                res.append(os.path.basename(i))
            elif os.path.isdir(x):
                res.append(self.buildRecursive(x, i, ignoreDirs))

        return {currDir: res}

    def buildRecursive2(self, path, ignoreDirs):
        """ 字典为主表示文件夹的递归形式，__files__作为关键字，保存该目录下的所有文件
        {
            '.': [
                'README.md',
                'index.json'
            ],
            'git': {
                'files': [

                ]
            },
            'linux': {
                '.': [

                ],
                'tmux': {
                    'files': [

                    ]
                }
            },
            'python': {
                '.': [

                ],
                'virtualenv': {
                    '.': [
                        'readme.md'
                    ]
                }
            }
        }
        """
        res = {".": []}
        lst = os.listdir(path)
        for i in sorted(lst):
            x = self.buildPath(path, i)

            if os.path.isdir(x):
                if i in ignoreDirs:
                    continue

            if os.path.isfile(x):
                res["."].append(os.path.basename(i))
            elif os.path.isdir(x):
                res[os.path.basename(x)] = self.buildRecursive2(x, ignoreDirs)

        return res


"""
def os_walk():
    git_dirs = []
    last_dir = []
    for root, dirs, files in os.walk(cmdblog_path):
        cur_dir = []
        for name in dirs:
            print(os.path.join(root, name))
            cur_dir.append({name: []})
        for file in files:
            print(os.path.join(root, name, file))
            cur_dir.append(file)
        last_dir = cur_dir


def save2json(dt):
    for k, v in dt.items():
        if k == '.':
            names = [i.lower() for i in dt['.']]
            if "readme.md" in names:
                # 构造readme的路径
                print(names)
        else:
            save2json(v)

save2json(dt)
"""

if __name__ == "__main__":
    dir = os.path.dirname(__file__)
    cmdblog_path = os.path.join(dir, 'cmdblog')
    # dt = DirTree().buildRecursive(cmdblog_path, '.', ignoreDirs=[".idea", ".git"])
    dt = DirTree().buildRecursive2(cmdblog_path, ignoreDirs=[".idea", ".git"])
    print(dt)
