import urllib.request
import requests

if __name__ == '__main__':
    # url = 'https://ja.wikipedia.org/wiki/日本'
    # url = 'https://wikiwiki.jp/nijisanji/%E6%9C%88%E3%83%8E%E7%BE%8E%E5%85%8E'

    url = 'https://wikiwiki.jp/nijisanji/%E9%88%B4%E9%B9%BF%E8%A9%A9%E5%AD%90'

    # print(requests.get(url).text)
    with urllib.request.urlopen(url) as req:
        a = req.read()
        print('あ')
        print(type('あ'))
        print(type(a))
         
