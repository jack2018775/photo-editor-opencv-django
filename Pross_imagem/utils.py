import cv2
import numpy as np
import imutils
import mahotas

def pega_img_mod(image,action):
    # 4 PYTHON
    # IMAGEM GRAY
    if action == 'COLOR_BGR2GRAY':
        edit=cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # IMAGEM HSV
    elif action == 'COLOR_BCOLOR_BGR2HSV':
        edit=cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # IMAGEM LAB
    elif action == 'COLOR_BGR2LAB':
        edit=cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    elif action == 'SUAVE1':
        img = image[::2,::2] 

        edit=suave = np.vstack([
        np.hstack([img, cv2.blur(img, ( 3, 3))]), 
        np.hstack([cv2.blur(img, (5,5)), cv2.blur(img, ( 7, 7))]), 
        np.hstack([cv2.blur(img, (9,9)), cv2.blur(img, (11, 11))]), 
        ])
    elif action == 'SUAVE2':
        img = image[::2,::2] 

        edit=suave = np.vstack([
        np.hstack([img,
        cv2.GaussianBlur(img, ( 3, 3), 0)]), 
        np.hstack([cv2.GaussianBlur(img, ( 5, 5), 0), 
        cv2.GaussianBlur(img, ( 7, 7), 0)]), 
        np.hstack([cv2.GaussianBlur(img, ( 9, 9), 0), 
        cv2.GaussianBlur(img, (11, 11), 0)]), 
        ])
    elif action == 'SUAVE3':
        img = image[::2,::2] 

        edit=suave = np.vstack([
        np.hstack([img,
        cv2.medianBlur(img, 3)]), 
        np.hstack([cv2.medianBlur(img, 5), 
        cv2.medianBlur(img, 7)]), 
        np.hstack([cv2.medianBlur(img, 9), 
        cv2.medianBlur(img, 11)]), 
        ])
    elif action == 'BINARIZACAO1':
        img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        suave = cv2.GaussianBlur(img, (7, 7), 0) 
        (T, bin) = cv2.threshold(suave, 160, 255, cv2.THRESH_BINARY)
        (T, binI) = cv2.threshold(suave, 160, 255, 
        cv2.THRESH_BINARY_INV)

        edit=resultado = np.vstack([
        np.hstack([suave, bin]),
        np.hstack([binI, cv2.bitwise_and(img, img, mask = binI)])
        ]) 
    elif action == 'BINARIZACAO2':
        img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        suave = cv2.GaussianBlur(img, (7, 7), 0) # aplica blur 
        bin1 = cv2.adaptiveThreshold(suave, 255,
        cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 21, 5)
        bin2 = cv2.adaptiveThreshold(suave, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 
        21, 5)

        edit=resultado = np.vstack([
        np.hstack([img, suave]),
        np.hstack([bin1, bin2])
        ]) 
    elif action == 'BINARIZACAO3':
        img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        suave = cv2.GaussianBlur(img, (7, 7), 0) # aplica blur 
        T = mahotas.thresholding.otsu(suave)
        temp = img.copy()
        temp[temp > T] = 255
        temp[temp < 255] = 0
        temp = cv2.bitwise_not(temp)
        T = mahotas.thresholding.rc(suave)
        temp2 = img.copy()
        temp2[temp2 > T] = 255
        temp2[temp2 < 255] = 0
        temp2 = cv2.bitwise_not(temp2)

        edit=resultado = np.vstack([
        np.hstack([img, suave]),
        np.hstack([temp, temp2])
        ])

    elif action == 'SEGMENTACAO1':
        img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        sobelX = cv2.Sobel(img, cv2.CV_64F, 1, 0)
        sobelY = cv2.Sobel(img, cv2.CV_64F, 0, 1)
        sobelX = np.uint8(np.absolute(sobelX))
        sobelY = np.uint8(np.absolute(sobelY))
        sobel = cv2.bitwise_or(sobelX, sobelY)

        edit=resultado = np.vstack([
        np.hstack([img, sobelX]),
        np.hstack([sobelY, sobel])
        ]) 
    elif action == 'SEGMENTACAO2':
        img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        lap = cv2.Laplacian(img, cv2.CV_64F)
        lap = np.uint8(np.absolute(lap))
        
        edit=resultado = np.vstack([img, lap]) 

    elif action == 'SEGMENTACAO3':
        img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        suave = cv2.GaussianBlur(img, (7, 7), 0)
        canny1 = cv2.Canny(suave, 20, 120)
        canny2 = cv2.Canny(suave, 70, 200)

        edit=resultado = np.vstack([
        np.hstack([img, suave ]),
        np.hstack([canny1, canny2])
        ]) 

    elif action == 'FATIAMENTO1':
        image[30:50, :] = (255, 0, 0)
        image[100:150, 50:100] = (0, 0, 255)
        image[:, 200:220] = (0, 255, 255)
        image[150:300, 250:350] = (0, 255, 0)
        image[300:400, 50:150] = (255, 255, 0)
        image[250:350, 300:400] = (255, 255, 255)
        image[70:100, 300: 450] = (0, 0, 0)
        edit=(image)



    return edit
