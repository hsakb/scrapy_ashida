import scrapy


class Ashimai01Spider(scrapy.Spider):
    name = 'ashimai01'
    allowed_domains = ['www.ashida.info']
    start_urls = ['http://www.ashida.info/ronbun/ashimai01.htm']

    def parse(self, response):
        sets = self.extract_sets(response)
        for set in sets:
            a_tag = set.xpath('.//a/text()').get()  # aタグのテキストを抽出するXPath
            p_tags = set.xpath('.//p/text()').getall()  # 複数のpタグのテキストを抽出するXPath

            yield {
                'a_tag': a_tag,
                'p_tags': p_tags
            }

    def extract_sets(self, response):
        response.css('ul')[3].css('li>a::attr("href")').getall()

        sets = []
        a_tags = response.xpath('//a[contains(@class, "mama")]')  # class名が"mama"を含むaタグを抽出するXPath

        for a_tag in a_tags:
            set = {'a_tag': a_tag.xpath('.//text()').get(), 'p_tags': []}
            p_tags = []

            next_elements = a_tag.xpath('./following-sibling::*')

            for next_element in next_elements:
                if next_element.tag == 'a':
                    break
                elif next_element.tag == 'p':
                    p_text = next_element.xpath('.//text()').get()
                    if p_text:
                        p_tags.append(p_text)

            set['p_tags'] = p_tags
            sets.append(set)

        return sets
