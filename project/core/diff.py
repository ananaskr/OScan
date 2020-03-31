import re
from difflib import SequenceMatcher

DYNAMICITY_BOUNDARY_LENGTH = 10


def checkDynamicContent(firstPage,secondPage):
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
							prefix = trimAlphaNum(prefix)
						if infix[-1].isalnum():
							suffix = trimAlphaNum(suffix)
						break

			dynamicMarkings.append((prefix if prefix else None, suffix if suffix else None))

	return dynamicMarkings

def removeDynamicContent(page,dynamicMarkings):
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

def trimAlphaNum(value):

    while value and value[-1].isalnum():
        value = value[:-1]

    while value and value[0].isalnum():
        value = value[1:]

    return value

def diff_status_code(res1,res2):
	return not (res1.status_code == res2.status_code)

def diff_headers(res1,res2,res3):
	remove_key = []
	for key,value in res1.headers.items():
		if res1.headers[key] != res2.headers[key]:
				remove_key.append(key)

	res3.header = res3.headers
	for key,value in list(res3.headers.items()):
		if key in remove_key:
			res3.header.pop(key)

	if len(res1.headers.items() | res3.headers.items()) != len(res1.headers.items()):
		return True

	return False

def diff_text(res1,res2,res3):

	ratio_t = SequenceMatcher(0,res1.text,res2.text).ratio()
	ratio_f = SequenceMatcher(0,res1.text,res3.text).ratio()

	if ratio_f <= 0.5:
		return True
	
	if ratio_t != 1.0:
		dymarks = checkDynamicContent(res1.text,res2.text)
		page_1 = removeDynamicContent(res1.text,dymarks)
		page_2 = removeDynamicContent(res3.text,dymarks)

		if SequenceMatcher(0,page_1,page_2).ratio() < 0.85:
			return True

	return False




