#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 Gabriel Fornaeus <gf@hax0r.se>
#
# Distributed under terms of the GPLv3 license.

"""
SLIDe animatoR is a small utility program that makes images from json-input
"""

import json
import yaml
import sys
import os



def getInfo(infoFile):
	"""
	Read the information from a json-encoded file and output it
	Keyword arguments:
	infoFile -- the file with the json-data
	"""

	jsonData= open(infoFile).read()
	data = json.loads(jsonData)
	return data

def shellEscape(s):
	return s.replace("(","\\(").replace(")","\\)").replace(" ","\\ ")

def readConfig():
	with open(r'slidr.yml') as file:
			configuration = yaml.load(file, Loader=yaml.FullLoader)
	return configuration

def writeToImage(inputFile,data):
	"""
	Create a videofile with next, previous and beamerinfo from json data
	Keyword arguments:
	inputFile -- The file to use as the base slide
	data -- json containing all the information
	"""

	"""
		This is the order of the fields in database
		"fields": [
			"id",
			"contributer",
			"entry_name",
			"beamer_info",
			"filename",
			"competition_id"
		]
	"""
	
	config = readConfig()
	print(config['entrySize'])
	for index, contribution in enumerate(data):
		# This is because the first entry will not have a previous entry
		if index != 0:
			previousContribution = "Previous Entry:" + data[index - 1]['group'] + " - " + data[index - 1]['name']
		else:
			previousContribution = " "
		contribDict = {
				'filename' : contribution['filename'].replace("zip","png"),
				'inputFile' : inputFile,
				'contribFilename': contribution['filename'],
				'id' : contribution['id'],
				'entryName' : contribution['name'],
				'group' : contribution['group'],
				'beamerInfo' : contribution['info'].replace("%", "\%"),
				'previousContribution': previousContribution,
				'inputFile' : inputFile,
				'index' : str(index),
				'entrySettings' : '-annotate %s -pointsize %s' % (config['entrySize'], config['entryPos']),
				'groupSettings' : '-annotate %s -pointsize %s' % (config['groupSize'], config['groupPos']),
				'beamerSettings' : '-annotate %s -pointsize %s' % (config['beamerSize'], config['beamerPos']),
				'previousSettings' : '-annotate %s -pointsize %s' % (config['previousSize'], config['previousPos'])
				}
		#imagemagickcommand="convert input.png -gravity North -pointsize 30 -fill white -annotate +1050+1040 '{entryName}' -annotate +36+1020 '{beamerInfo}' -annotate +26+100 '{previousContribution}' {filename}".format(**contribDict)
		imagemagickcommand="convert {inputFile} -fill white {entrySettings} '{entryName}' {groupSettings} 'by {group}' {beamerSettings} '{beamerInfo}' {previousContribution} '{previousContribution}' {index}-slide-{filename}".format(**contribDict)
		# Makes overlay
		print(imagemagickcommand)

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print("Usage: <json-file>")
		sys.exit(1)
	writeToImage(sys.argv[1],getInfo(sys.argv[2]))
