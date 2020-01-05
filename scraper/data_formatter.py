import re
from dateutil.relativedelta import relativedelta
from datetime import date

import db.dbkey as dbkey
import common.util as util

class DataFormatError(Exception):
    pass

AGE_SET = {'年齢：可変（永遠の17歳、初体験は20歳、100垓歳)': -1, # 花畑チャイカ
						 '年齢：樹齢19年(人とは年齢の数え方が違うらしく、飲酒はできるらしい)':19, # 桜凛月
						 '不詳(肉体年齢': 11,
						 '年齢：不明(200を過ぎてから数えなくなった)': 200, # 戌亥とこ
						 '年齢：26歳*3　→18歳': 27, # アンジュ・カトリーナ
						 '年齢永遠の20歳（次の誕生日で5000兆歳)5000兆歳はにじさんじ内で最年長になりたかった結果。最初はモイラ様越えの46億1歳になろうとしたが年齢不詳のベルモンド・バンデラスに勝つために余裕をもって増やした。ただ最年長は焼肉を奢らないといけないらしいため5000兆歳になるのは土下座を持って撤回するそうだ': 20, # エクス
						 '年齢：ピチピチの20代': 22, # 早瀬走
						 '年齢：お酒を飲める': 24, # 山神カルタ
						 '年齢:17歳 (ロングヘアの時は 23歳、ポニーテールの時は14歳)': 17,  # 静凛
						 '年齢：不明（地球誕生の頃には既に居たらしい。約46億歳超。）': 4600000000,  # モイラ
						 '年齢：10歳(体力年齢45歳→38歳)/15歳(精神年齢は10歳)*1(オトナver.)': 10,  # 森中花咲
						 '年齢：??歳*4': -1,
						 '年齢：未成年*6': 19,   # 本間ひまわり
						 '年齢：100歳から数えてないので不明': 100,  # 葛葉G
						 '年齢：16歳(121歳説あり)*1': 16,  # 町田ちま
						 '年齢：不明（成人済み）(VOIZ所属時は高校二年生の１７歳）': 20, # 成瀬鳴
						 '年齢：不明(46億歳以上138億歳未満・ビッグバン以降)*1': 10000000000,  # ベルモンドバンデラス
						 '年齢：20歳(切り捨て)*1': 20, # 郡道美玲
						 '年齢：22歳（24歳説、10歳説もあり）': 24, # 御伽原江良 (バランス年齢24歳より判断)
						 '年齢：永遠の20歳(誕生日の直前だけ19歳になる)': 20,  # 三枝明那
						 '年齢：永遠の21歳(誕生日ごとにバストサイズが1cm増える)': 21, # 愛園愛美
						 '年齢：不明 (こちらの世界に飛ばされたときに忘れてしまった)': -1, # ラトナ・プティ
						 '年齢：お酒は飲めるお年頃、レディに年齢聞くなんて失礼よ！': -1, # 健屋花那
						 '年齢：不詳': -1, # ルイス・キャミー
						 '年齢：20歳は超えてる': 20} # 不破湊

HEIGHT_SET = {'身長：138cm／153cm（18歳ver.）': 138, # 勇気ちひろ
								'身長：135cm/152cm (オトナver.)': 135, # 森中花咲
								'身長：15ｻｱﾝ!cm': 153, # 雪汝 
								'身長・体重：不詳*4 → 身長は170ちょっと、角を含めると175*5': 175, # ドーラ
								'身長：150cm+ヒール15cm＝靴を履いた時165cm': 150,  # 桜凛月
								'身長：不明': -1, # 語部紡
						 		'身長：158cm*4*5(頭上のセバスピヨも含め166cm)': 166, # リゼ・ヘルエスタ
						 		'身長：163cm(ヒール込みで167cm)': 163, # 健屋花那
						 		'身長：たぶん183らしいです。': 183, # シェリン・バーガンディ
						 		'身長：155cm(「良い感じの女の子の身長でございます。」)(靴は体の一部)': 155, # 星川サラ
						 		'身長：174cm(ヒール込みだと178cm)': 174, # 白雪巴
						 		'身長158cm（靴込みだと170cm*1）': 158} # Virtual Diva AZKi

def count_age(birthday_text):
	numbers = [int(number) for number in re.split('[年月日]', birthday_text) if number.isdecimal()]
	result = relativedelta(date.today(), date(numbers[0], numbers[1], numbers[2]))
	return result.years

def age(text, is_required=True):
	print('FMT : age: text = {}'.format(text))
	if text in AGE_SET:
		return AGE_SET[text]

	if '17+200歳の女子高生ハーフエルフ' in text: # ホロライブ：アキ・ローゼンタール
		return 217

	if '小学4年生' in text:
		return 10
	elif '女子高生' in text:
		return 17
	elif re.search('高校(3|三|)(年|)生', text):
		return 18
	elif re.search('高校(2|二|)(年|)生', text):
		return 17
	elif re.search('高校(1|一|)年生', text):
		return 16

	matchs = re.findall('[0-9]{1,6}[歳, さい]', text)
	if matchs:
		return util.numeric(matchs[-1])

	match = re.search('[0-9]{4}年[0-9]{1,2}月[0-9]{1,2}日', text)
	if match:
		return count_age(match[0])

	if text.startswith('西暦'):  # '西暦2002年11月11日' 等
		return int(extract_career(text.replace('西暦', ''))[:2])

	match = re.search('年齢：[0-9]{1,2}', text)
	if match:
		return util.numeric(match[0])

	if is_required:
		raise DataFormatError('invalid age format : {}'.format(text))
	return -1

def birthday(text):
	print('FMT : birthday : text = {}'.format(text))
	match = re.search('[0-9]{1,2}/[0-9]{1,2}', text)
	if match:
		return match[0]
	match = re.search('[0-9]{1,2}月[0-9]{1,2}日', text)
	if match:
		texts = match.group().split('月')
		return texts[0] + '/' + texts[1].replace('日', '')

	raise DataFormatError('invalid birthday format : {}'.format(text))

def height(text):
	print('FMT : height : text = {}'.format(text))
	if text in HEIGHT_SET:
		return HEIGHT_SET[text]

	match = re.search('[0-9]{1,999}バット', text)
	if match:
		return util.numeric(match.group())
	else:
		match = re.search('[0-9]{1,999}もいもい', text)
		if match:
			return util.numeric(match.group())
		else:
			matchs = re.findall('[0-9]{1,999}.[0-9]{1}[cm,ｃｍ,㎝]', text)
			if matchs:
				return util.numeric(matchs[-1])

	raise DataFormatError('invalid height format : {}'.format(text))




















def get_age(birthday):
	result = relativedelta(date.today(), date(birthday[0], birthday[1], birthday[2]))
	return '{}-{}-{}'.format(result.years, result.months, result.days)


def extract_name(name):
	return name.replace('\n', '')

def extract_youtube(url):
	return url

if __name__ == '__main__':
	pass

