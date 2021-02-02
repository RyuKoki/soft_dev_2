import tweepy, pandas, re, emoji, spacy, pythainlp, collections, langdetect, os, ast, operator
import matplotlib.pyplot as plt

class Twidty(object):

    def __init__(self):
        # consumer keys and authentication tokens
        # from https://developer.twitter.com
        self.consumer_key = 'xxxxxxxxxxx'
        self.consumer_secret = 'xxxxxxxxxxx'
        self.access_token = 'xxxxxxxxxxx'
        self.access_token_secret = 'xxxxxxxxxxx'

    def authentication(self):
        # confirm identity
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        api = tweepy.API(auth)
        return api

    def text_intercept(self, text):
        # delete emojis from text
        all_emoji = emoji.UNICODE_EMOJI
        for i in text:
            if i in all_emoji:
                text = text.replace(i, '')
        # delete mention (@)
        mention_pattern = r'(?:@[\w_]+)'
        # delete hashtags (#)
        hashtag_pattern = r"(?:\#+[\w\ก-๙_]+[\w\ก-๙\'_\-]*[\w\ก-๙_]+)"
        # delete website links
        web_pattern = r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+'
        # delete enter and tabs
        enter_pattern = r'[\n\t]'
        # delete all punctuations
        punctuations = r'[\!\(\)\-\[\]\{\}\:\;\'\\\"\,\<\>\.\/\?\@\$\%\^\&\*\_\~\ๆ]'
        # reference : https://marcobonzanini.com/2015/03/02/mining-twitter-data-with-python-part-1/
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
        # use spacy module and pythainlp
        # # @cmd >> pip install spacy
        # # @vs code [terminal] >> python -m pip install spacy 
        # # and you have to download dataset of 'en_core_web_sm' by ... >> python -m pip install spacy download en_core_web_sm
        spacy.load('en_core_web_sm')
        stopword_en = spacy.lang.en.stop_words.STOP_WORDS # 362 words
        stopword_th = list(pythainlp.corpus.thai_stopwords()) # 1030 words
        process = pythainlp.word_tokenize(text, engine='newmm') # list type
        # delete all of stop words
        for a_word in process:
            if (a_word in stopword_th) or (a_word in stopword_en):
                process.remove(a_word)
            elif (a_word == keyword):
                process.remove(a_word)
        return process # type:list

    def frequency_word(self, text_list):
        # use collections module for counting words list
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
            # use ast module to change from '['a', 'b', 'c]' >> type:text to ['a', 'b', 'c'] >> type:list
            list_output.extend(ast.literal_eval(a_list))
        return self.frequency_word(list_output)
    
    def search(self, keyword):
        api = self.authentication()
        query = str(keyword).replace('#', '')
        # when search by not to use '#', it will find '#' too
        tweets = tweepy.Cursor(api.search, 
                                q=query+'-filter:retweets', # use filter from tweepy
                                count=100, 
                                result_type='recent', 
                                tweet_mode='extended').items()
        df = pandas.DataFrame(columns=['Date', 'Text', 'Hashtag'])
        for tweet in tweets:
            date = tweet.created_at # date when twitter user tweet
            try:
                text = tweet.retweeted_status.full_text
            except:
                text = tweet.full_text

            if langdetect.detect(text) == 'th' or langdetect.detect(text) == 'en':
                find_hashtags = self.check_hashtags(text)
                text_intercept = self.text_intercept(text)
                text_tokenize = self.nlp(text_intercept, query)
                data_row = pandas.Series([date.date(), text_tokenize, find_hashtags], index=df.columns)
                df = df.append(data_row, ignore_index=True) # save database
            
            count_row = len(df.index)
            if count_row == 100:
                # get only 100 tweets
                break
        df.to_csv(r'D:\vs code\soft_dev_2\twitter\data\{}.csv'.format(keyword.replace('#', '')), index=False)

    def frequency_analysis(self, keyword):
        # 2 modes
        # # 1. user search by '#' keyword
        # # 2. user search by 'word'
        search_file = keyword.replace('#', '')
        file_name = "{}.csv".format(search_file)
        db = os.listdir('data')
        if '#' in keyword and file_name in db:
            df = pandas.read_csv(r'D:\vs code\soft_dev_2\twitter\data\{}.csv'.format(search_file))
            counter = self.extend_items(df['Hashtag'])
            return counter
        elif '#' not in keyword and file_name in db:
            df = pandas.read_csv(r'D:\vs code\soft_dev_2\twitter\data\{}.csv'.format(search_file))
            counter = self.extend_items(df['Text'])
            return counter
        elif file_name not in db:
            self.search(keyword)
            return self.frequency_analysis(keyword)

    def trend_tags(self, number):
        api = self.authentication()
        WOEID = 23424960 # Where On Earth ID
        trends = api.trends_place(id=WOEID) # json format
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
