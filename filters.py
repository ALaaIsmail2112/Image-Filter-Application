# filters.py
from PIL import  Image
import numpy as np
import cv2


# to not repeat the same steps 
def preprocess_image(image, resize_shape=(500, 500)):
    img_np = np.array(image)
    img_normalized = img_np / 255.0
    img_resized = cv2.resize(img_normalized, resize_shape)
    return img_resized

def postprocess_image(img_np):
    img_scaled = (img_np * 255).astype(np.uint8)
    return Image.fromarray(img_scaled)

# First Filter >>> Diagonal Filter
def diagonal_Filter(image):
    img_resized = preprocess_image(image)
    h,w = img_resized.shape
    for i in range(h):
        for j in range(w):
            if i == j or (i + j) == 500:
                img_resized[i, j] = 1 
    return postprocess_image(img_resized) 

# Second Filter >>> Increase Brightness
def increase_brightness(image):
    img_resized = preprocess_image(image)
    h, w = img_resized.shape  
    img_copy = img_resized.copy()
    for i in range(h):
        for j in range(w):
            img_copy[i, j] = np.clip(img_copy[i, j] * 1.5,0,1)
    return postprocess_image(img_copy)

# Third Filter >>> Decrease Brightness
def decrease_brightness(image):
    img_resized = preprocess_image(image)
    h,w= img_resized.shape
    img_copy = img_resized.copy()
    for i in range(h):
        for j in range(w):
            img_copy[i, j] =np.clip(img_copy[i, j] /2 ,0,1)
    return postprocess_image(img_copy)

# Fourth Filter ... Negative Filter
def negative_Filter(image):
    img_resized = preprocess_image(image)
    h,w= img_resized.shape
    img_copy = img_resized.copy()
    for i in range(h):
        for j in range(w):
            img_copy[i, j] =np.clip(1-img_copy[i, j] ,0,1) 
    return postprocess_image(img_copy)

# Five Filter ... Power Low Filter  
def PowerLow_Filter(image):
    img_resized = preprocess_image(image)
    h,w= img_resized.shape
    img_copy = img_resized.copy()

    for i in range(h):
        for j in range(w):
            img_copy[i][j] = ( img_copy[i][j] ) ** .6
    return postprocess_image(img_copy)

# six Filter ... Power Low Filter == Log transformation
def PowerLow_Log(image):
    img_resized = preprocess_image(image)
    h,w= img_resized.shape
    img_copy = img_resized.copy()

    for i in range(h):
        for j in range(w):
            img_copy[i][j] = (2 * img_copy[i][j] ) ** 0.5
    return postprocess_image(img_copy)

# seven Filter ... Log Transformation Filter
def logTransformation_Filter(image):
    img = np.array(image)
    img2 = cv2.resize(img,(500,500))
    img_resized = img2.copy()
    h,w= img_resized.shape
    for i in range(h):
     for j in range (w) :
          img_resized[i][j] =  30 *(np.log2(img_resized[i][j] +1))
    return Image.fromarray(img_resized)

# eight Filter ... Log Transformation Filter
filter_val = [
    [1/9, 1/9, 1/9],
    [1/9, 1/9, 1/9],
    [1/9, 1/9, 1/9]
]

def Average_Filter(image):
    img_resized = preprocess_image(image)
    h,w= img_resized.shape
    img_copy = img_resized.copy()

    for i in range(1 , h-1 , 1):
     for j in range(1 , w-1 , 1):
          img_copy[i][j] = (img_copy[i][j]* (1/9) + img_copy[i-1][j]* (1/9)+ img_copy[i+1][j]* (1/9)+\
                             img_copy[i][j-1]* (1/9)+ img_copy[i][j+1]* (1/9) + img_copy[i-1][j-1]* (1/9)+\
                              img_copy[i+1][j+1]* (1/9) + img_copy[i-1][j+1]* (1/9) + img_copy[i+1][j-1]* (1/9))
    return postprocess_image(img_copy)

# nine Filter ... Maxmimun_FilterFilter
def Maxmimun_Filter(image):
    img_resized = preprocess_image(image)
    h,w= img_resized.shape
    img_copy = img_resized.copy()
    zeros_matrix = np.zeros((h,w))
    for i in range(1 , h-1 , 1 ):
        for j in range(1 , w-1 ,1):
                list = [img_copy[i][j] , img_copy[i-1][j] , img_copy[i-1][j+1] , img_copy[i+1][j] ,img_copy[i+1][j+1] , img_copy[i+1][j-1] , img_copy[i-1][j-1] , img_copy[i][j+1] , img_copy[i][j-1]]

                zeros_matrix[i][j] = np.max(list)  
    return postprocess_image(zeros_matrix)

# ten Filter ... Minmium_Filter Filter
def Minmium_Filter(image):
    img_resized = preprocess_image(image)
    h,w= img_resized.shape
    img_copy = img_resized.copy()
    zeros_matrix = np.zeros((h,w))
    
    for i in range(1 , h-1 , 1 ):
        for j in range(1 , w-1 ,1):
                list = [img_copy[i][j] , img_copy[i-1][j] , img_copy[i-1][j+1] , img_copy[i+1][j] ,img_copy[i+1][j+1] , img_copy[i+1][j-1] , img_copy[i-1][j-1] , img_copy[i][j+1] , img_copy[i][j-1]]

                zeros_matrix[i][j] = np.min(list)  
    return postprocess_image(zeros_matrix)


# ten Filter ... median Filter
def Median_Filter(image):
    img_resized = preprocess_image(image)
    h,w= img_resized.shape
    zeros_matrix = np.zeros((h,w))

    for i in range(1 , h-1 , 1 ):
        for j in range(1 , w-1 ,1):
                list = [img_resized[i][j] , img_resized[i-1][j] , img_resized[i-1][j+1] , img_resized[i+1][j] ,img_resized[i+1][j+1] , img_resized[i+1][j-1] , img_resized[i-1][j-1] , img_resized[i][j+1] , img_resized[i][j-1]]

                zeros_matrix[i][j] = np.median(list)  
    return postprocess_image(zeros_matrix)


# eleven Filter ... sobel Filter with average filter
gx = [  [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1]]

gy = [[-1, -2, -1],
      [0, 0, 0],
      [1, 2, 1]]

def Sobel_Filter(image):
    img_resized = preprocess_image(image)
    h,w= img_resized.shape
    img_copy = img_resized.copy()
    for row in range(1, h- 1):
      for col in range(1, w - 1):
          GX = ((img_resized[row][col]) * gx[1][1])     + ((img_resized[row-1][col]) * gx[0][1]) +\
               ((img_resized[row-1][col+1]) * gx[0][2]) + ((img_resized[row+1][col]) * gx[2][1]) +\
               ((img_resized[row+1][col+1]) * gx[2][2]) + ((img_resized[row+1][col-1]) * gx[2][0]) +\
               ((img_resized[row-1][col-1]) * gx[0][0]) + ((img_resized[row][col+1]) * gx[1][2]) +\
               ((img_resized[row][col-1]) * gx[1][0])
        
          GY = ((img_resized[row][col]) * gy[1][1])     + ((img_resized[row-1][col]) * gy[0][1]) +\
               ((img_resized[row-1][col+1]) * gy[0][2]) + ((img_resized[row+1][col]) * gy[2][1]) +\
               ((img_resized[row+1][col+1]) * gy[2][2]) + ((img_resized[row+1][col-1]) * gy[2][0]) +\
               ((img_resized[row-1][col-1]) * gy[0][0]) + ((img_resized[row][col+1]) * gy[1][2]) +\
               ((img_resized[row][col-1]) * gy[1][0])
        

          G = np.sqrt((GX**2) + (GY**2))
          img_copy[row][col] = G
    return postprocess_image(img_copy)

# eleven Filter ... prewitt Filter with average filter
gx = [[-1, -1, -1],
      [0, 0, 0],
      [1, 1, 1]]

gy = [[-1, 0, 1],
      [-1, 0, 1],
      [-1, 0, 1]]

def Prewitt_Filter(image):
    img_resized = preprocess_image(image)
    h,w= img_resized.shape
    img_copy = img_resized.copy()
    for row in range(1,h- 1):
      for col in range(1, w - 1):
          GX = ((img_resized[row][col]) * gx[1][1])     + ((img_resized[row-1][col]) * gx[0][1]) +\
               ((img_resized[row-1][col+1]) * gx[0][2]) + ((img_resized[row+1][col]) * gx[2][1]) +\
               ((img_resized[row+1][col+1]) * gx[2][2]) + ((img_resized[row+1][col-1]) * gx[2][0]) +\
               ((img_resized[row-1][col-1]) * gx[0][0]) + ((img_resized[row][col+1]) * gx[1][2]) +\
               ((img_resized[row][col-1]) * gx[1][0])
        
          GY = ((img_resized[row][col]) * gy[1][1])     + ((img_resized[row-1][col]) * gy[0][1]) +\
               ((img_resized[row-1][col+1]) * gy[0][2]) + ((img_resized[row+1][col]) * gy[2][1]) +\
               ((img_resized[row+1][col+1]) * gy[2][2]) + ((img_resized[row+1][col-1]) * gy[2][0]) +\
               ((img_resized[row-1][col-1]) * gy[0][0]) + ((img_resized[row][col+1]) * gy[1][2]) +\
               ((img_resized[row][col-1]) * gy[1][0])
        

          G = np.sqrt((GX**2) + (GY**2))

          img_copy[row][col] = G
    return postprocess_image(img_copy)

def Histogram_Equalization(image):
    img = np.array(image)
    img_resized = cv2.resize(img, (500, 500)) 
    filteredImg = img_resized.copy()
    count = np.bincount(filteredImg.flatten(), minlength=256)
    pdf = count / np.size(img_resized)
    cdf = np.cumsum(pdf)
    norm = cdf * 255 
    norm = np.round(norm).astype(np.uint8)
    new_image = norm[img_resized.flatten()]
    new_image = new_image.reshape(img_resized.shape)

    return Image.fromarray(new_image)




def histogram_matching_algorithm(source_image, reference_image):
    source_img = np.array(source_image)
    reference_img = np.array(reference_image)

    if source_img.shape != reference_img.shape:
        reference_img = cv2.resize(reference_img, (source_img.shape[1], source_img.shape[0]))

    source_hist = np.bincount(source_img.flatten(), minlength=256)
    reference_hist = np.bincount(reference_img.flatten(), minlength=256)

    source_cdf = np.cumsum(source_hist)
    reference_cdf = np.cumsum(reference_hist)

    source_cdf_normalized = (source_cdf - source_cdf.min()) * 255 / (source_cdf.max() - source_cdf.min())
    reference_cdf_normalized = (reference_cdf - reference_cdf.min()) * 255 / (reference_cdf.max() - reference_cdf.min())

    lookup_table = np.zeros(256, dtype=np.uint8)
    g = 0
    for s in range(256):
        while g < 255 and source_cdf_normalized[s] > reference_cdf_normalized[g]:
            g += 1
        lookup_table[s] = g

    matched_image = cv2.LUT(source_img, lookup_table)

    return Image.fromarray(matched_image)
