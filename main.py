import requests
import json
import webbrowser
from wox import Wox
import os
import logging
from dirtree import DirTree

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename="cmd_error.log",
                    filemode='a')

logging.info('start test for linux-command')

try:
    import clipboard  # 注意要另外安装这个包
except:
    logging.error("need pip install clipboard")

try:
    from markdown_to_json.vendor import CommonMark
    from markdown_to_json.markdown_to_json import Renderer, CMarkASTNester
except:
    logging.error("need pip install markdown_to_json")


def list_nested(list_md):
    try:
        ast = CommonMark.DocParser().parse(list_md)
        return CMarkASTNester().nest(ast)
    except:
        logging.error("md文件不符合格式或没有h1的标题")


# 获取MD文件用raw
RAW_BASE_URL = "https://raw.githubusercontent.com/basicsp/cmdblog/master/"
# 连接到github网页
DIR_BASE_URL = "https://github.com/basicsp/cmdblog/tree/master/"
READ_ME = "README.md"

dir = os.path.dirname(__file__)
cmdblog_path = os.path.join(dir, 'cmdblog')


class Main(Wox):
# class Main():

    @staticmethod
    def update_github():
        """从github上clone或pull最新的文件"""
        try:
            if not os.path.exists(cmdblog_path):
                os.chdir(dir)
                # os.mkdir(cmdblog_path)  # git clone 可以生成该文件夹
                os.system("git clone https://github.com/basicsp/cmdblog.git")
            else:
                os.chdir(cmdblog_path)
                os.system("git pull")
        except Exception as e:
            return str(e)
        else:
            return True

    def query(self, query):

        if not query:
            return [{'Title': 'cmd blog', 'SubTitle': 'cb for cmb blog on github', 'IcoPath': 'icon.png',
                     "JsonRPCAction": {"method": "openUrl", "parameters": [DIR_BASE_URL]},
                     }]
        logging.info(str(query))

        if query == 'update':  # 强制刷新
            rst = Main.update_github()
            if rst == True:
                return [{'Title': 'update success', 'SubTitle': 'clone/pull github success!', 'IcoPath': 'icon.png'}]
            else:
                return [{'Title': 'update failed', 'SubTitle': rst, 'IcoPath': 'icon.png'}]

        dt = DirTree().buildRecursive2(cmdblog_path, ignoreDirs=[".idea", ".git"])
        # print(dt)
        results = []
        query_list = query.split(' ')[0:2]  # 最多取前两个参数
        if len(query_list) == 1:
            q1 = query_list[0]
            for k in dt:
                if k.find(q1) != -1:
                    res = {
                        "Title": k,
                        "SubTitle": k + "（回车可打开url）",
                        "IcoPath": "icon.png",
                        # 打开所在的文件夹路径
                        "JsonRPCAction": {
                            "method": "openUrl", "parameters": [DIR_BASE_URL + str(k)]},
                    }
                    results.append(res)
            return results
        else:
            # 当有两个参数的时候，第一个参数q1必须完全匹配, q2支持k的模糊搜索，凡是匹配的readme都打开
            q1, q2 = query_list
            if q1 not in dt:
                return []

            # 查找思路：直接构造readme文件的路径，查找是否存在该文件
            for k in dt[q1]:
                if k.find(q2) != -1:
                    for _ in dt[q1][k]:
                        readme_path = os.path.join(cmdblog_path, q1, k, READ_ME)
                        if os.path.isfile(readme_path):
                            with open(readme_path, 'r', encoding='UTF-8') as f:
                                j1 = list_nested(f.read())
                                j2 = Renderer().stringify_dict(j1)
                                for x, y in j2['Summary'].items() if 'Summary' in j2 else {}:
                                    res = {
                                        "Title": k + ": " + x,
                                        "SubTitle": y + "（回车可复制命令行）",
                                        "IcoPath": "icon.png",
                                        "JsonRPCAction": {  # 打开所在的文件夹路径
                                            "method": "copy_to_clip", "parameters": [y],  # 将命令拷贝到剪贴板
                                            "dontHideAfterAction": True}  # True: 执行操作后不隐藏wox
                                    }
                                    results.append(res)
            return results

    def openUrl(self, url):
        webbrowser.open(url)

    def copy_to_clip(self, text):
        clipboard.copy(text)


if __name__ == "__main__":
    Main()
    # print(Main().query(''))
    # print(Main().query('update'))
    # print(Main().query('pyth'))
    # print(Main().query('python vi'))

