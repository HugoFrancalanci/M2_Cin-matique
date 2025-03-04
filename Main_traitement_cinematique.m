%% ================= Traitement cinématique ================= %%  
clear; clc; close all;

%% -------- Chargement de l'environnement -------- %%
% Ajout de la bibliothèque "btk"
addpath(genpath('C:\Users\Francalanci Hugo\Documents\MATLAB\Stage Sainte-Justine\HUG\btk'));

% Ajout de la bibliothèque "3D Kinematics and Inverse Dynamics"
addpath(genpath('C:\Users\Francalanci Hugo\Documents\MATLAB\Stage Sainte-Justine\HUG\3D Kinematics and Inverse Dynamics'));

% Chargement du fichier c3d
fichier = 'C:\Users\Francalanci Hugo\Documents\MATLAB\Stage Sainte-Justine\HUG\Sujets\MF01\MF01-MF01-20240101-PROTOCOL01-ANALYTIC1-.c3d';
c3dH = btkReadAcquisition(fichier);

%% -------- Extraction des marqueurs -------- %%
markers = btkGetMarkers(c3dH);

% Récupération du nombre total de frames et fréquence d'échantillonnage
nFrames = btkGetLastFrame(c3dH);
fs = 200; % Fréquence d'acquisition en Hz
time = (0:nFrames-1) / fs; % Axe du temps en secondes

%% -------- Initialisation des matrices pour stocker les angles -------- %%
Angles_HT = zeros(nFrames, 3);
Angles_ST = zeros(nFrames, 3);
Angles_GH = zeros(nFrames, 3);

% Fonction pour normaliser un vecteur
normalize_vector = @(v) v / norm(v);

%% ======== Traitement des repères et extraction des angles d'Euler ======== %%
for i = 1:nFrames
    % Mise à jour des repères à chaque frame
    SJN = markers.SJN(i,:); CV7 = markers.CV7(i,:);
    TV8 = markers.TV8(i,:); SXS = markers.SXS(i,:);
    
    % Repère du thorax
    Ot = SJN;
    Yt = normalize_vector(mean([SXS; TV8]) - mean([SJN; CV7]));
    Zt = normalize_vector(cross(SJN - CV7, mean([SXS; TV8]) - SJN));
    Xt = normalize_vector(cross(Yt, Zt));

    % Vérification des vecteurs colinéaires
    if abs(dot(Yt, Zt)) > 0.99
        warning('Problème : les vecteurs Yt et Zt sont presque colinéaires !');
    end
    
    % Repère de la scapula
    RSAA = markers.RSAA(i,:); RSRS = markers.RSRS(i,:); RSIA = markers.RSIA(i,:);
    Os = RSAA;
    Zs = normalize_vector(RSAA - RSRS);
    Xs = normalize_vector(cross(RSIA - RSAA, RSRS - RSAA));
    Ys = normalize_vector(cross(Xs, Zs));

    % Repère de l'humérus
    RGH = markers.RSCT(i,:); RHME = markers.RHME(i,:); RHLE = markers.RHLE(i,:);
    Rmid_HLE_HME = mean([RHLE; RHME]);
    Oh = RGH;
    Yh = normalize_vector(RGH - Rmid_HLE_HME);
    Xh = normalize_vector(cross(RGH - RHLE, RGH - RHME));
    Zh = normalize_vector(cross(Yh, Xh));

    % Matrices de rotation
    Rt = [Xt', Yt', Zt']; % Thorax
    Rs = [Xs', Ys', Zs']; % Scapula
    Rh = [Xh', Yh', Zh']; % Humérus

    % Correction de l'orthonormalité (Gram-Schmidt)
    [Ut,~,Vt] = svd(Rt); Rt = Ut * Vt';
    [Us,~,Vs] = svd(Rs); Rs = Us * Vs';
    [Uh,~,Vh] = svd(Rh); Rh = Uh * Vh';

    % Matrices de rotation relatives
    R_HT = Rt' * Rh; % Humérus dans le repère du thorax
    R_ST = Rt' * Rs; % Scapula dans le repère du thorax
    R_GH = Rs' * Rh; % Humérus dans le repère de la scapula

    % Extraction des angles d'Euler Y-X-Y pour HT et GH
    Angles_HT(i,1) = atan2(R_HT(3,2), R_HT(3,3));
    Angles_HT(i,2) = asin(-R_HT(3,1));
    Angles_HT(i,3) = atan2(R_HT(2,1), R_HT(1,1));

    Angles_GH(i,1) = atan2(R_GH(3,2), R_GH(3,3));
    Angles_GH(i,2) = asin(-R_GH(3,1));
    Angles_GH(i,3) = atan2(R_GH(2,1), R_GH(1,1));

    % Extraction des angles d'Euler Y-X-Z pour ST
    Angles_ST(i,1) = atan2(-R_ST(2,1), R_ST(1,1));
    Angles_ST(i,2) = asin(R_ST(3,1));
    Angles_ST(i,3) = atan2(-R_ST(3,2), R_ST(3,3));
end

%% -------- Correction des discontinuités et filtrage -------- %%
Angles_HT = unwrap(Angles_HT);
Angles_ST = unwrap(Angles_ST);
Angles_GH = unwrap(Angles_GH);

fc = 6; % Fréquence de coupure (Hz)
[b, a] = butter(2, fc / (fs/2), 'low');

Angles_HT = filtfilt(b, a, Angles_HT);
Angles_ST = filtfilt(b, a, Angles_ST);
Angles_GH = filtfilt(b, a, Angles_GH);

%% -------- Affichage des angles d'Euler -------- %%
figure;
subplot(3,1,1);
plot(time, rad2deg(Angles_HT), 'LineWidth', 1.5);
xlabel('Temps (s)'); ylabel('Angle (°)');
legend('HT - Y', 'HT - X', 'HT - Y');
title('Angles Huméro-Thoracique (HT)'); grid on;

subplot(3,1,2);
plot(time, rad2deg(Angles_ST), 'LineWidth', 1.5);
xlabel('Temps (s)'); ylabel('Angle (°)');
legend('ST - Y', 'ST - X', 'ST - Z');
title('Angles Scapulo-Thoracique (ST)'); grid on;

subplot(3,1,3);
plot(time, rad2deg(Angles_GH), 'LineWidth', 1.5);
xlabel('Temps (s)'); ylabel('Angle (°)');
legend('GH - Y', 'GH - X', 'GH - Y');
title('Angles Gléno-Huméral (GH)'); grid on;

