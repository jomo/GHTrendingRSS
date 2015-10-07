#!/usr/bin/python

import webapp2
from google.appengine.ext.webapp.util import run_wsgi_app
import os
import jinja2
import github
import githubrss
import memorycache
import storecache

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)), extensions=['jinja2.ext.autoescape'])
rssproducer = githubrss.RSSCachedProducer(githubrss.RSSCachedProducer(githubrss.RSSProducer(), storecache.StoreCache()), memorycache.MemoryCache())


class RSS(webapp2.RequestHandler):
	def get(self):
		languageId = self.request.get("language")
		timespanId = self.request.get("timespan")

		if not (languageId != None and timespanId and (languageId in github.languages) and (timespanId in github.timespans)):
			self.error(404)
			return

		self.response.headers['Content-Type'] = 'application/rss+xml'
		self.response.out.write(rssproducer.get_rss(languageId, timespanId))

class HomePage(webapp2.RequestHandler):
	def get(self):
		values = {"languages": sorted(github.languages.values(), key=lambda l: l["id"]), "timespans": sorted(github.timespans.values(), key=lambda t: t["priority"])}
		self.response.write(JINJA_ENVIRONMENT.get_template('index.html').render(values))

app = webapp2.WSGIApplication([('/', HomePage), ('/rss', RSS)], debug=True)

