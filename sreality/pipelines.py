# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
import psycopg2

class SrealityPipeline:
    def open_spider(self, spider):
        self.conn = psycopg2.connect(
            port="5432",
            host="localhost",
            database="sreality",
            user="postgres",
            password="postgres"
        )        
        
        self.cursor = self.conn.cursor()
        
    def close_spider(self, spider):
        self.conn.close()
        self.cursor.close()

        
    def process_item(self, item, spider):
        sql = "INSERT INTO flats (title, img_url) VALUES (%s, %s)"
        data = (item["title"], item["img_url"])
        self.cursor.execute(sql, data)
        self.conn.commit()
        return item