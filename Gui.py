import tkinter as tk
import numpy as np
import cv2
import PIL, PIL.Image, PIL.ImageOps, PIL.ImageEnhance
from PIL import  Image, ImageTk
from tkinter import filedialog
import imutils

# Functions
def PhotoImage2Image(ima):   
    if str(type(ima)) == "<class 'tkinter.PhotoImage'>":
        ImageCoversion= ImageTk.getimage(ima).convert("L")
        return ImageCoversion
    if str(type(ima)) == "<class 'PIL.ImageTk.PhotoImage'>":
        ImageCoversion= ImageTk.getimage(ima).convert("L")
        return ImageCoversion
    else:
        print('Not a PhotoImaage at func, called with ', str(type(ima)))



def Anaglyph():
    #Anglyph
    global leftImage, rightImage, Merged
    RedAux=leftImage
    CyanAux=rightImage
    RedIm=PIL.ImageOps.colorize(RedAux,(0,0,0),(255,0,0))
    CyanIm=PIL.ImageOps.colorize(CyanAux,(0,0,0),(0,255,255))
    MergedImageData= PIL.Image.blend(RedIm,CyanIm,0.5)
    Np_blend=np.array(MergedImageData)
    CombinatedImage= imutils.resize(Np_blend, height=1920, width=1080)
    CombinatedImage=cv2.cvtColor(CombinatedImage, cv2.COLOR_BGR2RGB)
    CombinatedImage=CombinatedImage[:,:,::-1]
    CombinatedImage=Image.fromarray(CombinatedImage,'RGB')
    Merged=ImageTk.PhotoImage(CombinatedImage)
    

# GUI commands
def onMenuImportLeft():
    global leftImage, PhotoImLeft,UpperImage
    ImagePath=filedialog.askopenfilename(title="leftImage",filetypes=[('image',".jpeg"),('image',".jpg"),('image',".png")])
    if len(ImagePath)>0:
        fileim=Image.open(ImagePath,mode='r').resize((int(1920/2),1080))
        fileim2=Image.open(ImagePath,mode='r').resize((int(700),550))
        leftImage=fileim.convert('L')
        PhotoImLeft=ImageTk.PhotoImage(fileim)
        UpperImage=ImageTk.PhotoImage(fileim2)
        LeftImageHolder['image']=PhotoImLeft

def onMenuImportRight():
    global rightImage, PhotoImRight,LowerImage
    ImagePath=filedialog.askopenfilename(title="RightImage",filetypes=[('image',".jpeg"),('image',".jpg"),('image',".png")])
    if len(ImagePath)>0:
        fileim=Image.open(ImagePath,mode='r').resize((int(1920/2),1080))
        fileim2=Image.open(ImagePath,mode='r').resize((int(700),550))
        rightImage=fileim.convert('L')
        PhotoImRight=ImageTk.PhotoImage(fileim)
        LowerImage=ImageTk.PhotoImage(fileim2)
        RightImageHolder['image']=PhotoImRight

def onMenuAnaglyph():
    Anaglyph()
    global Merged
    AnaglyphImageHolder.grid(column=0,row=0,padx=int(root.winfo_width()/4.5))
    AnaglyphImageHolder['image']=Merged
    UpperImageHolder.grid_remove()
    LowerImageHolder.grid_remove()
    LeftImageHolder.grid_remove()
    RightImageHolder.grid_remove()

def onMenuParallel():
    global PhotoImRight, PhotoImLeft
    LeftImageHolder['image']=PhotoImLeft
    RightImageHolder['image']=PhotoImRight
    AnaglyphImageHolder.grid_remove()
    UpperImageHolder.grid_remove()
    LowerImageHolder.grid_remove()
    LeftImageHolder.grid(column=0,row=0)
    RightImageHolder.grid(column=3,row=0)

def onMenuCrossed():
    global PhotoImRight, PhotoImLeft
    LeftImageHolder['image']=PhotoImRight
    RightImageHolder['image']=PhotoImLeft
    AnaglyphImageHolder.grid_remove()
    UpperImageHolder.grid_remove()
    LowerImageHolder.grid_remove()
    LeftImageHolder.grid(column=0,row=0)
    RightImageHolder.grid(column=3,row=0)

def onMenuUpToDown():
    global LowerImage, UpperImage

    #auxImageLeft=ImageTk.PhotoImage(leftImage.resize((900,500)))

    UpperImageHolder['image']=LowerImage
    LowerImageHolder['image']=UpperImage

    UpperImageHolder.grid(column=0,row=0,padx=600)
    LowerImageHolder.grid(column=0,row=1,padx=600)
    AnaglyphImageHolder.grid_remove()
    LeftImageHolder.grid_remove()
    RightImageHolder.grid_remove()

def onFullScreen():
    root.attributes('-fullscreen', True)
    MenuBar.delete("Import")
    MenuBar.delete("Edit")
    MenuBar.delete("Full Screen")

def onEscape(event):
    if event.keysym=='Escape':
        root.attributes('-fullscreen', False)
        MenuBar.add_cascade(label='Import', menu=fileMenu)
        MenuBar.add_cascade(label='Edit', menu=EditMenu)
        MenuBar.add_command(label='Full Screen', command=onFullScreen)

        


    

# create the main window
root = tk.Tk()
root.bind('<Key>', onEscape)

root.title("Augmented Reality Glasses")
root.iconbitmap("ImagesAndIcons/Glasses.ico")

root.config(bg="darkgray")

# General Use Variables Definition
PhotoImLeft=tk.PhotoImage(file="ImagesAndIcons/Missing.png")
PhotoImRight=PhotoImLeft
Merged=PhotoImLeft
PhotoImRight=PhotoImLeft
UpperImage=PhotoImLeft
LowerImage=PhotoImLeft
rightImage=PhotoImLeft
leftImage=PhotoImLeft

# Frames definition
ImagesFrame=tk.Frame(width=1080,height=700, bg='darkgray')
ImagesFrame.grid(column=0,row=0)

    #Image display
        #ParallelView
LeftImageHolder=tk.Label(ImagesFrame,image=PhotoImLeft)
LeftImageHolder.grid(column=0,row=0)
RightImageHolder=tk.Label(ImagesFrame,image=PhotoImRight)
RightImageHolder.grid(column=3,row=0)

        #Anaglyph View
AnaglyphImageHolder=tk.Label(ImagesFrame,image=Merged)
AnaglyphImageHolder.grid(column=1,row=0)
AnaglyphImageHolder.grid_remove()
        #UptoDown View
UpperImageHolder=tk.Label(ImagesFrame,image=UpperImage)
UpperImageHolder.grid(column=0,row=0)
UpperImageHolder.grid_remove()
LowerImageHolder=tk.Label(ImagesFrame,image=LowerImage)
LowerImageHolder.grid(column=0,row=1)
LowerImageHolder.grid_remove()

# Menus Definition
MenuBar= tk.Menu(root)
fileMenu=tk.Menu(MenuBar, tearoff=0)

leftRightMenu=tk.Menu(fileMenu,tearoff=0)
leftRightMenu.add_command(label="Import left Image", command=onMenuImportLeft)
leftRightMenu.add_command(label="Import right Image", command=onMenuImportRight)

fileMenu.add_cascade(label='Import Images',menu=leftRightMenu)

EditMenu= tk.Menu(MenuBar, tearoff=0)
EditMenu.add_command(label="Anaglyph", command=onMenuAnaglyph)
EditMenu.add_command(label="Crossed sight", command=onMenuCrossed)
EditMenu.add_command(label="Parallel sight (Default view)", command=onMenuParallel)
EditMenu.add_command(label="Up to down sight", command=onMenuUpToDown)

MenuBar.add_cascade(label='Import', menu=fileMenu)
MenuBar.add_cascade(label='Edit', menu=EditMenu)
MenuBar.add_command(label='Full Screen', command=onFullScreen)






root.config(menu=MenuBar)
# run the GUI
root.mainloop()