from bs4 import BeautifulSoup
import requests

html = requests.get('https://www.w3.org/History/19921103-hypertext/hypertext/WWW/TheProject.html')
bs = BeautifulSoup(html.text, 'html.parser')
# print(bs)
# print(bs.text)
# print(bs.h1.text)
print(bs.title.text)

# print(bs.a['href'])

'''
for a in bs.find_all('a'):
	print(a['href'])
'''
