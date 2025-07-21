import scrapy
from Final.items import *
from bs4 import BeautifulSoup  # 导入bs4


class CBDSpider(scrapy.Spider):
    name = "cbd"
    city = ''
    # start_urls = [
    #     'https://bj.lianjia.com/ershoufang/',  # 替换为你的目标网址
    # ]
    allowed_domains = ['lianjia.com']
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'ITEM_PIPELINES': {
            'Final.pipelines.CBDPipeline': 300,
        }
    }

    def __init__(self, city):
        super().__init__()
        self.city = city

    def start_requests(self):
        # def start_requests(self):
        url = f'https://{self.city}.lianjia.com/ershoufang/'
        yield scrapy.Request(url=url, callback=self.parse_region)

    def parse_region(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        # 用CSS选择器定位所有区域按钮
        region_links = soup.select('div[data-role="ershoufang"] div a[href]')
        for a in region_links:
            region_url = response.urljoin(a['href'])
            # 不会多拼
            # response.urljoin(a['href']) 会自动处理路径拼接
            # 无论当前页面的 URL 是否以 /ershoufang/ 结尾
            # urljoin 都会用 a['href'] 替换掉原有路径的后半部分，生成正确的绝对地址。
            region_name = a.get_text(strip=True)
            yield scrapy.Request(url=region_url, callback=self.parse_station, meta={'region': region_name})

    def parse_station(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        # 精确定位到目标div
        target_div = soup.select_one('div.position dl:nth-of-type(2) dd > div:nth-of-type(1) > div:nth-of-type(2)')
        if target_div:
            station_links = target_div.find_all('a', href=True)
            for a in station_links:
                station_url = response.urljoin(a['href'])
                station_name = a.get_text(strip=True)

                # items
                item = CBDItem()
                item['city'] = self.city
                item['region'] = response.meta.get('region')
                item['name'] = station_name
                item['url'] = station_url
                # 发起请求，回调你后续处理的函数（如parse_detail）
                yield scrapy.Request(url=station_url, callback=self.parse_final, meta={
                    'region': response.meta.get('region'),
                    'station': station_name
                })

    def parse_final(self, response, item):
        soup = BeautifulSoup(response.text, 'html.parser')
        # 获取房源数量
        count_tag = soup.select_one('#content > div:nth-of-type(1) > div:nth-of-type(2) > h2 > span')
        item['total'] = count_tag.get_text(strip=True) if count_tag else '0'
        # 获取页码
        page_tag = soup.select_one('#content > div:nth-of-type(1) > div:nth-of-type(7) > div:nth-of-type(2) > div > a:nth-of-type(4)')
        item['page'] = page_tag.get_text(strip=True) if page_tag else '1'

        yield item


    def parse(self, response):
        # 入口回调，调用你的区域解析
        yield from self.parse_region(response)