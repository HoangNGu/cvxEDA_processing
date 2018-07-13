import cvxEDA
from numpy import array
from matplotlib import pyplot as pl
import pylab as pla
import EDA_myAPI as eda

csvfile = []
workingdir = "D:\ESISAR\Okayama_University\eSense_files\Experience_1_Diapo"
csvfile.append(workingdir+"\eSense Skin Response data from 08 February 2018 13_14_19 10Hz.csv")
csvfile.append(workingdir+"\eSense Skin Response data from 15 February 2018 09-32-54 10Hz.csv")
csvfile.append(workingdir+"\eSense Skin Response data from 20 February 2018 09_36_15 10Hz.csv")

numberOfDataSet= len(csvfile)
delta = 0.1 # delta = 1/Fs
threshold = 0.01 #threshold to define a SCR. If the amplitude of a peak is at least 0.01 it is identified as a SCR

x = [[] for i in range(numberOfDataSet)]
y = [[] for i in range(numberOfDataSet)]
ya = []
yn = []
yntemp=[]



for i in range(0,numberOfDataSet):
   eda.OpenCsvFile(csvfile[i],x[i],y[i])
   ya.append(array(y[i]))


ya[0] = ya[0][1150:81500] #include the 10 sec countdown. 
ya[1] = ya[1][900:81250]  
ya[2] = ya[2][781:48781] 



############# FILTER #################################################################
###median filter
##WindowSize = 801
##yafilt = eda.medianFilter(ya,WindowSize)
##ya2filt = eda.medianFilter(ya2,WindowSize)


yafilt = ya  # no filter needed according to cvxEDA paper



############# N0RMALIZATION ##########################################################
#zscore normalization
##yn = (yafilt - yafilt.mean()) / yafilt.std()
for i in range(0,numberOfDataSet): #(!) in Python, range(0,3) = 0,1,2
   yn.append(eda.zscoreNormalisation(yafilt[i]))
###Min-max normalization
yntemp = yn
yn =[]
for i in range(0,numberOfDataSet):
   yn.append(eda.minmaxNormalisation(yntemp[i]))

############# USING CVXEDA LIBRARY ###################################################
r,p,t,l,d,e,obj = [[] for i in range(numberOfDataSet)], [[] for i in range(numberOfDataSet)], [[] for i in range(numberOfDataSet)], [[] for i in range(numberOfDataSet)], [[] for i in range(numberOfDataSet)], [[] for i in range(numberOfDataSet)], [[] for i in range(numberOfDataSet)], 
for i in range(0,numberOfDataSet):
   [r[i], p[i], t[i], l[i], d[i], e[i], obj[i]] = cvxEDA.cvxEDA(yn[i], delta)

#create x values for ploting
tm = []
for i in range(0, numberOfDataSet):
   tm.append(eda.create_XAxis(yafilt[i],delta))

# Four subplots, the axes array is 1-d
f, axarr = pl.subplots(4, sharex=True)

for j in range(0,numberOfDataSet):
   axarr[0].plot(tm[j],yn[j])
for j in range(0,numberOfDataSet):
   axarr[1].plot(tm[j],t[j])
for j in range(0,numberOfDataSet):
   axarr[2].plot(tm[j],r[j])  
##for j in range(0,numberOfDataSet):
axarr[3].plot(tm[0],p[0])
      
axarr[0].set_title('Original data')
axarr[1].set_title('Tonic component')
axarr[2].set_title('Phasic component')
axarr[3].set_title('Sparse SMNA driver of phasic component')

############# WINDOW SIZING###########################################################
phasicList_8s = [array([]) for i in range(numberOfDataSet)] #This list is a list of list containing phasic component value in 8 sec time windows after each stimulus
phasicList_20imgs = [array([]) for i in range(numberOfDataSet)]  #This list is a list of list containing phasic component value in 160 time windows (20 images)
phasicList_WinSize = [array([]) for i in range(numberOfDataSet)]  #This list is a list of list containing phasic component value in 160 time windows (20 images)

nbImage = 20 #Change this variable to change the number of images in the window
WinStart = 3 #Use in WinSize, define the elapse time between stimulus and the start of the window
WinStop = 8 #Use in WinSize, define the elapse time between stimulus and the end of the window

for i in range(0,numberOfDataSet-1): #this will be change so the length is automaticaly detected.
   phasicList_8s[i] =(eda.WindowSizing(100,80350,80,p[i])) #begining of each stimulus, whole length, we start after 10 secs countdownand time window of 8s after each stimulus
   phasicList_20imgs[i]=(eda.WindowSizing_ImagNumber(100,80350,nbImage,p[i]))
   phasicList_WinSize[i]=(eda.WindowSizing_WinStartStop(100,80350,80,WinStart,WinStop,p[i]))

phasicList_8s[2]=(eda.WindowSizing(100,48000,80,p[2])) #begining of each stimulus, whole length, we start after 10 secs countdownand time window of 8s after each stimulus
phasicList_20imgs[2]=(eda.WindowSizing_ImagNumber(100,48000,nbImage,p[2]))
phasicList_WinSize[2]=(eda.WindowSizing_WinStartStop(100,48000,80,WinStart,WinStop,p[2]))
   
############# FEATURES EXTRACTION #####################################################################################
#### List use for the 8s windows lists
phasicList_8s = array( phasicList_8s)
phasicMeanList = [array([]) for i in range(numberOfDataSet)]
phasicSTDList = [array([]) for i in range(numberOfDataSet)]
phasicMaxList = [array([]) for i in range(numberOfDataSet)]
phasicNBpeakList = [array([]) for i in range(numberOfDataSet)]
phasicPeakAmplitude = [array([]) for i in range(numberOfDataSet)]
phasicLatency = [array([]) for i in range(numberOfDataSet)]
FirstPeakAmplitude = [array([]) for i in range(numberOfDataSet)]

#### List use for the 20imgs windows lists
phasicList_20imgs = array(phasicList_20imgs)
phasicNBpeakList_20imgs = [array([]) for i in range(numberOfDataSet)]
phasicPeakAmplitude_20imgs  = [array([]) for i in range(numberOfDataSet)]
phasicLatency_20imgs = [array([]) for i in range(numberOfDataSet)]
FirstPeakAmplitude_20imgs = [array([]) for i in range(numberOfDataSet)]
#### List use for the WinSize windows lists
phasicList_WinSize = array(phasicList_WinSize)
phasicNBpeakList_WinSize = [array([]) for i in range(numberOfDataSet)]
phasicPeakAmplitude_WinSize = [array([]) for i in range(numberOfDataSet)]
phasicLatency_WinSize = [array([]) for i in range(numberOfDataSet)]
FirstPeakAmplitude_WinSize = [array([]) for i in range(numberOfDataSet)]

for i in range(0, numberOfDataSet):
   #### features extraction for 8 seconds Window
   [phasicMeanList[i], phasicSTDList[i], phasicMaxList[i], phasicNBpeakList[i], phasicPeakAmplitude[i], phasicLatency[i]]= eda.featuresExtraction(array(phasicList_8s[i]),threshold)
   #### features extraction for 20 images Window
   [_,_,_, phasicNBpeakList_20imgs[i], phasicPeakAmplitude_20imgs[i], phasicLatency_20imgs[i]]= eda.featuresExtraction(array(phasicList_20imgs[i]),threshold)
   #### features extraction for WinSize window
   [_,_,_, phasicNBpeakList_WinSize[i], phasicPeakAmplitude_WinSize[i], phasicLatency_WinSize[i]]= eda.featuresExtraction(array(phasicList_WinSize[i]),threshold)
  
############# Plot results ############################################################################################################

############# Number of peaks in window ###############################################################################################

tmphasicAmplitude,tmphasicAmplitude_20imgs,tmphasicAmplitude_WinSize,tmPeaks, tmPeaks_20imgs, tmPeaks_WinSize, tmphasicLatency, tmphasicLatency_20imgs, tmphasicLatency_WinSize= [], [], [], [], [], [],[], [], []
for i in range(0,numberOfDataSet):
   #Create the xAxis fo peaks number
   tmPeaks.append(pla.arange(1., len(phasicNBpeakList[i])+1.))
   tmPeaks_20imgs.append(pla.arange(1., len(phasicNBpeakList_20imgs[i])+1.))
   tmPeaks_WinSize.append(pla.arange(1., len(phasicNBpeakList_WinSize[i])+1.))
   #Create the xAxis for the phasic Latency
   tmphasicLatency.append(pla.arange(1., len(phasicLatency[i])+1.))
   tmphasicLatency_20imgs.append(pla.arange(1., len(phasicLatency_20imgs[i])+1.))
   tmphasicLatency_WinSize.append(pla.arange(1., len(phasicLatency_WinSize[i])+1.))
   #Create the xAxis for the phasic Amplitude
   tmphasicAmplitude.append(pla.arange(1., len(FirstPeakAmplitude[i])+1.))
   tmphasicAmplitude_20imgs.append(pla.arange(1., len(FirstPeakAmplitude_20imgs[i])+1.))
   tmphasicAmplitude_WinSize.append(pla.arange(1., len(FirstPeakAmplitude_WinSize[i])+1.))
   
#### 8s window 
f2, axarr = pl.subplots(3, sharex=True)  #plot nb of peak when using 8s window size
for i in range(0,numberOfDataSet):
   axarr[i].bar(tmPeaks[i],phasicNBpeakList[i])
   axarr[i].set_title('dataset'+str(i+1)+'_8s Window size_number of peak')  

#### _20imgs
f3, axarr = pl.subplots(3, sharex=True)  #plot nb of peak when using 20 imgs window size
for i in range(0,numberOfDataSet):
   axarr[i].bar(tmPeaks_20imgs[i],phasicNBpeakList_20imgs[i])
   axarr[i].set_title('dataset'+str(i+1)+'_'+str(nbImage)+'imgs_number of peak')

###### _WinSize
f4, axarr = pl.subplots(3, sharex=True)  #plot nb of peak when using WinSize window size
for i in range(0,numberOfDataSet):
   axarr[i].bar(tmPeaks_WinSize[i],phasicNBpeakList_WinSize[i])
   axarr[i].set_title('dataset'+str(i+1)+'_WinSize_number of peak')


############## LATENCY: plot of all first peak latency in the window size
#8sec Window
# create x values
f5, axarr = pl.subplots(3, sharex = True)
for i in range(0,numberOfDataSet):
   axarr[i].bar(tmphasicLatency[i],phasicLatency[i])
   axarr[i].set_title('Latency_dataset'+str(i+1)+'_8sWindow')


#20 images Window
f6, axarr = pl.subplots(3, sharex = True)
for i in range(0,numberOfDataSet):
   axarr[i].bar(tmphasicLatency_20imgs[i],phasicLatency_20imgs[i])
   axarr[i].set_title('Latency_dataset'+str(i+1)+'_'+str(nbImage)+' imgs Window')


#WinSize (!) the latency plot here is between the first SCR peaks and the start of the window (WinStart) and not
#the latency between the first peaks of the window and the stimulus
f7, axarr = pl.subplots(3, sharex = True)
for i in range(0,numberOfDataSet):
   axarr[i].bar(tmphasicLatency_WinSize[i],phasicLatency_WinSize[i])
   axarr[i].set_title('Latency_dataset'+str(i+1)+'_WinSize')

############### MEAN LATENCY for a windowSizeLatency img window size ########################################
#SEPARATE THE LIST IN SECTION TO CALCULATE MEAN, STD,... OF FEATURES IN EVERY CHUNKS OF DATA AT THE BEGINING, MIDDLE, END, ... of EXP
windowSizeLatency =  20#Number of images used to compute the mean of every first peak latency 

chunkLatency = [[] for i in range(numberOfDataSet)]
for k in range(0,numberOfDataSet):
   chunkLatency[k] = [phasicLatency[k][i:i+windowSizeLatency] for i in range(0, len(phasicLatency[k]), windowSizeLatency)] #We cut the original data into chunk of 50 images

chunkLatency1mean = [[] for i in range(numberOfDataSet)]

for j in range(0,numberOfDataSet):
   for i in range(0,len(chunkLatency[j])-1) :
      chunkLatency1mean[j].append(array(chunkLatency[j][i]).mean()) #We add to chunkLatency1mean the average latency of the first peak of each 50 images chunks. For example, chunkLatencymean[0]
                                                                     # contains the average latency of the first peaks of the first 50 images.


tmphasicLatencymean = []
for i in range(0,numberOfDataSet):
   tmphasicLatencymean.append(pla.arange(1., len(chunkLatency1mean[i])+1.))


f8, axarr = pl.subplots(3, sharex = True)
for i in range(0,numberOfDataSet):
   axarr[i].bar(tmphasicLatencymean[i],chunkLatency1mean[i])
   axarr[i].set_title('Latency_mean_dataset'+str(i+1)+'_'+str(windowSizeLatency)+'img Window')


############## AMPLITUDE: plot of all first peak amplitude in the window size

#8sWindows
# =============================================================================
# f9, axarr = pl.subplots(3, sharex = True)
# for i in range(0,numberOfDataSet):
#    axarr[i].bar(tmphasicAmplitude[i],FirstPeakAmplitude[i])
#    axarr[i].set_title('Amplitude_dataset_'+str(i+1)+'_8secWin')
# #20images Windows
# f10, axarr = pl.subplots(3, sharex = True)
# for i in range(0,numberOfDataSet):
#    axarr[i].bar(tmphasicAmplitude_20imgs[i],FirstPeakAmplitude_20imgs[i])
#    axarr[i].set_title('Amplitude_dataset_'+str(i+1)+'_'+str(nbImage)+'window')
# #Winsize Window
# f11, axarr = pl.subplots(3, sharex = True)
# for i in range(0,numberOfDataSet):
#    axarr[i].bar(tmphasicAmplitude_WinSize[i],FirstPeakAmplitude_WinSize[i])
#    axarr[i].set_title('Amplitude_dataset_'+str(i+1)+'WinSize')
# pl.show()
# =============================================================================





