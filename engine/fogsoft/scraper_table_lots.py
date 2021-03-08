import asyncio
from playwright.async_api import async_playwright
import re
import scrapy
from .pipelines import MongodbPipeline


def cleaner_text(content=None):
    try:
        clean_dom = re.sub(r'[\n\t\r]', '', content)
        clean_dom = re.sub(r'\s+', ' ', clean_dom)
        return clean_dom
    except Exception as e:
        return content


def start(platform, start_url, slow_mo, limit_page):

    mongo_db = MongodbPipeline(platform)
    mongo_db.open_spider()

    async def parse_table(page, platform):
        page = scrapy.Selector(text=page)
        header_table = page.xpath('//table[@class="gridTable"]//tr[@class="gridHeader"]/td//a/text()').getall()
        for row in page.xpath('//table[@class="gridTable"]//tr[@class="gridRow"]'):
            item = {}
            item.update({
                "platform": platform})
            for i, name in enumerate(header_table):
                cell = cleaner_text(row.xpath(f'.//td[{i + 1}]'))
                href = cell.xpath('./a')
                if href:
                    item[name] = {
                        'url': href.xpath('./@href').get(),
                        'name': cleaner_text(href.xpath('./text()').get())}
                else:
                    item[name] = cleaner_text(cell.xpath('./text()').get())

            mongo_db.process_item(item)


    async def run(page, platform, num_page=1):

        print(f'\r{num_page} из {limit_page}', end="", flush=True)

        if num_page < limit_page:
            content = await page.content()
            await parse_table(content, platform)
            # TODO дописать проверрку last page пока сваливается в ошибку но все собирает норм работает
            if num_page % 10:
                num_page += 1
                await page.click(f"//td[@class='pager']/a[text()='{num_page}']")
                await run(page, platform, num_page)
            else:
                num_page += 1
                await page.click(f"//td[@class='pager']/a[text()='>>']")
                await run(page, platform, num_page)
        else:
            print(' - END')


    async def start_spider(platform, start_url, slow_mo):
        async with async_playwright() as playwright:
            chromium = playwright.chromium
            browser = await chromium.launch(headless=False, slow_mo=slow_mo)
            page = await browser.new_page()
            await page.goto(start_url)
            await run(page, platform)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_spider(platform, start_url, slow_mo))


