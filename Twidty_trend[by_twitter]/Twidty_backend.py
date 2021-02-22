import tweepy, pandas, re, emoji, spacy, pythainlp, collections, datetime, os, ast, operator, threading


class Twidty(object):

	def __init__(self):
		# consumer keys and authentication tokens
		# from https://developer.twitter.com
		self.consumer_key = 'xxx'
		self.consumer_secret = 'xxx'
		self.access_token = 'xxx'
		self.access_token_secret = 'xxx'

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
		mention_pattern = r'(?:@[\w_]+)'
		hashtag_pattern = r"(?:\#+[\w\ก-๙_]+[\w\ก-๙\'_\-]*[\w\ก-๙_]+)"
		web_pattern = r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+'
		enter_pattern = r'[\n\t]'
		punctuations = r'[\!\(\)\-\[\]\{\}\:\;\'\\\"\,\<\>\.\/\?\@\$\%\^\&\*\_\~\ๆ]'
		del_ment = re.sub(mention_pattern, '', text)
		del_tags = re.sub(hashtag_pattern, '', del_ment)
		del_web = re.sub(web_pattern, '', del_tags)
		del_enter = re.sub(enter_pattern, '', del_web)
		del_punct = re.sub(punctuations, '', del_enter)
		return del_punct

	def check_hashtags(self, text):
		# have to '#' at least 1
		# This is for thai and english language 
		hashtags_str = r"(?:\#+[\w\ก-๙_]+[\w\ก-๙\'_\-]*[\w\ก-๙_]+)"
		# find hashtags in tweet
		hashtags_regex = re.findall(hashtags_str, text)
		# print(hashtags_regex.findall(text))
		return hashtags_regex

	def nlp(self, text, keyword):
		spacy.load('en_core_web_sm')
		stopword_en = list(spacy.lang.en.stop_words.STOP_WORDS) # 362 words
		stopword_th = list(pythainlp.corpus.thai_stopwords()) # 1030 words
		process = pythainlp.word_tokenize(text, engine='newmm') # list type
		result = []
		for word in process:
			if word in stopword_th or word in stopword_en or word == keyword or word == ' ':
				continue
			else:
				result.append(word)

		return result

	def frequency_word(self, text_list):
		frequency = dict(collections.Counter(text_list))
		try:
			frequency.pop(' ')
		except:
			pass

		try:
			ranking = dict(sorted(frequency.items(), 
									key=operator.itemgetter(1), 
									reverse=True)[:5])
		except:
			pass
		return ranking

	def extend_items(self, items_list):
		list_output = []
		for a_list in items_list:
			list_output.extend(ast.literal_eval(a_list))
		return self.frequency_word(list_output)

	def search(self, keyword, start, stop):
		api = self.authentication()
		query = str(keyword).replace('#', '')

		df_tokenize = pandas.DataFrame(columns=['Date', 'Text', 'Hashtag'])

		df_text = pandas.DataFrame(columns=['Date', 'Text'])

		start_d = datetime.datetime.strptime(start, '%Y-%m-%d')
		stop_d = datetime.datetime.strptime(stop, '%Y-%m-%d')
		step_d = datetime.timedelta(days=1)
		while start_d <= stop_d:
			tweets = tweepy.Cursor(api.search, 
									q=query+'-filter:retweets', 
									since=str(start_d.date()), 
									until=str((start_d+step_d).date()), 
									result_type='recent', 
									tweet_mode='extended').items(50)
			for tweet in tweets:
				date = tweet.created_at.date()
				try:
					text = tweet.retweeted_status.full_text
				except:
					text = tweet.full_text
				
				text_intercept = self.text_intercept(text)
				text_intercept = " ".join(text_intercept.split())
				data_row_text = pandas.Series([date, text_intercept], index=df_text.columns)
				df_text = df_text.append(data_row_text, ignore_index=True)

				find_hashtags = self.check_hashtags(text)
				
				text_tokenize = self.nlp(text_intercept, query)
				data_row_tok = pandas.Series([date, text_tokenize, find_hashtags], index=df_tokenize.columns)
				df_tokenize = df_tokenize.append(data_row_tok, ignore_index=True)

			start_d += step_d

		df_tokenize.to_csv(r'D:\vs code\soft_dev_2\midterm_pro\data\twidty_tokenize\{}.csv'.format(query), index=False)
		df_text.to_csv(r'D:\vs code\soft_dev_2\midterm_pro\data\twidty_text\{}.csv'.format(query), index=False)


	def update_data_by_date(self, keyword, year, month, day):
		api = self.authentication()
		query = str(keyword).replace('#', '')
		due_date = datetime.date(year, month, day)
		next_date = datetime.timedelta(days=1)
		tweets = tweepy.Cursor(api.search, 
								q=query+'-filter:retweets', 
								since=str(due_date), 
								until=str(due_date+next_date), 
								result_type='recent', 
								tweet_mode='extended').items(50)
		# lastest_row = pandas.read_csv(r'D:\vs code\soft_dev_2\twitter\data\twidty_tokenize\{}.csv'.format(query))
		file_token = pandas.read_csv(r'D:\vs code\soft_dev_2\midterm_pro\data\twidty_tokenize\{}.csv'.format(query))
		file_text = pandas.read_csv(r'D:\vs code\soft_dev_2\midterm_pro\data\twidty_text\{}.csv'.format(query))
		for tweet in tweets:
			date = tweet.created_at.date()
			try:
				text = tweet.retweeted_status.full_text
			except:
				text = tweet.full_text
			text_intercept = self.text_intercept(text)
			text_intercept = " ".join(text_intercept.split())
			data_row_text = pandas.Series([date, text_intercept], index=file_text.columns)
			file_text = file_text.append(data_row_text, ignore_index=True)

			find_hashtags = self.check_hashtags(text)
			text_tokenize = self.nlp(text_intercept, query)

			data_row = pandas.Series([date, text_tokenize, find_hashtags], index=file_token.columns)
			file_token = file_token.append(data_row, ignore_index=True)

		file_token.to_csv(r'D:\vs code\soft_dev_2\midterm_pro\data\twidty_tokenize\{}.csv'.format(query), index=False)
		file_text.to_csv(r'D:\vs code\soft_dev_2\midterm_pro\data\twidty_text\{}.csv'.format(query), index=False)

	def trend_tags(self, number):
		api = self.authentication()
		WOEID = 23424960
		trends = api.trends_place(id=WOEID)
		# print(trends)
		trends_list = {}
		for i in trends:
			for j in i['trends']:
				if j['tweet_volume'] == None:
					pass
				elif j['tweet_volume'] != None:
					key, values = j['name'], j['tweet_volume']
					trends_list.update({key:values})
		ranking = dict(sorted(trends_list.items(), 
									key=operator.itemgetter(1), 
									reverse=True)[:int(number)])
		return ranking

	def frequency_analysis(self, keyword, start, stop):
		search_file = keyword.replace('#', '')
		file_name = "{}.csv".format(search_file)
		db = os.listdir(r'D:\vs code\soft_dev_2\midterm_pro\data\twidty_tokenize')
		df = pandas.read_csv(r'D:\vs code\soft_dev_2\midterm_pro\data\twidty_tokenize\{}.csv'.format(search_file))
		all_date = list(df['Date'])
		if file_name in db:
			if '#' in keyword:
				if start not in all_date or stop not in all_date:
					start_date = df['Date'].min()
					end_date = df['Date'].max()
					return [0, start_date, end_date]
				new_df = df.loc[(df['Date'] >= start) & (df['Date'] <= stop)]
				counter = self.extend_items(new_df['Hashtag'])
				return dict(counter)
			elif '#' not in keyword:
				if start not in all_date or stop not in all_date:
					start_date = df['Date'].min()
					end_date = df['Date'].max()
					return [0, start_date, end_date]
				new_df = df.loc[(df['Date'] >= start) & (df['Date'] <= stop)]
				counter = self.extend_items(new_df['Text'])
				return dict(counter)
		elif file_name not in db:
			return False
