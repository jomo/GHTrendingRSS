#!/usr/bin/python

from google.appengine.api import memcache

class MemoryCache:
	def get(self, key):
		return memcache.get(key)
	def set(self, key, value, expiration):
		memcache.set(key, value, expiration)

