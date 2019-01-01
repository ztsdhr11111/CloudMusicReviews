# Author : ZhangTong

import requests
import math
import random

from Crypto.Cipher import AES
import codecs
import base64


def get_comments_json(url, data):
    headers = {
        # 'Accept': '*/*',
        # 'Accept-Encoding': 'gzip, deflate, br',
        # 'Accept-Language': 'zh-CN,zh;q=0.9',
        # 'Connection': 'keep-alive',
        # 'Content-Length': 532,
        # 'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': '_iuqxldmzr_=32; _ntes_nnid=9d9bdd7439b3dbd407a50b36048caf40,1545995309013; _ntes_nuid=9d9bdd7439b3dbd407a50b36048caf40; __utmz=94650624.1545995311.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); WM_TID=of%2BMHHu1E41EQQBVBBI9Oq8wgQUn6%2BAF; __remember_me=true; JSESSIONID-WYYY=jQZJschbTnkWYpu0vHSSq3W97bsMppqQU6sqJf%5CrBGguhQEbZD6RO6ugHASjRH7GA19sCnAbSrGPnoO%5CMV%2B4pzpx8%2BXurNpF4RsVjUzITcEin1kNCjq2Uef%2F1aN1MbYQdBrj8KiVR0AyUJvtIFyY9jNHJGnv5itZDZhl8tIhU5d%2Bdiky%3A1546344583658; __utma=94650624.414176080.1545995311.1545995311.1546342785.2; __utmc=94650624; WM_NI=KTWkPXRss4WIA3wgdIjk5HgMSoqd1l4BlWXA6W%2FOlSyWgk8ieLIvU4EdKS%2BFhvcZrJIUIlrty8AQUJwu6r5pVAo31NVWoPh7ealLbtnxHflBsxtKGXEbbxorjjrBX%2BFfTUk%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eed8f14382eaae85f43b89868fa6c55b878e8eaaee64939d98a4b168fb9aa1a4b62af0fea7c3b92a898c998cd35492adbdd5d64383edb988e743aab5fba9e64791b1bf85b468f89ea4b8db4bf689e1b0ef59bb89a98cbb63a7948797d84087bc85b4aa4eacaaadbbf1428b8b878df180bbe88fb2d842b5abfa93b87c969fa1d4b4469689a1b1eb3da7bfa4ade180aea88887ef4ab1a8bcacc65487beae99ee7aaab6bea3db2186ba9cb6ea37e2a3; MUSIC_U=d0d2907658790270a0c6aa81b6ce47c7c46dba055b6904fd81c7483dae969ce341de2b2e2c34e453d0cc2419d7fad1859df9409031b588ee443f72c66f651bba102ee34f7daa43cbde39c620ce8469a8; __csrf=6405de6cff2020e4f31e68a8c679dfcb; __utmb=94650624.5.10.1546342785',
        # 'Host': 'music.163.com',
        # 'Referer': 'http://music.163.com/',
        # 'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }
    try:
        response = requests.post(url, data=data, headers=headers)
        if response.status_code == 200:
            # response.encoding = response.apparent_encoding    # 在这里不用的原因是：响应的编码是'utf-8'；在我的电脑上(Win10)如果使用这行代码会将编码格式改为：'Windows-1254'，会产生乱码
            return response.json()
    except:
        print('抓取json失败')

def generate_random_strs(length):
    '''
    生成16个随机字符
    :param length:
    :return:
    '''
    string = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    i = 0   # 控制次数参数i
    random_strs = ""    # 初始化随机字符串
    while i < length:
        e = random.random() * len(string)
        e = math.floor(e)   # 向下取整
        random_strs = random_strs + list(string)[e]
        i = i + 1
    return random_strs

def AESencrypt(msg, key):
    '''
    AES加密
    :param msg:
    :param key:
    :return:
    '''
    padding = 16 - len(msg) % 16    # 如果不是16的位数则进行填充
    msg = msg + padding * chr(padding)  # 使用padding对应的单字符进行填充

    iv = '0102030405060708'     # 用来加密或者解密的初始向量(必须是16位)

    cipher = AES.new(key, AES.MODE_CBC, iv)     # 通过AES处理初始密码字符串，并返回cipher对象
    encryptedbytes = cipher.encrypt(msg)    # 加密后得到的是bytes类型的数据
    encodestrs = base64.b64encode(encryptedbytes)   # 使用base64进行编码，返回byte字符串
    enctext = encodestrs.decode('utf-8')    # 对byte字符串按utf-8进行解码

    return enctext

def RSAencrypt(randomstrs, key, f):
    '''
    RSA加密
    :param randomstrs:
    :param key:
    :param f:
    :return:
    '''
    string = randomstrs[::-1]   # 随机字符串逆序排列
    text = bytes(string, 'utf-8')   # 将随机字符串转换成byte类型数据
    seckey = int(codecs.encode(text, encoding='hex'), 16) ** int(key, 16) % int(f, 16)
    return format(seckey, 'x').zfill(256)

def get_params(page):
    '''
    获取参数
    :param page:
    :return:
    '''
    # msg也可以协程msg = {"offset":"页面偏移量=(页数-1) * 20", "limit": "20"}, offset和limit这两个参数必须有(js)
    # limit最大值为100，当设为100时，获取第二页时，默认前一页是20个评论，也就是说第二页最新评论有80个，有20个是第一页显示的
    # msg = '{"offset":' + str(offset) + ', "total":"True", "limit": "20", "csrf_token":""}'
    # offset和limit是必选参数，其他参数是可选的，其他参数不影响data数据的生成
    offset = (page-1) * 20  # 偏移量
    msg = '{"offset": ' + str(offset) + ',"total": "True","limit": "20","csrf_token": ""}'
    key = '0CoJUm6Qyw8W8jud'
    f = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
    e = '010001'
    enctext = AESencrypt(msg, key)      # 第一次AES加密
    i = generate_random_strs(16)    # 生成长度为16的随机字符串

    encText = AESencrypt(enctext, i)   # 两次AES加密之后得到encText的值
    encSecKey = RSAencrypt(i, e, f)     # RSA加密之后的到encSecKey的值
    # print(encText, '\n', encSecKey)
    return encText, encSecKey

def hotcomments(html, songname, i, pages, total, filepath):
    with open(filepath, 'a', encoding='utf-8') as f:
        f.write('正在获取歌曲{}的第{}页评论，总共有{}页{}条评论！\n'.format(songname, i, pages, total))
    print('正在获取歌曲{}的第{}页评论，总共有{}页{}条评论！\n'.format(songname, i, pages, total))

    m = 1
    if 'hotComments' in html:
        for item in html['hotComments']:
            user = item['user']
            print('热门评论{}: {} : {}      点赞次数:{}'.format(m, user['nickname'], item['content'], item['likedCount']))
            with open(filepath, 'a', encoding='utf-8') as f:
                f.write('热门评论{}: {} : {}      点赞次数:{}'.format(m, user['nickname'], item['content'], item['likedCount']))
                if len(item['beReplied']) != 0:
                    for reply in item['beReplied']:
                        replyuser = reply['user']
                        print('回复：{} : {}'.format(replyuser['nickname'], reply['content']))
                        f.write('回复：{} : {}'.format(replyuser['nickname'], reply['content']))
            m += 1

def comments(html, songname, i, pages, total, filepath):
    with open(filepath, 'a', encoding='utf-8') as f:
        f.write('\n正在获取歌曲{}的第{}页评论，总共有{}页{}条评论！\n'.format(songname, i, pages, total))
    print('\n正在获取歌曲{}的第{}页评论，总共有{}页{}条评论！\n'.format(songname, i, pages, total))
    j = 1
    for item in html['comments']:
        user = item['user']
        print('全部评论{}: {} :{}   点赞次数： {}'.format(j, user['nickname'], item['content'], item['likedCount']))
        with open(filepath, 'a', encoding='utf-8') as f:
            f.write('全部评论{}: {} :{}   点赞次数： {}'.format(j, user['nickname'], item['content'], item['likedCount']))
            if len(item['beReplied']) != 0:
                for reply in item['beReplied']:
                    replyuser = reply['user']
                    print('回复：{} : {}'.format(replyuser['nickname'], reply['content']))
                    f.write('回复：{} : {}'.format(replyuser['nickname'], reply['content']))
        j += 1

def main():
    songid = 38592976       # 歌曲id
    songname = 'Dream it possible'      # 歌曲名称
    filepath = songname + '.txt'        # 文件路径

    page = 1
    params, encSecKey = get_params(page)        # post提交的参数

    url = 'https://music.163.com/weapi/v1/resource/comments/R_SO_4_' + str(songid) + '?csrf_token=0d0bfb205322c59fddc39017eaac9f50'
    data = {'params': params, 'encSecKey': encSecKey}
    html = get_comments_json(url, data)
    total = html['total']
    pages = math.ceil(total / 20)
    hotcomments(html, songname, page, pages, total, filepath)
    comments(html, songname, page, pages, total, filepath)

    page = 2
    while page <= pages:
        params, encSecKey = get_params(page)
        data = {'params': params, 'encSecKey': encSecKey}
        html = get_comments_json(url, data)
        comments(html, songname, page, pages, total, filepath)
        page += 1

if __name__ == '__main__':
    main()

