import re
from difflib import SequenceMatcher

DYNAMICITY_BOUNDARY_LENGTH = 10
Threshold = 0.85

# When judging whether the responses of two different requests are equal, it compares three parts: status_code, 
# headers and body content. 
class DiffResponse(object):

	def __init__(self,resp1,resp2,resp3):
		self.resp1 = resp1
		self.resp2 = resp2
		self.resp3 = resp3

	# Compare with status_code
	def diff_status_code(self):
		return not self.resp1.status_code == self.resp3.status_code

	# Compare with headers
	def diff_headers(self):
		remove_key = []
		for key,value in self.resp1.headers.items():
			if self.resp1.headers[key] != self.resp2.headers[key]:
					remove_key.append(key)

		headers = self.resp3.headers
		self.resp1.headers.pop('date')
		self.resp3.headers.pop('date')
		
		for key,value in list(self.resp3.headers.items()):
			if key in remove_key:
				headers.pop(key)
				self.resp1.headers.pop(key)
		#print(headers)
		#print(self.resp3.headers)
		if len(self.resp1.headers.items() | headers.items()) != len(self.resp1.headers.items()):
			return True
		for key,value in self.resp1.headers.items():
			if self.resp1.headers[key] != headers[key]:
				return True
		return False

	# Compare with response content.
	# @thanks to sqlmap page ratio, ratio [0~1]. The higher ratio means more false negative, the lower ratio 
	# means more false positive. 
	def diff_text(self):
		# Calculate the for pair separately
		# ratio_t means comparation of same requests. ratio_f means comparation of different requests.
		ratio_t = SequenceMatcher(0,self.resp1.text,self.resp2.text).ratio()
		ratio_f = SequenceMatcher(0,self.resp1.text,self.resp3.text).ratio()

		if ratio_f <= 0.5:
			return True
		
		# If response body contains dynamic content such as datetime, remove it and determine it.
		if ratio_t != 1.0:
			dymarks = self.checkDynamicContent(self.resp1.text,self.resp2.text)
			page_1 = self.removeDynamicContent(self.resp1.text,dymarks)
			page_2 = self.removeDynamicContent(self.resp3.text,dymarks)
			ratio_f = SequenceMatcher(0,page_1,page_2).ratio()

		if ratio_f < Threshold :
			return True
		
		return False

	# Remove the dynamic content from page content.
	def removeDynamicContent(self,page,dynamicMarkings):
		if page:
			for item in dynamicMarkings:
				prefix, suffix = item

				if prefix is None and suffix is None:
					continue
				elif prefix is None:
					page = re.sub(r"(?s)^.+%s" % re.escape(suffix), suffix.replace('\\', r'\\'), page)
				elif suffix is None:
					page = re.sub(r"(?s)%s.+$" % re.escape(prefix), prefix.replace('\\', r'\\'), page)
				else:
					page = re.sub(r"(?s)%s.+%s" % (re.escape(prefix), re.escape(suffix)), "%s%s" % (prefix.replace('\\', r'\\'), suffix.replace('\\', r'\\')), page)

		return page

	# Find the dynamic content from pages.
	def checkDynamicContent(self,firstPage,secondPage):
		dynamicMarkings = []
		blocks = list(SequenceMatcher(None,firstPage,secondPage).get_matching_blocks())

		#Removing too small matching blocks
		for block in blocks[:]:
			(_,_,length) = block

			if length <= 2 * DYNAMICITY_BOUNDARY_LENGTH:
				blocks.remove(block)

		# Making of dynamic markings based on prefix/suffix principal
		if len(blocks) > 0:
			blocks.insert(0,None)
			blocks.append(None)

			for i in range(len(blocks)-1):
				prefix = firstPage[blocks[i][0]:blocks[i][0] + blocks[i][2]] if blocks[i] else None
				suffix = firstPage[blocks[i + 1][0]:blocks[i + 1][0] + blocks[i + 1][2]] if blocks[i + 1] else None

				if prefix is None and blocks[i+1][0] == 0:
					continue

				if suffix is None and (blocks[i][0] + blocks[i][2] >= len(firstPage)):
					continue

				if prefix and suffix:
					prefix = prefix[-DYNAMICITY_BOUNDARY_LENGTH:]
					suffix = suffix[:DYNAMICITY_BOUNDARY_LENGTH]

					for _ in (firstPage, secondPage):
						match = re.search(r"(?s)%s(.+)%s" % (re.escape(prefix), re.escape(suffix)), _)
						if match:
							infix = match.group(1)
							if infix[0].isalnum():
								prefix = self.trimAlphaNum(prefix)
							if infix[-1].isalnum():
								suffix = self.trimAlphaNum(suffix)
							break

				dynamicMarkings.append((prefix if prefix else None, suffix if suffix else None))

		return dynamicMarkings

	def trimAlphaNum(self,value):
		while value and value[-1].isalnum():
			value = value[:-1]
		while value and value[0].isalnum():
			value = value[1:]
		return value

# The main function to compare responses of requests.
def diff(firstPage,secondPage,thirdPage):
	#print(firstPage)
	diff = DiffResponse(firstPage,secondPage,thirdPage)
	if diff.diff_status_code():
		return True
	if diff.diff_headers():
		return True
	if diff.diff_text():
		return True

	return False


















