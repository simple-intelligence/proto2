class _Getch:
	"""Gets a single character from standard input.

	Does not echo to the screen.

	Source: ("http://code.activestate.com/recipes/"
			 "134892-getch-like-unbuffered-character-reading-from-stdin/")

	Liscense: PSF
	Created by Danny Yoo on Fri, 21 Jun 2002

	"""
	def __init__(self):
		self.impl = _GetchUnix()

	def __call__(self):
		return self.impl()


class _GetchUnix:
	def __init__(self):
		import tty, sys

	def __call__(self):
		import sys, tty, termios
		fd = sys.stdin.fileno()
		old_settings = termios.tcgetattr(fd)
		try:
			tty.setraw(sys.stdin.fileno())
			ch = sys.stdin.read(1)
		finally:
			termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
		return ch
