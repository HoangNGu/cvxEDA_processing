from PIL import Image
import EDA_myAPI_ML as eda
############################################################
#directoryGAPEDpicture = r"\home\zeynep\Dropbox\teaching\supervision\2018_02_intern_nguyen\codes\2018_03_27\Keras\GAPED\GAPED\"
directoryGAPEDpicture = r"D:\ESISAR\Okayama_University\Python\Image_Dataset\GAPED_2\GAPED\GAPED\\"
train_path_Gaped = [directoryGAPEDpicture+"A.csv",directoryGAPEDpicture+"H.csv",directoryGAPEDpicture+"N.csv",
                    directoryGAPEDpicture+"P.csv",directoryGAPEDpicture+"Sn.csv",directoryGAPEDpicture+"Sp.csv"]

Name_Gaped,Valence_mean_Gaped,Arousal_mean_Gaped =[],[],[]
for i in range(len(train_path_Gaped)):
    Name_Gapedtmp,Valence_mean_Gapedtmp,Arousal_mean_Gapedtmp = [],[],[]
    Name_Gapedtmp,Valence_mean_Gapedtmp,Arousal_mean_Gapedtmp = eda.OpenCsvFile_Gaped(train_path_Gaped[i])
    Name_Gaped.extend(Name_Gapedtmp)
    #Valence_mean_Gaped.extend(Valence_mean_Gapedtmp)
    #Arousal_mean_Gaped.extend(Arousal_mean_Gapedtmp)

for i in range(len(Name_Gaped)):
    img = Image.open(directoryGAPEDpicture+Name_Gaped[i][0]+"/"+Name_Gaped[i]+".bmp").convert('RGB')
    new_img = img.resize( (500, 400) )
    new_img.save(directoryGAPEDpicture+Name_Gaped[i][0]+"/"+Name_Gaped[i]+".jpeg", 'jpeg')
############################################################

directoryOASISpicture = r"D:\ESISAR\Okayama_University\Python\Image_Dataset\oasis\F\\"
train_path_OASIS = [directoryOASISpicture+"../OASIS.csv"]

Name_OASIS,Valence_mean_OASIS,Valence_SD_OASIS,Valence_N_OASIS,Arousal_mean_OASIS,_OASISArousal_SD_OASIS,Arousal_N_OASIS = [],[],[],[],[],[],[]
Name_OASIS,Valence_mean_OASIS,Valence_SD_OASIS,Valence_N_OASIS,Arousal_mean_OASIS,_OASISArousal_SD_OASIS,Arousal_N_OASIS = eda.OpenCsvFile(train_path_OASIS[0])

for i in range(len(Name_OASIS)):
    img = Image.open(directoryOASISpicture+Name_OASIS[i]+".jpg").convert('RGB')
    new_img = img
    new_img.save(directoryOASISpicture+Name_OASIS[i]+".jpeg", 'jpeg')