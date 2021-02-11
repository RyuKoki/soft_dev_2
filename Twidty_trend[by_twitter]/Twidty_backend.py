import tweepy, pandas, re, emoji, spacy, pythainlp, collections, datetime, os, ast, operator


class Twidty(object):

    def __init__(self):
        # consumer keys and authentication tokens
        # from https://developer.twitter.com
        self.consumer_key = 'xxxxxxxxxx'
        self.consumer_secret = 'xxxxxxxxxx'
        self.access_token = 'xxxxxxxxxx'
        self.access_token_secret = 'xxxxxxxxxx'

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
            if word in stopword_th or word in stopword_en or word == keyword:
                pass
            else:
                result.append(word)

        return result

    def frequency_word(self, text_list):
        frequency = dict(collections.Counter(text_list))
        try:
            frequency.pop(' ')
            frequency.pop(' '*2)
            frequency.pop(' '*3)
            frequency.pop(' '*4)
            frequency.pop(' '*5)
            frequency.pop(' '*6)
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

    def search(self, keyword):
        api = self.authentication()
        query = str(keyword).replace('#', '')
        tweets = tweepy.Cursor(api.search, 
                                q=query+'-filter:retweets', 
                                count=100, 
                                result_type='recent', 
                                tweet_mode='extended').items()
        df = pandas.DataFrame(columns=['Date', 'Text', 'Hashtag'])
        for tweet in tweets:
            date = tweet.created_at

            try:
                text = tweet.retweeted_status.full_text
            except:
                text = tweet.full_text

            find_hashtags = self.check_hashtags(text)
            text_intercept = self.text_intercept(text)
            text_tokenize = self.nlp(text_intercept, query)
            data_row = pandas.Series([date.date(), text_tokenize, find_hashtags], index=df.columns)
            df = df.append(data_row, ignore_index=True)
            
            count_row = len(df.index)
            if count_row == 100:
                break

        df = df.sort_values(by='Date')
        df.to_csv(r'xxxxxxxxxxxxxxx\{}.csv'.format(keyword.replace('#', '')), index=False) # xxxxxxxxxxxx is path of directory that you want to save

    def update_data(self, keyword):
        api = self.authentication()
        query = str(keyword).replace('#', '')
        tweets = tweepy.Cursor(api.search, 
                                q=query+'-filter:retweets', 
                                result_type='recent', 
                                tweet_mode='extended').items(100)
        lastest_row = pandas.read_csv(r'xxxxxxxxxxxxxxx\{}.csv'.format(keyword.replace('#', '')))# xxxxxxxxxxxx is path of directory that you want to save
        data_file = pandas.read_csv(r'xxxxxxxxxxxxxxx\{}.csv'.format(keyword.replace('#', '')))
        today = datetime.datetime.now().date()
        for tweet in tweets:
            date = tweet.created_at
            if date.date() == today:
                try:
                    text = tweet.retweeted_status.full_text
                except:
                    text = tweet.full_text

                find_hashtags = self.check_hashtags(text)
                text_intercept = self.text_intercept(text)
                text_tokenize = self.nlp(text_intercept, query)
                data_row = pandas.Series([date.date(), text_tokenize, find_hashtags], index=data_file.columns)
                data_file = data_file.append(data_row, ignore_index=True)

                check_row = len(data_file.index)
                if check_row == len(lastest_row)+100:
                    break
        data_file.to_csv(r'xxxxxxxxxxxxxxx\{}.csv'.format(keyword.replace('#', '')), index=False)

    def update_data_by_date(self, keyword, year, month, day):
        api = self.authentication()
        query = str(keyword).replace('#', '')
        tweets = tweepy.Cursor(api.search, 
                                q=query+'-filter:retweets', 
                                count=100, 
                                result_type='recent', 
                                tweet_mode='extended').items()
        lastest_row = pandas.read_csv(r'xxxxxxxxxxxxxxx\{}.csv'.format(keyword.replace('#', '')))
        data_file = pandas.read_csv(r'xxxxxxxxxxxxxxx\{}.csv'.format(keyword.replace('#', '')))
        for tweet in tweets:
            date = tweet.created_at
            if date.date() == datetime.date(year, month, day):
                try:
                    text = tweet.retweeted_status.full_text
                except:
                    text = tweet.full_text

                find_hashtags = self.check_hashtags(text)
                text_intercept = self.text_intercept(text)
                text_tokenize = self.nlp(text_intercept, query)
                data_row = pandas.Series([date.date(), text_tokenize, find_hashtags], index=data_file.columns)
                data_file = data_file.append(data_row, ignore_index=True)

                check_row = len(data_file.index)
                if check_row == len(lastest_row)+100:
                    break
        data_file.to_csv(r'xxxxxxxxxxxxxxx\{}.csv'.format(keyword.replace('#', '')), index=False)

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
        db = os.listdir('data')
        if file_name in db:
            if '#' in keyword:
                df = pandas.read_csv(r'D:\vs code\soft_dev_2\twitter\data\{}.csv'.format(search_file))
                if stop != df['Date'].max() or start != df['Date'].min():
                    start_date = df['Date'].min()
                    end_date = df['Date'].max()
                    return [0, start_date, end_date]
                new_df = df.loc[(df['Date'] >= start) & (df['Date'] <= stop)]
                counter = self.extend_items(new_df['Hashtag'])
                return counter
            elif '#' not in keyword:
                df = pandas.read_csv(r'D:\vs code\soft_dev_2\twitter\data\{}.csv'.format(search_file))
                if stop != df['Date'].max() or start != df['Date'].min():
                    start_date = df['Date'].min()
                    end_date = df['Date'].max()
                    return [0, start_date, end_date]
                new_df = df.loc[(df['Date'] >= start) & (df['Date'] <= stop)]
                counter = self.extend_items(new_df['Text'])
                return counter
        elif file_name not in db:
            return False
