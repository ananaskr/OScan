
import asyncio
import aiohttp

from pybloom_live.pybloom import BloomFilter, ScalableBloomFilter, make_hashfuncs

from library.URLExtract import urlextract

max_threads = 5
# This class provide method to crawl th whole site.
class Spider(object):

	def __init__(self,target):
		self.target = target
		self.timeout = 20
		self.max_threads = max_threads
		self.uris = []
		self.bf = self.bloomf()
		self.queue = asyncio.Queue()

	def bloomf(self):
		bFilter = BloomFilter(capacity=1000, error_rate=0.001)
		return bFilter

	def dedup(self,uri):
		return self.bf.add(uri)


	async def httpsend(self,url):
		async with aiohttp.ClientSession() as session:
			async with session.get(url, self.timeout) as response:
				assert response.status == 200
				html = await response.read()
				return html

	def add_url(self,content):
		uris = urlextract(self.target, content)
		for _ in uris:
			if not self.bf.add(_):
				self.uris.append(_)
				self.queue.put_nowait(_)


	async def loop_crawl(self):
		while True:
			item = await self.queue.get()
			rescontent = self.httpsend(item)
			asyncio.ensure_future(self.add_url(rescontent))


	def eventloop(self):
		loop = asyncio.get_event_loop()
		loop.run_until_complete(self.loop_crawl())
		loop.close() 

	async def loop_crawl(self):
		while True:
			item = await self.queue.get()
			rescontent = self.httpsend(item)
			asyncio.ensure_future(self.add_url(rescontent))


def spider(target):
	s = Spider(target)
	if not s.bf.add(s.target):
		s.queue.put_nowait(s.target)
	s.eventloop()
	

