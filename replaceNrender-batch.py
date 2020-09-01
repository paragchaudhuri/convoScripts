# replaceNrender plugin
# This currently only works for the degree awarding scene

import csv
import os
import RLPy
from PySide2 import *
from PySide2.QtCore import Qt
from PySide2.shiboken2 import wrapInstance


# INSTRUCTIONS

# 1. To start the plugin -
# Go to Scripts > Load Python in iClone 7 and locate the file replaceNrender.py. Open it.
# Press OK on the dialog box that shows up
# Go to Plugins > replaceNrender > replaceNrender
# A window should open. The current selection in the scene should change to the student. The rollnumber should update in the window
# The selected scarf colour should show "None"

# 2. To load and render the scene with a new student -
# Make sure the iAvatar file is named as <rollnumber>-<scarfcolour> like 170502009-green
# Drag and drop this file on the selected student avatar in the scene.
# Drag and drop an iAvatar file onto the selected student. 
# Make sure the currently selected avatar name in the plugin window changed to the roll number of the imported iAvatar file.
# Make sure that the scarf colour in the plugin window changed to the scarf colour of the imported iAvatar file.
# Click render. 
# The video file should be named <rollnumber>.mp4 and will get created in the same path as the original iClone project file.
# Repeat 2. for other iAvatar files

# CHANGE THESE ONLY IF YOU KNOW WHAT YOU ARE DOING, OTHERWISE LEAVE THEM ALONE
director_avatar_name = "Director_iAvatar";
scarf_mesh_name = "Mesh.001";
scarf_material_name = "scarf";

scarf_path = "F://Realallusion/DEMO ASSETS/scarf";
scarf_path_exists=False;


# Global Variables
ui = {};
all_avatars = [];

avatar_list_file = "";
avatar_list_torender = [];
avatar_file_path = "";
avatar_list_file_exists = False;

green_image = "green.png";
blue_image = "blue.png";
red_image = "red.png";
scarf_type=["None","Green","Blue","Red"];

event_callback = None;
avatar_events = {};
student_avatar = None;

data_refresh_needed = True;
callback_registered = False;

student_name="";
scarf_name="";


############################################################################

#Callbacks
class AvatarLoadEventCallback(RLPy.REventCallback):
    def __init__(self):
        RLPy.REventCallback.__init__(self);

    def OnObjectDataChangedWithType(self, nChangeType):
        print('Object Data Changed: '+str(nChangeType));
        if (nChangeType == 64): 
        	update_on_avatar_change();

    def OnObjectSelectionChanged(self):
        print('Object Selection Changed');

    def OnObjectAdded(self):
        print('Object Added');


class DialogEventCallback(RLPy.RDialogCallback):
    def __init__(self):
        RLPy.RDialogCallback.__init__(self);

    def OnDialogClose(self):
        global avatar_events, callback_registered;

        if (callback_registered):
        	if (avatar_events.get('callback_id',False)):
        		RLPy.REventHandler.UnregisterCallback(avatar_events["callback_id"]);
        		avatar_events.clear;
        		callback_registered=False;
        		return True;

def set_avatar_select():
	global ui, all_avatars;

	index = ui["avatar-combo"].currentIndex();
	RLPy.RScene.SelectObject(all_avatars[index]);

def set_scarf_colour(material_component):
	global ui;

	colour_index = ui["scarf-combo"].currentIndex();

	if (colour_index==1):
		image_file=scarf_path+"/"+green_image;
	elif (colour_index==2):
		image_file=scarf_path+"/"+blue_image;
	elif (colour_index==3): 
		image_file=scarf_path+"/"+red_image;
	else:
		image_file="";

	result = material_component.LoadImageToTexture(scarf_mesh_name, scarf_material_name, RLPy.EMaterialTextureChannel_Diffuse, image_file);

def do_render():
	global ui, student_name;

	if (ui["scarf-combo"].currentIndex() != 0):
		video_name="/"+student_name+".mp4";
		print(student_name);
		RLPy.RGlobal.RenderVideo(video_name);
	else:
		RLPy.RUi.ShowMessageBox("Error", "Choose a Valid Scarf Colour.", RLPy.EMsgButton_Ok);

def do_batch_render():
	global ui, student_name, avatar_file_path, avatar_list_torender;

	ui["status-box"].insertPlainText("Batch Render Start ------------------------\n\n");

	for i in range(len(avatar_list_torender)):
		ui["status-box"].insertPlainText("Loading iAvatar : "+avatar_list_torender[i]+"\n");
		filename=avatar_file_path+"/"+avatar_list_torender[i]+".iavatar";
		current_avatar = RLPy.RFileIO.LoadObject(filename);
		
		if (ui["scarf-combo"].currentIndex() != 0):
			video_name="/"+student_name+".mp4";
			ui["status-box"].insertPlainText("Rendering iAvatar : "+student_name+".mp4\n");
			RLPy.RGlobal.RenderVideo(video_name);
			ui["status-box"].insertPlainText("Done.\n\n");
			bottom = ui["status-box"].verticalScrollBar().maximum();
			ui["status-box"].verticalScrollBar().setValue(bottom);

		else:
			RLPy.RUi.ShowMessageBox("Error", "No valid scarf colour selected.", RLPy.EMsgButton_Ok);

	ui["status-box"].insertPlainText("Batch Render End ------------------------\n\n");

def do_csv_file_load():
	global ui, avatar_list_torender;
	
	avatar_list_torender.clear();

	with open(avatar_list_file) as csvfile:
		filelistreader = csv.reader(csvfile)
		for row in filelistreader:
			avatar_list_torender.append(str(row[0]));

	ui["status-box"].insertPlainText("Read CSV file: "+avatar_list_file+"\n\n");
	ui["status-box"].insertPlainText("Found "+str(len(avatar_list_torender))+" iAvatar files to render.\n\n");

def do_find_and_load_csv():
	global ui, avatar_list_file, avatar_file_path, avatar_list_file_exists;

	avatar_list_file="";
	dummyTemp = QtWidgets.QFileDialog.getOpenFileName(ui["main-widget"], caption='Load CSV File', filter='CSV file (*.csv)');
	avatar_list_file=dummyTemp[0];

	if (str(avatar_list_file)!=""):
		ui["csv-file"].setText(str(avatar_list_file));
		avatar_file_path=os.path.split(str(avatar_list_file))[0];
		do_csv_file_load();
		avatar_list_file_exists=True;
		activate_batch_render();
	     
def do_find_scarf():
	global ui, scarf_path, scarf_path_exists, scarf_path;

	scarf_path="";
	scarf_path=QtWidgets.QFileDialog.getExistingDirectory()
	if (str(scarf_path!="")):
		ui["scarf-file-path"].setText(str(scarf_path));
		scarf_path_exists=True;
		activate_batch_render();

############################################################################

# Helpers

def activate_batch_render():
	global ui, scarf_path_exists, avatar_list_file_exists;
	if (scarf_path_exists and avatar_list_file_exists):
		ui["status-box"].insertPlainText("Batch Render Enabled!\n\n")
		ui["batch-render-button"].setDisabled(False)
		ui["batch-render-button"].setEnabled(True)

def update_avatar_data():
	global ui, all_avatars, student_avatar;
	try:
		
		all_avatars = RLPy.RScene.FindObjects(RLPy.EObjectType_Avatar);
		# Add an entry into the combo-box for every prop found
		for i in range(len(all_avatars)):
			ui["avatar-combo"].addItem(all_avatars[i].GetName());
			if (all_avatars[i].GetName() != director_avatar_name):
				RLPy.RScene.SelectObject(all_avatars[i]);
				ui["avatar-combo"].setCurrentIndex(i);
				student_avatar=all_avatars[i];
	except:
		RLPy.RUi.ShowMessageBox("Error", "Avatar error.", RLPy.EMsgButton_Ok);

def update_scarf_data():
	global ui, student_avatar;
	# morph_list = student_avatar.GetMorphComponent()
	try:
		material_component = student_avatar.GetMaterialComponent();
		ui["scarf-combo"].addItem("None");
		ui["scarf-combo"].addItem("Green");
		ui["scarf-combo"].addItem("Blue");
		ui["scarf-combo"].addItem("Red");
		ui["scarf-combo"].setCurrentIndex(0);
		ui["scarf-combo"].currentIndexChanged.connect(lambda: set_scarf_colour(material_component));
	except:
		RLPy.RUi.ShowMessageBox("Error", "Scarf error.", RLPy.EMsgButton_Ok);

def update_on_avatar_change():
	global ui, all_avatars, student_avatar, student_name, scarf_name;

	#all_avatars.clear()
	all_avatars = RLPy.RScene.FindObjects(RLPy.EObjectType_Avatar);
	# Add an entry into the combo-box for every prop found
	numavatars = len(all_avatars);
	ui["avatar-combo"].clear();
	if (numavatars > 0):
		for i in range(numavatars):
			ui["avatar-combo"].addItem(all_avatars[i].GetName());
			if (all_avatars[i].GetName() != director_avatar_name):
				RLPy.RScene.SelectObject(all_avatars[i]);
				ui["avatar-combo"].setCurrentIndex(i);
				student_avatar=all_avatars[i];

		if (student_avatar.IsValid()):
			material_component = student_avatar.GetMaterialComponent();

			temp_name=student_avatar.GetName().split("-",1)
			if (len(temp_name) > 1):
				student_name=temp_name[0];
				scarf_name=temp_name[1];
			else:
				student_name=""
				scarf_name=""
			if (scarf_name.lower() == "green"):
				ui["scarf-combo"].setCurrentIndex(1);
			elif (scarf_name.lower() == "blue"):
				ui["scarf-combo"].setCurrentIndex(2);
			elif (scarf_name.lower() == "red"):
				ui["scarf-combo"].setCurrentIndex(3);
			else:
				ui["scarf-combo"].setCurrentIndex(0);
			set_scarf_colour(material_component);
			#ui["scarf-combo"].clear()
			#update_scarf_data()
			data_refresh_needed=False;
	else:
		data_refresh_needed=True;

############################################################################

# Callback Helpers
def register_callbacks():
	global ui, avatar_events, callback_registered;

	# Register callback events
	avatar_events["callback"] = AvatarLoadEventCallback();
	avatar_events["callback_id"] = RLPy.REventHandler.RegisterCallback(avatar_events["callback"]);
	callback_registered = True;

def deregister_callbacks():
	global avatar_events, callback_registered;

	RLPy.REventHandler.UnregisterCallback(avatar_events["callback_id"]);
	avatar_events.clear();
	callback_registered = False;

############################################################################

# Create UI
def create_window():
	global ui, all_avatars, avatar_events, student_avatar, data_refresh_needed, callback_registered;

	try:
		ui["window"] = RLPy.RUi.CreateRDockWidget();
		ui["window"].SetWindowTitle("Replace N Render");
		ui["dock"] = wrapInstance(int(ui["window"].GetWindow()), QtWidgets.QDockWidget);
		ui["main-widget"] = QtWidgets.QWidget();
		ui["dock"].setWidget(ui["main-widget"]);

		ui["main-widget-layout"] = QtWidgets.QVBoxLayout();
		ui["main-widget"].setLayout(ui["main-widget-layout"]);

		ui["avatar-label"] = QtWidgets.QLabel("Currently Selected Avatar");
		ui["avatar-combo"] = QtWidgets.QComboBox();
		ui["main-widget-layout"].addWidget(ui["avatar-label"]);
		ui["main-widget-layout"].addWidget(ui["avatar-combo"]);
		ui["avatar-combo"].currentIndexChanged.connect(lambda: set_avatar_select());
		ui["avatar-combo"].setDisabled(True);

		ui["scarf-label"] = QtWidgets.QLabel("Scarf Colour");
		ui["scarf-combo"] = QtWidgets.QComboBox();
		ui["main-widget-layout"].addWidget(ui["scarf-label"]);
		ui["main-widget-layout"].addWidget(ui["scarf-combo"]);
		ui["scarf-combo"].setDisabled(True);

		ui["spacer"] = QtWidgets.QSpacerItem(20,20,QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum);
		ui["main-widget-layout"].addSpacerItem(ui["spacer"]);
		ui["main-widget-layout"].addSpacerItem(ui["spacer"]);

		ui["scarf-path-label"] = QtWidgets.QLabel("Path to Scarf Assets");
		ui["main-widget-layout"].addWidget(ui["scarf-path-label"]);
		ui["load-scarf-layout"] = QtWidgets.QHBoxLayout();
		ui["scarf-file-path"] = QtWidgets.QLineEdit();
		ui["scarf-file-path"].setReadOnly(True);
		ui["scarf-file-path"].setText("");
		ui["load-scarf-layout"].addWidget(ui["scarf-file-path"]);
		ui["scarf-path-button"] = QtWidgets.QPushButton("Find Scarf");
		ui["scarf-path-button"].clicked.connect(lambda: do_find_scarf());
		ui["load-scarf-layout"].addWidget(ui["scarf-path-button"]);
		ui["main-widget-layout"].addLayout(ui["load-scarf-layout"]);

		ui["csv-path-label"] = QtWidgets.QLabel("CSV File");
		ui["main-widget-layout"].addWidget(ui["csv-path-label"]);
		ui["load-file-layout"] = QtWidgets.QHBoxLayout();
		ui["csv-file"] = QtWidgets.QLineEdit();
		ui["csv-file"].setReadOnly(True);
		ui["csv-file"].setText("");
		ui["load-file-layout"].addWidget(ui["csv-file"]);
		ui["csv-file-button"] = QtWidgets.QPushButton("Find CSV");
		ui["csv-file-button"].clicked.connect(lambda: do_find_and_load_csv());
		ui["load-file-layout"].addWidget(ui["csv-file-button"]);
		ui["main-widget-layout"].addLayout(ui["load-file-layout"]);

		#ui["render-button"] = QtWidgets.QPushButton("Render");
		#ui["main-widget-layout"].addWidget(ui["render-button"]);
		#ui["render-button"].clicked.connect(lambda: do_render());
		#ui["main-widget-layout"].addSpacerItem(ui["spacer"]);

		ui["batch-render-button"] = QtWidgets.QPushButton("Batch Render all iAvatar files");
		ui["main-widget-layout"].addWidget(ui["batch-render-button"]);
		ui["batch-render-button"].clicked.connect(lambda: do_batch_render());
		ui["batch-render-button"].setDisabled(True);

		ui["main-widget-layout"].addSpacerItem(ui["spacer"]);

		ui["status-label"] = QtWidgets.QLabel("Status");
		ui["main-widget-layout"].addWidget(ui["status-label"]);
		ui["status-box"] = QtWidgets.QTextEdit(readOnly=True);
		ui["main-widget-layout"].addWidget(ui["status-box"]);

		# Register dialog event callback
		avatar_events["dialog_callbacks"] = DialogEventCallback();
		ui["window"].RegisterEventCallback(avatar_events["dialog_callbacks"]);
	except:
		RLPy.RUi.ShowMessageBox("Error", "GUI Create Error.", RLPy.EMsgButton_Ok);

	# Grab all avatars in the scene
	if (data_refresh_needed):
		update_avatar_data();
		update_scarf_data();
		data_refresh_needed=False;

	if (not callback_registered): 
		register_callbacks();

	ui["window"].Show();
	ui["status-box"].insertPlainText("Plugin initialized.\n\n")

# Show UI
def show_window():
    global ui, data_refresh_needed, callback_registered;

    try:
	    if "window" in ui:
	    	if (not ui["window"].IsVisible()):
	    		ui["csv-file"].setText("");
	    		ui["scarf-file-path"].setText("");
	    		scarf_path_exists=False;
	    		avatar_list_file_exists=False;
	    		ui["batch-render-button"].setDisabled(True);
	    		ui["status-box"].clear();
	    		data_refresh_needed=True;
	    		if (callback_registered):
	    			deregister_callbacks();

	    		if (data_refresh_needed):
	    			update_avatar_data();
	    			update_scarf_data();
	    			data_refresh_needed=False;
    			if (not callback_registered):
    				register_callbacks();
	    		ui["window"].Show();
	    else:
	    	create_window();
    except:
    	RLPy.RUi.ShowMessageBox("Error", "No Avatar or Scarf found.", RLPy.EMsgButton_Ok);
    	data_refresh_needed = True;
    	if (callback_registered):
    		deregister_callbacks();


############################################################################

#Init plugin
def initialize_plugin():
    # Create Pyside interface with iClone main window
    ic_dlg = wrapInstance(int(RLPy.RUi.GetMainWindow()), QtWidgets.QMainWindow);

    plugin_menu = ic_dlg.menuBar().findChild(QtWidgets.QMenu, "Replace N Render")  # Check if the menu item exists

    if plugin_menu is None:
        plugin_menu = wrapInstance(int(RLPy.RUi.AddMenu("Replace N Render", RLPy.EMenu_Plugins)), QtWidgets.QMenu);
        # Setting an object name for the menu is equivalent to giving it an ID
        plugin_menu.setObjectName("Replace N Render");  

    # Check if the menu action already exists
    menu_actions = plugin_menu.actions();
    for i in range(len(menu_actions)):
        if menu_actions[i].text() == "replaceNrender":
            plugin_menu.removeAction(menu_actions[i]);  # Remove duplicate actions

    # Set up the menu action
    menu_action = plugin_menu.addAction("replaceNrender");
    menu_action.triggered.connect(show_window);

#Script entry
def run_script():
	initialize_plugin();
	RLPy.RUi.ShowMessageBox("Replace N Render",
		"You can run the replaceNrender plugin from the menu bar under <b>Plugins > replaceNrender</b>.",
		RLPy.EMsgButton_Ok
		);

############################################################################
