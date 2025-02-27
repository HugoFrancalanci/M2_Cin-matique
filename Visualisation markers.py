# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 14:12:28 2025

@author: Francalanci Hugo
"""

import kineticstoolkit.lab as ktk

# Charger le fichier C3D
c3d_file = r"C:\Users\Francalanci Hugo\Code_stage_M2_ISMH\MF01\MF01-MF01-20240101-PROTOCOL01-ANALYTIC1-.c3d"

# Charge le fichier C3D
c3d_data = ktk.read_c3d(c3d_file)

# Liste les marqueurs disponibles
markers_list = list(c3d_data["Points"].data.keys())

# Affichage des marqueurs
print("Liste des marqueurs disponibles dans le fichier C3D :")
for marker in markers_list:
    print(marker)

# Charger les données du fichier C3D
data = ktk.read_c3d(c3d_file)
markers = data["Points"]  # Extraction des marqueurs 3D

# Créer une TimeSeries pour stocker les données des marqueurs
transforms = ktk.TimeSeries(time=markers.time)

# Ajouter les marqueurs à la TimeSeries sous forme de vecteurs 3D
for marker_name in markers.data.keys():
    transforms.data[marker_name] = markers.data[marker_name]  # Pas besoin de transformation

# Lancer l'affichage interactif avec KTK Player
p = ktk.Player(markers)

# Définition des interconnexions
interconnections = p.get_interconnections()

interconnections["LUpperLimb"] = {
    "Color": (0.0, 0.5, 1.0),
    "Links": [
        ["LSCT","LSCT1", "LSCT2", "LGJC", "LCAJ", "LSAA","LSCT", "LACM","LACM2", "LACM3", "LSRS"],         
        ["LHUM1", "LHUM2", "LHUM3", "LHUM4","LHUM1"],
        ["LHME", "LEJC", "LHLE"],       
        ["LHME","LRSP", "LUSP", "LHLE"],
    ],
}

interconnections["RUpperLimb"] = {
    "Color": (1.0, 0.5, 0.0),
    "Links": [
        ["RSCT","RSCT1", "RSCT2", "RGJC", "RCAJ", "RSAA","RSCT", "RACM","RACM2", "RACM3", "RSRS"],         
        ["RHUM1", "RHUM2", "RHUM3", "RHUM4","RHUM1"],
        ["RHME", "REJC", "RHLE"],       
        ["RHME","RRSP", "RUSP", "RHLE"],
    ],
}

interconnections["TrunkPelvis"] = {
    "Color": (0.5, 1.0, 0.5),
    "Links": [
        ["RSIA", "LSIA", "RSIA", "TV8","LSIA","TV8","SXS"], 
    ],
}

# 📌 Appliquer les interconnexions
p.set_interconnections(interconnections)

# 📌 Jouer l'animation
p.play()