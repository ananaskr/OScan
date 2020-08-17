import configparser
import sys
import os

config = configparser.ConfigParser()


# It provide a convenient way to obtain data from .property
def get_config(filename,section,name):
	if os.getcwd().split('/')[-1] == 'modules':
		dir_name = '../config/'
	else:
		dir_name = 'config/' 

	filename = dir_name+filename
	config.read(filename)
	return config.get(section,name).split(',')

# It provide a convenient way to obtain data from other files, such like .txt
def get_file(filename):
	result = []
	if os.getcwd().split('/')[-1] == 'modules':
		dir_name = '../config/'
	else:
		dir_name = 'config/' 
	filename = dir_name + filename
	with open(filename,'r') as f:
		result.append(f.readline())

	return result





