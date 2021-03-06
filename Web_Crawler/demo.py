import newspaper, pandas, pythainlp, spacy, threading, requests, bs4
from Twidty_backend import Twidty 

class NewsCrawler():

	def __init__(self):
		self.list_news_links = [	'https://www.thairath.co.th',  
									'https://www.dailynews.co.th', 
									'https://www.bangkokbiznews.com',  
									'https://www.komchadluek.net', 
									'https://www.matichon.co.th', 
									'https://mgronline.com', 
									'https://www.thansettakij.com', 
									'https://www.bangkokpost.com'		]

	def get_headlines(self, url):
		news = newspaper.Article(url)
		news.download()
		news.parse()
		headline = news.title
		return headline

	def save_data(self, url):
		df_text = pandas.DataFrame(columns=['Date', 'Text', 'Tokenize'])

		web_source = requests.get(url)
		soup = bs4.BeautifulSoup(web_source.text, 'html.parser')
		news_links = soup.find_all('a', href=True)

		for link in news_links:
			# print(link.getText())
			if url not in link['href']:
				new_url = url + link['href']
			else:
				new_url = link['href']
			try:
				news_data = self.get_headlines(new_url)
			except:
				continue
			if news_data in '\n\t' or news_data == '':
				continue
			print(news_data)

list_news_links = [	'https://www.thairath.co.th',  
					'https://www.dailynews.co.th', 
					'https://www.bangkokbiznews.com',  
					'https://www.komchadluek.net', 
					'https://www.matichon.co.th', 
					'https://mgronline.com', 
					'https://www.thansettakij.com', 
					'https://www.bangkokpost.com'		]
news_crawler = NewsCrawler()
news_crawler.save_data(list_news_links[5])
