import scrapy
import json
import re
import psycopg2
import time
class FlatsSpider(scrapy.Spider):
    name = "flats"
    
    current_page = 1
    scraped_items = 0
    max_items_to_scrape = 500
    start_urls = ["https://www.sreality.cz/en/search/for-sale/apartments"]
    conn = None
    
    def __init__(self):
        retries = 10
        for i in range(retries):
            try:
                self.conn = psycopg2.connect(
                    dbname="sreality",
                    user="postgres",
                    password="postgres",
                    host="db",
                    port="5432"
                )
                
                self.cursor = self.conn.cursor()
            except Exception as e:
                pass
            if self.conn:
                break
            else:
                time.sleep(5)
    
    def parse(self, response):
        for page in range(self.max_items_to_scrape//60 + 1):
            url = f"https://www.sreality.cz/api/en/v2/estates?category_main_cb=1&category_type_cb=1&page={page}&per_page=60&tms=1690911976383"
            headers = {
            "Accept": "application/json",
            "Accept-Encoding":"gzip, deflate, br",
            "Accept-Language":"sl-SI,sl;q=0.9,en-GB;q=0.8,en;q=0.7",
            "Referer":"https://www.sreality.cz/en/search/for-sale/apartments",
            "Sec-Fetch-Mode":"cors",
            "Sec-Fetch-Site":"same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
            }
            request = scrapy.Request(url, headers=headers, callback=self.parse_api)
            yield request
        
        
    def parse_api(self, response):
        data = json.loads(response.body)['_embedded']['estates']

        for item in data:
            
            title = item['name']
            img_url = item['_links']['images'][0]['href']
            item_data = {
                "title": re.sub(r'[^\x00-\x7F]', '', title),
                "img_url": img_url
            }
            sql = "INSERT INTO flats (title, img_url) VALUES (%s, %s)"
            data = (item_data["title"], item_data["img_url"])
            self.cursor.execute(sql, data)
            self.conn.commit()
            self.scraped_items += 1
            if self.scraped_items >= self.max_items_to_scrape:
                break
        self.current_page += 1
        
        if self.scraped_items < self.max_items_to_scrape:
            yield scrapy.Request(response.url, callback=self.parse)