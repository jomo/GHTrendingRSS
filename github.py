#!/usr/bin/python

import urllib2
import re
import HTMLParser
import storecache
import memorycache
import logging
from bs4 import BeautifulSoup


languages = {"debug_language_id": {"name": "Debug language name", "id": "debug_language_id"}}
timespans = {"daily": {"id": "daily", "name": "Daily", "priority": 0}, "weekly": {"id": "weekly", "name": "Weekly", "priority": 1}, "monthly": {"id": "monthly", "name": "Monthly", "priority": 2}}


def get_content(bsobject):
	if bsobject and bsobject.string:
		return bsobject.string.strip()
	else:
		return ""

titleExtractor = re.compile('<span class="prefix">.*</span>\s*<span class="slash">/</span>\s*(.*?)\s*</a>')
def get_title(bsobject):
	result = titleExtractor.findall(str(bsobject))
	if len(result) > 0:
		return result[0].strip()
	else:
		return None

def get_projects(languageId, timespanId):
	logging.info("Updating projects for language %s, timespan %s" % (languageId, timespanId))
	url = "https://github.com/trending?l=%s&since=%s" % (languageId, timespanId)
	webpage = BeautifulSoup(urllib2.urlopen(url).read().decode('utf-8'))
	projects_raw = webpage.find_all(class_="repo-list-item")
	projects = [{
		"url": "https://github.com" + project_raw.find(class_="repo-list-name").find('a')["href"], 
		"name": get_title(project_raw.find(class_="repo-list-name")),
		"description": get_content(project_raw.find(class_="repo-list-description"))
		} for project_raw in projects_raw]
	return projects


def get_languages():
	logging.info("Updating languages...")
	url = "https://github.com/trending"
	webpage = urllib2.urlopen(url).read()
	new_languages_raw = re.findall('<a href="https://github.com/trending\?l=(.*?)" class="select-menu-item-text js-select-button-text js-navigation-open">(.*?)</a>', webpage)

	new_languages = {"": {"name": "All", "id": ""}}
	for new_language_raw in new_languages_raw:
		new_languages[new_language_raw[0]] = {"id": new_language_raw[0], "name": new_language_raw[1]}
	
	return new_languages


# Languages caching logic should be somewhere else... But where?
LANGUAGES_CACHE_TIME = 86400
def languages_cached_getter(cache, language_getter):
	def get_languages_cached():
		result = cache.get("languages")
		if result:
			return result
		result = language_getter()
		cache.set("languages", result, LANGUAGES_CACHE_TIME)
		return result
	return get_languages_cached

languages = languages_cached_getter(memorycache.MemoryCache(), languages_cached_getter(storecache.StoreCache(), get_languages)) () # ... Sorry
