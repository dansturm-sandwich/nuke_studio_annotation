import hiero.core
import hiero.ui
import os
import datetime
import time
from PySide6.QtCore import Qt


def annotationShot():
    te = hiero.ui.currentViewer()        # Get active viewer
    ve = te.player()                     # Get player element of viewer

    vti = ve.time()                      # Get current playhead position in timeline
    seq = ve.sequence()                  # Get sequence in viewer
    tia = seq.trackItemAt(vti)           # Get track item in sequence at playhead
    timg = te.image()                    # Get viewer image

    # Frame padding (4 digits)
    ptts = f'{(int(tia.mapTimelineToSource(vti) + 1)):04}'

    # Source clip name
    ss = str(tia.source()).split("'")[1]

    # Path to project file (minus filename)
    opt = hiero.core.projects()[-1].path().rsplit("/", 1)[0]

    # Dated folder
    fdte = datetime.datetime.now().strftime("%y%m%d")
    jpth = os.path.join(opt, "_notes", fdte)
    os.makedirs(jpth, exist_ok=True)

    # Build base filename (no timestamp)
    base_name = f"{ss}.{ptts}"

    # Find next available index (.1, .2, etc.)
    index = 1
    while True:
        fin = f"{base_name}.{index}.jpg"
        fpth = os.path.join(jpth, fin)
        if not os.path.exists(fpth):
            break
        index += 1

    # Sequence format info
    swid = seq.format().width()
    shig = seq.format().height()
    asp = seq.format().pixelAspect()
    swid = swid * asp

    vwid = timg.size().width()
    vhig = timg.size().height()

    svwid = vwid * (shig / vhig)
    svhig = vhig * (swid / vwid)

    sratio = swid / shig
    vratio = vwid / vhig

    # Scale and crop viewer image to match sequence format
    if sratio > vratio:
        ssx = (svhig / 2) - (shig / 2)
        simg = timg.scaledToWidth(swid, mode=Qt.SmoothTransformation)
        cimg = simg.copy(0, ssx, swid, shig)
    else:
        ssx = (svwid / 2) - (swid / 2)
        simg = timg.scaledToHeight(shig, mode=Qt.SmoothTransformation)
        cimg = simg.copy(ssx, 0, swid, shig)

    # Save cropped/scaled image
    cimg.save(fpth, "jpg")

    # Apply display ICC profile
    os.system(f'sips -s profile /Library/ColorSync/Profiles/Displays/StudioDisplay-7B124C67-2DD2-8F2D-1452-F1C958A0C9F4.icc "{fpth}"')

    # Open the saved image and containing folder
    os.system(f'open "{jpth}"')
    os.system(f'open "{fpth}"')

    # Activate annotation tool (Cmd+Shift+A)
    time.sleep(1)
    os.system("""osascript -e 'tell application "System Events" to keystroke "a" using {command down, shift down}'""")

    print(f"Saved annotation: {fpth}")