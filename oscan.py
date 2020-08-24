import sys
import json
import argparse

from core.check import check
from db.logger import logger
from library.ScanTask import scantask

def get_target(path):
	with open(path,'r') as f:
		target = json.loads(f.read())
	return target

def get_arg(args=None):
	parser = argparse.ArgumentParser(description='OScan - OAuth Web Security Detecting Framework')
	parser.add_argument('-r','--request',help='The request of the API, format is a file. At least Specify one.')
	parser.add_argument('-u','--url',help='The Target url to be detected.')

	results = parser.parse_args(args)
	
	target1 = None
	target2 = None
	if results.request:
		files = results.request.split(' ')
		target1 = get_target(files[0])
		if len(files) == 2:
			target2 = get_target(files[1])
	elif results.url:
		target1 = results.url
	else:
		print("At least one argument is needed.\nFor further information check help: python oscan.py --help")
		sys.exit(1)

	return target1,target2


def main():
	target1,target2 = get_arg(sys.argv[1:])
	#print("Starting scanning......................................................")
	task = scantask(target1,target2)
	#print("Complete scanning......................................................")



if __name__ == '__main__':
	scan_logger = logger()
	scan_logger.banner()
	check()
	main()