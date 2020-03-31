class logger(object):
	def __init__(self):
		self.G = '\033[92m'
		self.Y = '\033[93m'
		self.B = '\033[94m'
		self.R = '\033[91m'
		self.W = '\033[0m' 


	def banner(self):
		print('''%s			
		   _____
		  / _,_ \\
		 / /   \\ \\   ___    ___    __ _   _____ 
		| |     | | / __   / _ \  / _  | |  _  |
		 \ \___/ /  \__ \ | (_   | (_| | | | | |
		  \_____/   \___/  \___/  \__,_| | | | |
			%s'''%(self.G,self.W))