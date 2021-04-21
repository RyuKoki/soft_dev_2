from Twidty import Twidty
from spacy.lang.en.stop_words import STOP_WORDS
import unittest, tweepy, pythainlp, re, collections, operator, functools, datetime

class TwidtyTest(unittest.TestCase):

	twidty = Twidty()
	test_input = '''@nicha เอามาแบ่งปันสำหรับคนที่สนใจสินค้า cruelty-free ค่ะ 😁💕 https://ethicalelephant.com/cruelty-free-logos/ #SaveRalph'''
	keyword = 'cruelty-free'

	'''def testAutentication(self):
		self.assertEqual(type(self.twidty.authentication()), 
						type(tweepy.api))

	def testText_intercept(self):
		test_predict = "เอามาแบ่งปันสำหรับคนที่สนใจสินค้า cruelty-free ค่ะ"
		self.assertEqual(self.twidty.text_intercept(self.test_input), 
						test_predict)

	def testCheck_hashtags(self):
		test_predict = ["#SaveRalph"]
		self.assertEqual(self.twidty.check_hashtags(self.test_input), 
						test_predict)

	def testStopwords(self):
		th_stopwords = pythainlp.corpus.thai_stopwords()
		add_en_stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 
						'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 
						'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 
						"she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 
						'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 
						'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 
						'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 
						'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 
						'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 
						'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 
						'through', 'during', 'before', 'after', 'above', 'below', 'to', 
						'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 
						'again', 'further', 'then', 'once', 'here', 'there', 'when', 
						'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 
						'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 
						'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 
						'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 
						're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', 
						"didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', 
						"haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 
						'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 
						'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]
		for adding_word in list(STOP_WORDS):
			add_en_stopwords.append(adding_word)
		pattern = r"[\'\"\“\”\‘\’]"
		en_stopwords = []
		for word in add_en_stopwords:
			result = re.sub(pattern, "", word)
			en_stopwords.append(result)
		test_predict = {"stopword_en":en_stopwords, "stopword_th":th_stopwords}
		twidty_en_stopwords = len(self.twidty.stopwords()['stopword_en'])
		twidty_th_stopwords = len(self.twidty.stopwords()['stopword_th'])
		self.assertEqual(twidty_en_stopwords+twidty_th_stopwords, 
							len(test_predict['stopword_en'])+len(test_predict['stopword_th']))'''

	def testNLP(self):
		test_input = "เอามาแบ่งปันสำหรับคนที่สนใจสินค้า cruelty-free"
		test_predict = ['แบ่งปัน', 'สำหรับ', 'คน', 'สนใจ', 'สินค้า']
		self.assertEqual(self.twidty.nlp(test_input, self.keyword), 
						test_predict)

	'''def testFrequency_word(self):
		test_input = ['แบ่งปัน', 'สำหรับ', 'คน', 'สนใจ', 'สินค้า', 'สำหรับ', 'ไม่ทารุน', 'สัตว์']
		test_num_freq = 3
		counter = dict(collections.Counter(test_input))
		test_predict = dict(sorted(counter.items(), 
									key=operator.itemgetter(1), 
									reverse=True)[:test_num_freq])
		self.assertDictEqual(self.twidty.frequency_word(self.keyword, test_input, test_num_freq), 
							test_predict)

	def testExtend_items(self):
		test_input = ["['แบ่งปัน', 'สำหรับ', 'คน', 'สนใจ', 'สินค้า']", "['สำหรับ', 'ไม่ทารุน', 'สัตว์']"]
		test_predict = {'สำหรับ': 2, 'แบ่งปัน': 1, 'คน': 1, 'สนใจ': 1, 'สินค้า': 1}
		self.assertEqual(self.twidty.extend_items(self.keyword, test_input), 
						test_predict)

	def testSentiment(self):
		test_pos_th = 'คุณหล่อมาก'
		test_neu_th = 'ไปก็ไปด้วยกัน'
		test_neg_th = 'ร้านนี้บริการห่วยแตก'
		test_pos_en = 'You are so handsome.'
		test_neu_en = 'Let go together!'
		test_neg_en = 'This sevices are so bad.'
		self.assertEqual(twidty.sentiment(test_pos_th), 'positive')
		self.assertEqual(twidty.sentiment(test_neu_th), 'neutral')
		self.assertEqual(twidty.sentiment(test_neg_th), 'negative')
		self.assertEqual(twidty.sentiment(test_pos_en), 'positive')
		self.assertEqual(twidty.sentiment(test_neu_en), 'neutral')
		self.assertEqual(twidty.sentiment(test_neg_en), 'negative')

	def testTrendy(self):
		self.assertEqual(type(self.twidty.trendy()), type(list()))

	def testSave_new_data(self):
		keyword = 'อังคารคลุมโปง'
		now = datetime.datetime.now()
		self.assertEqual(self.twidty.save_new_data(keyword, str(now.date())), None)

	def testSearch(self):
		keyword = 'bitcoin'
		start_db = '2021-03-23'
		stop_db = '2021-03-31'
		self.assertEqual(type(self.twidty.search(keyword, start_db, stop_db)), 
						type(dict()))
		new_keyword = 'test_keyword'
		self.assertEqual(self.twidty.search(new_keyword, start_db, stop_db), False)
		now = datetime.datetime.now()
		step_date = datetime.timedelta(days=1)
		start_not_db = now + step_date
		self.assertEqual(self.twidty.search(keyword, str(start_not_db.date()), str(start_not_db.date())), True)'''


if __name__ == "__main__":
	unittest.main()
