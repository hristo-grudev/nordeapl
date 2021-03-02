import scrapy

from scrapy.loader import ItemLoader
from ..items import NordeaplItem
from itemloaders.processors import TakeFirst


class NordeaplSpider(scrapy.Spider):
	name = 'nordeapl'
	start_urls = ['https://www.nordea.com/en/press-and-news/news-and-press-releases/']

	def parse(self, response):
		post_links = response.xpath('//h3[@class="title grid span-24 "]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//article//text()[normalize-space() and not(ancestor::small)]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//article/small/text()').get().split('|')[0]

		item = ItemLoader(item=NordeaplItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
