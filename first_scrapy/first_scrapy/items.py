# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewHouseData(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    building_name = scrapy.Field()
    type = scrapy.Field()
    position = scrapy.Field()
    house_type = scrapy.Field()
    area = scrapy.Field()
    sigle_price = scrapy.Field()
    total_price = scrapy.Field()
    pass

class SecondHouseData(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    district_name = scrapy.Field()
    type = scrapy.Field()
    position = scrapy.Field()
    house_type = scrapy.Field()
    sigle_price = scrapy.Field()
    total_price = scrapy.Field()
    pass