import csv
import pylab as pla
from numpy import array
from PeakDetect import peakdet

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # #  GLOBAL FUNCTIONS # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#### Global variable ####
global numberOfDataSet

#### Range for loop ####

def my_range(start, end, step):
    while start <= end:
        yield start
        start += step

#### Open directory ####

def OpenCsvFile (csvfile, x, y):
   f=open(csvfile,'r') # opens file for reading
   reader = csv.reader(f, delimiter=';')
   for i in range(1,11):
      next(reader)
   for row in reader:
      x.append(float(row[0]))
      y.append(float(row[1]))

#### Create x axis for a list ####

def create_XAxis(y,delta):
   tm = pla.arange(1.,len(y)+1.) * delta
   return(tm)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # FILTERING # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def medianFilter (y,Windowsize):
   ya= signal.medfilt(y, Windowsize)
   return(ya)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # NORMALIZATION # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

#### Z-score normalisation ####

def zscoreNormalisation(y):
   yn = (y-y.mean())/ y.std()
   return(yn)

#### Min-max normalization ####

def minmaxNormalisation(y):
   yn = (y-y.min())/(y.max() - y.min())
   return(yn)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # WINDOW SIZING # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def WindowSizing(start,stop,step, ListToCut):
## this function create a sliding window startint at t0, of size step and going from start to step,
## incrementing of step each time  
   ListPhaseIter = []
   ListOut = []
   for i in my_range(start,stop-step,step): #begining of each stimulus, whole length, we start after 10 secs countdown
      for j in range(i,i+step): #time window of 8s after each stimulus
         ListPhaseIter.append(float(ListToCut[j]))
      ListOut.append(ListPhaseIter)
      ListPhaseIter = []
   return(ListOut)

def WindowSizing_ImagNumber(start,stop,ImgNumber, ListToCut):
   step = ImgNumber*8*10 #Each stimulus is 8seconds long * 10 to get number of points
   ListPhaseIter = []
   ListOut = []
   for i in my_range(start-1,stop-step,step): #begining of each stimulus, whole length, we start after 10 secs countdown
      for j in my_range(i,i+step,1): #time window of 8s after each stimulus
         ListPhaseIter.append(float(ListToCut[j]))
      ListOut.append(ListPhaseIter)
      ListPhaseIter = []
   return(ListOut)

def WindowSizing_WinStartStop(start,stop,step,WinStart,WinStop, ListToCut):
   ListPhaseIter = []
   ListOut = []
   WinStart = 10*WinStart #seconds to number of points
   WinStop = 10*WinStop
   WinSize = WinStop - WinStart
   for i in my_range(start-1,stop-step,step): #begining of each stimulus, whole length, we start after 10 secs countdown
      for j in my_range(i+WinStart,i+WinSize,1): #time window of 8s after each stimulus
         ListPhaseIter.append(float(ListToCut[j]))
      ListOut.append(ListPhaseIter)
      ListPhaseIter = []
   return(ListOut)

def WindowSizing_DifferentStep(ListStep, ListToCut):
    x = 0
    y = 0
    ListAppend = [] #contains only question phase
    ListAppendStory = [] #contains only story phase
    ListAppendWholeList = [] #contains both story and question phase
    for i in range(0,len(ListStep)):
        x = y + ListStep[i]
        ListAppendStory.append(ListToCut[int(y):int(x)])
        ListAppendWholeList.append(ListToCut[int(y):int(x)])
        y = x + 17.
        ListAppend.append(ListToCut[int(x):int(y)])
        ListAppendWholeList.append(ListToCut[int(x):int(y)])
    return ListAppend, ListAppendStory, ListAppendWholeList
    
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # FEATURES EXTRACTION # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def featuresExtraction(List,threshold):
    '''This function return the following features from List:Mean,Standard Deviation(STD), the Maximimum of amplitude of the peaks, The number of peaks, The amplitude of the peaks, the Latency of the first peak'''
    mean = []
    STD = []
    MAX = []
    PeakNb = []
    PeakAmplitude = []
    FirstPeakAmplitude = []
    Latency = []
    for k in range(0, len(List)):
        Once = False
        maxtab = []
        mintab = []
        mean.append(List[k].mean())
        STD.append(List[k].std())
        MAX.append(List[k].max())
        Latency.append(float((onsetDetection(List[k],threshold)[0])/10))
        maxtab,mintab = peakdet(List[k],threshold) #Consider a peak if onset of at least 0.01
        PeakNb.append(len(maxtab)) #len(maxtab) is equal to the number of peaks 
        if not maxtab.all():
            PeakAmplitude.append(0.)
            if not Once:     
                    FirstPeakAmplitude.append(0.)
                    Once=True                    
        else:
            for j in range(0,len(maxtab)):
                PeakAmplitude.append(maxtab[j][1]) #Stock the peak amplitude value
                if not Once:
                    FirstPeakAmplitude.append(maxtab[0][1])   
                    Once = True
            
    return mean,STD,MAX,PeakNb,PeakAmplitude,Latency #,FirstPeakAmplitude
      
def frequencyOfPeaks(List,time, threshold):
    '''time is in seconds'''
    ListFrequency= []
    PeakNb = []
    for k in range(0,len(List)):
        maxtab,mintab = peakdet(List[k],threshold) #Consider a peak if onset of at least 0.01
        PeakNb.append(len(maxtab))
    for i in range(0,len(List)):
        ListFrequency.append(float((time*PeakNb[i])/(len(List[i]*10))))
    return ListFrequency

def onsetDetection(List, threshold):
    global xOnset
    global yOnset
    i = 0
    '''return the onset (higher than the threshold) of the first peak in the list'''
    while(List[i]<threshold and i<len(List)-1):
        i = i+1
    if(i == len(List)-1 and List[i]<threshold): #no peak detected
        xOnset = 0
        yOnset = 0
    else:
        xOnset = float(i)
        yOnset = float(List[i])
    
    return float(xOnset),float(yOnset)





















   
   
