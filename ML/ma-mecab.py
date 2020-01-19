import MeCab

mecab = MeCab.Tagger('-Ochasen')
malist = mecab.parse('庭には二羽鶏がいる')
print(malist)
