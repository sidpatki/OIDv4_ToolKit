# lines added by siddharth to remove ros opencv from environment for running this project
import sys;
import numpy as np
import pandas as pd
import os
import glob


print("preparing data for class: ",sys.argv[1])

# provide absolute paths to the following files on your machine
f=pd.read_csv("/home/spatki/rail/rail_developer/rocyolo/OIDv4_ToolKit/OID/csv_folder/train-annotations-bbox.csv")
cdf=pd.read_csv("/home/spatki/rail/rail_developer/rocyolo/OIDv4_ToolKit/OID/csv_folder/class-descriptions-boxable.csv")

class_name = sys.argv[1];
class_id = cdf[cdf.iloc[:,1] == class_name].iloc[0,0];

# directory where annotations will be generated
trainDirName = "/home/spatki/rail/rail_developer/rocyolo/OIDv4_ToolKit/OID/Dataset/train/" + class_name + "/"

# u = f.loc[f['LabelName'] == class_id]
# keep_col = ['ImageID','XMin','XMax','YMin','YMax']
#
# new_f = u[keep_col]
# new_f['width'] = new_f['XMax'] - new_f['XMin']
# new_f['height'] = new_f['YMax'] - new_f['YMin']
# new_f['x'] = (new_f['XMax'] + new_f['XMin'])/2
# new_f['y'] = (new_f['YMax'] + new_f['YMin'])/2
# keep_col = ['ImageID','x','y','width','height']
# new_f_2 = new_f[keep_col]
#
# for root, dirs, files in os.walk(trainDirName):
# 	for filename in files:
#
# 		if filename.endswith(".jpg"):
# 			fn = filename[:-4]
# 			nf = new_f_2.loc[new_f_2['ImageID'] == fn]
# 			#if only training one class
# 			nf['class_name'] = 0
# 			#If training multiple
# 			#nf['class_name'] = numClasses.index(nf['LabelName'])
# 			keep_col = ['class_name','x','y','width','height']
# 			new_nf = nf[keep_col]
# 			# print(nf)
# 			imgpath = trainDirName + fn + ".txt"
# 			print(imgpath)
#
# 			new_nf.to_csv(imgpath, index=False, header=False, sep=' ')
# 			#pull the x,y,width,height data, for each row with the imageid, to a variable
# 			continue
# 		else:
# 			continue

## Code to generate train.txt and test.txt files required by darknet training program
# it lists absolute paths to all image files

# Percentage of images to be used for the test set
percentage_test = 1;
# Create and/or truncate train.txt and test.txt
file_train = open( trainDirName+"train.txt", 'w')
file_test = open( trainDirName+"test.txt", 'w')
# Populate train.txt and test.txt
counter = 1
index_test = round(100 / percentage_test)
for pathAndFilename in glob.iglob(os.path.join(trainDirName, "*.jpg")):
    title, ext = os.path.splitext(os.path.basename(pathAndFilename))
    if counter == index_test:
        counter = 1
        file_test.write(trainDirName + title + '.jpg' + "\n")
    else:
        file_train.write(trainDirName + title + '.jpg' + "\n")
        counter = counter + 1



#### generate the .names file
file_names = open(trainDirName+class_name+".names", 'w')
file_names.write(class_name);

#### generate the .names file
file_data = open(trainDirName+class_name+".data", 'w')
file_data.write("classes = 1\n")
file_data.write("train = "+trainDirName+"train.txt\n")
file_data.write("valid = "+trainDirName+"test.txt\n")
file_data.write("names = "+trainDirName+class_name+".names\n")
try:
    # Create target Directory
    os.mkdir(trainDirName+"../../../../../trained_weights/"+class_name)
except FileExistsError:
    print("Directory already exists")
file_data.write("backup = "+trainDirName+"../../../../../trained_weights/"+class_name+"\n")
