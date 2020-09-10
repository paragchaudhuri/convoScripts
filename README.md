# replaceNrender
This is an iClone 7 plugin for the iit bombay convocation project

## To download the script
Use
`git clone git://github.com/paragchaudhuri/replaceNrender`
to get all three scripts. Or download the zip from the github.com repository page.

The `replaceNrender-glass-batch.py` script does a batch render while taking care of the glass/noglass condition and scarf colour, so most probably that is the one you want. 

## To run the script

1. To start the plugin in iClone -
- Go to *Scripts > Load Python* in iClone and locate the python file for this script. Open it.
- Press *OK* on the dialog box that shows up.
- Go to *Plugins > replaceNrender > replaceNrender*
- A window should open. The current selection in the scene should change to the student. The rollnumber should update in the window
- Currently selected avatar shoud show the name of the student avatar asset
- Scarf colour should show *None*. Glasses should show *None*.


2. To load and render the scene with new student avatars -
- Click on **Find Scarf** in the plugin window, locate and select the folder containing the scarf textures.
- This folder must have the files `blue.png`, `green.png` and `red.png` for the blue, green and red scarf textures. 
- Make sure there are two images called `black.png` and `white.png` which are of size *1024x1024* in the same folder. These are grayscale, single channel, all black and all white images respectively.
- Make sure all the iAvatar files to be rendered are named as `<rollnumber>-<scarfcolour>-glass` or `<rollnumber>-<scarfcolour>-noglass`, e.g., `170502009-green-noglass`.
- Locate a CSV file by clicking **Find CSV** that contains the list of avatar files to be rendered. This file should be in the same folder as the iAvatar files.
- It should contain one filename on every line, without the file extension.
- The status box should update and show the number of avatar filenames found in the CSV file.
- **Batch Render all iAvatar files** button should now be enabled.
- Click this button and all the iAavatar files will be imported one by one and the project will be rendered for each.
- The video file should be named `<rollnumber>.mp4` and will get created in the same path as the original iClone project file.

