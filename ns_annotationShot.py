import hiero.core
import hiero.ui
import os
import os.path 
import datetime
from PySide2 import QtCore
from PySide2.QtCore import *



def annotationShot():
	te = hiero.ui.currentViewer()		# Get active viewer
	ve = te.player()			        # Get player element of viewer

	vti = ve.time()        		# get current playhead position in timeilne
	seq = ve.sequence()       	# get name of sequence in viewer
	tia = seq.trackItemAt(vti)	# get track item in sequence at playhead

	timg = te.image()			# get viewer image

	ptts = f'{(int(tia.mapTimelineToSource(vti)+1)):04}' #map timeline time to source clip with 4 digit padding

	ss = str(tia.source()).split("'")[1]	# get source clip name from track item

	opt = hiero.core.projects()[-1].path().rsplit("/", 1)[0]	# get path to project file and remove project filename

	x = datetime.datetime.now()			# create date time object
	fdte = x.strftime("%y%m%d")			# format date object

	fin = ss + "." + str(ptts)			# create final screenshot filename

	fpth = opt + "/_notes/" + fdte + "/" + fin + ".png"		# full path + filename and extension
	jpth = opt + "/_notes/" + fdte + "/"	# just the full path, no filename

	swid = seq.format().width()                      # width of sequence
	shig = seq.format().height()                     # height of sequence
	asp = seq.format().pixelAspect()
	swid = swid*asp

	vwid = timg.size().width()                    # viewer image width
	vhig = timg.size().height()                   # viewer image height

	svwid = vwid*(shig/vhig)				# scaled width of viewer


	ssx = (svwid/2) - (swid/2)				# position of left edge of frame

	simg = timg.scaledToHeight(shig, mode=Qt.SmoothTransformation)      # scale viewer image to format height

	cimg = simg.copy(ssx, 0, swid, shig)  	# crop image to format


	dircmd = 'mkdir -p "' + jpth + '"'		# if it doesn't exist, make dated folder inside _notes folder
	os.system(dircmd)				# run mkdir command

	cimg.save(fpth, "PNG")			# save cropped & scaled image to folder
	
	# add the colorsync profile
	os.system( 'sips -s profile /Library/ColorSync/Profiles/Displays/StudioDisplay-7B124C67-2DD2-8F2D-1452-F1C958A0C9F4.icc "' + fpth + '"')

	os.system('open "' + jpth + '"')	# open the folder containing the screenshot
	os.system('open "' + fpth + '"')	# open the screenshot


	print(fpth)

