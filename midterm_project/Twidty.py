import tweepy, datetime, threading, requests
import re, emoji, langdetect
import spacy, pythainlp
import collections, ast, operator, functools
import pandas, os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from spacy.lang.en.stop_words import STOP_WORDS

class Twidty(object):

	def __init__(self):
		# consumer keys and authentication tokens
		# from https://developer.twitter.com
		self.consumer_key = 'xxx'
		self.consumer_secret = 'xxx'
		self.access_token = 'xxxxxx'
		self.access_token_secret = 'xxx'
		self.save_file_path = r"D:\vs code\soft_dev_2\midterm_pro\data\twitter"
		self.data_sentiment = self.sentiment_words_data()
		self.data_negative = self.data_sentiment['negative']
		self.data_positive = self.data_sentiment['positive']
		self.data_swear = self.data_sentiment['swear']
		self.data_stopwords = self.stopwords()
		self.stopwords_en = self.data_stopwords['stopword_en']
		self.stopwords_th = self.data_stopwords['stopword_th']

	def sentiment_words_data(self):
		positive_vocab = []
		negative_vocab = []
		swear_words = []
		with open(r"D:\vs code\soft_dev_2\carry\negative-sentiment-words.txt", 'r', encoding='utf-8') as f:
			for line in f:
				negative_vocab.append(line.rstrip())
		with open(r"D:\vs code\soft_dev_2\carry\positive-sentiment-words.txt", 'r', encoding='utf-8') as f:
			for line in f:
				positive_vocab.append(line.rstrip())
		with open(r"D:\vs code\soft_dev_2\carry\swear-words.txt", 'r', encoding='utf-8') as f:
			for line in f:
				swear_words.append(line.rstrip())
		return {'negative':negative_vocab, 'positive':positive_vocab, 'swear':swear_words}

	def stopwords(self):
		# list of english stop words
		stopword_en_1 = list(STOP_WORDS) # 362 words
		stopword_en_2 = []
		with open(r"D:\vs code\soft_dev_2\midterm_pro\stopwords_en_adding.txt", 'r', encoding='utf-8') as f:
			for line in f:
				stopword_en_2.append(line.rstrip())
		pattern = r"[\'\"\“\”\‘\’]"
		stopword_en = []
		for i in stopword_en_1:
			i_c = re.sub(pattern, "", i)
			stopword_en.append(i_c)
		for j in stopword_en_2:
			j_c = re.sub(pattern, "", j)
			stopword_en.append(j_c)
		# list of thai stop words
		stopword_th = list(pythainlp.corpus.thai_stopwords()) # 1030 words
		return {"stopword_en":stopword_en, "stopword_th":stopword_th}

	def authentication(self):
		# confirm identity
		auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
		auth.set_access_token(self.access_token, self.access_token_secret)
		api = tweepy.API(auth)
		return api

	def text_intercept(self, text):
		all_emoji = emoji.UNICODE_EMOJI
		for i in text:
			if i in all_emoji:
				text = text.replace(i, '')
		# pattern for keeping mentions
		mention_pattern = r'(?:@[\w_]+)'
		# pattern for keeping hashtags
		hashtag_pattern = r"(?:\#+[\w\ก-๙_]+[\w\ก-๙\'_\-]*[\w\ก-๙_]+)"
		# pattern for keeping links of website
		web_pattern = r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+'
		# pattern for 'enter' and 'tab'
		enter_pattern = r'[\n\t]'
		# pattern for punctuations
		punctuations = r"[^\w\s]"
		# pattern for digits
		digits_pattern = r'[0-9]|[๐-๙]'
		# delete 'mentions' from post
		del_ment = re.sub(mention_pattern, '', text)
		# delete 'hashtags' from post
		del_tags = re.sub(hashtag_pattern, '', del_ment)
		# delete 'links of website' from post
		del_web = re.sub(web_pattern, '', del_tags)
		# delete 'enter' and 'tab' from post
		del_enter = re.sub(enter_pattern, '', del_web)
		# delete 'punctuations' from post
		del_punct = re.sub(punctuations, '', del_enter)
		# delete 'digit number'
		del_digit = re.sub(digits_pattern, '', del_punct)
		# final values
		result = " ".join(del_digit.split())
		return result

	def check_hashtags(self, text):
		# have to '#' at least 1
		# This is for thai and english language 
		hashtags_str = r"(?:\#+[\w\ก-๙_]+[\w\ก-๙\'_\-]*[\w\ก-๙_]+)"
		# find hashtags in tweet
		hashtags_regex = re.findall(hashtags_str, text)
		# print(hashtags_regex.findall(text))
		return hashtags_regex

	def nlp(self, text, keyword):
		process = pythainlp.word_tokenize(text, engine='newmm') # list type
		# list for finally result 
		result = []
		# check stop word from text
		for word in process:
			if word in self.stopwords_th or word.lower() in self.stopwords_en:
				continue
			elif word.lower() == keyword or word == ' ':
				continue
			else:
				result.append(word)

		return result

	def frequency_word(self, keyword, text_list, number):
		# count each tokenize words
		frequency = dict(collections.Counter(text_list))
		# get key of frequency dictionary
		keys = list(frequency.keys())
		# all of punctuations
		punctuations = '''!()+-[]{}:;'\",<>./?@$%^&*_~ๆ“”‘’|฿— \u200b\u2014'''
		for key in keys:
			# if it's the key pop it from dict()
			if key in punctuations:
				frequency.pop(key)
			# if lower of words is keyword pop it
			if key.lower() == keyword.lower():
				frequency.pop(key)
			if key.lower() in self.stopwords_en or key in self.stopwords_th:
				frequency.pop(key)
		# try to sort by values of dict() type
		ranking = dict(sorted(frequency.items(), 
							key=operator.itemgetter(1), 
							reverse=True)[:number])
		return ranking

	def extend_items(self, keyword, items_list):
		list_output = []
		# casting string of list to list()
		for a_list in items_list:
			list_output.extend(ast.literal_eval(a_list.strip()))
		return self.frequency_word(keyword, list_output, 5)

	def merge_many_ranking(self, keyword, dict_data):
		try:
			result = dict(functools.reduce(operator.add, map(collections.Counter, dict_data)))
		except:
			result = {keyword:0}
		return result

	def sentiment(self, text, list_text_tokenize):
		thai_sentiment = self.sentiment_th(list_text_tokenize)
		if thai_sentiment == 'neutral' and langdetect.detect(text) != 'th':
			eng_sentiment = self.sentiment_en(text)
			result = eng_sentiment
		else:
			result = thai_sentiment
		return result

	def sentiment_en(self, text):
		sentiment_vader = SentimentIntensityAnalyzer()
		sentiment_text = sentiment_vader.polarity_scores(text)
		if sentiment_text['compound'] >= 0.05:
			return 'positive'
		elif sentiment_text['compound'] <= -0.05:
			return 'negative'
		else:
			return 'neutral'

	def sentiment_th(self, tokenize_text_list):
		negative = 0
		positive = 0
		for word in tokenize_text_list:
			if word in self.data_positive:
				positive += 1
			elif word in self.data_negative or word in self.data_swear:
				negative += 1
		if positive > negative:
			return 'positive'
		elif negative > positive:
			return 'negative'
		else:
			return 'neutral'

	def trendy(self):
		woeid = 23424960 #thailand woeid
		api = self.authentication()
		trends = api.trends_place(id=woeid)
		trends_list = []
		for value in trends:
			for trend in value['trends']:
				# print(trend['name'])
				trends_list.append(trend['name'])
		return trends_list

	def save_new_data(self, keyword, start):
		# authentication of twitter from API keys
		api = self.authentication()
		# if search in hashtag, delete it and search by word
		query = str(keyword).replace('#', '')
		# create path of keyword for storage
		path = r"D:\vs code\soft_dev_2\midterm_pro\data\twitter\{}".format(query)
		# os.mkdir(path)
		# casting string of date() in datetime() type
		start_d = datetime.datetime.strptime(start, '%Y-%m-%d')
		# stop_d = datetime.datetime.strptime(stop, '%Y-%m-%d')
		# use step date (1 day) for adding start day to stop day
		step_d = datetime.timedelta(days=1)
		# create data frame
		df = pandas.DataFrame(columns=['Date', 'Tokenize', 'Hashtag', 'Sentiment'])
		# use tweepy API for searching keyword
		# print('search api')
		tweets = tweepy.Cursor(api.search, count=100, 
								q=query+'-filter:retweets', 
								since=str(start_d.date()), 
								until=str((start_d+step_d).date()),
								result_type='recent', 
								tweet_mode='extended').items(500) 
		# access in all tweets that keeping
		for tweet in tweets:
			# date in post
			date = tweet.created_at.date()
			# keeping full text from post
			try:
				text = tweet.retweeted_status.full_text
			except:
				text = tweet.full_text
			# intercept the punctuations and non-characters
			text_intercept = self.text_intercept(text)
			# intercept double space bar
			text_intercept = " ".join(text_intercept.split())
			# use re library find hashtag from post
			find_hashtags = self.check_hashtags(text)
			# tokenize sentences
			text_tokenize = self.nlp(text_intercept, query)
			# print(text_tokenize)
			# try to analysis sentiment of sentense
			try:
				text_sentiment = self.sentiment(text, text_tokenize)
				# print(text_sentiment)
			except:
				# print('continue')
				continue
			# add tokenize data in data row
			data_row_tok = pandas.Series([date, text_tokenize, find_hashtags, text_sentiment], index=df.columns)
			# add data row in data frame
			df = df.append(data_row_tok, ignore_index=True)
			# use only 50 data per day
			if len(df.index) == 100:
				break
			# print("next")
		# save csv file of all data
		df.to_csv(path + r'\{}.csv'.format(start), index=False)

	def search(self, keyword, start, stop):
		# casting string datetime to datetime
		start_d = datetime.datetime.strptime(start, '%Y-%m-%d')
		stop_d = datetime.datetime.strptime(stop, '%Y-%m-%d')
		# setting timedelta
		step_d = datetime.timedelta(days=1)
		check_seven_date = datetime.timedelta(days=7)
		date_now = datetime.datetime.now()
		# getting path of keyword for storing
		path = r"D:\vs code\soft_dev_2\midterm_pro\data\twitter"
		# list of keywords
		all_keys = os.listdir(path)
		# checking parameter keyword is in all_keys
		if keyword not in all_keys:
			os.mkdir(path + r"\{}".format(keyword))
			return False
		else:
			path_data = path + r"\{}".format(keyword)
			# for carrying the freqencies of words
			freq_carry = []
			# for carrying the sentiment of sentence that have searched word
			sent_carry = []
			# access all file from date to search
			while start_d <= stop_d:
				# list of all data in keyword
				data_date = os.listdir(path_data)
				# if searching date is not in list of all data of keyword
				# and its date has to less or equal than 7 days (twitter API rate limit)
				if (str(start_d.date())+'.csv' not in data_date) and ((date_now-start_d) <= check_seven_date):
					return True
				elif (str(start_d.date())+'.csv' in data_date):
					# if str(start_d.date())+'.csv' in data_date:
					read_df = pandas.read_csv(path_data + r"\{}.csv".format(start_d.date()))
					freq_cnt = self.extend_items(keyword, read_df['Tokenize'])
					# print(freq_cnt)
					freq_carry.append(freq_cnt)
					sent_cnt = read_df['Sentiment']
					sent_carry.append(dict(collections.Counter(sent_cnt)))
					start_d += step_d
				else:
					start_d += step_d
			freq_result = self.merge_many_ranking(keyword, freq_carry)
			sent_result = self.merge_many_ranking(keyword, sent_carry)
			# print(freq_result)
			# print(sent_result)
			ranking = dict(sorted(freq_result.items(), 
										key=operator.itemgetter(1), 
										reverse=True)[:5])
			# print(ranking)
			return {"related_words":ranking, "sentiment":sent_result}
