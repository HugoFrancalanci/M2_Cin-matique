# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 10:22:04 2025

@author: Francalanci Hugo
"""
import kineticstoolkit.lab as ktk 
import numpy as np
import matplotlib.pyplot as plt

# 📂 Fichier C3D contenant les angles
c3d_filenames = [
    r"C:\Users\Francalanci Hugo\Code_stage_M2_ISMH\MF01\MF01-MF01-20240101-PROTOCOL01-ANALYTIC1-.c3d"
]

def extract_and_plot_angles(c3d_filenames):
    """ Extrait les angles des six derniers points du fichier C3D, affiche les données et trace les graphes. """
    
    # Charger le fichier C3D
    c3d_data = ktk.read_c3d(c3d_filenames[0])

    # Vérifier si "Points" contient les angles
    if "Points" not in c3d_data:
        raise ValueError("🚨 'Points' non trouvé dans le fichier C3D.")

    # 📌 Liste des six derniers marqueurs (angles)
    angle_labels = ["RHT", "RGH", "RST", "LHT", "LGH", "LST"]
    
    # Extraire les angles
    angles_dict = {}
    for label in angle_labels:
        if label in c3d_data["Points"].data:
            angles_dict[label] = c3d_data["Points"].data[label]
        else:
            print(f"⚠️ Angle {label} non trouvé dans 'Points'.")

    # Extraire le temps
    time = c3d_data["Points"].time

    # 📊 Afficher les données des angles dans la console
    print("\n📊 Données des Angles :")
    print("Temps (s) |", " | ".join([f"{label} (Flex/Ext, Abd/Add, Rot Int/Ext)" for label in angle_labels]))
    for i in range(len(time)):
        row = [f"{time[i]:.3f}"]  # Ajoute le temps
        for label in angle_labels:
            if label in angles_dict:
                angles = angles_dict[label][i]
                row.append(f"({angles[0]:.2f}, {angles[1]:.2f}, {angles[2]:.2f})")
            else:
                row.append("(-, -, -)")
        print(" | ".join(row))

    # 📊 Tracer les angles
    plt.style.use("dark_background")

    for label, angles in angles_dict.items():
        plt.figure(figsize=(12, 6))
        plt.plot(time, angles[:, 0], linewidth=2, color="red", label="Flexion/Extension")
        plt.plot(time, angles[:, 1], linewidth=2, color="green", label="Abduction/Adduction")
        plt.plot(time, angles[:, 2], linewidth=2, color="blue", label="Rotation Interne/Externe")

        plt.xlabel("Temps (seconde)")
        plt.ylabel("Angle (degré)")
        plt.legend()
        plt.title(f"Angles {label}", fontsize=14, fontweight="bold")
        plt.grid(False)
        plt.show()

# Exécution du script
extract_and_plot_angles(c3d_filenames)


