# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 20:16:26 2025

@author: Francalanci Hugo
"""

import numpy as np
import kineticstoolkit.lab as ktk
import matplotlib.pyplot as plt

c3d_filenames = [r"C:\Users\Francalanci Hugo\Code_stage_M2_ISMH\MF01\MF01-MF01-20240101-PROTOCOL01-ANALYTIC1-.c3d"]

def get_shoulder_angles(side, c3d_filenames):
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
    
    # Calcul des angles
    humerus_to_thorax = ktk.geometry.get_local_coordinates(frames.data["Thorax"], frames.data["Humerus"])
    scapula_to_thorax = ktk.geometry.get_local_coordinates(frames.data["Thorax"], frames.data["Scapula"])
    humerus_to_scapula = ktk.geometry.get_local_coordinates(frames.data["Scapula"], frames.data["Humerus"])

    # Conversion en angles d'Euler
    angles_GH = ktk.geometry.get_angles(humerus_to_scapula, "ZXY", degrees=True)
    angles_HT = ktk.geometry.get_angles(humerus_to_thorax, "ZXY", degrees=True)
    angles_ST = ktk.geometry.get_angles(scapula_to_thorax, "YXZ", degrees=True)


    # Interpolation des données manquantes
    def interpolate_nan(data):
        for i in range(data.shape[1]):
            angle_data = data[:, i]
            indices = np.arange(len(angle_data))
            non_nan_indices = indices[~np.isnan(angle_data)]
            estimated_data = np.interp(indices, non_nan_indices, angle_data[~np.isnan(angle_data)])
            data[:, i] = estimated_data
        return data

    angles_HT = interpolate_nan(angles_HT)
    angles_ST = interpolate_nan(angles_ST)
    angles_GH = interpolate_nan(angles_GH)

    # Fonction d'affichage des figures
    def plot_angles(time, angles, labels, title):
        plt.figure(figsize=(12, 6))
        plt.style.use('dark_background')
        plt.plot(time, angles[:, 0], linewidth=2, color='red', label=f"{labels[0]}")
        plt.plot(time, angles[:, 1], linewidth=2, color='green', label=f"{labels[1]}")
        plt.plot(time, angles[:, 2], linewidth=2, color='blue', label=f"{labels[2]}")
        plt.xlabel("Temps (seconde)")
        plt.ylabel("Angle (degré)")
        plt.legend()
        plt.title(title, fontsize=12.5, fontweight='bold', fontstyle='italic')
        plt.grid(False)
        plt.show()

    # Affichage des angles séparés
    plot_angles(markers.time, angles_HT, 
                ["Flexion/Extension HT", "Abduction/Adduction HT", "Rotation interne/externe HT"], 
                f"Angles HT (Humerus-Thorax) - {side}")

    plot_angles(markers.time, angles_GH, 
                ["Flexion/Extension GH", "Abduction/Adduction GH", "Rotation interne/externe GH"], 
                f"Angles GH (Gleno-Humeral) - {side}")

    plot_angles(markers.time, angles_ST, 
                ["Flexion/Extension ST", "Abduction/Adduction ST", "Rotation interne/externe ST"], 
                f"Angles ST (Scapulo-Thoracique) - {side}")

    return angles_HT, angles_GH, angles_ST

# Exécution pour chaque côté avec figures séparées
angles_HT_droit, angles_GH_droit, angles_ST_droit = get_shoulder_angles('droit', c3d_filenames)
angles_HT_gauche, angles_GH_gauche, angles_ST_gauche = get_shoulder_angles('gauche', c3d_filenames)


