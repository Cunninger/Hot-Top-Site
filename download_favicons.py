import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os


def get_favicon(url, name):
    try:
        # 发送请求获取网页内容
        response = requests.get(f"https://{url}")
        soup = BeautifulSoup(response.content, 'html.parser')

        # 查找favicon链接
        icon_link = soup.find('link', rel=lambda x: x and 'icon' in x.lower())

        if icon_link and icon_link.get('href'):
            favicon_url = icon_link['href']
            # 如果是相对路径，转换为绝对路径
            if not favicon_url.startswith(('http:', 'https:')):
                favicon_url = urljoin(f"https://{url}", favicon_url)
        else:
            # 如果没有找到图标链接，尝试默认的favicon.ico
            favicon_url = f"https://{url}/favicon.ico"

        # 下载图标
        icon_response = requests.get(favicon_url)
        if icon_response.status_code == 200:
            with open(f"{name}.png", 'wb') as f:
                f.write(icon_response.content)
            print(f"成功下载 {name} 的图标")
        else:
            print(f"无法下载 {name} 的图标")
    except Exception as e:
        print(f"获取 {name} 的图标时出错: {str(e)}")


# 网站列表
websites = [
    ('zhihu.com', '知乎'), ('weibo.com', '微博'), ('baidu.com', '百度'),
    ('tieba.baidu.com', '百度贴吧'), ('news.qq.com', '腾讯新闻'),
    ('news.163.com', '网易新闻'), ('thepaper.cn', '澎湃新闻'),
    ('toutiao.com', '今日头条'), ('sspai.com', '少数派'),
    ('ithome.com', 'IT之家'), ('36kr.com', '36氪'),
    ('juejin.cn', '稀土掘金'), ('weread.qq.com', '微信读书'),
    ('lol.qq.com', '英雄联盟'), ('ys.mihoyo.com', '原神'),
    ('baike.baidu.com/calendar', '历史上的今天'), ('douyin.com', '抖音'),
    ('kuaishou.com', '快手'), ('bilibili.com', '哔哩哔哩')
]

# 创建保存图标的目录
if not os.path.exists('icons'):
    os.makedirs('icons')

# 切换到icons目录
os.chdir('icons')

# 遍历网站列表并下载图标
for url, name in websites:
    get_favicon(url, name)