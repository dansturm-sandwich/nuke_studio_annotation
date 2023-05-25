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
		tia = seq.trackItemAt(vti)    # get track item in sequence at playhead

		timg = te.image()			# get viewer image

		tts = tia.mapTimelineToSource(vti)+1  # map timeline time to source clip plus one because start frame 
		tts = int(tts)			# get frame as an integer (no decimals)
		ptts = f'{tts:04}'		# 4 digit padding for frame number

		stb = tia.source()    	# get source clip name from Track Item

		slc = str(stb)      	# source clip name as string
		ss = slc.split("'")[1]  # pull clip name out of NS "Clip('')" format


		prj = hiero.core.projects()[-1]		# get project asset
		ppt = prj.path()					# get path to project on disk
		opt = ppt.rsplit("/", 1)[0]			# remove project filename from path

		x = datetime.datetime.now()			# create date time object
		fdte = x.strftime("%y%m%d")			# format date object

		fin = ss + "." + str(ptts)			# create final screenshot filename

		fpth = opt + "/_notes/" + fdte + "/" + fin + ".png"		# full path + filename and extension
		jpth = opt + "/_notes/" + fdte + "/"	# just the full path, no filename

		fmt = seq.format()                      # format of sequence
		swid = fmt.width()                      # width of sequence
		shig = fmt.height()                     # height of sequence


		vsize = timg.size()                     # viewer image size
		vwid = vsize.width()                    # viewer image width
		vhig = vsize.height()                   # viewer image height

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

