from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import matplotlib.pyplot as plt
import pylab as py

import EDA_myAPI_ML as eda

directory = "D:\ESISAR\Okayama_University\Python"
directorySource = "D:\ESISAR\Okayama_University\Python\Image_Dataset\oasis\images"
directoryGAPEDpicture = r"D:\ESISAR\Okayama_University\Python\Image_Dataset\GAPED_2\GAPED\GAPED\\"
directoryEmoMadridPicture = r"D:\ESISAR\Okayama_University\Python\Image_Dataset\EmoMadrid"

directoryReceptArousalGaped = "D:\ESISAR\Okayama_University\Python\ArousalGapedTrainingSet"
directoryReceptArousalEmoMadrid = "D:\ESISAR\Okayama_University\Python\ArousalEmoMadridTrainingSet"
directoryReceptArousalOasis = "D:\ESISAR\Okayama_University\Python\ArousalOasisTrainingSet"

directoryReceptValenceGaped = "D:\ESISAR\Okayama_University\Python\ValenceGapedTrainingSet"
directoryReceptValenceEmoMadrid = "D:\ESISAR\Okayama_University\Python\ValenceEmoMadridTrainingSet"
directoryReceptValenceOasis = "D:\ESISAR\Okayama_University\Python\ValenceOasisTrainingSet"

#Read labels
train_path = "D:\ESISAR\Okayama_University\Python\Image_Dataset\oasis\OASIS.csv"
train_path_Gaped = [directoryGAPEDpicture+"A.csv",directoryGAPEDpicture+"H.csv",directoryGAPEDpicture+"N.csv",
                    directoryGAPEDpicture+"P.csv",directoryGAPEDpicture+"Sn.csv",directoryGAPEDpicture+"Sp.csv"]
train_path_Emomadrid = [directoryEmoMadridPicture+"\image_names.txt",directoryEmoMadridPicture+"\MeanValence.txt",\
                        directoryEmoMadridPicture+"\MeanArousal.txt"]

Name,Valence_mean_train,Valence_SD_train,Valence_N_train,Arousal_mean_train,_trainArousal_SD_train,Arousal_N_train = [],[],[],[],[],[],[]
Name,Valence_mean_train,Valence_SD_train,Valence_N_train,Arousal_mean_train,_trainArousal_SD_train,Arousal_N_train = eda.OpenCsvFile(train_path)
Name_Gaped,Valence_mean_Gaped,Arousal_mean_Gaped, Name_EmoMadrid, Valence_mean_EmoMadrid, Arousal_mean_EmoMadrid =[],[],[],[],[],[]

Name_EmoMadrid = eda.readTxtFile(train_path_Emomadrid[0],False)
Valence_mean_EmoMadrid = eda.readTxtFile(train_path_Emomadrid[1],True)
Arousal_mean_EmoMadrid = eda.readTxtFile(train_path_Emomadrid[2],True)

for i in range(len(train_path_Gaped)):
    Name_Gapedtmp,Valence_mean_Gapedtmp,Arousal_mean_Gapedtmp = [],[],[]
    Name_Gapedtmp,Valence_mean_Gapedtmp,Arousal_mean_Gapedtmp = eda.OpenCsvFile_Gaped(train_path_Gaped[i])
    Name_Gaped.extend(Name_Gapedtmp)
    Valence_mean_Gaped.extend(Valence_mean_Gapedtmp)
    Arousal_mean_Gaped.extend(Valence_mean_Gapedtmp)

roundMeanArousal,roundMeanValence,roundMeanArousalEmoMadrid,roundMeanValenceEmoMadrid = [],[],[],[]

for i in range(len(Valence_mean_EmoMadrid)):
    roundMeanValenceEmoMadrid.append(round(Valence_mean_EmoMadrid[i]))
for i in range(len(Arousal_mean_EmoMadrid)):
    roundMeanArousalEmoMadrid.append(round(Arousal_mean_EmoMadrid[i]))
for i in range(len(Arousal_mean_train)):
    roundMeanArousal.append(round(Arousal_mean_train[i]))
for i in range(len(Valence_mean_train)):
    roundMeanValence.append(round(Valence_mean_train[i]))
#classifying using 7-point scales
# =============================================================================
# 1 Very low,2 Moderately low,3 Somewhat low,4 Neither low nor
# high,5 Somewhat high,6 Moderately high, and 7 Very high.
ListLevel = [r"\Moderately_Low",r"\Somewhat_low",r"\Neither_Low_nor_High",r"\Somewhat_High",r"\Moderately_High"]

# =============================================================================
fichier = open("batch_imageClassification_Arousal.bat","w+") #batch file that will be use to class the photo
fichierValence = open("batch_imageClassification_Valence.bat","w+") #batch file that will be use to class the photo


#Arousal

#OASIS
# =============================================================================
# for i in range(len(roundMeanArousal)):
# 
#     if(roundMeanArousal[i]==1 or roundMeanArousal[i]==2): #Moderately Low or very low
#         fichier.write("if not exist \""+directoryReceptArousalOasis+ListLevel[0]+"\\"+Name[i]+".jpg\" xcopy /s \""
#                       +directorySource+"\\"+Name[i]+".jpg\" \"" +directoryReceptArousalOasis+ListLevel[0]+"\\"+Name[i]+".jpg*\"\n")
#     elif(roundMeanArousal[i]==3): #Moderately Low
#         fichier.write("if not exist \""+directoryReceptArousalOasis+ListLevel[1]+"\\"+Name[i]+".jpg\" xcopy /s \""
#                       +directorySource+"\\"+Name[i]+".jpg\" \"" +directoryReceptArousalOasis+ListLevel[1]+"\\"+Name[i]+".jpg*\"\n")
#     elif(roundMeanArousal[i]==4): #Moderately Low
#         fichier.write("if not exist \""+directoryReceptArousalOasis+ListLevel[2]+"\\"+Name[i]+".jpg\" xcopy /s \""
#                       +directorySource+"\\"+Name[i]+".jpg\" \"" +directoryReceptArousalOasis+ListLevel[2]+"\\"+Name[i]+".jpg*\"\n")
#     elif(roundMeanArousal[i]==5): #Moderately Low
#         fichier.write("if not exist \""+directoryReceptArousalOasis+ListLevel[3]+"\\"+Name[i]+".jpg\" xcopy /s \""
#                       +directorySource+"\\"+Name[i]+".jpg\" \"" +directoryReceptArousalOasis+ListLevel[3]+"\\"+Name[i]+".jpg*\"\n")
#     elif(roundMeanArousal[i]==6 or roundMeanArousal[i]==7): #Moderately high or very high
#         fichier.write("if not exist \""+directoryReceptArousalOasis+ListLevel[4]+"\\"+Name[i]+".jpg\" xcopy /s \""
#                       +directorySource+"\\"+Name[i]+".jpg\" \"" +directoryReceptArousalOasis+ListLevel[4]+"\\"+Name[i]+".jpg*\"\n")
# =============================================================================
#GAPED
# =============================================================================
# for i in range(len(Arousal_mean_Gaped)):
#     if round(Arousal_mean_Gaped[i]) in range(0,20):
#         fichier.write("if not exist \""+directoryReceptArousalGaped+ListLevel[0]+"\\"+Name_Gaped[i]+".jpg\" xcopy /s \""
#                       +directoryGAPEDpicture+Name_Gaped[i][0]+"\\"+Name_Gaped[i]+".jpg\" \"" +directoryReceptArousalGaped+ListLevel[0]+"\\"+Name_Gaped[i]+".jpg*\"\n")
#     elif round(Arousal_mean_Gaped[i]) in range(20,40):
#         fichier.write("if not exist \""+directoryReceptArousalGaped+ListLevel[1]+"\\"+Name_Gaped[i]+".jpg\" xcopy /s \""
#                       +directoryGAPEDpicture+Name_Gaped[i][0]+"\\"+Name_Gaped[i]+".jpg\" \"" +directoryReceptArousalGaped+ListLevel[1]+"\\"+Name_Gaped[i]+".jpg*\"\n")
#     elif round(Arousal_mean_Gaped[i]) in range(40,60):
#         fichier.write("if not exist \""+directoryReceptArousalGaped+ListLevel[2]+"\\"+Name_Gaped[i]+".jpg\" xcopy /s \""
#                       +directoryGAPEDpicture+Name_Gaped[i][0]+"\\"+Name_Gaped[i]+".jpg\" \"" +directoryReceptArousalGaped+ListLevel[2]+"\\"+Name_Gaped[i]+".jpg*\"\n")
#     elif round(Arousal_mean_Gaped[i]) in range(60,80):
#         fichier.write("if not exist \""+directoryReceptArousalGaped+ListLevel[3]+"\\"+Name_Gaped[i]+".jpg\" xcopy /s \""
#                       +directoryGAPEDpicture+Name_Gaped[i][0]+"\\"+Name_Gaped[i]+".jpg\" \"" +directoryReceptArousalGaped+ListLevel[3]+"\\"+Name_Gaped[i]+".jpg*\"\n")
#     elif round(Arousal_mean_Gaped[i]) in range(80,100):
#         fichier.write("if not exist \""+directoryReceptArousalGaped+ListLevel[4]+"\\"+Name_Gaped[i]+".jpg\" xcopy /s \""
#                       +directoryGAPEDpicture+Name_Gaped[i][0]+"\\"+Name_Gaped[i]+".jpg\" \"" +directoryReceptArousalGaped+ListLevel[4]+"\\"+Name_Gaped[i]+".jpg*\"\n")
# 
# =============================================================================
#EmoMadrid
for i in range(len(roundMeanArousalEmoMadrid)):

    if(roundMeanArousalEmoMadrid==-2): #Moderately Low or very low
        fichier.write("if not exist \""+directoryReceptArousalEmoMadrid+ListLevel[0]+"\\"+Name_EmoMadrid[i]+".jpg\" xcopy /s \""
                      +directoryEmoMadridPicture+"\\"+Name_EmoMadrid[i]+".jpg\" \"" +directoryReceptArousalEmoMadrid+ListLevel[0]+"\\"+Name_EmoMadrid[i]+".jpg*\"\n")
    elif(roundMeanArousalEmoMadrid[i]==-1): #Moderately Low
        fichier.write("if not exist \""+directoryReceptArousalEmoMadrid+ListLevel[1]+"\\"+Name_EmoMadrid[i]+".jpg\" xcopy /s \""
                      +directoryEmoMadridPicture+"\\"+Name_EmoMadrid[i]+".jpg\" \"" +directoryReceptArousalEmoMadrid+ListLevel[1]+"\\"+Name_EmoMadrid[i]+".jpg*\"\n")
    elif(roundMeanArousalEmoMadrid[i]==0): #Moderately Low
        fichier.write("if not exist \""+directoryReceptArousalEmoMadrid+ListLevel[2]+"\\"+Name_EmoMadrid[i]+".jpg\" xcopy /s \""
                      +directoryEmoMadridPicture+"\\"+Name_EmoMadrid[i]+".jpg\" \"" +directoryReceptArousalEmoMadrid+ListLevel[2]+"\\"+Name_EmoMadrid[i]+".jpg*\"\n")
    elif(roundMeanArousalEmoMadrid[i]==1): #Moderately Low
        fichier.write("if not exist \""+directoryReceptArousalEmoMadrid+ListLevel[3]+"\\"+Name_EmoMadrid[i]+".jpg\" xcopy /s \""
                      +directoryEmoMadridPicture+"\\"+Name_EmoMadrid[i]+".jpg\" \"" +directoryReceptArousalEmoMadrid+ListLevel[3]+"\\"+Name_EmoMadrid[i]+".jpg*\"\n")
    elif(roundMeanArousalEmoMadrid[i]==2): #Moderately high or very high
        fichier.write("if not exist \""+directoryReceptArousalEmoMadrid+ListLevel[4]+"\\"+Name_EmoMadrid[i]+".jpg\" xcopy /s \""
                      +directoryEmoMadridPicture+"\\"+Name_EmoMadrid[i]+".jpg\" \"" +directoryReceptArousalEmoMadrid+ListLevel[4]+"\\"+Name_EmoMadrid[i]+".jpg*\"\n")

fichier.write("Pause \n")
fichier.close()



#Valence

#OASIS
# =============================================================================
# for i in range(len(roundMeanValence)):
# 
#     if(roundMeanValence[i]==1 or roundMeanValence[i]==2): #Moderately Low or very low
#         fichierValence.write("if not exist \""+directoryReceptValenceOasis+ListLevel[0]+"\\"+Name[i]+".jpg\" xcopy /s \""
#                       +directorySource+"\\"+Name[i]+".jpg\" \"" +directoryReceptValenceOasis+ListLevel[0]+"\\"+Name[i]+".jpg*\"\n")
#     elif(roundMeanValence[i]==3): #Moderately Low
#         fichierValence.write("if not exist \""+directoryReceptValenceOasis+ListLevel[1]+"\\"+Name[i]+".jpg\" xcopy /s \""
#                       +directorySource+"\\"+Name[i]+".jpg\" \"" +directoryReceptValenceOasis+ListLevel[1]+"\\"+Name[i]+".jpg*\"\n")
#     elif(roundMeanValence[i]==4): #Moderately Low
#         fichierValence.write("if not exist \""+directoryReceptValenceOasis+ListLevel[2]+"\\"+Name[i]+".jpg\" xcopy /s \""
#                       +directorySource+"\\"+Name[i]+".jpg\" \"" +directoryReceptValenceOasis+ListLevel[2]+"\\"+Name[i]+".jpg*\"\n")
#     elif(roundMeanValence[i]==5): #Moderately Low
#         fichierValence.write("if not exist \""+directoryReceptValenceOasis+ListLevel[3]+"\\"+Name[i]+".jpg\" xcopy /s \""
#                       +directorySource+"\\"+Name[i]+".jpg\" \"" +directoryReceptValenceOasis+ListLevel[3]+"\\"+Name[i]+".jpg*\"\n")
#     elif(roundMeanValence[i]==6 or roundMeanValence[i]==7): #Moderately high or very high
#         fichierValence.write("if not exist \""+directoryReceptValenceOasis+ListLevel[4]+"\\"+Name[i]+".jpg\" xcopy /s \""
#                       +directorySource+"\\"+Name[i]+".jpg\" \"" +directoryReceptValenceOasis+ListLevel[4]+"\\"+Name[i]+".jpg*\"\n")
# =============================================================================
#GAPED
# =============================================================================
# for i in range(len(Valence_mean_Gaped)):
#     if round(Valence_mean_Gaped[i]) in range(0,20):
#         fichierValence.write("if not exist \""+directoryReceptValenceGaped+ListLevel[0]+"\\"+Name_Gaped[i]+".jpg\" xcopy /s \""
#                       +directoryGAPEDpicture+Name_Gaped[i][0]+"\\"+Name_Gaped[i]+".jpg\" \"" +directoryReceptValenceGaped+ListLevel[0]+"\\"+Name_Gaped[i]+".jpg*\"\n")
#     elif round(Valence_mean_Gaped[i]) in range(20,40):
#         fichierValence.write("if not exist \""+directoryReceptValenceGaped+ListLevel[1]+"\\"+Name_Gaped[i]+".jpg\" xcopy /s \""
#                       +directoryGAPEDpicture+Name_Gaped[i][0]+"\\"+Name_Gaped[i]+".jpg\" \"" +directoryReceptValenceGaped+ListLevel[1]+"\\"+Name_Gaped[i]+".jpg*\"\n")
#     elif round(Valence_mean_Gaped[i]) in range(40,60):
#         fichierValence.write("if not exist \""+directoryReceptValenceGaped+ListLevel[2]+"\\"+Name_Gaped[i]+".jpg\" xcopy /s \""
#                       +directoryGAPEDpicture+Name_Gaped[i][0]+"\\"+Name_Gaped[i]+".jpg\" \"" +directoryReceptValenceGaped+ListLevel[2]+"\\"+Name_Gaped[i]+".jpg*\"\n")
#     elif round(Valence_mean_Gaped[i]) in range(60,80):
#         fichierValence.write("if not exist \""+directoryReceptValenceGaped+ListLevel[3]+"\\"+Name_Gaped[i]+".jpg\" xcopy /s \""
#                       +directoryGAPEDpicture+Name_Gaped[i][0]+"\\"+Name_Gaped[i]+".jpg\" \"" +directoryReceptValenceGaped+ListLevel[3]+"\\"+Name_Gaped[i]+".jpg*\"\n")
#     elif round(Valence_mean_Gaped[i]) in range(80,100):
#         fichierValence.write("if not exist \""+directoryReceptValenceGaped+ListLevel[4]+"\\"+Name_Gaped[i]+".jpg\" xcopy /s \""
#                       +directoryGAPEDpicture+Name_Gaped[i][0]+"\\"+Name_Gaped[i]+".jpg\" \"" +directoryReceptValenceGaped+ListLevel[4]+"\\"+Name_Gaped[i]+".jpg*\"\n")
#         
# =============================================================================
#EmoMadrid
for i in range(len(roundMeanValenceEmoMadrid)):

    if(roundMeanValenceEmoMadrid==-2): #Moderately Low or very low
        fichierValence.write("if not exist \""+directoryReceptValenceEmoMadrid+ListLevel[0]+"\\"+Name_EmoMadrid[i]+".jpg\" xcopy /s \""
                      +directoryEmoMadridPicture+"\\"+Name_EmoMadrid[i]+".jpg\" \"" +directoryReceptValenceEmoMadrid+ListLevel[0]+"\\"+Name_EmoMadrid[i]+".jpg*\"\n")
    elif(roundMeanValenceEmoMadrid[i]==-1): #Moderately Low
        fichierValence.write("if not exist \""+directoryReceptValenceEmoMadrid+ListLevel[1]+"\\"+Name_EmoMadrid[i]+".jpg\" xcopy /s \""
                      +directoryEmoMadridPicture+"\\"+Name_EmoMadrid[i]+".jpg\" \"" +directoryReceptValenceEmoMadrid+ListLevel[1]+"\\"+Name_EmoMadrid[i]+".jpg*\"\n")
    elif(roundMeanValenceEmoMadrid[i]==0): #Moderately Low
        fichierValence.write("if not exist \""+directoryReceptValenceEmoMadrid+ListLevel[2]+"\\"+Name_EmoMadrid[i]+".jpg\" xcopy /s \""
                      +directoryEmoMadridPicture+"\\"+Name_EmoMadrid[i]+".jpg\" \"" +directoryReceptValenceEmoMadrid+ListLevel[2]+"\\"+Name_EmoMadrid[i]+".jpg*\"\n")
    elif(roundMeanValenceEmoMadrid[i]==1): #Moderately Low
        fichierValence.write("if not exist \""+directoryReceptValenceEmoMadrid+ListLevel[3]+"\\"+Name_EmoMadrid[i]+".jpg\" xcopy /s \""
                      +directoryEmoMadridPicture+"\\"+Name_EmoMadrid[i]+".jpg\" \"" +directoryReceptValenceEmoMadrid+ListLevel[3]+"\\"+Name_EmoMadrid[i]+".jpg*\"\n")
    elif(roundMeanValenceEmoMadrid[i]==2): #Moderately high or very high
        fichierValence.write("if not exist \""+directoryReceptValenceEmoMadrid+ListLevel[4]+"\\"+Name_EmoMadrid[i]+".jpg\" xcopy /s \""
                      +directoryEmoMadridPicture+"\\"+Name_EmoMadrid[i]+".jpg\" \"" +directoryReceptValenceEmoMadrid+ListLevel[4]+"\\"+Name_EmoMadrid[i]+".jpg*\"\n")


fichierValence.write("Pause \n")
fichierValence.close()
#Extracting features from jpg images
#Reading images
# =============================================================================
# python tensorflow/examples/label_image/label_image.py --graph=/tmp/output_graph.pb --labels=/tmp/output_labels.txt --input_layer=Mul --output_layer=final_result --input_mean=128 --input_std=128 --image=D:\ESISAR\Okayama_University\eSense_files\Experience_1_Diapo\ALLSTIMULI\ALLSTIMULI\i05june05_static_street_boston_p1010764.jpeg
# =============================================================================

#Resize images (500*400) according to training and test dataset images

#JPG to numpy array to be use in Tensorflow
# =============================================================================
# np_1 = imread(filename)
# np_1_2 = np.vstack((np_1.flatten(), np_2.flatten()))
# 
# =============================================================================


#TensorFlow part
# =============================================================================
# Label use are valence and arousal level
# Features use are JPG images from OASIS dataset
# =============================================================================
