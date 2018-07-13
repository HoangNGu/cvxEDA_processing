import cvxEDA
from numpy import array
from matplotlib import pyplot as pl
import pylab as pla
import EDA_myAPI as eda

#Reading csv file
csvfile = []
workingdir = r"D:\ESISAR\Okayama_University\eSense_files\Experience_2_StoryAndQuestion"
csvfile.append(workingdir+"\eSense Skin Response data from 21 February 2018 14-20-44 10Hz.csv")
csvfile.append(workingdir+"\eSense Skin Response data from 26 February 2018 13-18-26 10Hz.csv")
numberOfDataSet= len(csvfile)

#Reading txt file containing length
durationVideo = []
file = open(workingdir+r"\totduration.txt", "r") 
for line in file: 
    line = line[:-2] # We suppress \n at the end of line
    durationVideo.append(float(line))
file.close()



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

ya[0] = ya[0][1731:90030]
ya[1] = ya[1][331:90030] 

# =============================================================================
# ############# FILTER #################################################################
# =============================================================================
###median filter
##WindowSize = 801
##yafilt = eda.medianFilter(ya,WindowSize)
##ya2filt = eda.medianFilter(ya2,WindowSize)


yafilt = ya  # no filter needed according to cvxEDA paper



# =============================================================================
# ############# N0RMALIZATION ##########################################################
# =============================================================================
#zscore normalization
##yn = (yafilt - yafilt.mean()) / yafilt.std()
for i in range(0,numberOfDataSet): #(!) in Python, range(0,3) = 0,1,2
   yn.append(eda.zscoreNormalisation(yafilt[i]))
###Min-max normalization
yntemp = yn
yn =[]
for i in range(0,numberOfDataSet):
   yn.append(eda.minmaxNormalisation(yntemp[i]))

# =============================================================================
# ############# USING CVXEDA LIBRARY ###################################################
# =============================================================================
r,p,t,l,d,e,obj = [[] for i in range(numberOfDataSet)], [[] for i in range(numberOfDataSet)], [[] for i in range(numberOfDataSet)], [[] for i in range(numberOfDataSet)], [[] for i in range(numberOfDataSet)], [[] for i in range(numberOfDataSet)], [[] for i in range(numberOfDataSet)], 
for i in range(0,numberOfDataSet):
   [r[i], p[i], t[i], l[i], d[i], e[i], obj[i]] = cvxEDA.cvxEDA(yn[i], delta)

#create x values for ploting
tm = []
for i in range(0, numberOfDataSet):
   tm.append(eda.create_XAxis(yafilt[i],delta))

# Four subplots, the axes array is 1-d
f1, axarr = pl.subplots(4, sharex=True)

for j in range(0,numberOfDataSet):
   axarr[0].plot(tm[j],yn[j])
for j in range(0,numberOfDataSet):
   axarr[1].plot(tm[j],t[j])
for j in range(0,numberOfDataSet):
   axarr[2].plot(tm[j],r[j])  
for j in range(0,numberOfDataSet):
    axarr[3].plot(tm[j],p[j])

x=0
y=0
for j in range(0,len(durationVideo)):
    x = y + durationVideo[j]
    axarr[0].axvline(x)
    axarr[1].axvline(x)
    axarr[2].axvline(x)
    axarr[3].axvline(x)
    y = x + 17.
    axarr[0].axvline(y)
    axarr[1].axvline(y)
    axarr[2].axvline(y)
    axarr[3].axvline(y)
    
axarr[0].set_title('Original data')
axarr[1].set_title('Tonic component')
axarr[2].set_title('Phasic component')
axarr[3].set_title('Sparse SMNA driver of phasic component')



# =============================================================================
# ############# WINDOW SIZING###########################################################
# =============================================================================
phasicSubset_List = [array([]) for i in range(numberOfDataSet)]
phasicSubset_Story_List = [array([]) for i in range(numberOfDataSet)]
phasicSubset_QuestionAndStory_List = [array([]) for i in range(numberOfDataSet)]


for i in range(0,numberOfDataSet):
    phasicSubset_List[i], phasicSubset_Story_List[i], phasicSubset_QuestionAndStory_List[i] = eda.WindowSizing_DifferentStep(durationVideo,p[i])



# =============================================================================
# ############# FEATURES EXTRACTION #####################################################################################
# =============================================================================
# =============================================================================
# The following list are use to stock features of the question part
# =============================================================================
phasicSubset_List = array( phasicSubset_List)
phasicMeanList = [array([]) for i in range(numberOfDataSet)]
phasicSTDList = [array([]) for i in range(numberOfDataSet)]
phasicMaxList = [array([]) for i in range(numberOfDataSet)]
phasicNBpeakList = [array([]) for i in range(numberOfDataSet)]
phasicPeakAmplitude = [array([]) for i in range(numberOfDataSet)]
phasicLatency = [array([]) for i in range(numberOfDataSet)]

# =============================================================================
# The following list are use to stock features of the story part
# =============================================================================
phasicSubset_Story_List = array(phasicSubset_Story_List)
phasicMeanList_Story_List = [array([]) for i in range(numberOfDataSet)]
phasicSTDList_Story_List = [array([]) for i in range(numberOfDataSet)]
phasicMaxList_Story_List = [array([]) for i in range(numberOfDataSet)]
phasicNBpeakList_Story_List = [array([]) for i in range(numberOfDataSet)]
phasicPeakAmplitude_Story_List = [array([]) for i in range(numberOfDataSet)]
phasicLatency_Story_List = [array([]) for i in range(numberOfDataSet)]

# =============================================================================
# The following list are use to stock features of the story + question parts
# =============================================================================
phasicSubset_QuestionAndStory_List = array(phasicSubset_QuestionAndStory_List)
phasicMeanList_QuestionAndStory_List = [array([]) for i in range(numberOfDataSet)]
phasicSTDList_QuestionAndStory_List = [array([]) for i in range(numberOfDataSet)]
phasicMaxList_QuestionAndStory_List = [array([]) for i in range(numberOfDataSet)]
phasicNBpeakList_QuestionAndStory_List = [array([]) for i in range(numberOfDataSet)]
phasicPeakAmplitude_QuestionAndStory_List = [array([]) for i in range(numberOfDataSet)]
phasicLatency_QuestionAndStory_List = [array([]) for i in range(numberOfDataSet)]

for i in range(0, numberOfDataSet):
   #### features extraction 
   [phasicMeanList[i], phasicSTDList[i], phasicMaxList[i], phasicNBpeakList[i], phasicPeakAmplitude[i], phasicLatency[i]]= eda.featuresExtraction(array(phasicSubset_List[i]),threshold)
   [phasicMeanList_Story_List[i], phasicSTDList_Story_List[i], phasicMaxList_Story_List[i], phasicNBpeakList_Story_List[i], phasicPeakAmplitude_Story_List[i], phasicLatency_Story_List[i]]= eda.featuresExtraction(array(phasicSubset_Story_List[i]),threshold)
   [phasicMeanList_QuestionAndStory_List[i], phasicSTDList_QuestionAndStory_List[i], phasicMaxList_QuestionAndStory_List[i], phasicNBpeakList_QuestionAndStory_List[i], phasicPeakAmplitude_QuestionAndStory_List[i], phasicLatency_QuestionAndStory_List[i]]= eda.featuresExtraction(array(phasicSubset_QuestionAndStory_List[i]),threshold)
# =============================================================================
# ############# Plot results ############################################################################################################
# =============================================================================
# ############# frequency of peaks in window ###############################################################################################
# =============================================================================

frequencyofPeak_Story = [array([]) for i in range(numberOfDataSet)]
for i in range(numberOfDataSet):
    frequencyofPeak_Story[i] = eda.frequencyOfPeaks(phasicSubset_Story_List[i],60,threshold)



tmphasicAmplitude,tmfrequencyPeaks,tmPeaks,tmPeaksWholeData, tmphasicLatency= [], [], [], [],[]
for i in range(0,numberOfDataSet):
   #Create the xAxis fo peaks number
   tmPeaks.append(pla.arange(1., len(phasicNBpeakList[i])+1.))
   tmfrequencyPeaks.append(pla.arange(1., len(frequencyofPeak_Story[i])+1.))
   tmPeaksWholeData.append(pla.arange(1., len(phasicNBpeakList_QuestionAndStory_List[i])+1.))
   #Create the xAxis for the phasic Latency
   tmphasicLatency.append(pla.arange(1., len(phasicLatency[i])+1.))

#### QuestionPart
f2, axarr = pl.subplots(3, sharex=True)  #plot nb of peak when using question part
for i in range(0,numberOfDataSet):
   axarr[i].bar(tmPeaks[i],phasicNBpeakList[i])
   axarr[i].set_title('NBpeaks per stimuli_dataset'+str(i+1)+'question part')
   
#### Storypart
f3, axarr = pl.subplots(3, sharex=True)  #plot nb of peak when using question part
for i in range(0,numberOfDataSet):
   axarr[i].bar(tmfrequencyPeaks[i],frequencyofPeak_Story[i])
   axarr[i].set_title('frequency NBpeaks/min per stimuli_dataset'+str(i+1)+'story part')
   
   
# =============================================================================
# ############## LATENCY: plot of all first peak latency in the window size
# =============================================================================
#question part
f4, axarr = pl.subplots(3, sharex = True)
for i in range(0,numberOfDataSet):
   axarr[i].bar(tmphasicLatency[i],phasicLatency[i])
   axarr[i].set_title('Latency_dataset'+str(i+1)+'question part')

f5, axarr = pl.subplots(3, sharex = True)
for i in range(0,numberOfDataSet):
   axarr[i].bar(tmphasicLatency[i],phasicLatency_Story_List[i])
   axarr[i].set_title('Latency_dataset'+str(i+1)+'story part')
   
   #### Story + question parts
f6, axarr = pl.subplots(3, sharex=True)  #plot nb of peak when using question part
for i in range(0,numberOfDataSet):
   axarr[i].bar(tmPeaksWholeData[i],phasicLatency_QuestionAndStory_List[i])
   axarr[i].set_title('Latency_dataset'+str(i+1)+'story + question parts')
# =============================================================================
# ############### MEAN LATENCY for a windowSizeLatency img window size ########################################
# =============================================================================
#SEPARATE THE LIST IN SECTION TO CALCULATE MEAN, STD,... OF FEATURES IN EVERY CHUNKS OF DATA AT THE BEGINING, MIDDLE, END, ... of EXP
windowSizeLatency =  1#Number of images used to compute the mean of every first peak latency 

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


f7, axarr = pl.subplots(3, sharex = True)
for i in range(0,numberOfDataSet):
   axarr[i].bar(tmphasicLatencymean[i],chunkLatency1mean[i])
   axarr[i].set_title('Latency_mean_dataset'+str(i+1)+'_'+str(windowSizeLatency)+'question part')


# =============================================================================
# ############## AMPLITUDE: plot of all first peak amplitude in the window size
# =============================================================================

# =============================================================================
# #8sWindows
# amplitudeMean = [[] for i in range(numberOfDataSet)]
# for i in range(0,numberOfDataSet):
#     for j in range(len(phasicPeakAmplitude)):
#         amplitudeMean[i].append(array(phasicPeakAmplitude[j]).mean())
#        #Create the xAxis for the phasic Amplitude
#     tmphasicAmplitude.append(pla.arange(1., len(amplitudeMean[i])+1.))
#     
# f5, axarr = pl.subplots(3, sharex = True)
# for i in range(0,numberOfDataSet):
#    axarr[i].bar(tmphasicAmplitude[i],amplitudeMean[i])
#    axarr[i].set_title('Amplitude_dataset_'+str(i+1)+'_8secWin')
# =============================================================================
