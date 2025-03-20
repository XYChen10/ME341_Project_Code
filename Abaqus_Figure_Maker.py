import csv
import os
from abaqus import *
from abaqusConstants import *
import __main__
import section
import regionToolset
import displayGroupMdbToolset as dgm
import part
import material
import assembly
import step
import interaction
import load
import mesh
import optimization
import job
import sketch
import visualization
import xyPlot
import displayGroupOdbToolset as dgo
import connectorBehavior
import odbAccess
import math

# Define design variables
L = 3890.0 # Shell length
R = 978.0 # Endcap radius
t1 = 207.0 # shell thickness 
t2 = 115.0 # End cap thickness
t3 = 99.0 # Nozzle thickness
y_nozzle_position = 150.0 # Nozzle y-position
nozzle_radius = 150.0 # Nozzle radius

# Make new abaqus model (remove the need for new model database step)
Mdb()

# Creating the part on abaqus
s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=1500.0)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=STANDALONE)
s.ConstructionLine(point1=(0.0, -750), point2=(0.0, 750))
s.FixedConstraint(entity=g[2])
s.Spot(point=(0.0, 0.0))
s.FixedConstraint(entity=v[0])
s.FixedConstraint(entity=v[0])
s.ConstructionLine(point1=(0.0, 0.0), angle=0.0)
s.CoincidentConstraint(entity1=v[0], entity2=g[3], addUndoState=False)
s.HorizontalConstraint(entity=g[3], addUndoState=False)
s.Spot(point=(350.0, 0.0))
s.CoincidentConstraint(entity1=v[1], entity2=g[3], addUndoState=False)
s.Spot(point=(0.0, 450.0))
s.CoincidentConstraint(entity1=v[2], entity2=g[2], addUndoState=False)
s.CircleByCenterPerimeter(center=(0.0, 450.0), point1=(350.0, 450.0))
s.autoTrimCurve(curve1=g[4], point1=(-203.102996826172, 536.772766113281))
s.autoTrimCurve(curve1=g[6], point1=(328.960479736328, 264.485412597656))
s.Line(point1=(350.0, 0.0), point2=(350.0, 450.0))
s.VerticalConstraint(entity=g[7], addUndoState=False)
s.sketchOptions.setValues(constructionGeometry=ON)
s.Line(point1=(0.0, 450.0), point2=(350.0, 450.0))
s.HorizontalConstraint(entity=g[8], addUndoState=False)
s.setAsConstruction(objectList=(g[8], ))
s.Spot(point=(0.0, 750.0))
s.CoincidentConstraint(entity1=v[12], entity2=g[2], addUndoState=False)
s.CoincidentConstraint(entity1=v[6], entity2=v[12])
s.CoincidentConstraint(entity1=v[6], entity2=g[2])

# Selection of endcap radius (R) and shell length (L)
s.RadialDimension(curve=g[5], textPoint=(101.609802246094, 537.171142578125), radius=R)
s.ObliqueDimension(vertex1=v[10], vertex2=v[5], textPoint=(602.590393066406, 345.290863037109), value=L)

# Setting parameter names
s = mdb.models['Model-1'].sketches['__profile__']
s.sketchOptions.setValues(constructionGeometry=ON)
s.assignCenterline(line=g[2])
p = mdb.models['Model-1'].Part(name='PressureVesselPart', dimensionality=THREE_D, type=DEFORMABLE_BODY)
p = mdb.models['Model-1'].parts['PressureVesselPart']
p.BaseShellRevolve(sketch=s, angle=180.0, flipRevolveDirection=OFF)
s.unsetPrimaryObject()
p = mdb.models['Model-1'].parts['PressureVesselPart']
del mdb.models['Model-1'].sketches['__profile__']

p = mdb.models['Model-1'].parts['PressureVesselPart']
e = p.edges
p.DatumPlaneByThreePoints(point1=p.InterestingPoint(edge=e[3], rule=MIDDLE), 
point2=p.InterestingPoint(edge=e[1], rule=MIDDLE), 
point3=p.InterestingPoint(edge=e[4], rule=MIDDLE))

# offset datum planels (bounds for design)
p = mdb.models['Model-1'].parts['PressureVesselPart']
p.DatumPlaneByPrincipalPlane(principalPlane=YZPLANE, offset= R + 150.0)
p = mdb.models['Model-1'].parts['PressureVesselPart']
p.DatumPlaneByPrincipalPlane(principalPlane=YZPLANE, offset= -150.0 - R)

p = mdb.models['Model-1'].parts['PressureVesselPart']
f = p.faces
pickedFaces = f.getSequenceFromMask(mask=('[#3 ]', ), )
d1 = p.datums
p.PartitionFaceByDatumPlane(datumPlane=d1[2], faces=pickedFaces)
p = mdb.models['Model-1'].parts['PressureVesselPart']
e1, d2 = p.edges, p.datums
t = p.MakeSketchTransform(sketchPlane=d2[2], sketchUpEdge=e1[3], 
sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(0.0, 625.0, 
250.0))
s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
sheetSize=4119.46, gridSpacing=102.98, transform=t)
g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
s1.setPrimaryObject(option=SUPERIMPOSE)
p = mdb.models['Model-1'].parts['PressureVesselPart']
p.projectReferencesOntoSketch(sketch=s1, filter=COPLANAR_EDGES)
p = mdb.models['Model-1'].parts['PressureVesselPart']
e, p1 = p.edges, p.elemEdges
p.projectEdgesOntoSketch(sketch=s1, edges=(e[7], ), constrainToBackground=False)
p = mdb.models['Model-1'].parts['PressureVesselPart']
e1, p2 = p.edges, p.elemEdges
p.projectEdgesOntoSketch(sketch=s1, edges=(e1[3], ), constrainToBackground=False)
s1.Spot(point=(-250.0, -625.0))
s1.CoincidentConstraint(entity1=v[7], entity2=g[7], addUndoState=False)
s1.Spot(point=(-250.0, -192.329895019531))
s1.CoincidentConstraint(entity1=v[8], entity2=g[6], addUndoState=False)
s1.CircleByCenterPerimeter(center=(-250.0, -192.329895019531), point1=(-102.98, 
-180.215))
s1.VerticalDimension(vertex1=v[8], vertex2=v[4], textPoint=(-448.049194335938, 
-488.958068847656), value=y_nozzle_position)

# Nozzle radius
s1.RadialDimension(curve=g[9], textPoint=(-59.35693359375, -79.4198608398438), 
radius=nozzle_radius)
s1.FixedConstraint(entity=v[4])
s=mdb.models['Model-1'].sketches['__profile__']
s1.autoTrimCurve(curve1=g[8], point1=(257.375457763672, 132.073974609375))
s1.autoTrimCurve(curve1=g[7], point1=(130.089324951172, -626.151672363281))
s1.undo()
s1.setAsConstruction(objectList=(g[7], ))

p = mdb.models['Model-1'].parts['PressureVesselPart']
e, d1 = p.edges, p.datums
p.CutExtrude(sketchPlane=d1[2], sketchUpEdge=e[3], sketchPlaneSide=SIDE1, 
sketchOrientation=RIGHT, sketch=s1, flipExtrudeDirection=OFF)
s1.unsetPrimaryObject()
del mdb.models['Model-1'].sketches['__profile__']

p = mdb.models['Model-1'].parts['PressureVesselPart']
e1, d2 = p.edges, p.datums
t = p.MakeSketchTransform(sketchPlane=d2[3], sketchUpEdge=e1[4], 
sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(650.0, 625.0, 249.999854))
s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
sheetSize=4119.46, gridSpacing=102.98, transform=t)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=SUPERIMPOSE)
p = mdb.models['Model-1'].parts['PressureVesselPart']
p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)
p = mdb.models['Model-1'].parts['PressureVesselPart']
e, p1 = p.edges, p.elemEdges
p.projectEdgesOntoSketch(sketch=s, edges=(e[5], ), constrainToBackground=False)
s.setAsConstruction(objectList=(g[3], ))
s.Spot(point=(249.999854, -625.0))
s.CoincidentConstraint(entity1=v[2], entity2=g[3], addUndoState=False)
s.Spot(point=(249.999854, -228.820739746094))
s.CoincidentConstraint(entity1=v[3], entity2=g[2], addUndoState=False)
s.CircleByCenterPerimeter(center=(249.999854, -228.820739746094), point1=(411.92, -283.195))

# Nozzle y-position
s.VerticalDimension(vertex1=v[3], vertex2=v[1], textPoint=(600.599860103516, -442.782989501953), value=y_nozzle_position)
s.autoTrimCurve(curve1=g[4], point1=(390.489020259766, -369.481109619141))
s.autoTrimCurve(curve1=g[5], point1=(408.328619869141, -220.896179199219))
s.CoincidentConstraint(entity1=v[9], entity2=g[2])
s.CoincidentConstraint(entity1=v[10], entity2=g[2])

# Nozzle radius
s.RadialDimension(curve=g[6], textPoint=(3.90189257421875, 17.4852905273438), radius=nozzle_radius)

p = mdb.models['Model-1'].parts['PressureVesselPart']
f = p.faces
e1, d1 = p.edges, p.datums
p.ShellExtrude(sketchPlane=d1[3], sketchUpEdge=e1[4], upToFace=f[1], 
sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, sketch=s, 
flipExtrudeDirection=ON)
s.unsetPrimaryObject()
del mdb.models['Model-1'].sketches['__profile__']

p = mdb.models['Model-1'].parts['PressureVesselPart']
s1 = p.features['Shell extrude-1'].sketch
mdb.models['Model-1'].ConstrainedSketch(name='__edit__', objectToCopy=s1)
s2 = mdb.models['Model-1'].sketches['__edit__']
g, v, d, c = s2.geometry, s2.vertices, s2.dimensions, s2.constraints
s2.setPrimaryObject(option=SUPERIMPOSE)
p.projectReferencesOntoSketch(sketch=s2, upToFeature=p.features['Shell extrude-1'], filter=COPLANAR_EDGES)
d[0].setValues(value=600, )
d[0].setValues(value=400, )
s2.unsetPrimaryObject()
del mdb.models['Model-1'].sketches['__edit__']

p = mdb.models['Model-1'].parts['PressureVesselPart']
s = p.features['Shell extrude-1'].sketch
mdb.models['Model-1'].ConstrainedSketch(name='__edit__', objectToCopy=s)
s1 = mdb.models['Model-1'].sketches['__edit__']
g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
s1.setPrimaryObject(option=SUPERIMPOSE)
p.projectReferencesOntoSketch(sketch=s1, upToFeature=p.features['Shell extrude-1'], filter=COPLANAR_EDGES)
s1.CoincidentConstraint(entity1=v[1], entity2=g[3])
s1.CoincidentConstraint(entity1=v[1], entity2=g[3])
s1.CoincidentConstraint(entity1=v[1], entity2=g[2])
s1.CoincidentConstraint(entity1=v[1], entity2=g[3])
d[0].setValues(value=600, )
s1.undo()
s1.FixedConstraint(entity=g[3])
s=mdb.models['Model-1'].sketches['__edit__']
# s.Parameter(name='NozzleYpositionExtrude', path='dimensions[0]', expression='400')
# s.Parameter(name='NozzleRadiusExtrude', path='dimensions[1]', expression='150', previousParameter='NozzleYpositionExtrude')
s1.unsetPrimaryObject()
p = mdb.models['Model-1'].parts['PressureVesselPart']
p.features['Shell extrude-1'].setValues(sketch=s1)

p = mdb.models['Model-1'].parts['PressureVesselPart']
f1, e, d2 = p.faces, p.edges, p.datums
t = p.MakeSketchTransform(sketchPlane=d2[4], sketchUpEdge=e[10], sketchPlaneSide=SIDE2, origin=(-650.0, 625.0, 249.999854))
s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=4119.46, gridSpacing=102.98, transform=t)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=SUPERIMPOSE)
p = mdb.models['Model-1'].parts['PressureVesselPart']
p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)
p = mdb.models['Model-1'].parts['PressureVesselPart']
e1, p2 = p.edges, p.elemEdges
p.projectEdgesOntoSketch(sketch=s, edges=(e1[13], ), constrainToBackground=False)
p = mdb.models['Model-1'].parts['PressureVesselPart']
e, p1 = p.edges, p.elemEdges
p.projectEdgesOntoSketch(sketch=s, edges=(e[10], ), constrainToBackground=False)
s.setAsConstruction(objectList=(g[3], g[4]))
s.FixedConstraint(entity=g[3])
s.FixedConstraint(entity=g[4])
s.Spot(point=(-249.999854, -625.0))
s.CoincidentConstraint(entity1=v[3], entity2=g[3], addUndoState=False)
s.undo()
s.rectangle(point1=(-249.999854, -107.9716796875), point2=(250.000146, -379.386779785156))
s.CoincidentConstraint(entity1=v[3], entity2=g[2], addUndoState=False)
s.CoincidentConstraint(entity1=v[5], entity2=g[4], addUndoState=False)
s.DistanceDimension(entity1=g[8], entity2=g[6], textPoint=(-368.901739986328, -254.575500488281), value=150.0)
s.VerticalDimension(vertex1=v[4], vertex2=v[0], textPoint=(-446.252081783203, -551.745239257812), value=300.0)
s=mdb.models['Model-1'].sketches['__profile__']
p = mdb.models['Model-1'].parts['PressureVesselPart']
f = p.faces
pickedFaces = f.getSequenceFromMask(mask=('[#8 ]', ), )
f, e1, d1 = p.faces, p.edges, p.datums
p.PartitionFaceBySketchThruAll(sketchPlane=d1[4], sketchUpEdge=e1[10], faces=pickedFaces, sketchPlaneSide=SIDE2, sketch=s)
s.unsetPrimaryObject()
del mdb.models['Model-1'].sketches['__profile__']

# Setting the material
mdb.models['Model-1'].Material(name='SAS516GR70', description='From Reference Paper')
mdb.models['Model-1'].materials['SAS516GR70'].Density(table=((7.75e-09, ), ))
mdb.models['Model-1'].materials['SAS516GR70'].Elastic(table=((193000.0, 0.3), ))
mdb.models['Model-1'].materials['SAS516GR70'].Plastic(scaleStress=None, table=((260.0, 0.0), ))

# Assigning part thickness
mdb.models['Model-1'].HomogeneousShellSection(name='EndCapThickness', 
preIntegrate=OFF, material='SAS516GR70', thicknessType=UNIFORM, 
thickness=t2, thicknessField='', nodalThicknessField='', 
idealization=NO_IDEALIZATION, poissonDefinition=DEFAULT, 
thicknessModulus=None, temperature=GRADIENT, useDensity=OFF, 
integrationRule=SIMPSON, numIntPts=5)
mdb.models['Model-1'].HomogeneousShellSection(name='ShellThickness', 
preIntegrate=OFF, material='SAS516GR70', thicknessType=UNIFORM, 
thickness=t1, thicknessField='', nodalThicknessField='', 
idealization=NO_IDEALIZATION, poissonDefinition=DEFAULT, 
thicknessModulus=None, temperature=GRADIENT, useDensity=OFF, 
integrationRule=SIMPSON, numIntPts=5)
mdb.models['Model-1'].HomogeneousShellSection(name='NozzleThickness', 
preIntegrate=OFF, material='SAS516GR70', thicknessType=UNIFORM, 
thickness=t3, thicknessField='', nodalThicknessField='', 
idealization=NO_IDEALIZATION, poissonDefinition=DEFAULT, 
thicknessModulus=None, temperature=GRADIENT, useDensity=OFF, 
integrationRule=SIMPSON, numIntPts=5)

p = mdb.models['Model-1'].parts['PressureVesselPart']
f = p.faces
faces = f.getSequenceFromMask(mask=('[#48 ]', ), )
region = regionToolset.Region(faces=faces)
p = mdb.models['Model-1'].parts['PressureVesselPart']
p.SectionAssignment(region=region, sectionName='EndCapThickness', offset=0.0, 
offsetType=MIDDLE_SURFACE, offsetField='', 
thicknessAssignment=FROM_SECTION)

p = mdb.models['Model-1'].parts['PressureVesselPart']
f = p.faces
faces = f.getSequenceFromMask(mask=('[#33 ]', ), )
region = regionToolset.Region(faces=faces)
p = mdb.models['Model-1'].parts['PressureVesselPart']
p.SectionAssignment(region=region, sectionName='ShellThickness', offset=0.0, 
offsetType=MIDDLE_SURFACE, offsetField='', 
thicknessAssignment=FROM_SECTION)

p = mdb.models['Model-1'].parts['PressureVesselPart']
f = p.faces
faces = f.getSequenceFromMask(mask=('[#4 ]', ), )
region = regionToolset.Region(faces=faces)
p = mdb.models['Model-1'].parts['PressureVesselPart']
p.SectionAssignment(region=region, sectionName='NozzleThickness', offset=0.0, 
offsetType=TOP_SURFACE, offsetField='', 
thicknessAssignment=FROM_SECTION)

# Part assembly
a = mdb.models['Model-1'].rootAssembly
a.DatumCsysByDefault(CARTESIAN)
p = mdb.models['Model-1'].parts['PressureVesselPart']
a.Instance(name='PressureVesselPart-1', part=p, dependent=ON)

mdb.models['Model-1'].StaticStep(name='PressureStep', previous='Initial', initialInc=0.1)
a = mdb.models['Model-1'].rootAssembly
s1 = a.instances['PressureVesselPart-1'].faces
side1Faces1 = s1.getSequenceFromMask(mask=('[#7b ]', ), )
region = regionToolset.Region(side1Faces=side1Faces1)
mdb.models['Model-1'].Pressure(name='PressureLoad', 
createStepName='PressureStep', region=region, distributionType=UNIFORM, 
field='', magnitude=10.0, amplitude=UNSET)

a = mdb.models['Model-1'].rootAssembly
e1 = a.instances['PressureVesselPart-1'].edges
edges1 = e1.getSequenceFromMask(mask=('[#38d428 ]', ), )
region = regionToolset.Region(edges=edges1)
mdb.models['Model-1'].ZsymmBC(name='Z-Symmetric', createStepName='PressureStep', region=region, localCsys=None)

a = mdb.models['Model-1'].rootAssembly
e1 = a.instances['PressureVesselPart-1'].edges
edges1 = e1.getSequenceFromMask(mask=('[#10004 ]', ), )
region = regionToolset.Region(edges=edges1)
mdb.models['Model-1'].YsymmBC(name='Y-Symmetry', createStepName='PressureStep', region=region, localCsys=None)

a = mdb.models['Model-1'].rootAssembly
f1 = a.instances['PressureVesselPart-1'].faces
faces1 = f1.getSequenceFromMask(mask=('[#20 ]', ), )
region = regionToolset.Region(faces=faces1)
mdb.models['Model-1'].DisplacementBC(name='SaddleBC', createStepName='Initial', 
region=region, u1=SET, u2=SET, u3=UNSET, ur1=UNSET, ur2=UNSET, 
ur3=UNSET, amplitude=UNSET, distributionType=UNIFORM, fieldName='', 
localCsys=None)

del mdb.models['Model-1'].boundaryConditions['Y-Symmetry']
del mdb.models['Model-1'].boundaryConditions['Z-Symmetric']

a = mdb.models['Model-1'].rootAssembly
e1 = a.instances['PressureVesselPart-1'].edges
edges1 = e1.getSequenceFromMask(mask=('[#10004 ]', ), )
region = regionToolset.Region(edges=edges1)
mdb.models['Model-1'].YsymmBC(name='Y-Symmetry', createStepName='Initial', region=region, localCsys=None)

a = mdb.models['Model-1'].rootAssembly
e1 = a.instances['PressureVesselPart-1'].edges
edges1 = e1.getSequenceFromMask(mask=('[#38d428 ]', ), )
region = regionToolset.Region(edges=edges1)
mdb.models['Model-1'].ZsymmBC(name='Z-Symmetry', createStepName='Initial', region=region, localCsys=None)

p = mdb.models['Model-1'].parts['PressureVesselPart']
p = mdb.models['Model-1'].parts['PressureVesselPart']
f = p.faces
pickedRegions = f.getSequenceFromMask(mask=('[#6b ]', ), )
p.setMeshControls(regions=pickedRegions, elemShape=QUAD, technique=STRUCTURED)

# Creating the mesh
p = mdb.models['Model-1'].parts['PressureVesselPart']
f = p.faces
pickedRegions = f.getSequenceFromMask(mask=('[#14 ]', ), )
p.setMeshControls(regions=pickedRegions, elemShape=QUAD)
p = mdb.models['Model-1'].parts['PressureVesselPart']
p.seedPart(size=20.0, deviationFactor=0.1, minSizeFactor=0.1)
p = mdb.models['Model-1'].parts['PressureVesselPart']
p.generateMesh()

a1 = mdb.models['Model-1'].rootAssembly
a1.regenerate()
a = mdb.models['Model-1'].rootAssembly

mdb.models['Model-1'].HistoryOutputRequest(name='H-Output-2', 
createStepName='PressureStep', variables=('IRA1', 'IRA2', 'IRA3', 
'IRAR1', 'IRAR2', 'IRAR3', 'IRF1', 'IRF2', 'IRF3', 'IRM1', 'IRM2', 
'IRM3', 'CSTRESS', 'CDSTRESS', 'CDISP', 'CFNM', 'CFN1', 'CFN2', 'CFN3', 
'CFSM', 'CFS1', 'CFS2', 'CFS3', 'CFTM', 'CFT1', 'CFT2', 'CFT3', 
'CICPS', 'CMNM', 'CMN1', 'CMN2', 'CMN3', 'CMSM', 'CMS1', 'CMS2', 
'CMS3', 'CMTM', 'CMT1', 'CMT2', 'CMT3', 'CAREA', 'CTRQ', 'XN1', 'XN2', 
'XN3', 'XS1', 'XS2', 'XS3', 'XT1', 'XT2', 'XT3', 'PPRESS', 'ALLAE', 
'ALLCD', 'ALLDMD', 'ALLEE', 'ALLFD', 'ALLIE', 'ALLJD', 'ALLKE', 
'ALLKL', 'ALLPD', 'ALLQB', 'ALLSE', 'ALLSD', 'ALLVD', 'ALLWK', 
'ETOTAL', 'DBS11', 'DBS12', 'DBT', 'DBSF', 'OPENBC', 'CRSTS11', 
'CRSTS12', 'CRSTS13', 'ENRRT11', 'ENRRT12', 'ENRRT13', 'EFENRRTR', 
'BDSTAT', 'CSDMG', 'CSMAXSCRT', 'CSMAXUCRT', 'CSQUADSCRT', 
'CSQUADUCRT', 'IRX1', 'IRX2', 'IRX3', 'IRRI11', 'IRRI22', 'IRRI33', 
'IRRI12', 'IRRI13', 'IRRI23', 'IRMASS'))

# This creates the job (pressure analysis of part)
mdb.Job(name='PressueAnalysis', model='Model-1', description='', type=ANALYSIS, 
atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
modelPrint=ON, contactPrint=ON, historyPrint=ON, userSubroutine='', 
scratch='', resultsFormat=BOTH, numThreadsPerMpiProcess=1, 
multiprocessingMode=DEFAULT, numCpus=1, numGPUs=0)

mdb.jobs['PressueAnalysis'].submit(consistencyChecking=OFF)
