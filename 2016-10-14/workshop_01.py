from larlib import *

def buildingStruct(pillarSec, beamSec, pillarDist, beamDist):
	"""
    La funzione crea una struttura di colonne e travi il cui numero e' dato dalle lunghezze delle liste pillarDist e beamDist.
    :param beamSec: dimensione di una singola trave lungo asse x e z.
    :param pillarSec: dimensione di un singolo pilastro lungo asse x e y.
    :param pillarDist: lista di distanze tra i pilastri.
    :param beamDist: lista di distanze tra le travi.
    :return: un oggetto HPC
    """

	(px,py) = pillarSec
	(bx,bz) = beamSec

    #CREAZIONE DEI PILASTRI
	pillarsX = []
	for i in range(0, len(pillarDist)):
		pillarsX.extend([py, -pillarDist[i]])
	pillarsX.extend([py]) 

	pillarsY = []
	for i in range(0,len(beamDist)):
		pillarsY.extend([beamDist[i], -bz])  

	pillarsBases = PROD([Q(px),QUOTE(pillarsX)])
	pillars = PROD([pillarsBases, QUOTE(pillarsY)])

    #CREAZIONE DELLE TRAVI

	beamsX = []
	for i in range(0, len(pillarDist)):
		beamLenght = pillarDist[i] + py
		if i==0 or i == len(pillarDist) - 1:
			beamLenght += py/2.0 + (py/2.0 if len(pillarDist) == 1 else 0)
		beamsX.extend([beamLenght])

	beamsY = []
	for i in range(0,len(beamDist)):
		beamsY.extend([-beamDist[i], bz])  

	beamsBases = PROD([Q(bx),QUOTE(beamsX)])
	beams = PROD([beamsBases, QUOTE(beamsY)])

	return STRUCT([pillars,beams])

s = buildingStruct((0.5, 1.0), (0.5, 0.75), [1,0.5,2.0,5,1], [1, 3, 1.5, 0.5, 3])
skeleton = COLOR(BLUE)(SKELETON(1)(s))
VIEW(STRUCT([s, skeleton]))
