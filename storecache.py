#!/usr/bin/python
import datetime
import json
from google.appengine.ext import db

class StoreCache(db.Model):
	value = db.TextProperty()
	expiration = db.DateTimeProperty()

	@classmethod
	def get(self, key):
		result = self.get_by_key_name(key)
		if result:
			if datetime.datetime.now() > result.expiration:
				result.delete()
				return None
			return json.loads(result.value)
		else:
			return None

	@classmethod
	def set(self, key, value, expiration):
		date_expiration = datetime.datetime.utcnow() + datetime.timedelta(seconds=expiration)
		entity = self(key_name=key, value=json.dumps(value), expiration = date_expiration)
		entity.put()
