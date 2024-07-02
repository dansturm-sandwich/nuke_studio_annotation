import hiero.core
import hiero.ui
import os
import os.path 
import datetime



def annotationShot():
		te = hiero.ui.currentViewer()		# Get active viewer
		ve = te.player()			        # Get player element of viewer

		vti = ve.time()        		# get current playhead position in timeilne
		seq = ve.sequence()       	# get name of sequence in viewer
		tia = seq.trackItemAt(vti)    # get track item in sequence at playhead


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


		dircmd = 'mkdir -p "' + jpth + '"'		# if it doesn't exist, make dated folder inside _notes folder
		scapcmd = 'screencapture -R317,148,1930,1090 "' + fpth + '"' 	# caputre the image to the new path

		os.system(dircmd)				# run mkdir command
		os.system(scapcmd)				# run screencapture command
		os.system('open "' + jpth + '"')	# open the folder containing the screenshot
		os.system('open "' + fpth + '"')	# open the screenshot

		print(jpth)
		print(fpth)

