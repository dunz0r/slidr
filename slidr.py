#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 Gabriel Fornaeus <gf@hax0r.se>
#
# Distributed under terms of the GPLv3 license.

"""
SLIDe animatoR is a small utility program that puts text on videofiles
"""

import json
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

def writeToVideo(inputFile,data):
    """
    Create a videofile with next, previous and beamerinfo from json data
    Keyword arguments:
    inputFile -- The file to use as the base slide
    data -- json containing all the information
    """

    # A small explanation of what some of the ffmpeg-options do
    # expansion=none makes it so that no text-expansion happens, all %s and stuff remains unchanged
    # -c:v libx264 -qp 0 -c:a copy -- codec video x264, don't care about filesize be fast instead, quality profile 0(highest), copy audio stream
    fontFile = "./arial.ttf"
    entrySettings = "drawtext=fontsize=30:fontcolor=0xFFFFFFFF:shadowcolor=0x000000EE:shadowx=2:shadowy=2:fontfile=%s:x=1050:y=1040:expansion=none:text=" % (fontFile)
    beamerSettings = "drawtext=fontsize=30:fontcolor=0xFFFFFFFF:shadowcolor=0x000000EE:shadowx=2:shadowy=2:fontfile=%s:x=36:y=1020:expansion=none:text=" % (fontFile)
    previousSettings = "drawtext=fontsize=30:fontcolor=0xFFFFFFFF:shadowcolor=0x000000EE:shadowx=2:shadowy=2:fontfile=%s:x=26:y=100:expansion=none:text=" % (fontFile)
    encodingSettings = "-c:v libx264 -preset ultrafast -qp 0 -c:a copy "

    """
        This is the order of the fields in database
        "fields": [
            "contribution_id",
            "contributer",
            "entry_name",
            "beamer_info",
            "filename",
            "competition_id"
        ]
    """
    for index, contribution in enumerate(data):
        # This is because the first entry will not have a previous entry
        if index != 0:
            previousContribution = data[index - 1]['contributer'] + " - " + data[index - 1]['entry_name']
        else:
            previousContribution = "-"
        contribDict = {
                'filename' : shellEscape(os.path.splitext(str(index) + "-" + str(contribution['contributer']) + "-" + contribution['entry_name'])[0] + "-slide.mkv"),
                'inputFile' : inputFile,
                'id' : contribution['contribution_id'],
                'entryName' : contribution['contributer'] + " - " + contribution['entry_name'],
                'beamerInfo' : contribution['beamer_info'].replace("%", "\%"),
                'beamerSettings': beamerSettings,
                'entrySettings': entrySettings,
                'previousSettings': previousSettings,
                'previousContribution': previousContribution,
                'encodingSettings': encodingSettings
                }
        ffmpegcommand = "ffmpeg -threads 8 -i {inputFile} -vf \"[in]{entrySettings}{entryName}, {beamerSettings}{beamerInfo}, {previousSettings}{previousContribution}\" {encodingSettings} \"{filename}\"".format(**contribDict)
        os.system(ffmpegcommand)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: <input videfile> <json-file>")
        sys.exit(1)
    writeToVideo(sys.argv[1],getInfo(sys.argv[2]))
