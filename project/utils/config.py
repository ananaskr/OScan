import configparser
import sys
import os

config = configparser.ConfigParser()


def get_list(filename,section,name):
	if os.getcwd().split('/')[-1] == 'modules':
		dir_name = '../utils/'
	else:
		dir_name = 'utils/' 

	filename = dir_name+filename
	config.read(filename)
	return config.get(section,name).split(',')




