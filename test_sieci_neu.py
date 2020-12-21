import glob
import plaidml.keras
plaidml.keras.install_backend()
import keras
import imageio
import numpy as np
import os
from keras.models import load_model

genderModel = load_model('siec.h5')
genderModel.summary()

ImgWidth = 100
ImgHeight = 100
blad_m=0
blad_k=0
BazaImg = np.empty((2,ImgHeight,ImgWidth,3))
PATH_TO_TEST_IMAGES_DIR_m = '.\\baza_testowa\\m\\'
searchstr_m = os.path.join(PATH_TO_TEST_IMAGES_DIR_m, '*.jpg')
list_of_images_m = glob.glob(searchstr_m)

PATH_TO_TEST_IMAGES_DIR_k = '.\\baza_testowa\\k\\'
searchstr_k = os.path.join(PATH_TO_TEST_IMAGES_DIR_k, '*.jpg')
list_of_images_k = glob.glob(searchstr_k)
if os.path.exists("wynik_sieci.txt"):
    os.remove("wynik_sieci.txt")
fil=open("wynik_sieci.txt","w+",encoding="utf-8")
fil.write("+-------------------------+-------------------------+\n")
fil.write("|                         | Faktyczna płeć osoby    |\n")
fil.write("|                         | na zdjęciu              |\n")
fil.write("+-------------------------+------------+------------+\n")
fil.write("|                         | Mężczyzna  |   Kobieta  |\n")
fil.write("+------------+------------+------------+-------------\n")
for i in range(len(list_of_images_k)):
    FileName_m = list_of_images_m[i]
    Img_m = imageio.imread(FileName_m)
    Img_m = (Img_m / 127.5) - 1
    BazaImg[0,:,:,:] = Img_m[0:ImgHeight,0:ImgWidth,0:3]

    FileName_k = list_of_images_k[i]
    Img_k = imageio.imread(FileName_k)
    Img_k = (Img_k / 127.5) - 1
    BazaImg[1,:,:,:] = Img_k[0:ImgHeight,0:ImgWidth,0:3]

    gender = genderModel.predict(BazaImg) # 0 - m, 1 - k
    if(gender[0]<=0.5):
        fil.write("| Odpowiedź  | Kobieta    |            |            |\n")
        fil.write("| sieci      +------------+--------------------------\n")
        fil.write("|            | Mężczyzna  |     ✓      |            |\n")
        fil.write("+------------+------------+------------+------------+\n")
    else:
        fil.write("| Odpowiedź  | Kobieta    |     ✓      |            |\n")
        fil.write("| sieci      +------------+--------------------------\n")
        fil.write("|            | Mężczyzna  |            |            |\n")
        fil.write("+------------+------------+------------+------------+\n")
        blad_m=blad_m+1
    if(gender[1]>0.5):
        fil.write("| Odpowiedź  | Kobieta    |            |      ✓     |\n")
        fil.write("| sieci      +------------+--------------------------\n")
        fil.write("|            | Mężczyzna  |            |            |\n")
        fil.write("+------------+------------+------------+------------+\n")
    else:
        fil.write("| Odpowiedź  | Kobieta    |            |            |\n")
        fil.write("| sieci      +------------+--------------------------\n")
        fil.write("|            | Mężczyzna  |            |      ✓     |\n")
        fil.write("+------------+------------+------------+------------+\n")
        blad_k=blad_k+1
d_m=25-blad_m
d_k=25-blad_k
fil.write("Poprawnie wybrani mężczyźni  "+str(d_m)+"\n")
fil.write("Poprawnie wybrane kobiety  "+str(d_k)+"\n")
fil.write("Błędnie zakwalifikowani mężczyźni  "+str(blad_m)+"\n")
fil.write("Błędnie zakwalifikowane kobiety  "+str(blad_k)+"\n")
fil.close()