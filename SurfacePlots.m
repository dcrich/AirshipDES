output = readtable('ExperimentImpacts2022-02-16_06-00-35-PM.csv');

% Payload = xlsread('ExperimentImpacts2022-02-16_06-00-35-PM.csv',1,'B2:B101');
% Speed = xlsread('ExperimentImpacts2022-02-16_06-00-35-PM.csv',1,'C2:C101');
% BoatJobLoss = xlsread('ExperimentImpacts2022-02-16_06-00-35-PM.csv',1,'P2:P101');
% CropLoss = xlsread('ExperimentImpacts2022-02-16_06-00-35-PM.csv',1,'Q2:Q101');
% Income= xlsread('ExperimentImpacts2022-02-16_06-00-35-PM.csv',1,'R2:R101');
% ForestLoss = xlsread('ExperimentImpacts2022-02-16_06-00-35-PM.csv',1,'S2:S101');
% TimeSavings = xlsread('ExperimentImpacts2022-02-16_06-00-35-PM.csv',1,'T2:T101');

figure
surfc(X,Y,Z)
xlabel('Payload (tons)')
ylabel('Cruise Speed (knots)')
zlabel('Crop Loss Impact (tons)')
oldcolors = colormap;
colormap(flipud(oldcolors))
colorbar
view(115,22)