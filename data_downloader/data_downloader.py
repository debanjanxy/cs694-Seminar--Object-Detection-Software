
# coding: utf-8

# In[2]:


import urllib.request
import cv2
import numpy as np
import pandas as pd
import re
import sys


# In[3]:


def download_normal_image(lat,long,zoom,filename_norm):
    url_norm = 'https://maps.googleapis.com/maps/api/staticmap?center='+str(lat)+','+str(long)+'&zoom='+str(zoom)+'&size=512x512'
    img_norm = urllib.request.urlretrieve(url_norm,filename_norm)


# In[4]:


#data downloading module
def download_negative_images(lat,long):
    for i in range(500):
        #filename_norm = 'not_well'+str(i)+'.png' 
#         download_normal_image(lat,long,i,zoom)
#         is_water_body = find_water_body(filename_norm)
#         download_satellite_image(lat,long,zoom,is_water_body,i)
        satellite_image_downloader(lat,long,'19',i,'64','n')
        lat = lat + 0.0001
        long = long + 0.0001


# In[5]:


def download_satellite_image(lat,long,zoom,is_water_body,itr):
    url_sat = 'https://maps.googleapis.com/maps/api/staticmap?center='+str(lat)+','+str(long)+'&zoom='+str(zoom)+'&size=512x512&maptype=satellite'
    if is_water_body:
        filename_sat = 'map_sat_present'+str(itr)+'.png'
    else:
        filename_sat = 'map_sat_absent'+str(itr)+'.png'
    img_sat = urllib.request.urlretrieve(url_sat,filename_sat)
    


# In[6]:


def find_water_body(filename_norm):
    frame = cv2.imread(filename_norm)
    img = frame
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)   
    lower_blue = np.array([107,92,255])
    upper_blue = np.array([107,92,255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    mask_thresh = cv2.erode(mask,None,iterations=2)
    mask_thresh = cv2.dilate(mask_thresh,None,iterations=4)
    f = 0
    dimensions = mask_thresh.shape
    for i in range(dimensions[0]):
        for j in range(dimensions[1]):
            if mask_thresh[i,j] == 255:
                print("Water body is present")
                return True
    if f==0:
        print("Water body is not present.")
        return False

def satellite_image_downloader(lat,long,i,flag):
	size = "64" #input("Enter the size of the image: ")
	zoom = "19" #input("Enter zoom level: ")
	url = 'https://maps.googleapis.com/maps/api/staticmap?center='+str(lat)+','+str(long)+'&zoom='+zoom+'&size='+size+'x'+size+'&maptype=satellite'
	if flag=='t':
		filename = "well"+str(i)
	else:
		filename = "not_well"+str(i)
	image = urllib.request.urlretrieve(url,filename)
	print("Download done of image ",i)


def read_latlong_from_textfile(file):
    res0 = []
    for i in file:
        i = re.sub('[ \n]','',i)
        hm = i.split(',')
        if(hm[0]==''):
            pass
        else:
            res0.append(hm)
    res1 = np.array(res0)
    res = pd.DataFrame(res1)
    return res

def save_images():
    size = "64" #input("Enter the size of the image: ")
    zoom = "19" #input("Enter zoom level: ")
    flag = input("Text(t) or CSV(c): ")
    if flag=='c':
        data = pd.read_csv('Gondala_Wells.csv')
        print(type(data))
    else:
        file = open('not_well','r')
        lines = file.readlines()
        data = read_latlong_from_textfile(lines)
    total_rows = data.count()[0]
    for i in range(total_rows):
        r = data.iloc[i]
        if flag=='c':
            lat = r[1]
            long = r[0]
        else:
            lat=r[0]
            long=r[1]
        satellite_image_downloader(lat,long,i,flag)



filename = sys.argv[1]
file = open(filename,'r')
lines = file.readlines()
flag = 't'
data = read_latlong_from_textfile(lines)
print(data)
#data
total_rows = data.count()[0]
for i in range(total_rows):
    r = data.iloc[i]
    if flag=='c':
        lat = r[1]
        long = r[0]
    else:
        lat=r[0]
        long=r[1]
    satellite_image_downloader(lat,long,i,flag)