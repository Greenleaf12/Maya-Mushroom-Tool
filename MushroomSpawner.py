# Mushroom Tool By Rory Gardner

import maya.cmds as cmds
import random
import re

noiseAmount = 1.1
noise_Var = True
stemBulge_Var = False
capRoundness = 80

StemShader = cmds.shadingNode( 'lambert', asShader = True)    
cmds.setAttr( StemShader + '.color', 0.497, 0.426, 0.312, type = 'double3' )

CapShader = cmds.shadingNode( 'lambert', asShader = True)    
cmds.setAttr( CapShader + '.color', 0.258, 0.092, 0.049, type = 'double3' )

GrillShader = cmds.shadingNode( 'lambert', asShader = True)    
cmds.setAttr( GrillShader + '.color', 0.158, 1.092, 0.049, type = 'double3' )

#DotShader = cmds.shadingNode( 'Blinn', asShader = True)    
#cmds.setAttr( DotShader + '.color', 0.500, 0.440, 0.330, type = 'double3' )

def Mushroom(winID, noiseAmount, stemSections, mushroomHeight, mushroomWidth, stemWidth, moveStem, capSize, capSizeBase, stemRotate, capHeight, stemHeight, capBaseHeight, baseBulge, bendScale):
       
    cmds.softSelect(sse=0, ssd = 1)
        
    if cmds.objExists('MushroomOriginal'): 
        cmds.select("MushroomOriginal")
        cmds.delete()
       
    #Random Numbers
    randomFloatScaleZXY = random.uniform(-0.1,0.1)
    
    #Make Stalk primitive
    Cylinder=cmds.polyCylinder (h=mushroomHeight,r=mushroomWidth,sx=42,sy=1,name='MushroomOriginal')
    cmds.hyperShade(assign = StemShader)
    cmds.select(Cylinder[0]+'.f[43]')
    cmds.scale(stemWidth,1,stemWidth, r=True)
    
    #Adjust Stalk
    stepScaleInput = 0.3
    stepScaleInput2 = 1.5
    
    for i in range (stemSections):
        
        randomFloatRotate = random.uniform(-stemRotate,stemRotate)
        randomFloatScale = random.uniform(0.01,0.02)
        randomFloatX = random.uniform(-moveStem,moveStem)
        randomFloatY = random.uniform(0.1,0.2)
        randomFloatZ = random.uniform(-moveStem,moveStem)
        
        randomFloatTopY = random.uniform(0.8,1.2)
        randomFloatTopYsmall = random.uniform(0.1,0.2)
        
        cmds.select(Cylinder[0]+'.f[43]')
        
        cmds.polyExtrudeFacet(s=(stepScaleInput+randomFloatScale, stemHeight+randomFloatY, stepScaleInput+randomFloatScale),  t=(randomFloatX, randomFloatY, randomFloatZ), d=1)
        cmds.rotate(randomFloatRotate,0,randomFloatRotate)
        cmds.move(0,stemHeight/2,0, os=True, r=True , ls=True) 
         
        randomFloatRotate += bendScale
        stepScaleInput += 0.3

    #Stem Bulge 
    if stemBulge_Var:          
        for j in range (stemSections):
        
            cmds.select(Cylinder[0]+'.f[43]')
            cmds.polyExtrudeFacet(s=(stepScaleInput2-randomFloatScale,randomFloatY,stepScaleInput2-randomFloatScale), t=(randomFloatX, randomFloatY, randomFloatZ), d=1)
            cmds.move(0,stemHeight/5,0, os=True, r=True , ls=True) 
            stepScaleInput2 -= 0.3
            cmds.rotate(randomFloatRotate,0,randomFloatRotate)      
            randomFloatRotate += bendScale
        
    #Scale the top stalk extrusion    
    cmds.scale(0.8,1.0,0.8, r=False)
       
    #Create Gills
    morphUnder = random.uniform(0.01, 0.05)
    cmds.select(Cylinder[0]+'.f[43]')
    cmds.polyExtrudeFacet(s=(1.4+randomFloatScaleZXY,1.4+randomFloatScaleZXY,1.4+randomFloatScaleZXY+morphUnder), t=(0, randomFloatTopYsmall, 0), ls=(1, 1, 1), d=1)   
    cmds.polyExtrudeFacet(s=(1.5+randomFloatScaleZXY,1.5+randomFloatScaleZXY,1.5+randomFloatScaleZXY+morphUnder), t=(0, randomFloatTopYsmall, 0),  ls=(1, 1, 1), d=1)    
    cmds.polyExtrudeFacet(s=(1.6+randomFloatScaleZXY,1.6+randomFloatScaleZXY,1.6+randomFloatScaleZXY+morphUnder), t=(0, randomFloatTopYsmall, 0),  ls=(1, 1, 1), d=1)      
    cmds.polyExtrudeFacet(s=(1.3+randomFloatScaleZXY,1.3+randomFloatScaleZXY,1.3+randomFloatScaleZXY+morphUnder), t=(0, randomFloatTopYsmall-0.2, 0),  ls=(1, 1, 1), d=1)
    cmds.polyExtrudeFacet(s=(1.2+randomFloatScaleZXY,1.2+randomFloatScaleZXY,1.2+randomFloatScaleZXY+morphUnder), t=(0, randomFloatTopYsmall-0.3, 0),  ls=(1, 1, 1), d=1)  
    cmds.hyperShade(assign = CapShader)
      
    #Cap Base
    randomCapRotate = random.uniform(-3,3)
    cmds.select(Cylinder[0]+'.f[43]')
    cmds.scale(capSizeBase,capSizeBase,capSizeBase, r=True, cs=True)
    cmds.polyCircularizeFace(divisions=0, radialOffset=capSizeBase/4, supportingEdges=1) 
    cmds.move(0,-capBaseHeight,0, r=True) 
    #cmds.rotate(randomCapRotate,randomCapRotate,randomCapRotate, r=True)  
    cmds.select(clear=True)
    
    #Create Cap  
    topStep=capHeight
    cmds.select(Cylinder[0]+'.f[43]')
    #cmds.scale(capSizeBase/2,capSizeBase/2,capSizeBase/2, r=True, cs=True)
    polyInfo = cmds.polyInfo(fn=True)
    polyInfoArray = re.findall(r"[\w.-]+", polyInfo[0])
    polyInfoX = float(polyInfoArray[2])
    polyInfoY = float(polyInfoArray[3])
    polyInfoZ = float(polyInfoArray[4])
    
    cmds.polySubdivideFacet(dv=1)
        
    for i in range (4):
       morph = random.uniform(-0.05,-0.1)
       cmds.polyExtrudeFacet(s=(capSize+morph,topStep+morph,capSize+morph), t=(polyInfoX/45, polyInfoY/40, polyInfoZ/45),  d=1)       
       capSize = capRoundness * capSize / 100
       topStep -=0.2
       #polyInfoY -=0.2
       cmds.hyperShade(assign = CapShader)
       
    #Scale top of Cap    
    #cmds.scale(0.8,1.0,0.8, r=True)
    
    #Create Base
    cmds.select(Cylinder[0]+'.f[42]')
 
    cmds.scale(3.5,1.5,3.5, r=True)
    cmds.select(Cylinder[0]+'.f[86:127]')
    cmds.scale(baseBulge,1.0,baseBulge, r=True)
    cmds.select(Cylinder[0]+'.f[170:211]')
    cmds.scale(baseBulge/2,1.0,baseBulge/2, r=True)
    cmds.polySubdivideFacet (dv=0) 
    cmds.select(clear=True)
    cmds.select('MushroomOriginal')
    
    # Gill Shader
    if stemBulge_Var:  
        cmds.select(Cylinder[0]+'.f[548:589]')
        cmds.hyperShade(assign = GrillShader)
        cmds.select(Cylinder[0]+'.f[506:547]')
        cmds.hyperShade(assign = GrillShader)
    else:
        cmds.select(Cylinder[0]+'.f[338:379]')
        cmds.hyperShade(assign = GrillShader)
        cmds.select(Cylinder[0]+'.f[380:421]')
        cmds.hyperShade(assign = GrillShader)
        
       
    #Add Noise 
    if noise_Var:
        addNoise(noiseAmount)
        capSelection = 11500
    cmds.select(clear=True)
    
    #Add Spots     
def addSpots (winID, spotAmount, spotSize, spotSpread, spotStartPos):
    
    MushroomOriginal = 'MushroomOriginal'   
    capSelection = spotStartPos 
    if noise_Var:
        capSelection = spotStartPos
    for i in range (spotAmount):
        capSpotScale = random.uniform(0.05,0.1)
        capSpotScaleOffset = random.uniform(0.04,0.1)
        cmds.select(MushroomOriginal+'.f['+str(capSelection)+']')
        cmds.scale(capSpotScale,capSpotScale,capSpotScale, r=True, cs=True)
        cmds.move(0,0.03,0, r=True)
        cmds.hyperShade(assign = GrillShader)
        cmds.polyCircularizeFace(divisions=3, radialOffset=spotSize+capSpotScaleOffset, supportingEdges=1)       
        cmds.select(clear=True)
               
        capSelection +=spotSpread
                
def bend(winID, bendAmount):   
    randomBend = random.uniform(-1.5,1.5)
    MushroomOriginal = 'MushroomOriginal'
    cmds.select(MushroomOriginal+'.f[950]')                
    cmds.softSelect(sse=1, ssd = 5, ssc='0,1,1,1,0.6,2')
    cmds.rotate(0,0,bendAmount+randomBend, r=True, ws=True)   
     
def noise(input):
    global noise_Var
    noise_Var = input
    
def stemB(inputBulge):
    global stemBulge_Var
    stemBulge_Var = inputBulge
           
def addNoise(noiseAmount):
    
    cmds.select('MushroomOriginal')

    vtxCount = list(range(cmds.polyEvaluate(v=True)))
    random.shuffle(vtxCount)
    values = [random.triangular(0,noiseAmount,0) for i in range(10)]
    values_count = len(values)
    optimize_setter = []
    
    for x in vtxCount:
        mod = x % values_count
        optimize_setter += [values[mod-1]*1,values[mod-1]*1,values[mod-1]*1]
    cmds.setAttr('MushroomOriginal.vtx[:]', *optimize_setter)
    cmds.polySmooth(c=1,dv=2,kb=True,ro=1)  
  
def uvw(winID):
    
    cmds.select("MushroomOriginal")
    cmds.ls( selection=True )
    cmds.polyProjection('MushroomOriginal.f[*]', type='Cylindrical', ch=1, ibd=True, sf=True)         
     
	#Close UI
def cancelProc(winID, *pArgs):
    cmds.deleteUI(winID)
    
def undoAction(winID):   
    cmds.undo()

    #Create UI            
def createUI():
         
    winID = cmds.window( title = 'Mushroom Tool', w = 350, h = 100)
    if cmds.window(winID, exists = True):
        cmds.deleteUI(winID)
    winID = cmds.window( title = 'Mushroom Tool', w = 200, h = 100)
    cmds.rowColumnLayout( numberOfRows=28, cs=[50,50], rs=[50,50], rh=[40,40], adjustableColumn=True)
    
    cmds.text( label='Mushroom Tool', align='center', h=40, fn='boldLabelFont' )
       
    #Mushroom
    cmds.separator(h=15)      
    cmds.button(label = "Make Mushroom", h=40,command = lambda *args: Mushroom(winID, cmds.floatSliderGrp(noiseAmount, query=True, value=True), 
    cmds.intSliderGrp(stemSections, query=True, value=True), 
    cmds.floatSliderGrp(mushroomHeight, query=True, value=True), 
    cmds.floatSliderGrp(mushroomWidth, query=True, value=True), 
    cmds.floatSliderGrp(stemWidth, query=True, value=True), 
    cmds.floatSliderGrp(moveStem, query=True, value=True),
    cmds.floatSliderGrp(capSize, query=True, value=True),
    cmds.floatSliderGrp(capSizeBase, query=True, value=True),
    cmds.floatSliderGrp(stemRotate, query=True, value=True), 
    cmds.floatSliderGrp(capHeight, query=True, value=True),
    cmds.floatSliderGrp(stemHeight, query=True, value=True),          
    cmds.floatSliderGrp(capBaseHeight, query=True, value=True), 
    cmds.floatSliderGrp(baseBulge, query=True, value=True), 
    cmds.floatSliderGrp(bendScale, query=True, value=True))) 
     
    #Base
    cmds.separator(h=15)  
    cmds.text( label='Base Options', align='center', h=40, fn='boldLabelFont' )
    mushroomHeight = cmds.floatSliderGrp(label='Base Height', minValue=0.1, maxValue=10, value=0.14, step=0.1, field=True)
    mushroomWidth = cmds.floatSliderGrp(label='Base Width', minValue=0.1, maxValue=2, value=0.5, step=0.1, field=True)
    baseBulge = cmds.floatSliderGrp(label='Base Bulge', minValue=1, maxValue=5, value=1.5, step=0.1, field=True)
    
    #Stem
    cmds.separator(h=15)  
    cmds.text( label='Stem Options', align='center', h=40, fn='boldLabelFont' )
    stemSections = cmds.intSliderGrp(label='Step Sections', minValue=1, maxValue=4, value=4, step=1, field=True) 
    stemHeight = cmds.floatSliderGrp(label='Stem Height', minValue=1.0, maxValue=5, value=1.0, step=0.1, pre=2, field=True)  
    stemWidth = cmds.floatSliderGrp(label='Stem Width', minValue=1.0, maxValue=4.0, value=2.0, step=0.1, pre=2, field=True)
    moveStem = cmds.floatSliderGrp(label='Stem Move', minValue=0.0, maxValue=2, value=0.0, step=0.1, pre=2, field=True)
    stemRotate = cmds.floatSliderGrp(label='Stem Bend', minValue=0.0, maxValue=15, value=0.0, step=0.1, pre=2, field=True)
    bendScale = cmds.floatSliderGrp(label='Stem Bend Scale', minValue=-2.0, maxValue=2, value=0.0, step=0.01, pre=2, field=True)
    cmds.separator(h=15)  
    cmds.text( label='Stem Bulge', align='center', h=40, fn='boldLabelFont' )
    cmds.radioCollection()
    cmds.radioButton( label='On', align='center',  onCommand=lambda x:stemB(True))
    cmds.radioButton( label='Off', align='center', sl=True, onCommand=lambda x:stemB(False))
    
    #Cap 
    cmds.separator(h=15)  
    cmds.text( label='Cap Options', align='center', h=40, fn='boldLabelFont' )
    capSize = cmds.floatSliderGrp(label='Cap Pointy', minValue=0.2, maxValue=1, value=0.8, step=0.01, pre=2, field=True)
    #capRoundness = cmds.floatSliderGrp(label='Cap Roundness', minValue=1, maxValue=100, value=80, step=1, field=True)
    capSizeBase = cmds.floatSliderGrp(label='Cap Base Size', minValue=1, maxValue=10, value=2.0, step=1, field=True)
    capHeight = cmds.floatSliderGrp(label='Cap Height', minValue=0.5, maxValue=3, value=1, step=0.1, field=True)
    capBaseHeight = cmds.floatSliderGrp(label='Cap Base Height', minValue=0.1, maxValue=2, value=0.2, step=0.1, field=True)
    
    #bender
    cmds.separator(h=15)  
    cmds.text( label='Bend', align='center', h=40, fn='boldLabelFont' )
    cmds.button(label = "Bend Mushroom", h=40,command = lambda *args: bend(winID, cmds.floatSliderGrp(bendAmount, query=True, value=True)))
    bendAmount = cmds.floatSliderGrp(label='Bend Amount', minValue=0.01, maxValue=35, value=0.05, step=0.01, pre=2, field=True)
   
    #Spots
    cmds.separator(h=15)  
    cmds.text( label='Spots', align='center', h=40, fn='boldLabelFont' )
    cmds.button(label = "Make Spots", h=40,command = lambda *args: addSpots(winID, cmds.intSliderGrp(spotAmount, query=True, value=True),
    cmds.floatSliderGrp(spotSize, query=True, value=True), 
    cmds.intSliderGrp(spotSpread, query=True, value=True),
    cmds.intSliderGrp(spotStartPos, query=True, value=True))) 
      
    spotAmount = cmds.intSliderGrp(label='Spot Amount', minValue=1, maxValue=100, value=20, step=1, field=True)
    spotSize = cmds.floatSliderGrp(label='Spot Size', minValue=0.01, maxValue=2, value=0.01, step=0.01, pre=2, field=True)
    spotSpread = cmds.intSliderGrp(label='Spot Spread', minValue=10, maxValue=200, value=80, step=1, field=True)
    spotStartPos = cmds.intSliderGrp(label='Spot Start Position', minValue=500, maxValue=12000, value=10500, step=1, field=True)
    cmds.separator(h=15) 
        
    #Noise
    cmds.text( label='Noise', align='center', h=40, fn='boldLabelFont' )
    cmds.radioCollection()
    cmds.radioButton( label='On', align='center', sl=True, onCommand=lambda x:noise(True))
    cmds.radioButton( label='Off', align='center',  onCommand=lambda x:noise(False))
    noiseAmount = cmds.floatSliderGrp(label='Noise Amount', minValue=0.01, maxValue=1, value=0.05, step=0.01, pre=2, field=True)
    
    cmds.separator(h=15)  
    
    #UV
    cmds.button(label = "UVs", h=40,command = lambda *args: uvw(winID))   
         
    #Remove All
    cmds.button(label = "Undo", h=40,command = lambda *args: undoAction(winID))   
    
    cmds.separator(h=25) 
     
    #Exit    
    cmds.button(label = "Exit", h=40, command = lambda *args: cancelProc(winID))
    cmds.showWindow()    

if __name__ == "__main__":
    createUI()
