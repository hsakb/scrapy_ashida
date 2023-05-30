import scrapy


class AshidaInfoBlogSpider(scrapy.Spider):
    name = 'ashida-info-blog'
    allowed_domains = ['www.ashida.info']
    start_urls = ['http://www.ashida.info/blog']

    def parse(self, response):
        # 月別のlinks
        res = self.preprocessing(response)
        for r1 in res:
            yield scrapy.Request(r1, callback=self.parse_data)

    def parse_data(self, response):
        r2 = response.css('div.content').css('a::attr("href")').getall()
        for r3 in r2:
            if r3 == "http://www.ashida.info/blog/" or r3 == "#":
                pass
            else:
                yield scrapy.Request(r3, callback=self.parse_data2)

    def parse_data2(self, response):
        content = response.css('div.content')
        title = content.css('h3::text').get()
        p_list = content.css('p::text').getall()
        joined_p = ''.join(p_list)
        yield {
            'title' : title,
            'content': joined_p,
        }


    def preprocessing(self, response):
        # 月別のlinks
        res = response.css('ul')[3].css('li>a::attr("href")').getall()
        return res 

