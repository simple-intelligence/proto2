import os
import sys


def main ():
	server = video_server ()
	server.daemon = True
	server.run ()

if __name__=="__main__":
	main ()
