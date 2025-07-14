import scrapy
from first_scrapy.items import NewHouseData

class NewHouseSpider(scrapy.Spider):
    name = "new_house"
    allowed_domains = ["sz.fang.lianjia.com"]
    # 修改起始页数范围为3到10
    start_urls = [
        f"https://sz.fang.lianjia.com/loupan/pg{i}/" for i in range(1, 4)
    ]

    def parse(self, response):
        for house in response.css('ul.resblock-list-wrapper li'):
            detail_url = house.css('div.resblock-name h2 a::attr(href)').get()
            area = house.css('div.resblock-area span::text').get()
            # 提取地理位置
            location = '/'.join(house.css('div.resblock-location span::text, div.resblock-location a::text').getall())
            if detail_url:
                detail_url = response.urljoin(detail_url)
                yield scrapy.Request(
                    detail_url,
                    callback=self.parse_detail,
                    meta={'area': area, 'position': location}
                )

    def parse_detail(self, response):
        item = NewHouseData()
        item['building_name'] = response.css('div.mod-wrap.mod-resblock-name-bar.clearfix h1::text').get()
        item['type'] = response.css('span.tag-item.house-type-tag::text').get()
        # 从meta获取地理位置
        item['position'] = response.meta.get('position')
        item['house_type'] = '/'.join(response.css('span.house-type-item::text').getall())
        item['area'] = response.meta.get('area')
        item['sigle_price'] = response.css('div.price > span:nth-child(3)::text').get()
        item['total_price'] = response.css('div.price > span:nth-child(5)::text').get()
        yield item