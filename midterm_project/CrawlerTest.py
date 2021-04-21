from NewsCrawler import NewsCrawler
import unittest, datetime

class CrawlerTest(unittest.TestCase):

	crawler = NewsCrawler()

	def testCheck_dup_text(self):
		test_input = ['หยุดใช้สัตว์ในการทดลอง', 'แบนสินค้าที่ใช้สัตว์', 'หยุดใช้สัตว์ในการทดลอง']
		self.assertListEqual(type(self.crawler.check_dup_text(test_input)), type(list()))

	def testFind_main_headlines(self):
		test_url = "https://tna.mcot.net"
		self.assertEqual(type(self.crawler.find_main_headlines(test_url)), type(dict()))

	def testFind_all_headlines(self):
		test_url = "https://www.settrade.com"
		self.assertEqual(type(self.crawler.find_all_headlines(test_url)), type(list()))

	def testGet_freq_tokenize(self):
		test_input = ["['แบ่งปัน', 'สำหรับ', 'คน', 'สนใจ', 'สินค้า']", "['สำหรับ', 'ไม่ทารุน', 'สัตว์']"]
		self.assertEqual(type(self.crawler.get_freq_tokenize(test_input)), type(dict()))

	def testUpdate_data(self):
		test_url = "https://tna.mcot.net"
		self.assertEqual(self.crawler.update_data(test_url), None)

	def testSearch(self):
		keyword = "โควิด"
		now = datetime.datetime.now()
		step = datetime.timedelta(days=1)
		yesterday = now - step
		self.assertEqual(type(self.crawler.search(keyword, str(yesterday.date()), str(yesterday.date()))), type(dict()))

if __name__ == "__main__":
	unittest.main()
