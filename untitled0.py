# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 23:09:45 2019

@author: ASUS
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 10:29:26 2019

@author: ASUS
"""

import pickle
with open("2019-06-11_16-52-56.pickle", "rb") as f:
    data_list1 = pickle.load(f)
import pickle
with open("2019-06-13_10-30-44.pickle", "rb") as f:
    data_list2 = pickle.load(f)
import pickle
with open("2019-06-13_10-34-35.pickle", "rb") as f:
    data_list3 = pickle.load(f)
import pickle
with open("2019-05-31_00-50-21.pickle", "rb") as f:
    data_list4 = pickle.load(f)

data_list = data_list1 + data_list2 + data_list3 + data_list4
# save each information seperately
Ballposition=[]
Ballspeed=[]
PlatformPosition=[]
Command1P=[]
Status=[]

for i in range(0, len(data_list)):
    Ballposition.append(data_list[i].ball)
    Ballspeed.append(data_list[i].ball_speed)
    PlatformPosition.append(data_list[i].platform_1P)
    Command1P.append(data_list[i].command_1P)
    Status.append(data_list[i].status)
    
#%% calculate instruction of each frame using platformposition
import numpy as np
flag=[]
final=[]
final2=[]
PlatX = np.array(PlatformPosition)[:,0][:, np.newaxis]
PlatX_next = PlatX[2:,:]
# select some features to make x
Ballarraylast = np.array(Ballposition[0:-1]) 
Ballarray = np.array(Ballposition[1:]) 
for i in range(0, len(Ballarray)):
    if Ballarraylast[i][0]<=Ballarray[i][0] and Ballarraylast[i][1]<=Ballarray[i][1]:
        flag.append(1)
    elif Ballarraylast[i][0]<=Ballarray[i][0] and Ballarraylast[i][1]>=Ballarray[i][1]:
        flag.append(2)
    elif Ballarraylast[i][0]>=Ballarray[i][0] and Ballarraylast[i][1]>=Ballarray[i][1]:
        flag.append(3)
    elif Ballarraylast[i][0]>=Ballarray[i][0] and Ballarraylast[i][1]<=Ballarray[i][1]:
        flag.append(4)
        
    speed = Ballspeed[i]
    xx = Ballarray[i][0]
    yy = Ballarray[i][1]
    if flag[i]==2 or flag[i]==3: 
        while yy > 80:
            if xx==0:
                if yy-80<=195:
                    xx = (yy-80)//speed*speed
                    yy = yy-(yy-80)//speed*speed
                    xx = (xx+speed) if (yy>80) else xx
                    yy = 80
                else:
                    xx = 195//speed*speed
                    yy = yy-195//speed*speed
                    yy = (yy-speed) if (xx<195) else yy
                    xx = 195
            elif xx==195:
                if 195-(yy-80)>=0:
                    xx = 195-(yy-80)//speed*speed
                    yy = yy-(yy-80)//speed*speed
                    xx = (xx-speed) if (yy>80) else xx
                    yy = 80
                else: 
                    xx = 195-195//speed*speed
                    yy = yy-195//speed*speed
                    yy = (yy-speed) if (xx>0) else yy
                    xx = 0
            elif flag[i] == 2:
                if xx+(yy-80)<=195:
                    xx = xx+(yy-80)//speed*speed
                    yy = yy-(yy-80)//speed*speed
                    xx = (xx+speed) if (yy>80) else xx
                    yy = 80
                else: 
                    yy = yy-(195-xx)//speed*speed
                    xx = xx+(195-xx)//speed*speed
                    yy = (yy-speed) if (xx<195) else yy
                    xx = 195
            elif flag[i] == 3:
                if yy-80<=xx:
                    xx = xx-(yy-80)//speed*speed
                    yy = yy-(yy-80)//speed*speed
                    xx = (xx-speed) if (yy>80) else xx
                    yy = 80
                else:
                    yy = yy-xx//speed*speed
                    xx = xx-xx//speed*speed
                    yy = (yy-speed) if (xx>0) else yy
                    xx = 0
        #xx = xx-(xx%5);
    final.append(xx)
    xx = Ballarray[i][0]
    yy = Ballarray[i][1]
    if flag[i]==1 or flag[i]==4: 
        while yy < 415:
            if xx==0:
                if 415-yy<=195:
                    xx = ((415-yy)//speed)*speed
                    yy = yy+((415-yy)//speed)*speed
                    xx = (xx+speed) if (yy<415) else xx
                    yy = 415
                else:
                    xx = 195//speed*speed
                    yy = yy+195//speed*speed
                    yy = (yy+speed) if (xx<195) else yy
                    xx = 195
            elif xx==195:
                if 415-yy<=195:
                    xx = 195-(415-yy)//speed*speed
                    yy = yy+(415-yy)//speed*speed
                    xx = (xx-speed) if (yy<415) else xx
                    yy = 415
                else: 
                    yy = yy+xx//speed*speed
                    xx = 195-xx//speed*speed
                    yy = (yy+speed) if (xx>0) else yy
                    xx = 0
            elif flag[i] == 1:
                if xx+415-yy<=195:
                    xx = xx+(415-yy)//speed*speed
                    yy = yy+(415-yy)//speed*speed
                    xx = (xx+speed) if (yy<415) else xx
                    yy = 415
                else: 
                    yy = yy+(195-xx)//speed*speed
                    xx = xx+(195-xx)//speed*speed
                    yy = (yy+speed) if (xx<195) else yy
                    xx = 195
            elif flag[i] == 4:
                if xx-(415-yy)>=0:
                    xx = xx-(415-yy)//speed*speed
                    yy = yy+(415-yy)//speed*speed
                    xx = (xx-speed) if (yy<415) else xx
                    yy = 415
                else:
                    yy = yy+xx//speed*speed
                    xx = xx-xx//speed*speed
                    yy = (yy+speed) if (xx>0) else yy
                    xx = 0
        #xx = xx-(xx%5);
    final2.append(xx)
final = np.array(final)[:][:, np.newaxis]
final2 = np.array(final2)[:][:, np.newaxis]
flag = np.array(flag)[:][:, np.newaxis]
Ballspeed = np.array(Ballspeed)[1:][:, np.newaxis]
x = np.hstack((Ballarraylast, Ballarray, flag, Ballspeed))
# select intructions as y
y = np.hstack((final, final2))

#%% train your model herefrom sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import numpy as np
x_train, x_test, y_train, y_test = train_test_split(x, y, random_state = 3)
model = RandomForestRegressor(n_estimators=10, random_state=41)
model.fit(x_train,y_train)
yt = model.predict(x_test)
# check the acc to see how well you've trained the model
#plot_decision_regions(x_train, y_train, classifier=model)

import pickle
filename = "model.sav"
pickle.dump(model, open(filename, 'wb'))

