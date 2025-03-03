%% ===========================
%      TRAITEMENT CINÉMATIQUE
% ===========================
clc; clear; close all;

%% -------- Chargement de l'environnement -------- %%

% Ajout de la bibliothèque "btk"
addpath(genpath('C:\Users\Francalanci Hugo\Documents\MATLAB\Stage Sainte-Justine\HUG\btk'));

% Ajout de la bibliothèque "3D Kinematics and Inverse Dynamics"
addpath(genpath('C:\Users\Francalanci Hugo\Documents\MATLAB\Stage Sainte-Justine\HUG\3D Kinematics and Inverse Dynamics'));

% Accès au fichier C3D
fichier = 'C:\Users\Francalanci Hugo\Documents\MATLAB\Stage Sainte-Justine\HUG\Sujets\MF01\MF01-MF01-20240101-PROTOCOL01-ANALYTIC1-.c3d';
c3dH = btkReadAcquisition(fichier);

%% -------- Extraction des marqueurs -------- %%
markers = btkGetMarkers(c3dH);
available_markers = fieldnames(markers);
num_frames = size(markers.CV7, 1); % Nombre de frames

% Extraction de la fréquence d'échantillonnage
freq = btkGetPointFrequency(c3dH);
time = (0:num_frames-1) / freq; % Vecteur temps en secondes

%% -------- Visualisation des marqueurs en 3D -------- %%
figure; hold on;
for i = 1:length(available_markers)
    marker = markers.(available_markers{i});
    scatter3(marker(:,1), -marker(:,3), marker(:,2), 50, 'filled');
end
xlabel('X (mm)'); ylabel('Z (mm)'); zlabel('Y (mm)');
title('Position des marqueurs en 3D');
grid on; axis equal; rotate3d on;

%% -------- Initialisation des matrices -------- %%
Euler_angles = zeros(num_frames, 3); % Stockage des angles ZXY

%% -------- Calcul des angles pour chaque frame -------- %%
for frame = 1:num_frames
    % Extraction des marqueurs de la frame actuelle
    CV7 = markers.CV7(frame,:);
    TV8 = markers.TV8(frame,:);
    SJN = markers.SJN(frame,:);
    SXS = markers.SXS(frame,:);
    
    GH  = markers.RHUM1(frame,:);
    HLE = markers.REJC(frame,:);
    HME = markers.RGJC(frame,:);
    
    % ======= Définition des repères locaux =======
    
    % Thorax (Xt, Yt, Zt)
    Yt = normalize(mean([SXS; TV8]) - mean([SJN; CV7])); 
    Zt = normalize(cross(SJN - CV7, mean([SXS; TV8]) - SJN));
    Xt = cross(Yt, Zt);
    Ot = mean([SJN; CV7]); 

    % Humérus (Xh, Yh, Zh)
    Yh = normalize(GH - mean([HLE; HME]));
    Xh = normalize(cross(GH - HLE, GH - HME));
    Zh = cross(Yh, Xh);  
    Oh = GH; 

    % ======= Matrices homogènes =======
    T_torax  = compute_homogeneous_matrix(Xt, Yt, Zt, Ot);
    T_humerus = compute_homogeneous_matrix(Xh, Yh, Zh, Oh);

    % ======= Transformation relative =======
    T_hum_thorax = Mprod_array3(Tinv_array3(T_torax), T_humerus);

    % ======= Extraction des angles d'Euler =======
    Euler_angles(frame, :) = rad2deg(R2mobileZXY_array3(T_hum_thorax(1:3, 1:3)));
end

%% -------- Visualisation des angles en fonction du temps -------- %%
figure;
subplot(3,1,1);
plot(time, Euler_angles(:,1), 'r', 'LineWidth', 1.5);
xlabel('Temps (s)'); ylabel('Angle Z (°)'); title('Rotation selon Z'); grid on;

subplot(3,1,2);
plot(time, Euler_angles(:,2), 'g', 'LineWidth', 1.5);
xlabel('Temps (s)'); ylabel('Angle X (°)'); title('Rotation selon X'); grid on;

subplot(3,1,3);
plot(time, Euler_angles(:,3), 'b', 'LineWidth', 1.5);
xlabel('Temps (s)'); ylabel('Angle Y (°)'); title('Rotation selon Y'); grid on;

%% ===========================
%     FONCTIONS UTILITAIRES
% ===========================

function T = compute_homogeneous_matrix(X, Y, Z, O)
    % Construction de la matrice homogène 4x4
    R = [X(:), Y(:), Z(:)];
    T = eye(4);
    T(1:3, 1:3) = R;
    T(1:3, 4) = O(:);
end

