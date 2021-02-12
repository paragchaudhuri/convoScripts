# Create directories (folders) for each image in CSV with their
# corresponding avatar body profile chosen from the template dir

import csv
import os.path
import shutil

from contextlib import ExitStack


rootDir="../runs/convo2020"

rootDir = os.path.expanduser(rootDir)

imageDir="front-images"
templateDir="templates"
avataroutputDir="avatars"

profilefile=os.path.join(rootDir , 'testprof.csv')

genderdict = { 'f': 'female', 'm':'male'}

animTemplates = ['short', 'equal', 'tall']

# for a in animTemplates:
#     listfiles[i] = os.path.join(rootDir + avataroutputDir , a, "allavatars.csv")

lstfp = {}

with ExitStack() as stack:
    # All opened files will automatically be closed at the end of
    # the with statement, even if attempts to open files later
    # in the list raise an exception
    # https://stackoverflow.com/a/53363923/2601819
    ifp = stack.enter_context(open(profilefile, 'r'))
    for a in animTemplates:
        rollDir = os.path.join(rootDir , avataroutputDir , a)
        os.makedirs(rollDir,exist_ok=True)
        listfile = os.path.join(rollDir, "allavatars.csv")
        lstfp[a] =  stack.enter_context(open(listfile, 'w'))
        

    csvr = csv.reader(ifp)
    next(csvr) # gobble one header line

    for row in csvr:
        rollno = row[0].lower()
        gender = row[1]
        bodywt = row[2]
        height = row[3]
        ucolor = row[4]
        specs = row[5]

        frontimg=rollno + "_front.jpg"

        imgpath = os.path.join(rootDir, imageDir, frontimg)

        #if os.path.isfile(imgpath) and os.access(imgpath, os.R_OK):
        if not os.path.exists(imgpath):
            print("%s does not exist or not readable" % imgpath)
        else:
        
            template= genderdict[gender] + "_" + bodywt + \
                "_" + height + '.iAvatar' 

            src  = os.path.join(rootDir, templateDir, template)
            
            if os.path.exists(src):
                destdir = os.path.join(rootDir, avataroutputDir, height, rollno)
                os.makedirs(destdir,exist_ok=True)

                # copy front facing photo
                shutil.copy(imgpath,destdir)

                avatar = rollno + "-" + ucolor + '-' + specs + '.iAvatar'
                #print(frontimg, template, avatar, destdir)
                print("Copying for", rollno, template)
                dest = os.path.join(destdir,avatar)

                # copy the template avatar
                shutil.copy(src,dest)

                lstfp[height].writelines(rollno + '/' + avatar+'\n')
            else:
                print("%s does not exist or not readable" % src)

        
        
