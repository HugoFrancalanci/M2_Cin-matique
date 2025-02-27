# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 11:04:57 2025

@author: Francalanci Hugo
"""

import numpy as np
import kineticstoolkit.lab as ktk
import matplotlib.pyplot as plt

# 📂 Fichier C3D contenant les données
c3d_filenames = [r"C:\Users\Francalanci Hugo\Code_stage_M2_ISMH\MF01\MF01-MF01-20240101-PROTOCOL01-ANALYTIC1-.c3d"]

# 🔥 Combinaisons Valides de Repères Locaux
repere_options = [
    ("y", "yz"), ("x", "xz"), ("z", "yz")
]

# 🔥 Liste des angles à tester
angles_labels = ["RHT", "RGH", "RST"]

def test_one_angle(side, c3d_filenames, repere_combination, angle_label):
    """ Teste une configuration de repères pour voir son impact sur un angle donné. """

    # Charger le fichier C3D
    markers = ktk.read_c3d(c3d_filenames[0])["Points"]
    rep_y, rep_yz = repere_combination  # 🏆 Choix du repère testé

    if side == 'droit':
        # 🔴 Thorax
        thorax_origin = markers.data["SJN"]
        thorax_y = markers.data["CV7"] - markers.data["SJN"]
        thorax_yz = markers.data["TV8"] - markers.data["CV7"]

        # 🔵 Scapula
        scapula_origin = markers.data["RSAA"]
        scapula_y = markers.data["RSIA"] - markers.data["RSAA"]
        scapula_yz = markers.data["RSRS"] - markers.data["RSIA"]

        # 🟢 Humérus
        humerus_origin = 0.5 * (markers.data["RHLE"] + markers.data["RHME"])
        humerus_y = markers.data["RHLE"] - markers.data["RHME"]
        humerus_yz = markers.data["REOS1"] - humerus_origin

    elif side == 'gauche':
        # 🔴 Thorax
        thorax_origin = markers.data["SJN"]
        thorax_y = markers.data["CV7"] - markers.data["SJN"]
        thorax_yz = markers.data["TV8"] - markers.data["CV7"]

        # 🔵 Scapula
        scapula_origin = markers.data["LSAA"]
        scapula_y = markers.data["LSIA"] - markers.data["LSAA"]
        scapula_yz = markers.data["LSRS"] - markers.data["LSIA"]

        # 🟢 Humérus
        humerus_origin = 0.5 * (markers.data["LHLE"] + markers.data["LHME"])
        humerus_y = markers.data["LHLE"] - markers.data["LHME"]
        humerus_yz = markers.data["LEOS1"] - humerus_origin

    else:
        raise ValueError("Invalid side specified. Use 'droit' or 'gauche'.")

    # 📌 Création des repères locaux avec la combinaison testée
    frames = ktk.TimeSeries(time=markers.time)
    frames.data["Thorax"] = ktk.geometry.create_frames(origin=thorax_origin, **{rep_y: thorax_y, rep_yz: thorax_yz})
    frames.data["Scapula"] = ktk.geometry.create_frames(origin=scapula_origin, **{rep_y: scapula_y, rep_yz: scapula_yz})
    frames.data["Humerus"] = ktk.geometry.create_frames(origin=humerus_origin, **{rep_y: humerus_y, rep_yz: humerus_yz})

    # 📌 Calcul des angles
    humerus_to_thorax = ktk.geometry.get_local_coordinates(frames.data["Thorax"], frames.data["Humerus"])
    scapula_to_thorax = ktk.geometry.get_local_coordinates(frames.data["Thorax"], frames.data["Scapula"])
    humerus_to_scapula = ktk.geometry.get_local_coordinates(frames.data["Scapula"], frames.data["Humerus"])

    # 📌 Conversion en angles d'Euler
    angles_GH = ktk.geometry.get_angles(humerus_to_scapula, "ZXY", degrees=True)
    angles_HT = ktk.geometry.get_angles(humerus_to_thorax, "ZXY", degrees=True)
    angles_ST = ktk.geometry.get_angles(scapula_to_thorax, "YXZ", degrees=True)

    # 📌 Extraction des angles du fichier C3D
    angles_c3d = {label: markers.data[label][:, 0] for label in angles_labels if label in markers.data}

    # 📌 Utilisation de l’angle correspondant
    angles_calculated = {
        "RHT": angles_HT[:, 1], 
        "RGH": angles_GH[:, 1], 
        "RST": angles_ST[:, 1] 
    }

    # 📊 Comparaison de l'angle sélectionné
    def plot_comparison(time, calculated, extracted, label, repere_combination):
        plt.figure(figsize=(12, 6))
        plt.plot(time, calculated, linewidth=2, color="red", linestyle="dashed", label="Calculé")
        if label in extracted:
            plt.plot(time, extracted[label], linewidth=2, color="blue", label="C3D")
        plt.xlabel("Temps (seconde)")
        plt.ylabel("Angle (degré)")
        plt.legend()
        plt.title(f"Test {repere_combination} - Comparaison {label}")
        plt.grid(False)
        plt.show()

    # Vérifier que l'angle sélectionné est bien dans les données C3D
    if angle_label in angles_calculated and angle_label in angles_c3d:
        plot_comparison(markers.time, angles_calculated[angle_label], angles_c3d, angle_label, repere_combination)
    else:
        print(f"⚠️ Angle {angle_label} non trouvé dans le fichier C3D.")

    return angles_calculated[angle_label] if angle_label in angles_calculated else None

# 🔥 Exécuter les tests UN ANGLE À LA FOIS
angle_a_tester = "RST"  # ⬅️ Modifier ici pour tester "RHT", "RGH" ou "RST"

for repere_combination in repere_options:
    print(f"🔄 Test de la configuration {repere_combination} pour {angle_a_tester}...")
    test_one_angle('droit', c3d_filenames, repere_combination, angle_a_tester)
