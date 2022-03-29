warning off
close all
% how to optimize with jumps due to fleet size
% how to explain spikes due to stochastic natural of simulation
if false %exist('uniform12149.mat','file')
    load uniform12149.mat
else
    steps = [1,1,1];
%     steps = [2,2,1];
%     steps = [2,5,1];
%     steps = [5,10,1];
    file = uigetfile('*.csv');
    output = readtable(file);
    x = output.Payload;
    y = output.CruiseSpeed;
    f = output.FleetSize;
    all = [x,y,f];
    zI = output.Income;
    zT = output.TimeSavings;
    zC = output.CropLoss;
    zB = output.BoatTripLoss;
    zF = output.ForestLoss;
    
    payloadrange = [min(output.Payload),max(output.Payload)];
    speedrange = [min(output.CruiseSpeed),max(output.CruiseSpeed)];
    fleetrange = [min(output.FleetSize),max(output.FleetSize)];
    payload = payloadrange(1):steps(1):payloadrange(2);
    speed = speedrange(1):steps(2):speedrange(2);
    fleet = fleetrange(1):steps(3):fleetrange(2);
    [payloadG, speedG, fleetG] = meshgrid(payload, speed, fleet);
    
    ZB = zeros(length(speed),length(payload),length(fleet));
    ZC = ZB;
    ZF = ZB;
    ZI = ZB;
    ZT = ZB;
    X = ZB;
    Y = ZB;
    F = ZB;
    counter = 1;
    for i = 1:length(speed)
        for j = 1:length(payload)
            for k = 1:length(fleet)
                X(i,j,k) = x(counter);
                Y(i,j,k) = y(counter);
                F(i,j,k) = f(counter);
                ZB(i,j,k) = zB(counter);
                ZC(i,j,k) = zC(counter);
                ZF(i,j,k) = zF(counter);
                ZI(i,j,k) = zI(counter);
                ZT(i,j,k) = zT(counter);
                counter = counter + 1;
            end
        end
    end
end
%%
% thecolormap = [0, 1, 0; 
%                0.5, 0.5, 0.5; 
%                1, 0, 0];
%universal red: 191/255, 50/255, 136/255
%universal mid: 214/255, 209/255, 213/255
%universal green: 103/255, 170/255, 62/255
darken = 0.99;
red1 = linspace(191/256, 214/256, 1000);
red2 = linspace(214/256, 103/256, 1000);
red = [red1,red2];
green1 = linspace(50/256, 209/256, 1000);
green2 = linspace(209/256, 170/256, 1000);
green = [green1,green2];
blue1 = linspace(136/256, 213/256, 1000);
blue2 = linspace(213/256, 62/256, 1000);
blue = [blue1,blue2];
thecolormap = darken*[red;green;blue]';
% individual
figure1 = figure(111);
for i = 1:1%length(fleet)
    zScaled = -100*ZB(:,:,i)/min(ZB(:,:,i),[],'all');
    % Create axes
    axes1 = axes('Parent',figure1);
    hold(axes1,'on');
    scatter3(min(X,[],'all'),min(Y,[],'all'),1.005*max(zScaled,[],'all'),100,'kx','LineWidth',2)
    % Create surf
    surf(X(:,:,i),Y(:,:,i),zScaled,'Parent',axes1);
    % Create zlabel
    zlabel('Impact to Boat Jobs (%\Delta)')
    % Create ylabel
    ylabel('Cruise Speed (knots)');
    % Create xlabel
    xlabel('Payload (tons)');
    view(axes1,[137.803767077795 23.2496477308791]);
    grid(axes1,'on');
    hold(axes1,'off');
    % Set the remaining axes properties
    set(axes1,'FontSize',16.5);
    % Create colorbar
    colorbar(axes1);
    colormap(thecolormap)
end
hold off
figure2 = figure(222);
for i = 1:1%length(fleet)
    normfact = 0.01*(max(ZC(:,:,i),[],'all')-min(ZC(:,:,i),[],'all'));
    % Create axes
    axes1 = axes('Parent',figure2);
    hold(axes1,'on');
    scatter3(max(X,[],'all'),max(Y,[],'all'),min(zC(:,:,i)/normfact,[],'all'),50,'kx','LineWidth',2)
    scatter3(max(X,[],'all'),max(Y,[],'all'),1.005*max(zC(:,:,i)/normfact,[],'all'),50,'kx','LineWidth',2)
    % Create surf
    surfc(X(:,:,i),Y(:,:,i),ZC(:,:,i)/normfact,'Parent',axes1);
    % Create zlabel
    zlabel('Impact to Crop Savings (%\Delta)');
    % Create ylabel
    ylabel('Cruise Speed (knots)');
    % Create xlabel
    xlabel('Payload (tons)');
    view(axes1,[-40.4007675816258 23.2496477308791]);
    grid(axes1,'on');
    hold(axes1,'off');
    % Set the remaining axes properties
    set(axes1,'FontSize',16.5);
    % Create colorbar
    colorbar(axes1);
    colormap(thecolormap)
end
% zlim([0,max(ZC(:,:,:),[],'all')])
hold off
% figure3 = figure(333);
% for i = 1:1%length(fleet)
%     % Create axes
%     axes1 = axes('Parent',figure3);
%     hold(axes1,'on');
%     % Create surf
%     surfc(X(:,:,i),Y(:,:,i),-2.29568e-5*ZF(:,:,i),'Parent',axes1);
%     % Create zlabel
%     zlabel('Impact to Forest Loss (acres)');
%     % Create ylabel
%     ylabel('Cruise Speed (knots)');
%     % Create xlabel
%     xlabel('Payload (tons)');
%     view(axes1,[-40.4007675816258 23.2496477308791]);
%     grid(axes1,'on');
%     hold(axes1,'off');
%     % Set the remaining axes properties
%     set(axes1,'FontSize',16);
%     % Create colorbar
%     colorbar(axes1);
%     colormap(thecolormap)
% end
% hold off
figure4 = figure(444);
for i = 1:1%length(fleet)
    normfact = 0.01*(max(ZI(:,:,i),[],'all')-min(ZI(:,:,i),[],'all'));
    % Create axes
    axes1 = axes('Parent',figure4);
    hold(axes1,'on');
    [maxval,id] = max(ZI,[],'all');
    scatter3(X(id),Y(id),min(ZI/normfact,[],'all'),80,'kx','LineWidth',2)
    scatter3(X(id),Y(id),1.005*max(ZI/normfact,[],'all'),80,'kx','LineWidth',2)
    % Create surf
    surfc(X(:,:,i),Y(:,:,i),ZI(:,:,i)/normfact,'Parent',axes1);
    % Create zlabel
    zlabel('Impact to Income (%\Delta)');
    % Create ylabel
    ylabel('Cruise Speed (knots)');
    % Create xlabel
    xlabel('Payload (tons)');
    view(axes1,[51.4539268828763 14.2365090036341]);
    grid(axes1,'on');
    hold(axes1,'off');
    % Set the remaining axes properties
    set(axes1,'FontSize',16.5);
    % Create colorbar
    colorbar(axes1);
    colormap(thecolormap)
end

% zlim([0,max(ZI(:,:,:),[],'all')])
% set(gca,'ColorScale','linear','CLim',[-6*10^5, max(ZI(:,:,i),[],'all')])
hold off
figure5 = figure(555);
for i = 1:1%length(fleet)
    normfact = 0.01*(max(ZT(:,:,i),[],'all')-min(ZT(:,:,i),[],'all'));
    % Create axes
    axes1 = axes('Parent',figure5);
    hold(axes1,'on');
    scatter3(max(X,[],'all'),max(Y,[],'all'),min(ZT/normfact,[],'all'),50,'kx','LineWidth',2)
    scatter3(max(X,[],'all'),max(Y,[],'all'),1.005*max(ZT/normfact,[],'all'),50,'kx','LineWidth',2)
    % Create surf
    surfc(X(:,:,i),Y(:,:,i),ZT(:,:,i)/normfact,'Parent',axes1,'FaceLighting','flat');
    % Create zlabel
    zlabel('Impact to Time Savings (%\Delta)');
    % Create ylabel
    ylabel('Cruise Speed (knots)');
    % Create xlabel
    xlabel('Payload (tons)');
    view(axes1,[-40.4007675816258 23.2496477308791]);
    grid(axes1,'on');
    hold(axes1,'off');
    % Set the remaining axes properties
    set(axes1,'FontSize',16.5);
    % Create colorbar
    colorbar(axes1);
    colormap(thecolormap)
    
end
hold off

% % subplots
% figure(1)
% subplot(2,3,1);
% for i = 1:length(fleet)
%     zScaled = -100*ZB(:,:,i)/min(ZB(:,:,i),[],'all');
%     surfc(X(:,:,i),Y(:,:,i),zScaled)
%     xlabel('Payload (tons)')
%     ylabel('Cruise Speed (knots)')
%     zlabel('Boat Job Loss (percent decrease))')
%     colormap(thecolormap)
%     colorbar
%     view(115,22)
%     hold on
% end
% hold off
% % figure(2)
% subplot(2,3,2);
% for i = 1:length(fleet)
%     surfc(X(:,:,i),Y(:,:,i),ZC(:,:,i))
%     xlabel('Payload (tons)')
%     ylabel('Cruise Speed (knots)')
%     zlabel('Crop Loss (tons crops saved)')
%     colormap(thecolormap)
%     colorbar
%     view(115,22)
%     hold on
% end
% zlim([0,max(ZC(:,:,:),[],'all')])
% hold off
% % figure(3)
% subplot(2,3,3);
% for i = 1:length(fleet)
%     surfc(X(:,:,i),Y(:,:,i),-2.29568e-5*ZF(:,:,i))
%     xlabel('Payload (tons)')
%     ylabel('Cruise Speed (knots)')
%     zlabel('Forest Loss (acres lost)')
%     oldcolors = colormap;
%     colormap(flipud(oldcolors))
%     colorbar
%     view(115,22)
%     hold on
% end
% hold off
% % figure(4)
% subplot(2,3,4);
% for i = 1:length(fleet)
%     surfc(X(:,:,i),Y(:,:,i),ZI(:,:,i))
%     xlabel('Payload (tons)')
%     ylabel('Cruise Speed (knots)')
%     zlabel('Income (R$)')
%     colormap(thecolormap)
%     colorbar
%     view(115,22)
%     hold on
% end
% zlim([0,max(ZI(:,:,:),[],'all')])
% % set(gca,'ColorScale','linear','CLim',[-6*10^5, max(ZI(:,:,i),[],'all')])
% hold off
% % figure(5)
% subplot(2,3,5);
% for i = 1:length(fleet)
%     surfc(X(:,:,i),Y(:,:,i),ZT(:,:,i))
%     xlabel('Payload (tons)')
%     ylabel('Cruise Speed (knots)')
%     zlabel('Time Savings (hours)')
%     colormap(thecolormap)
%     colorbar
%     view(115,22)
%     hold on
% end
% hold off
% 
% 
% 
% 
% 
