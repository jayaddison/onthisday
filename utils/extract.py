import sys
import urllib2
import simplejson as json
import logging
import re

from mwlib.parser import Section, Item, Link
from mwlib.uparser import parseString
from mwlib.utils import fetch_url
from mwlib import advtree

logging.basicConfig()

# Check that a date has been specified
if not len(sys.argv) == 2:

	print 'Please provide exactly one argument - the title page of the date to extract events from in wikipedia (e.g. January_1)'
	sys.exit(1)

# Gather content from wikipedia
title = sys.argv[1]
page = urllib2.urlopen('http://en.wikipedia.org/w/index.php?action=raw&title=%s' % title).read().decode('utf-8')
tree = parseString(title, page)

# Add some utility methods to the item
advtree.extendClasses(tree)

# Iterate through the items listed in the wiki page
results = {}
for node in tree.allchildren():

	if isinstance(node, Section) and node.children[0].asText().strip() in (u'Events', u'Births', u'Deaths'):

		section = node.children[0].asText().strip().lower().encode('utf-8')
		if not section == "events":
			continue

		results[section] = []

		for item in [x.children[0] for x in node.children[1].allchildren() if isinstance(x, Item)]:

			# Extract the year and text from the item
			raw = item.getAllDisplayText().strip()
			matches = re.match(u'([^\u2013]*)[\s]*(\u2013|&ndash;)[\s]*(.*)', raw)

			if not matches:
				logging.log(logging.WARN, '%s - Unable to split year and text from string: "%s"' % (title, raw))
				continue

			year = matches.group(1).strip()
			text = matches.group(3).strip()

			result = {
				'year': year,
				'text': text
			}

			results[section].append(result)

print json.dumps(results, separators=(',', ':'), ensure_ascii=False).encode('utf-8')
