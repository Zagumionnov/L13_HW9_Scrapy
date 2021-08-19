import scrapy


class WorkuaSpider(scrapy.Spider):
    name = 'workua'
    allowed_domains = ['work.ua']
    start_urls = ['https://www.work.ua/resumes-kharkiv/']

    def parse(self, response):

        for item in response.css('div#pjax-resume-list div.card.resume-link'):

            card_uri = item.css('h2 a::attr(href)').get()

            result = {
                'pos': item.css('h2 a::text').get(),
                'name': item.css('div > b::text').get(),
                'old': None
            }

            yield response.follow(card_uri, self.parse_card, meta={
                'result': result
            })

        for page in response.css('ul.pagination li'):

            if page.css('a::text').get() == 'Наступна':
                yield response.follow(
                    page.css('a::attr(href)').get(),
                    self.parse
                )




    def parse_card(self, response):

        header = response.css('div.card > h2::text').get()

        description = ' '.join(response.css('div.card > p::text').getall())
        description = ' '.join(description.split())

        old = response.css('div.card div.row div dl.dl-horizontal dd::text').get()
        old = ' '.join(old.split())

        response.meta['result']['old'] = old
        response.meta['result']['description'] = header + description

        yield response.meta['result']
