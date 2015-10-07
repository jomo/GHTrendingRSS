#!/usr/bin/python
import github
import rss

RSS_CACHE_TIME = 1800

class RSSProducer:
	def get_rss(self, languageId, timespanId):
		rss_feed = rss.get_rss(github.languages[languageId], github.timespans[timespanId], github.get_projects(languageId, timespanId))
	
		return rss_feed

class RSSCachedProducer:
	def __init__(self, rssproducer, cache):
		self.cache = cache
		self.rssproducer = rssproducer

	def get_rss(self, languageId, timespanId):
		key = "%s|%s" % (languageId, timespanId)
		rss_feed = self.cache.get(key)

		if not rss_feed:
			rss_feed = self.rssproducer.get_rss(languageId, timespanId)
			self.cache.set(key, rss_feed, RSS_CACHE_TIME)

		return rss_feed
