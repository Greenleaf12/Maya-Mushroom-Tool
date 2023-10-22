# Mushroom Tool By Rory Gardner

import maya.cmds as cmds
import random
import re
import MASH.api as mapi

noiseAmount = 1.1
noise_Var = True
stemBulge_Var = False
capRoundness = 80
Terrain_Sphere_Var = False
Terrain_Plane_Var = True

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
        cmds.delete("MushroomOriginal")
    if cmds.objExists('Terrain*'):
        cmds.delete('Terrain*')    
    if cmds.objExists('Mushrooms*'):
        cmds.delete('Mushrooms')
           
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
    
    #cmds.polySubdivideFacet(dv=1)
        
    for i in range (4):
       morph = random.uniform(-0.05,-0.1)
       cmds.polyExtrudeFacet(s=(capSize+morph,topStep+morph,capSize+morph), t=(polyInfoX/45, polyInfoY/40, polyInfoZ/45),  d=1)       
       capSize = capRoundness * capSize / 100
       topStep -=0.2
       #polyInfoY -=0.2
       cmds.hyperShade(assign = CapShader)       
    
    #Create Base
    cmds.select(Cylinder[0]+'.f[42]') 
    cmds.scale(2.2,2.2,2.2, r=True)
    cmds.select(Cylinder[0]+'.f[86:127]')
    cmds.scale(baseBulge,1.0,baseBulge, r=True)
    cmds.select(Cylinder[0]+'.f[170:211]')
    cmds.scale(baseBulge/2,1.0,baseBulge/2, r=True)
    cmds.polySubdivideFacet (dv=0) 
    cmds.select(clear=True)
    cmds.select('MushroomOriginal')
    
    #Create Bulb
    cmds.select(Cylinder[0]+'.f[42]') 
    cmds.move(0,-0.4,0, r=True) 
    cmds.polyExtrudeFacet(s=(0.9,0.9,0.9), t=(0, -0.5, 0),  d=1)
    cmds.polyExtrudeFacet(s=(0.8,0.8,0.8), t=(0, -0.4, 0),  d=1)
    cmds.polyExtrudeFacet(s=(0.8,0.8,0.8), t=(0, -0.3, 0),  d=1)      
    
    #Gill Shader
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

    #Spawn On Terrain        
def objTerrainSpawn(winID, noiseAmount, stemSections, mushroomHeight, mushroomWidth, stemWidth, moveStem, capSize, capSizeBase, stemRotate, capHeight, stemHeight, capBaseHeight, baseBulge, bendScale, mushroomAmount):
    
    if cmds.objExists('Terrain*'):
        cmds.delete()
    else:
        #Plane=cmds.polyPlane (w=250,h=250,sx=50,sy=50,name='Terrain')
        sphere=cmds.polySphere (r=100,name='Terrain')
   
    MushroomOrg1=Mushroom(winID, noiseAmount, stemSections, mushroomHeight, mushroomWidth, stemWidth, moveStem, capSize, capSizeBase, stemRotate, capHeight, stemHeight, capBaseHeight, baseBulge, bendScale)
    cmds.select("MushroomOriginal")
    cmds.rename('MushroomOrg1')
    MushroomOrg2=Mushroom(winID, noiseAmount, stemSections, mushroomHeight, mushroomWidth, stemWidth, moveStem, capSize, capSizeBase, stemRotate, capHeight, stemHeight, capBaseHeight, baseBulge, bendScale)
    cmds.select("MushroomOriginal")
    cmds.rename('MushroomOrg2')
    MushroomOrg3=Mushroom(winID, noiseAmount, stemSections, mushroomHeight, mushroomWidth, stemWidth, moveStem, capSize, capSizeBase, stemRotate, capHeight, stemHeight, capBaseHeight, baseBulge, bendScale)
    cmds.select("MushroomOriginal")
    cmds.rename('MushroomOrg3')
    MushroomOrg4=Mushroom(winID, noiseAmount, stemSections, mushroomHeight, mushroomWidth, stemWidth, moveStem, capSize, capSizeBase, stemRotate, capHeight, stemHeight, capBaseHeight, baseBulge, bendScale)
    cmds.select("MushroomOriginal")
    cmds.rename('MushroomOrg4')
    
    terrainShape ="Terrain"

    rockData = {"MushroomOrg1": mushroomAmount, "MushroomOrg2": mushroomAmount, "MushroomOrg3": mushroomAmount, "MushroomOrg4": mushroomAmount} 
    
    numVertex = cmds.polyEvaluate(terrainShape, vertex=True)
    selectedVertices = random.sample(range(numVertex), numVertex)
      
    currentIndex = 0
    for pair in rockData.items():
        for i in range(pair[1]):
            if currentIndex>numVertex-1:
                break
            pos = cmds.pointPosition (terrainShape+".vtx["+str(selectedVertices[currentIndex])+"]", world=True)
            normalX = cmds.polyNormalPerVertex(terrainShape+".vtx["+str(selectedVertices[currentIndex])+"]", query=False, x=True)  
            normalY = cmds.polyNormalPerVertex(terrainShape+".vtx["+str(selectedVertices[currentIndex])+"]", query=False, y=True)  
            normalZ = cmds.polyNormalPerVertex(terrainShape+".vtx["+str(selectedVertices[currentIndex])+"]", query=False, z=True)  
                                               
            newobj = cmds.instance(pair[0])           
            cmds.move(pos[0],pos[1],pos[2],newobj)
            #cmds.rotate(normalX,normalY,normalZ)
            cmds.scale (random.uniform(0.8,1.2),random.uniform(0.5,2.0), random.uniform(0.8,1.2),newobj)
            cmds.rotate(0, random.randint(0,360),0,newobj)

            if pos[1] > 200:
                cmds.delete(newobj)                   
            currentIndex+=1
    
    cmds.delete("MushroomOrg1", "MushroomOrg2", "MushroomOrg3", "MushroomOrg4")
    
    if cmds.objExists('MushroomOrg*'):
        cmds.select("MushroomOrg*")
        cmds.group(name="Mushrooms")

    #Spawn on terrain (MASH)
def mashMushrooms(winID, noiseAmount, stemSections, mushroomHeight, mushroomWidth, stemWidth, moveStem, capSize, capSizeBase, stemRotate, capHeight, stemHeight, capBaseHeight, baseBulge, bendScale, mushroomAmount, mushroomScale):
    
    Mushroom(winID, noiseAmount, stemSections, mushroomHeight, mushroomWidth, stemWidth, moveStem, capSize, capSizeBase, stemRotate, capHeight, stemHeight, capBaseHeight, baseBulge, bendScale)
    
    if cmds.objExists('Terrain*'):
        cmds.delete()
    if Terrain_Sphere_Var == True:       
        sphere=cmds.polySphere (r=150, sy=80, sx=80, name='Terrain')
    if Terrain_Plane_Var == True: 
        Plane=cmds.polyPlane (w=250,h=250,sx=50,sy=50,name='Terrain')
        
    Terrain = "Terrain"
    
    if cmds.objExists('Mushrooms*'):
        cmds.delete('Mushrooms')
                 
    cmds.select("MushroomOriginal")
    
    # create MASH network
    mashNetwork = mapi.Network()
    mashNetwork.createNetwork(name="Mushrooms")
    mashNetwork.meshDistribute(Terrain)
    
    # set MASH points 
    mashNetwork.setPointCount(mushroomAmount)
    cmds.setAttr ("Mushrooms_Distribute.calcRotation", 1)
    cmds.setAttr ("Mushrooms_Distribute.distanceAlongNormal", 0) 
    
    mashNetwork.addNode("MASH_Random")
    cmds.setAttr ("Mushrooms_Random.rotationY", 5)
    cmds.setAttr ("Mushrooms_Random.rotationX", 5)
    cmds.setAttr ("Mushrooms_Random.rotationZ", 5)
    cmds.setAttr ("Mushrooms_Random.scaleX", mushroomScale)
    cmds.setAttr ("Mushrooms_Random.scaleY", mushroomScale)
    cmds.setAttr ("Mushrooms_Random.scaleZ", mushroomScale)
    cmds.setAttr ("Mushrooms_Random.absoluteScale", 1)
    cmds.setAttr ("Mushrooms_Random.uniformRandom", 1)
    
    nodes = mashNetwork.getAllNodesInNetwork()
    
    for node in nodes:
        mashNode = mapi.Node(node)
        falloffs = mashNode.getFalloffs()               
                        
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

def tSphere(TSphereInput):
    global Terrain_Sphere_Var
    Terrain_Sphere_Var = TSphereInput    
        
def tPlane(TPlaneInput):
    global Terrain_Plane_Var
    Terrain_Plane_Var = TPlaneInput
      
def uvw(winID):
    
    cmds.select("MushroomOriginal")
    cmds.ls( selection=True )
    cmds.polyProjection('MushroomOriginal.f[*]', type='Cylindrical', ch=1, ibd=True, sf=True)         
     
	#Close UI
def exitProgram(winID, *pArgs):
    cmds.deleteUI(winID)
    
def undoAction(winID):   
    cmds.undo()

    #Create UI            
def createUI():
         
    winID = cmds.window( title = 'Mushroom Tool', w = 350, h = 100)
    if cmds.window(winID, exists = True):
        cmds.deleteUI(winID)
    winID = cmds.window( title = 'Mushroom Tool', w = 350, h = 100)
    cmds.rowColumnLayout( numberOfRows=27, cs=[10,10], rs=[10,10], rh=[40,40], adjustableColumn=True)
    
    cmds.text( label='Mushroom Tool', align='center', h=40, fn='boldLabelFont' )
    cmds.separator(h=10) 
       
    #Mushroom 
    cmds.button(label = "Make Mushroom", h=40,command = lambda *args: Mushroom(winID, 
    cmds.floatSliderGrp(noiseAmount, query=True, value=True), 
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
    cmds.separator(h=10)  
    cmds.text( label='Base Options', align='center', h=40, fn='boldLabelFont' )
    cmds.separator(h=10)   
    mushroomHeight = cmds.floatSliderGrp(label='Base Height', minValue=0.1, maxValue=10, value=0.14, step=0.1, field=True)
    mushroomWidth = cmds.floatSliderGrp(label='Base Width', minValue=0.1, maxValue=2, value=0.5, step=0.1, field=True)
    baseBulge = cmds.floatSliderGrp(label='Base Bulge', minValue=1, maxValue=5, value=1.5, step=0.1, field=True)
    
    #Stem
    cmds.separator(h=10)  
    cmds.text( label='Stem Options', align='center', h=40, fn='boldLabelFont' )
    cmds.separator(h=10) 
    cmds.radioButtonGrp( label='Stem Skirt', labelArray2=['On', 'Off'], numberOfRadioButtons=2, h=40, 
    onCommand1=lambda x:stemB(True), 
    onCommand2=lambda x:stemB(False))
    
    stemSections = cmds.intSliderGrp(label='Step Sections', minValue=1, maxValue=4, value=4, step=1, field=True) 
    stemHeight = cmds.floatSliderGrp(label='Stem Height', minValue=1.0, maxValue=5, value=1.0, step=0.1, pre=2, field=True)  
    stemWidth = cmds.floatSliderGrp(label='Stem Width', minValue=1.0, maxValue=4.0, value=2.0, step=0.1, pre=2, field=True)
    moveStem = cmds.floatSliderGrp(label='Stem Move', minValue=0.0, maxValue=2, value=0.0, step=0.1, pre=2, field=True)
    stemRotate = cmds.floatSliderGrp(label='Stem Bend', minValue=0.0, maxValue=15, value=0.0, step=0.1, pre=2, field=True)
    bendScale = cmds.floatSliderGrp(label='Stem Bend Scale', minValue=-2.0, maxValue=2, value=0.0, step=0.01, pre=2, field=True)
  
    #Cap 
    cmds.separator(h=10)  
    cmds.text( label='Cap Options', align='center', h=40, fn='boldLabelFont' )
    cmds.separator(h=10)  
    capSize = cmds.floatSliderGrp(label='Cap Pointy', minValue=0.2, maxValue=1, value=0.8, step=0.01, pre=2, field=True)
    #capRoundness = cmds.floatSliderGrp(label='Cap Roundness', minValue=1, maxValue=100, value=80, step=1, field=True)
    capSizeBase = cmds.floatSliderGrp(label='Cap Base Size', minValue=1, maxValue=10, value=2.0, step=1, field=True)
    capHeight = cmds.floatSliderGrp(label='Cap Height', minValue=0.5, maxValue=3, value=1, step=0.1, field=True)
    capBaseHeight = cmds.floatSliderGrp(label='Cap Base Height', minValue=0.1, maxValue=2, value=0.2, step=0.1, field=True)
   
    #Spots
    cmds.separator(h=10)  
    cmds.text( label='Spots', align='center', h=40, fn='boldLabelFont' )
    cmds.separator(h=10) 
    cmds.button(label = "Make Spots", h=40,command = lambda *args: addSpots(winID, cmds.intSliderGrp(spotAmount, query=True, value=True),
    cmds.floatSliderGrp(spotSize, query=True, value=True), 
    cmds.intSliderGrp(spotSpread, query=True, value=True),
    cmds.intSliderGrp(spotStartPos, query=True, value=True))) 
      
    spotAmount = cmds.intSliderGrp(label='Spot Amount', minValue=1, maxValue=100, value=20, step=1, field=True)
    spotSize = cmds.floatSliderGrp(label='Spot Size', minValue=0.01, maxValue=2, value=0.01, step=0.01, pre=2, field=True)
    spotSpread = cmds.intSliderGrp(label='Spot Spread', minValue=10, maxValue=200, value=80, step=1, field=True)
    spotStartPos = cmds.intSliderGrp(label='Spot Start Position', minValue=500, maxValue=12000, value=10500, step=1, field=True)
    cmds.separator(h=10) 
        
    #Noise
    cmds.text( label='Noise', align='center', h=40, fn='boldLabelFont' )
    cmds.separator(h=10)
    cmds.radioButtonGrp( label='Noise', labelArray2=['On', 'Off'], numberOfRadioButtons=2, h=40, onCommand1=lambda x:noise(True), onCommand2=lambda x:noise(False), sl=1) 
    noiseAmount = cmds.floatSliderGrp(label='Noise Amount', minValue=0.01, maxValue=1, value=0.05, step=0.01, pre=2, field=True)
    
    cmds.separator(h=25)  
    
    #Terrain Spawn MASH
    cmds.button(label = "Spawn On Terrain (MASH)", h=40,command = lambda *args: mashMushrooms(winID, 
    cmds.floatSliderGrp(noiseAmount, query=True, value=True), 
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
    cmds.floatSliderGrp(bendScale, query=True, value=True),
    cmds.intSliderGrp(mushroomAmount, query=True, value=True),
    cmds.intSliderGrp(mushroomScale, query=True, value=True)))
    
    cmds.radioButtonGrp( label='Terrain Shape ',  labelArray3=['Plane', 'Sphere', 'None'], numberOfRadioButtons=3, h=50, 
    on1=lambda x:tPlane(True), sl=1, 
    on2=lambda x:tSphere(True),
    of1=lambda x:tPlane(False), 
    of2=lambda x:tSphere(False))
    
    mushroomAmount = cmds.intSliderGrp(label='Mushroom Amount', minValue=1, maxValue=250, value=25, step=1, field=True)
    mushroomScale = cmds.intSliderGrp(label='Mushroom Sale', minValue=1, maxValue=100, value=1, step=1, field=True)
    
    cmds.separator(h=25)  
    
    #UV
    cmds.button(label = "Create UVs", h=40,command = lambda *args: uvw(winID))   
    cmds.separator(h=25)   
      
    #Remove All
    cmds.button(label = "Undo", h=40,command = lambda *args: undoAction(winID))       
    cmds.separator(h=25) 
     
    #Exit    
    cmds.button(label = "Exit", h=40, command = lambda *args: exitProgram(winID))
    cmds.showWindow()    

if __name__ == "__main__":
    createUI()
