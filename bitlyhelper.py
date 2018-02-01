import config
try:
	import urllib2
except ImportError:
	import urllib.request as urllib2
import json

TOKEN = config.bitly_oauth
ROOT_URL = "https://api-ssl.bitly.com"
SHORTEN = "/v3/shorten?access_token={}&longUrl={}"

class BitlyHelper:
	def shorten_url(self, long_url):
		try:
			url = ROOT_URL + SHORTEN.format(TOKEN, long_url)
			response = urllib2.urlopen(url).read()
			jr = json.loads(response.decode("utf-8"))
			return jr['data']['url']
		except Exception as e:
			print(e)