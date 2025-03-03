%% Traitement cinématique %% 


%% -------- Chargement de l'environnement -------- %%

% Ajout de la bibliothèque "btk"
addpath(genpath('C:\Users\Francalanci Hugo\Documents\MATLAB\Stage Sainte-Justine\HUG\btk'));

% Ajout de la bibliothèque "3D Kinematics and Inverse Dynamics" 
addpath(genpath('C:\Users\Francalanci Hugo\Documents\MATLAB\Stage Sainte-Justine\HUG\3D Kinematics and Inverse Dynamics'));

% Accès au fichier c3d
fichier = 'C:\Users\Francalanci Hugo\Documents\MATLAB\Stage Sainte-Justine\HUG\Sujets\MF01\MF01-MF01-20240101-PROTOCOL01-ANALYTIC1-.c3d';
c3dH = btkReadAcquisition(fichier);

%% -------- Extraction des marqueurs -------- %%

% Extraction des coordonnées des marqueurs
markers = btkGetMarkers(c3dH);

% Affichage des noms des signaux analogiques
markers_list = { ...
    'RFHD', 'RBHD', 'LBHD', 'LFHD', 'SJN', 'SME', 'SXS', 'CV7', 'TV5', 'TV8', ...
    'RCAS', 'RCAS2', 'RCAJ2', 'RCAJ', 'RSIA', 'RSRS', 'RSAA', 'RSCT', 'RSIA2', 'RSRS2', ...
    'RSAA2', 'RSCT2', 'RACM1', 'RACM2', 'RACM3', 'RHDT', 'RHTI', 'RHBI', 'RHME', 'RHLE', ...
    'REOS1', 'REOS2', 'REOS3', 'LCAS', 'LCAS2', 'LCAJ2', 'LCAJ', 'LSIA', 'LSRS', 'LSAA', ...
    'LSCT', 'LSIA2', 'LSRS2', 'LSAA2', 'LSCT2', 'LACM1', 'LACM2', 'LACM3', 'LHDT', 'LHTI', ...
    'LHBI', 'LHME', 'LHLE', 'LEOS1', 'LEOS2', 'LEOS3', 'RRSP', 'RUSP', 'RWUP', 'RWBK', ...
    'LRSP', 'LUSP', 'LWUP', 'LWBK', 'STY01', 'STY02', 'STY03', 'STY04', 'STY05', 'S1', ...
    'LHUM1', 'LHUM2', 'LHUM3', 'LHUM4', 'RHUM1', 'RHUM2', 'RHUM3', 'RHUM4', 'REJC', 'RGJC', ...
    'LEJC', 'LGJC' ...
};


%% -------- Affichage des marqueurs en 3D -------- %%

% Extraction des coordonnées des marqueurs présents
available_markers = fieldnames(markers);
num_markers = length(available_markers); 

% Création d'une matrice contenant toutes les coordonnées des marqueurs
X = zeros(num_markers, 1);
Y = zeros(num_markers, 1);
Z = zeros(num_markers, 1);

for i = 1:num_markers
    marker_name = available_markers{i};
    coords = markers.(marker_name);
    
    % Première frame
    X(i) = coords(1,1); 
    Y(i) = coords(1,2);
    Z(i) = coords(1,3);
end

figure;
scatter3(X, -Z, Y, 50, 'filled'); % Permutation et inversion des axes
text(X, -Z, Y, available_markers, 'FontSize', 8, 'VerticalAlignment', 'bottom', 'HorizontalAlignment', 'right'); 
xlabel('X (mm)'); 
ylabel('Z (mm)'); 
zlabel('Y (mm)'); 
title('Position des marqueurs en 3D - Orientation corrigée');
grid on;
axis equal;
view([90, 0]); % Vue de face
rotate3d on;

%% -------- Définition des repères locaux selon Wu et al. (2005) -------- %%

CV7 = markers.CV7(1,:);
TV8 = markers.TV8(1,:);
SJN = markers.SJN(1,:);
SXS = markers.SXS(1,:);

LSIA = markers.LSIA(1,:);
LSAA = markers.LSAA(1,:);
LSCT = markers.LSCT(1,:);

GH  = markers.RHUM1(1,:);
HLE = markers.REJC(1,:); 
HME = markers.RGJC(1,:);  

% Repère Thorax (Xt, Yt, Zt)
Yt = normalize(mean([SXS; TV8]) - mean([SJN; CV7]));  % Axe vertical
Zt = normalize(cross(SJN - CV7, mean([SXS; TV8]) - SJN));  % Axe transversal
Xt = cross(Yt, Zt);  % Axe antéro-postérieur
Ot = mean([SJN; CV7]); % Origine du thorax

% Repère Scapula (Xs, Ys, Zs)
Ys = normalize(cross(LSAA - LSCT, LSIA - LSCT));  % Axe vertical
Zs = normalize(LSCT - LSAA);  % Axe transversal
Xs = cross(Ys, Zs);  % Axe antéro-postérieur
Os = LSAA; % Origine de la scapula

% Repère Humérus (Xh, Yh, Zh)
Yh = normalize(GH - mean([HLE; HME]));  % Axe longitudinal
Xh = normalize(cross(GH - HLE, GH - HME));  % Axe perpendiculaire
Zh = cross(Yh, Xh);  % Axe transversal
Oh = GH; % Origine de l'humérus

%% -------- Construction les matrices de transformation homogène (T) -------- %%

function T = compute_homogeneous_matrix(X, Y, Z, O)
    R = [X(:), Y(:), Z(:)]; % Matrice de rotation 3x3
    T = eye(4); % Matrice homogène initialisée
    T(1:3, 1:3) = R;
    T(1:3, 4) = O(:); % Ajout du vecteur de position
end

T_torax  = compute_homogeneous_matrix(Xt, Yt, Zt, Ot);
T_scapula = compute_homogeneous_matrix(Xs, Ys, Zs, Os);
T_humerus = compute_homogeneous_matrix(Xh, Yh, Zh, Oh);

T_hum_thorax = Mprod_array3(Tinv_array3(T_torax), T_humerus);

Euler_angles = R2mobileZXY_array3(T_hum_thorax(1:3, 1:3));
disp('Angles d’Euler (ZXY) :');
disp(rad2deg(Euler_angles)); % Convertit en degrés

