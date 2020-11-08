# Create directories (folders) for each image in CSV with their
# corresponding avatar body profile chosen from the template dir

import csv
import os.path
import shutil


rootDir="../runs/convo2020/"

rootDir = os.path.expanduser(rootDir)

imageDir="fronts"
templateDir="templates"
avataroutputDir="avatars"

profilefile=rootDir + 'testprof.csv'

genderdict = { 'f': 'female', 'm':'male'}

listfile = os.path.join(rootDir + avataroutputDir , "allavatars.csv")

with open(profilefile, 'r') as ifp, open(listfile,'w') as lstfp:
    csvr = csv.reader(ifp)
    next(csvr) # gobble one header line

    for row in csvr:
        rollno = row[0]
        gender = row[1]
        bodywt = row[2]
        height = row[3]
        ucolor = row[4]
        specs = row[5]

        frontimg=rollno + "_front.jpg"

        imgpath = os.path.join(rootDir+imageDir, frontimg)

        #if os.path.isfile(imgpath) and os.access(imgpath, os.R_OK):
        if not os.path.exists(imgpath):
            print("%s does not exist or not readable" % imgpath)
        else:
        
            template= genderdict[gender] + "_" + bodywt + \
                "_" + height + '.iAvatar' 

            src  = os.path.join(rootDir+templateDir, template)
            
            if os.path.exists(src):
                destdir = os.path.join(rootDir+avataroutputDir, rollno)
                os.makedirs(destdir,exist_ok=True)

                # copy front facing photo
                shutil.copy(imgpath,destdir)

                avatar = rollno + "-" + ucolor + '-' + specs + '.iAvatar'
                print(frontimg, template, avatar, destdir)
                dest = os.path.join(destdir,avatar)

                # copy the template avatar
                shutil.copy(src,dest)

                lstfp.writelines(rollno + '/' + avatar+'\n')
            else:
                print("%s does not exist or not readable" % src)

        
        
