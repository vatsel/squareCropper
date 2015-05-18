#!python3

from PIL import Image
from fractions import Fraction
import glob, re, os
 
class SquareTileCropper:
    def __init__(self,maxRows = 27,minRows = 21,dirToGlob= "Input\\*.jpg",outputDir='output\\'):
        self.maxRows, self.minRows, self.dirToGlob, self.outputDir = maxRows, minRows, dirToGlob,outputDir
        images = [] 
    
    def crop(self,printOutput=True): 
        images = self.globImages()
        for imgName,img in images:
            w,h = img.size
            newWidth,newHeight,tileSize = SquareTileCropper.findLeastCroppedTileableImage(w,h,minRows=self.minRows,maxRows=self.maxRows)
            cropWidthLeft = int((w-newWidth)/2)
            cropHeightTop = int((h-newHeight)/2)
            cropped = img.crop((cropWidthLeft,cropHeightTop,cropWidthLeft+newWidth,cropHeightTop+newHeight))
            self.cropImageIntoSquares(cropped,tileSize,imgName,self.outputDir)
            if printOutput: print('Cropped '+imgName+' to '+str(int(newWidth/tileSize))+'x'+str(int(newHeight/tileSize))+' tiles of size '+str(tileSize)+'px. Deleted '+str(cropWidthLeft*2)+'px from image width & '+str(cropHeightTop*2)+'px from image height')
        if printOutput:
            if len(images) > 0: print('processed '+str(len(images))+' images.')
            else: print("Found no images for processing in specified directory. supplied dirToGlob parameter "+dirToGlob)
        #for imgName,img in self.

    def globImages(self):
        images = []
        for imageFile in glob.glob(self.dirToGlob):
            image = Image.open(imageFile)
            imageFileName = re.findall('[^\\\\]+',imageFile)
            imageFileName = imageFileName[len(imageFileName)-1]
            images.append((imageFileName,image))
        return images
    
    @staticmethod
    def findCroppedSize(width,height,rowNum=25):
        'finds a size that will be tileable using the number of rows'
        newRatio = (height - height%rowNum)/ height
        height,width = int(height*newRatio),int(width*newRatio) # discarding pixel fractions, very slightly decreasing accuracy
        width -= int(width%(height/rowNum)) # right hand side operation:  width % tile_size
        return width,height

    @staticmethod
    def findLeastCroppedTileableImage(width, height,minRows=21,maxRows=27):
        '''iterates between number of rows for optimal solution. returns ((width,height),tileSize)'''
        leastCroppedWidth,leastCroppedHeight = 0,0 # w,h
        tileNum = 0
        for i in range(minRows,maxRows):
            w,h = SquareTileCropper.findCroppedSize(width,height,rowNum=i)
            if leastCroppedWidth+leastCroppedHeight < w+h: leastCroppedWidth,leastCroppedHeight,tileNum = w,h,i
        if w>0: return leastCroppedWidth,leastCroppedHeight,tileNum
        
    @staticmethod
    def cropImageIntoSquares(img,tileSize,imgName,outputDir):
        if not os.path.exists(outputDir): os.mkdir(outputDir)
        imgName = imgName.split('.')[0]
        if not os.path.exists(outputDir+'\\'+imgName): os.mkdir(outputDir+'\\'+imgName)        
        for row in range(int(img.size[1]/tileSize)):
            for column in range(int(img.size[0]/tileSize)):
                outputTile = img.crop((column*tileSize,row*tileSize,(column+1)*tileSize,(row+1)*tileSize))
                outputTile.save(outputDir+imgName+'\\'+str(row)+'_'+str(column)+'.jpg',"JPEG")
        
        
