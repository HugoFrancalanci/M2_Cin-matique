# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 10:31:34 2025

@author: Francalanci Hugo
"""

import kineticstoolkit.lab as ktk

# 📂 Fichier C3D
c3d_filenames = [
    r"C:\Users\Francalanci Hugo\Code_stage_M2_ISMH\MF01\MF01-MF01-20240101-PROTOCOL01-ANALYTIC1-.c3d"
]

# Charger le fichier C3D
c3d_data = ktk.read_c3d(c3d_filenames[0])

# Vérifier si la section 'Points' existe
if "Points" in c3d_data:
    marker_names = list(c3d_data["Points"].data.keys())  # Récupérer les noms des marqueurs
    print(f"🔢 Nombre total de points : {len(marker_names)}")
    print(f"📌 Liste des points : {marker_names}")
else:
    print("🚨 Aucun point trouvé dans le fichier C3D.")
