BOT_NAME = "sreality"

SPIDER_MODULES = ["sreality.spiders"]
NEWSPIDER_MODULE = "sreality.spiders"

ITEM_PIPELINES = {
    "sreality.pipelines.SrealityPipeline": 300,
}

LOG_LEVEL = "WARNING"
ROBOTSTXT_OBEY = False



REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
