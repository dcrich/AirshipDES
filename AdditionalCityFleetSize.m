file = uigetfile('*.csv');
output = readtable(file);
% coordWithBestFleet1 = zeros(3,length(output));
% coordWithBestFleet2 = zeros(3,length(output));
counter1 = 1;
counter2 = 1;
for i = 1:2:height(output)
    indfleet1 = i;
    indfleet2 = i+1;
    
    if output.Income(indfleet2) > output.Income(indfleet1)
        coordWithBestFleet2(1,counter2) = output.Lat(indfleet2);
        coordWithBestFleet2(2,counter2) = output.Lon(indfleet2);
        coordWithBestFleet2(3,counter2) = 2;
        counter2 = counter2 + 1;
    else
        coordWithBestFleet1(1,counter1) = output.Lat(indfleet1);
        coordWithBestFleet1(2,counter1) = output.Lon(indfleet1);
        coordWithBestFleet1(3,counter1) = 1;
        counter1 = counter1 + 1;
    end

end

%%
cities =   [-3.196, -59.826;
            -3.276, -60.190;
            -3.387, -60.344;
            -3.441, -60.462];
hub = [-3.117, -60.025];
figure(1)
geoscatter(coordWithBestFleet1(1,:),coordWithBestFleet1(2,:),120,'v','LineWidth',1,'MarkerFaceColor',0.5*[103/255, 170/255, 62/255])
hold on
geoscatter(coordWithBestFleet2(1,:),coordWithBestFleet2(2,:),120,'^','LineWidth',1,'MarkerFaceColor',[191/255, 50/255, 136/255])
geoscatter(cities(:,1),cities(:,2),300,'filled','s','MarkerFaceColor',[200/255, 200/255, 100/255])
geoscatter(hub(1),hub(2),600,'filled','pk')
legend('1 Airship','2 Airships','Original Cities', 'Manaus')
hold off
% axesm('MapProjection','mercator')
geobasemap colorterrain
axes = gca;
axes.FontSize = 16;
