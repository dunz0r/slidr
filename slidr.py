#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 Gabriel Fornaeus <gf@hax0r.se>
#
# Distributed under terms of the GPLv3 license.

"""
SLIDe ANimator is a small utility program that puts text on videofiles
"""

import json
import sys
import os

# Databas-kommando?
def getInfo(infoFile):
    jsonData= open(infoFile).read()
    data = json.loads(jsonData)
    return data

"""
    "fields": [
        "contribution_id",
        "contributer",
        "entry_name",
        "beamer_info",
        "filename",
        "competition_id"
    ]
"""
def writeToVideo(inputFile,data):
    """
    create a videofile with next, previous and beamerinfo from json data
    Keyword arguments:
    inputFile -- The file to use as the base
    data -- json containing all the information
    """

    fontFile = "./arial.ttf"
    entrySettings = "drawtext=fontsize=30:fontcolor=0xFFFFFFFF:shadowcolor=0x000000EE:shadowx=2:shadowy=2:fontfile='%s':x=36:y=995:text=" % (fontFile)
    beamerSettings = "drawtext=fontsize=30:fontcolor=0xFFFFFFFF:shadowcolor=0x000000EE:shadowx=2:shadowy=2:fontfile='%s':x=1337:y=143:text=" % (fontFile)
    previousSettings = "drawtext=fontsize=30:fontcolor=0xFFFFFFFF:shadowcolor=0x000000EE:shadowx=2:shadowy=2:fontfile='%s':x=1337:y=70:text=" % (fontFile)
    encodingSettings = "-c:v libx264 -preset ultrafast -qp 0 -c:a copy "

    for index, contribution in enumerate(data['data']):
        previousContribution = data['data'][index - 1][1] + " - " + data['data'][index - 1][2]
        contributionId =  contribution[0]
        contributer = contribution[1]
        entryName = contributer + " - " + contribution[2]
        beamerInfo = contribution[3]
        filename = os.path.splitext(contribution[4])[0] + "-slide.mkv"
        contribDict = {
                'filename' : filename,
                'inputFile' : inputFile,
                'id' : contributionId, 
                'contributer' : contributer, 
                'entryName' : entryName, 
                'beamerInfo' : beamerInfo,
                'beamerSettings': beamerSettings,
                'entryName' : entryName,
                'entrySettings': entrySettings,
                'previousSettings': previousSettings,
                'previousContribution': previousContribution,
                'encodingSettings': encodingSettings
                }

        ffmpegcommand = "ffmpeg -threads 8 -i {inputFile} -vf \"[in]{entrySettings}{entryName}, {beamerSettings}{beamerInfo}, {previousSettings}{previousContribution}\" {encodingSettings} {filename}".format(**contribDict)
        print(ffmpegcommand)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: <input videfile> <json-file>")
        sys.exit(1)
    writeToVideo(sys.argv[1],getInfo(sys.argv[2]))
