import os
import sys


def main ():
	reciever = video_reciever ()
	reciever.daemon = True
	reciever.run ()

if __name__=="__main__":
	main ()
