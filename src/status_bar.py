""" status_bar.py
	
	Author         : James Mnatzaganian
	Contact        : http://techtorials.me
	Date Created   : 09/27/14
	
	Modified By    : James Mnatzaganian
	Last Modified  : 09/27/14
	
	Description    : Makes a nice little status bar
	Usage          : See "run_example()"
	Python Version : 2.7.8
	
	Version        : 1.0
	
	License        : MIT License http://opensource.org/licenses/mit-license.php
	
	The MIT License (MIT)
	
	Copyright (c) 2014 James Mnatzaganian
	
	Permission is hereby granted, free of charge, to any person obtaining a
	copy of this software and associated documentation files (the "Software"),
	to deal in the Software without restriction, including without limitation
	the rights to use, copy, modify, merge, publish, distribute, sublicense,
	and/or sell	copies of the Software, and to permit persons to whom the
	Software is	furnished to do so, subject to the following conditions:
	
	The above copyright notice and this permission notice shall be included in
	all copies or substantial portions of the Software.
	
	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
	IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
	FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
	AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
	LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
	FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
	DEALINGS IN THE SOFTWARE.
"""

# Native imports
import sys

class status_bar():
	""" status_bar

		Description: Creates a fancy status bar
	"""
	
	class _StatusBarLengthTooSmallError(Exception):
		""" _StatusBarLengthTooSmallError

			Description: Exception that is raised if the bar length drops
			below a length of one.
		"""
		
		def __init__(self):
			""" __init__
			
				Description: Initalizes the class			
			"""
			
			print '' # Finishes up the status bar
			self.value = '\n\tThe bar length became too small to represent.' \
				'\n\tThis occurs when the percent complete reaches a very ' \
				'larger number.\n\tMax sure that your total_length value is ' \
				'accurate.'
		
		def __str__(self):
			""" __str__
			
				Description: Returns the string explaining this error
			"""
			
			return self.value
		
	def __init__(self, total_length, bar_length=72, max_bar_length=72,
		min_bar_length=1, style=('[','=',']')):
		""" __init__
		
			Description: Initializes the class
			
			Inputs:
				1) total          : Max value to work with

				2) bar_length     : How many characters the bar should be on
				   the screen
				3) max_bar_length : The maximum length of the bar. Set to be
				   79 (screen width - compatible with Windows, *NIX can use 80)
				   - 7 (2 closing braces + 1 space + 3 digits + 1 percent
				   sign). Max sure the max_bar_length is always 7 less than the
				   total window size.
				4) style          : The status bar style format to use. Needs
				   to be a tuple of three elements: start of bar, bar progress
				   notation, and end of bar.
		"""
		
		# Initializations
		self.total_length   = total_length
		self.bar_length     = bar_length
		self.max_bar_length = max_bar_length
		self.min_bar_length = min_bar_length
		self.style          = style
		self.position       = 0
		self.percent_length = 3
		
		# Ensure that the minimum bar length isn't too small
		if self.min_bar_length < 0:
			self.min_bar_length = 1
		
		# Ensure that everything can fit in a normal window
		if self.bar_length > self.max_bar_length:
			self.bar_length = max_bar_length
		
		# Ensure that the bar_length isn't too small
		if self.bar_length < self.min_bar_length:
			self.bar_length = self.min_bar_length
		
		# Ensure that the provided style is valid
		if (len(style) != 3) or (sum([len(x) for x in style]) != 3):
			self.style = ('[','=',']')
		
	def increment(self, step_size=1):
		""" increment
		
			Description: Increments the bars position by the specified amount
			
			Inputs:
				1) step_size: The number to increment the bar's position by
		"""
		
		# Update position
		self.position += step_size
		
		# Calculate the progress
		progress         = self.position / float(self.total_length)
		percent_progress = int(progress * 100)
		percent_length   = len(str(percent_progress))
		
		# Calculate the current bar length, limiting it to the max size
		current_bar_length = min(int(progress * self.bar_length),
			self.bar_length)
		
		# Shrink bar to account for overflow scenarios
		if (current_bar_length == self.bar_length) and \
			(percent_length > self.percent_length):
			
			# If the bar length has room to grow, give it to it
			if (self.bar_length + percent_length - 3) < self.max_bar_length:
				self.bar_length     += 1
				current_bar_length  = self.bar_length
				self.percent_length = percent_length
			else:			
				self.bar_length     -= (percent_length - self.percent_length)
				current_bar_length  = self.bar_length
				self.percent_length = percent_length
				
				# Check for bar being too small
				if self.bar_length < self.min_bar_length:
					raise self._StatusBarLengthTooSmallError()
		
		# Update the status bar
		bars       = self.style[1] * current_bar_length
		bar_spaces = ' ' * (self.bar_length - current_bar_length)
		sys.stdout.write('\r{0}{1}{2}{3} {4}%'.format(self.style[0], bars,
			bar_spaces, self.style[2], percent_progress))
		sys.stdout.flush()
	
	def finish(self):
		""" finish
		
			Description: Ends the status bar, resetting the terminal to normal
			usage.
		"""
		
		print ''

def run_example():
	""" run_example
	
		Description: Example of various usage cases for this status bar
	"""
	
	# Native imports
	import time
	
	# Initializations
	total_length = 100                      # Total number of steps
	sb           = status_bar(total_length) # Create the class instance
	
	print '\nThis example shows how the status bar will work under regular ' \
		'conditions'
	
	# Increment the status bar by 1 for every item
	for i in xrange(total_length):
		time.sleep(0.05)
		sb.increment()
	
	# Disable the status bar
	sb.finish()
	
	print '\nThis example shows how the status bar handles overflow ' \
		'(completeness > 100%)'
	
	# Create the class instance
	sb = status_bar(total_length, bar_length=70)
	
	# Increment the status bar by 100 for every item
	for i in xrange(total_length):
		time.sleep(0.05)
		sb.increment(100)
	
	# Disable the status bar
	sb.finish()
	
	print '\nThis example shows what happens if the status bar gets to be ' \
		'small'
	
	# Create the class instance
	sb = status_bar(total_length, bar_length=3)
	
	# Increment the status bar
	for i in xrange(total_length):
		time.sleep(0.05)
		sb.increment(100*i)
	
	# Disable the status bar
	sb.finish()
	
	print "\nThis example shows what happens if the status bar can't grow " \
		"anymore."
	
	# Create the class instance
	sb = status_bar(total_length, bar_length=3, max_bar_length=5,
		min_bar_length=2)
	
	# Increment the status bar to cause fatal termination
	try:
		for i in xrange(total_length):
			time.sleep(0.05)
			sb.increment(500*i)
	except sb._StatusBarLengthTooSmallError, e:
		print 'StatusBarLengthTooSmallError Exception Caught', e
	
	print '\nThis example shows how styling the status bar works.' \
		'\nNote that invalid styles will be ignored.'
	
	# Create the class instance
	sb = status_bar(total_length, style=('{','-','}'))
	
	# Increment the status bar
	for i in xrange(total_length):
		time.sleep(0.05)
		sb.increment(i)
	
	# Disable the status bar
	sb.finish()

if __name__ == "__main__":
	run_example()
