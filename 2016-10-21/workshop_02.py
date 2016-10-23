from larlib import *
import csv


def ggpl_bone_structure(file_name):

	pillarSec = ()
	beamSec = ()
	pillarDistY = []
	pillarDistX = []
	beamDistY = []

	with open(file_name, 'rb') as f:
		reader = csv.reader(f, delimiter=';', quotechar=',')
		for i, row in enumerate(reader):
			#print i
			if (i+1)%2.0==0:
				#print type (row[0])
				#print (row[0])
				#print type (row[3])
				pillarSec = row[0]
				pillarSec = tuple(pillarSec.split(','))
				pillarSec = map(float,pillarSec)
				#print (pillarSec)
				beamSec = row[1]
				beamSec = tuple(beamSec.split(','))
				beamSec = map(float,beamSec)
				#print(beamSec)
				pillarDistY = row[2]
				pillarDistY = pillarDistY.split(',')
				pillarDistY = map(float,pillarDistY)
				#print (pillarDistY)
				beamDistY = row[3]
				beamDistY = beamDistY.split(',')
				beamDistY = map(float,beamDistY)
				#print(pillarDistX)
			else:
				for i in row:
					#print "ok"
					pillarDistX.append(i)
				pillarDistX = ''.join(pillarDistX)
				pillarDistX = pillarDistX.split(',')
				pillarDistX = map(float,pillarDistX)
	#pillarSec = tuple(pillarSec.split(','))
	#beamSec = tuple(beamSec.split(','))
	(px,py) = pillarSec
	(bx,bz) = beamSec

    #CREAZIONE DEI PILASTRI
	pillarsX = []
	for i in range(0, len(pillarDistY)):
		pillarsX.extend([py, -pillarDistY[i]])
	pillarsX.extend([py])

	pillarsY = []
	for i in range(0,len(beamDistY)):
		pillarsY.extend([beamDistY[i], -bz])  

	pillarsX2 = []
	for i in range(0, len(pillarDistX)):
		pillarsX2.extend([px, -pillarDistX[i]])
	pillarsX2.extend([py]) 

	pillarsBases2 = PROD([QUOTE(pillarsX2), QUOTE(pillarsX)])
	pillarsBases = PROD([Q(px),QUOTE(pillarsX)])
	#pillarBasesY = PROD([QUOTE(pillarsY2), Q(px)])
	pillars = PROD([pillarsBases2, QUOTE(pillarsY)])
	#VIEW(pillars)

    #CREAZIONE DELLE TRAVI

	beamsX = []
	for i in range(0, len(pillarDistY)):
		beamLenght = pillarDistY[i] + py
		if i==0 or i == len(pillarDistY) - 1:
			beamLenght += py/2.0 + (py/2.0 if len(pillarDistY) == 1 else 0)
		beamsX.extend([beamLenght])

	beamsY = []
	for i in range(0,len(beamDistY)):
		beamsY.extend([-beamDistY[i], bz])  

	beamsX2 = []
	for i in range(0, len(pillarDistX)):
		beamLenght = pillarDistX[i] + px
		if i==0 or i == len(pillarDistX) - 1:
			beamLenght += py/2.0 + (py/2.0 if len(pillarDistX) == 1 else 0)
		beamsX2.extend([beamLenght])


	beamsBases = PROD([QUOTE(pillarsX2),QUOTE(beamsX)])
	beamsBases2 = PROD([QUOTE(beamsX2),QUOTE(pillarsX)])
	beams = PROD([beamsBases, QUOTE(beamsY)])
	beams2 = PROD([beamsBases2, QUOTE(beamsY)])
	#VIEW(beams)
	#VIEW(beams2)
	beamsTot = STRUCT([beams,beams2])
	#VIEW(beamsTot)
	
	return STRUCT([pillars,beamsTot])

s = ggpl_bone_structure("frame_data_441481.csv")
VIEW(s)
#skeleton = COLOR(BLUE)(SKELETON(1)(s))
#VIEW(STRUCT([s, skeleton]))
