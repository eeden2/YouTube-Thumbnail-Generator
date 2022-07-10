import _thread
from concurrent.futures import thread
import threading
from tkinter import *
from tkinter import filedialog
import tkinter
from tkinter import ttk
from tkinter.tix import IMAGETEXT
from turtle import left, right
import cv2 as theEngine
import random
import numpy as np
from urllib.request import urlopen
import urllib.request
import requests
from matplotlib import pyplot as plt
import scipy.spatial as spatial
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QLabel as qt
import sys
from tkinter import *
from PIL import Image, ImageTk, ImageSequence
import urllib3
from itertools import count, cycle


thumbnail_resolution = (460,360)
text = ''
app = Tk()
app.title("Generate Memez")
times = 0
tabOwner = ttk.Notebook(master = app)
tab1 = Frame(tabOwner)
tab2 = Frame(tabOwner)
tabOwner.add(tab1, text = "Generator")
tabOwner.add(tab2, text="User Input")
tabOwner.grid(row=0,column=0,sticky="ew")
label = Label(tab1, image= '')

#Next is for the main Dwayne Johnson Photo to keep the GUI look decent
imageFinish = ImageTk.PhotoImage(Image.open("6j39t1.jpg"))

label.config(image=imageFinish)
label.grid(row=0, column=2, pady=2)

entryLabel = Label(tab1, text= 'How Many Clickbait Arrows? (Default=1): ')
entryLabel.grid(row=1,column=2, pady=2)

numOfArrows = Entry(tab1, width= 20)
numOfArrows.grid(row=2,column=2,pady=2)

#This next part is the same layout, but for the user input section
label2 = Label(tab2,image = '')
label2.config(image=imageFinish)
label2.grid(row=0, column=2)

entryLabel2 = Label(tab2, text= 'How Many Clickbait Arrows? (Default=1): ')
entryLabel2.grid(row=1,column=2, pady=2)

numOfArrows2 = Entry(tab2, width= 20)
numOfArrows2.grid(row=2,column=2,pady=2)

whatText = Label(tab2,text = "What Text Shall Da Meme Display My Lord?\nType \"GENERATE\" if you wish to generate text")
whatText.grid(row=3,column=2,pady=2)

textEntry = Entry(tab2,width=20)
textEntry.grid(row=4,column=2,pady=2)

whatImage = Label(tab2,text="Please Upload the meme image")
whatImage.grid(row=5,column=2,pady=2)

class userInput:
    
    def runGIF(fileName,fileName2):
        lbl = ImageLabel(tab2)
        lbl2 = ImageLabel(tab2)
        lbl2.load(fileName2,False)        
        lbl2.grid(row=0, column=3, pady=2)
        lbl.load(fileName,False)
        lbl.grid(row=0,column=1,pady=1)
        userInput.hitTheGriddy()
        return
    
    def hitTheGriddy():
        label2.grid(row=0, column=2,pady=2)
        entryLabel2.grid(row=1,column=2, pady=4)
        whatText.grid(row=3,column=2,pady=2)
        textEntry.grid(row=4,column=2,pady=2)
        whatImage.grid(row=5,column=2,pady=2)
       
        
    
    def userUploadImage():
        global times
        
        filetypes =(('JPEG File', '*.jpg'),('PNG File', '*.png'))
        userImage = theEngine.imread(filedialog.askopenfile(filetypes=filetypes).name)
        arrows = 1
        
        try:
         arrows = int(numOfArrows2.get())
        except:
            print('')
            pass
        text = textEntry.get()
        if(text=="GENERATE"):
            text = makingImage.get_text()
        else:
            text = textEntry.get()
        saveBtn = Button (tab2, text = "Save the Image Bro", command = makingImage.saveFile, width = 20)
        saveBtn.grid(row=7,column=2,pady=2)
        if times >0:
            label.config(image='') 
            saveBtn.destroy() 
            label.grid(row=0, column=1, pady=2)
            
        cropped_img = makingImage.crop_image(userImage)
                       

        densest = makingImage.get_densest(makingImage.get_kp(cropped_img))            
        print('Densest Point is at: ' + str(densest))
        circled_img = makingImage.draw_shapes(cropped_img, densest,arrows)
            
        x_length = circled_img.shape[1]
        txt_scale, txt_height = makingImage.get_font_scale(makingImage.get_text(), x_length)
        if densest[1] > circled_img.shape[0] / 2:
            pos = (0, txt_height + int(.07 * circled_img.shape[0]))
        else:
            pos = (0,  + circled_img.shape[0] - int(.07 * circled_img.shape[0]))            
        line_width = txt_scale * 3
        txted_img = theEngine.putText(circled_img, text, pos, theEngine.FONT_HERSHEY_DUPLEX, txt_scale, (0, 0 ,0), int(line_width * 4), theEngine.LINE_AA)
        txted_img = theEngine.putText(circled_img, text, pos, theEngine.FONT_HERSHEY_DUPLEX, txt_scale, (255, 255, 255), int(line_width), theEngine.LINE_AA)
            
        blue,green,red = theEngine.split(txted_img)
        firstStep = theEngine.merge((red,green,blue))
        secondStep= Image.fromarray(firstStep)
        global saveImage 
        saveImage= secondStep
        imageFin = ImageTk.PhotoImage(image = secondStep)
        label2.config(image=imageFin)
        print("Configged Image")
        label2.grid(row=0, column=3, pady=2)
        times+=1
        userInput.runGIF("frog_left.gif","frog_right.gif")
        tab2.config(bg='blue')
        app.mainloop()
        
    def gifTab2():
        userInput.userUploadImage()
        makingImage.runGIF("frog_left.gif","frog_right.gif")
        
    
    
class ImageLabel(tkinter.Label):
    
    """
    A Label that displays images, and plays them if they are gifs
    :im: A PIL Image instance or a string filename
    """
    def load(self, im,definer):
                
        if isinstance(im, str):
            im = Image.open(im)
        frames = []
 
        try:
            for i in count(1):
                frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass
        self.frames = cycle(frames)
 
        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100
 
        if len(frames) == 1:
            self.config(image=next(self.frames))
        else:
            self.next_frame()
 
    def unload(self):
        self.config(image=None)
        self.frames = None
 
    def next_frame(self):
        if self.frames:
            self.config(image=next(self.frames))
            self.after(self.delay, self.next_frame)

class makingImage():
    def get_image(width, height):
        req = urlopen('https://picsum.photos/{}/{}'.format(width, height))
        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        img = theEngine.imdecode(arr, -1) 
        return img

    def crop_image(raw_img):
        global thumbnail_resolution
        #Crops the image to youtube thumbnail aspect ratio, centering the crop with the center of the image
        ideal_aspect_ratio = thumbnail_resolution[0] / thumbnail_resolution[1]

        orig_y = raw_img.shape[0]

        orig_x = raw_img.shape[1]

        aspect_ratio = round(orig_x / orig_y, 16)

        if aspect_ratio < ideal_aspect_ratio:
            print('Excess y pixels')
            new_y = int(orig_x / ideal_aspect_ratio)
            y_center = int(orig_y / 2)
            cropped_img = raw_img[y_center - int(new_y / 2):y_center + int(new_y / 2), 0:orig_x]

        elif aspect_ratio > ideal_aspect_ratio:
            print('Excess x pixels')
            new_x = int(orig_y * ideal_aspect_ratio)
            x_center = int(orig_x / 2)
            cropped_img = raw_img[0:orig_y, x_center - int(new_x / 2):x_center + int(new_x / 2)]
        else: 
            print('Correct aspect ratio')
            cropped_img = raw_img

        print('New Res: ' + str(cropped_img.shape))
        print('Current Aspect Ratio: ' + str(cropped_img.shape[1] / cropped_img.shape[0]))
        cropped_img = theEngine.resize(cropped_img, thumbnail_resolution)

        return cropped_img


    def get_font_scale(text, width):
        for scale in reversed(range(0, 50, 1)):
            textSize = theEngine.getTextSize(text, fontFace=theEngine.FONT_HERSHEY_DUPLEX, fontScale=scale/10, thickness=1)
            new_width = textSize[0][0]
            if (new_width <= width):
                return scale/10, textSize[0][1]


    def generate_txt(raw_img, txt, circle_pos):
        x_length = raw_img.shape[1]
        txt_scale, txt_height = makingImage.get_font_scale(txt, x_length)
        if circle_pos[1] > raw_img.shape[0] / 2:
            pos = (0, txt_height + int(.07 * raw_img.shape[0]))
        else:
            pos = (0,  + raw_img.shape[0] - int(.07 * raw_img.shape[0]))
        line_width = txt_scale * 3
        txted_img = theEngine.putText(raw_img, text, pos, theEngine.FONT_HERSHEY_DUPLEX, txt_scale, (0, 0 ,0), int(line_width * 4), theEngine.LINE_AA)
        txted_img = theEngine.putText(raw_img, text, pos, theEngine.FONT_HERSHEY_DUPLEX, txt_scale, (255, 255, 255), int(line_width), theEngine.LINE_AA)
        return txted_img

    def get_text():
        ender_list = ['', '!', '!!!', '?', '??', '!?', '!??', '..!', '...'] 
        r = requests.post(
            "https://api.deepai.org/api/text-generator",
            files={
                'text':'Kanye West fan account',
            },
            headers={'api-key': 'f55c37e9-7b66-48e2-9c76-041b3bf47c5d'}
        )
        raw_text = r.json()['output']
        print(raw_text)
        ender = ender_list[random.randint(0,len(ender_list) - 1)]
        words = raw_text.split(' ')
        word_count = random.randint(2,4)
        place_in_text = random.randint(0,len(words) - word_count)
        kept_words = []
        for word in range(place_in_text, place_in_text + word_count):
            kept_words.append(words[word].replace('\n', ''))
        text = ' '.join(kept_words) + ender
        return text

    def get_kp(image):
        orb = theEngine.ORB_create()
        grayscale_image = theEngine.cvtColor(image, theEngine.COLOR_BGR2GRAY)
        kp = orb.detect(grayscale_image, None)
        kp, des = orb.compute(grayscale_image, kp)
        kp_locations = []
        for keypoint in kp:
            kp_locations.append((keypoint.pt[0], keypoint.pt[1]))
        return kp_locations

    def get_densest(points_list):
        points = np.array(points_list) #list of tuples with x and y value
        tree = spatial.KDTree(np.array(points))
        radius = 3.0
        neighbors = tree.query_ball_tree(tree, radius)
        neighbors_ordered = sorted(neighbors, key=len)
        dense_list = []
        for point in neighbors_ordered:
            dense_list.append(tuple(points[neighbors.index(point)]))
        return dense_list

    def draw_circle(image, position):
        radius = int(image.shape[1] / 10)
        thickness = int(image.shape[1] / 75)
        theEngine.circle(image, (int(position[0]), int(position[1])), radius, (0,0,255), thickness, lineType=theEngine.LINE_AA)
        return image

    
    def get_arrow_cords(image, circle_pos, circle_radius):
        closer_point_length = circle_radius + (.05 * image.shape[1])
        further_point_length = closer_point_length + (.3 * image.shape[1])
        angle = random.randint(0,360)
        print(angle)
        print(circle_pos)
        arrow_start = (int(circle_pos[0] + (further_point_length * np.sin(angle))),
        int(circle_pos[1] + (further_point_length * np.cos(angle))))
        arrow_stop = (int(circle_pos[0] + (closer_point_length * np.sin(angle))),
        int(circle_pos[1] + (closer_point_length * np.cos(angle))))
        return arrow_start, arrow_stop

    def draw_shapes(image, dense_list, numOfArrows):
        radius = int(image.shape[1] / 10)
        thickness = int(image.shape[1] / 75)
        arrows_drawn = 0
        temp_images = []
        while arrows_drawn < numOfArrows:
            image = theEngine.circle(image, (int(dense_list[arrows_drawn][0]), int(dense_list[arrows_drawn][1])), radius, (0,0,255), thickness, lineType=theEngine.LINE_AA)
            print('Drawn circle at:')
            print(dense_list[arrows_drawn])
            arrow_start = (-50, -50)
            while arrow_start[0] not in range(0, image.shape[1]) or arrow_start[1] not in range(image.shape[0]):
                arrow_start, arrow_stop = makingImage.get_arrow_cords(image, dense_list[arrows_drawn], radius)
            #image = theEngine.arrowedLine(image, arrow_start, arrow_stop, (0,0,255), int(image.shape[1] / 30), theEngine.LINE_AA, tipLength=(image.shape[1] / 2000))
            temp_images.append(theEngine.arrowedLine(image, arrow_start, arrow_stop, (0,0,255), int(image.shape[1] / 30), theEngine.LINE_AA, tipLength=(image.shape[1] / 2000)))
            
            arrows_drawn += 1
        iterate = len(temp_images)-1
        for i in range(iterate):
            currentItImage = image
            if i==0:
                currentItImage = temp_images[i]
                image = theEngine.bitwise_and(currentItImage,temp_images[1])
            if i>0:
                image = theEngine.bitwise_and(currentItImage,temp_images[i+1])    
        return image
            
    
    def runGIF(fileName,fileName2):
        lbl = ImageLabel(tab1)
        lbl2 = ImageLabel(tab1)
        lbl2.load(fileName2,False)        
        lbl2.grid(row=0, column=3, pady=2)
        lbl.load(fileName,False)
        lbl.grid(row=0,column=1,pady=2)
        return
    
    def makeImage():
        
        makingImage.runGIF("frog_left.gif","frog_right.gif")
        print('working')
        global times
        global numOfArrows
        
        arrows = 1
        try:
         arrows = int(numOfArrows.get())
        except:
            print('')
            pass
        
        text = makingImage.get_text()
        saveBtn = Button (tab1, text = "Save the Image Bro", command = makingImage.saveFile, width = 20)
        saveBtn.grid(row=4,column=2,pady=2)
        if times >0:
            label.config(image='') 
            saveBtn.destroy() 
            label.grid(row=0, column=1, pady=2)
        
        img = makingImage.get_image(thumbnail_resolution[0], thumbnail_resolution[1])

        cropped_img = makingImage.crop_image(img)
        

        densest = makingImage.get_densest(makingImage.get_kp(cropped_img))
        print('Densest Point is at: ' + str(densest))
        circled_img = makingImage.draw_shapes(cropped_img, densest,arrows)
       
        
        x_length = circled_img.shape[1]
        txt_scale, txt_height = makingImage.get_font_scale(makingImage.get_text(), x_length)
        if densest[0][1] > circled_img.shape[0] / 2:
            pos = (0, txt_height + int(.07 * circled_img.shape[0]))
        else:
            pos = (0,  + circled_img.shape[0] - int(.07 * circled_img.shape[0]))
        line_width = txt_scale * 3
        txted_img = theEngine.putText(circled_img, text, pos, theEngine.FONT_HERSHEY_DUPLEX, txt_scale, (0, 0 ,0), int(line_width * 4), theEngine.LINE_AA)
        txted_img = theEngine.putText(circled_img, text, pos, theEngine.FONT_HERSHEY_DUPLEX, txt_scale, (255, 255, 255), int(line_width), theEngine.LINE_AA)
        
        
        blue,green,red = theEngine.split(txted_img)
        firstStep = theEngine.merge((red,green,blue))
        secondStep= Image.fromarray(firstStep)
        global saveImage 
        saveImage= secondStep
        imageFin = ImageTk.PhotoImage(image = secondStep)
        label.config(image=imageFin)
        
        label.grid(row=0, column=2, pady=2)
        times+=1
        tab1.config(bg='blue')
        btn.grid(row=5,column=2,pady=2)
        app.mainloop()
        
    
    def saveFile():
        filename = filedialog.asksaveasfile(mode='w', defaultextension=".jpg")
        global saveImage
        if not filename:
            return
        saveImage.save(filename)
        
    
    

if __name__ == '__main__':
   
    btn = Button(tab1, text = "Generate Da Meme", command = makingImage.makeImage,width=20)
    btn.grid(row=4,column=2,pady=2)
    openBtn = Button(tab2,text = "Upload Image",command= userInput.gifTab2)
    openBtn.grid(row=6, column =2, pady=2)
    app.mainloop()







        


