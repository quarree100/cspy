# /////////////////////////////////////////////////////////////////////////////
# {{ CityScopePy }}
# Copyright (C) {{ 2018 }}  {{ Ariel Noyman }}

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# /////////////////////////////////////////////////////////////////////////////

# CityScopePy SCANNER
# a simple decoder of 2d array made of LEGO bricks, parsing and sending for visualzation

# "@context": "https://github.com/CityScope/", "@type": "Person", "address": {
# "@type": "75 Amherst St, Cambridge, MA 02139", "addressLocality":
# "Cambridge", "addressRegion": "MA",},
# "jobTitle": "Research Scientist", "name": "Ariel Noyman",
# "alumniOf": "MIT", "url": "http://arielnoyman.com",
# "https://www.linkedin.com/", "http://twitter.com/relno",
# https://github.com/RELNO]

# raise SystemExit(0)

import math
import numpy as np
import cv2
import MODULES

import json


# load the tags text file
# tagsArray = np.loadtxt('tags.txt', dtype=str)

tagsArray = []
with open('tags.json') as json_data:
    jd = json.load(json_data)

    for i in jd['tags']:
        npTag = np.array([int(ch) for ch in i])
        tagsArray.append(npTag)


# raise SystemExit(0)

# load the keystone data from file
# keyStoneData = np.loadtxt('../KEYSTONE/keystone.txt')

pts = [
    # 0
    (800, 130),
    # 1
    (1000, 130),
    # 2
    (800, 250),
    # 3
    (1000, 250)
]

x = 0


# define the video
webcam = cv2.VideoCapture(0)

# define the video window
cv2.namedWindow('webcamWindow')

# NOTE: must fit KEYSTONE resolution
# set res. for webcamWindow
videoResX = 1600
videoResY = 800

# define the grid size
gridX = 6
gridY = 3

# define the number of grid pixel scanners
gridSize = gridX*gridY

# define the size for each scanner
cropSize = 10

# call colors dictionary
colors = MODULES.colDict

# equal divide of canvas
step = int(videoResX/gridSize)

scanLocArr = MODULES.makeGridOrigins(videoResX, videoResY, cropSize)


# run the video loop forever
while(True):

    # zero an array to collect the scanners
    colorArr = []

    # init counter
    counter = 0

    # read video frames
    _, thisFrame = webcam.read()

    '''

    # show the whole camera
    cv2.imshow('test', thisFrame)

    NOTE: have fine grain keystone method here
    '''

    # break video loop by pressing ESC
    key = cv2.waitKey(5) & 0xFF
    if key == 27:
        break

    keyStoneData = MODULES.fineGrainKeystone(pts)

    # warp the video based on keystone info
    distortVid = cv2.warpPerspective(
        thisFrame, keyStoneData, (videoResX, videoResY))

    # run through locations list and make scanners
    for loc in scanLocArr:

        # set x and y from locations array
        x = loc[0]
        y = loc[1]

        # set scanner crop box size and position
        # at x,y + crop box size
        crop = distortVid[y:y+cropSize, x:x+cropSize]

        # draw rects with mean value of color
        meanCol = cv2.mean(crop)

        # convert colors to rgb
        b, g, r, _ = np.uint8(meanCol)
        mCol = np.uint8([[[b, g, r]]])

        # select the right color based on sample
        scannerCol = MODULES.colorSelect(mCol)

        # get color from dict
        thisColor = colors[scannerCol]

        # add colors to array for type analysis
        colorArr.append(scannerCol)

        # draw rects with frame colored by range result
        cv2.rectangle(distortVid, (x, y),
                      (x+cropSize, y+cropSize),
                      thisColor, 1)

        # draw the mean color itself
        # cv2.rectangle(distortVid, (x, y),
        #               (x+cropSize, y+cropSize),
        #               meanCol, -1)

        cv2.putText(distortVid, str(counter) + '_' + str(scannerCol),
                    (x, y), cv2.FONT_HERSHEY_SIMPLEX,
                    0.2, (0, 0, 0))

        counter += 1

    # create the output colors array
    resultColorArray = np.reshape(colorArr, (18, 9))

    # send array to check types
    t = MODULES.findType(resultColorArray, tagsArray)
    # print('\n', t)

    # draw the video to screen
    cv2.imshow("webcamWindow", distortVid)


# break the loop
webcam.release()
cv2.destroyAllWindows()
