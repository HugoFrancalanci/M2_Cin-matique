# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 21:13:09 2025

@author: Francalanci Hugo
"""

from fun_XprocessData import obtenir_max_points
import kineticstoolkit.lab as ktk
import matplotlib.pyplot as plt

# Chemin des fichiers C3D
c3d_filenames = [
    r"C:\Users\Francalanci Hugo\Code_stage_M2_ISMH\MF01\MF01-MF01-20240101-PROTOCOL01-ANALYTIC1-.c3d"
]

# Récupération du nombre de points max
num_points = obtenir_max_points(c3d_filenames)

def visualize_shoulder(side, c3d_filenames, num_points):
    markers = ktk.read_c3d(c3d_filenames[0])["Points"]
    
    if side == 'droit':
        # Thorax
        thorax_origin = markers.data["SJN"]
        thorax_y = markers.data["CV7"] - markers.data["SJN"]
        thorax_yz = markers.data["TV8"] - markers.data["CV7"]
        
        # Scapula
        scapula_origin = markers.data["RSAA"]
        scapula_y = markers.data["RSIA"] - markers.data["RSAA"]
        scapula_yz = markers.data["RSRS"] - markers.data["RSIA"]

        # Humerus
        humerus_origin = 0.5 * (markers.data["RHLE"] + markers.data["RHME"])
        humerus_y = markers.data["RHLE"] - markers.data["RHME"]
        humerus_yz = markers.data["REOS1"] - humerus_origin
        
    elif side == 'gauche':
        # Thorax
        thorax_origin = markers.data["SJN"]
        thorax_y = markers.data["CV7"] - markers.data["SJN"]
        thorax_yz = markers.data["TV8"] - markers.data["CV7"]
        
        # Scapula
        scapula_origin = markers.data["LSAA"]
        scapula_y = markers.data["LSIA"] - markers.data["LSAA"]
        scapula_yz = markers.data["LSRS"] - markers.data["LSIA"]

        # Humerus
        humerus_origin = 0.5 * (markers.data["LHLE"] + markers.data["LHME"])
        humerus_y = markers.data["LHLE"] - markers.data["LHME"]
        humerus_yz = markers.data["LEOS1"] - humerus_origin
        
    else:
        raise ValueError("Invalid side specified. Use 'droit' or 'gauche'.")

    # Création des repères locaux
    frames = ktk.TimeSeries(time=markers.time)
    frames.data["Thorax"] = ktk.geometry.create_frames(origin=thorax_origin, y=thorax_y, yz=thorax_yz)
    frames.data["Scapula"] = ktk.geometry.create_frames(origin=scapula_origin, y=scapula_y, yz=scapula_yz)
    frames.data["Humerus"] = ktk.geometry.create_frames(origin=humerus_origin, y=humerus_y, yz=humerus_yz)
    
    # Fusion des marqueurs et des repères pour la visualisation
    merged_data = ktk.TimeSeries.merge(markers, frames)

    # Lancement du Player pour visualiser les données
    ktk.Player(merged_data, up="z", anterior="y")

# Exécution pour chaque côté avec visualisation en temps réel
visualize_shoulder('droit', c3d_filenames, num_points)
visualize_shoulder('gauche', c3d_filenames, num_points)

# Affichage
plt.show()
