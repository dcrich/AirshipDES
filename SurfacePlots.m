warning off
% how to optimize with jumps due to fleet size
% how to explain spikes due to stochastic natural of simulation
if exist('uniform12149.mat','file')
    load uniform12149.mat
else
%     steps = [1,1,1];
    steps = [5,10,1];
    file = uigetfile('*.csv');
    output = readtable(file);
    x = output.Payload;
    y = output.CruiseSpeed;
    f = output.FleetSize;
    all = [x,y,f];
    zI = output.Income;
    zT = output.TimeSavings;
    zC = output.CropLoss;
    zB = output.BoatJobLoss;
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

% individual
figure(1)
for i = 1:length(fleet)
    zScaled = -100*ZB(:,:,i)/min(ZB(:,:,i),[],'all');
    surf(X(:,:,i),Y(:,:,i),zScaled)
    xlabel('Payload (tons)')
    ylabel('Cruise Speed (knots)')
    zlabel('Boat Job Loss (percent decrease))')
    colormap parula
    colorbar
    view(115,22)
    hold on
end
hold off
figure(2)
for i = 1:1%length(fleet)
    surf(X(:,:,i),Y(:,:,i),ZC(:,:,i))
    xlabel('Payload (tons)')
    ylabel('Cruise Speed (knots)')
    zlabel('Crop Loss (tons crops saved)')
    colormap parula
    colorbar
    view(115,22)
    hold on
end
% zlim([0,max(ZC(:,:,:),[],'all')])
hold off
figure(3)
for i = 1:length(fleet)
    surf(X(:,:,i),Y(:,:,i),-2.29568e-5*ZF(:,:,i))
    xlabel('Payload (tons)')
    ylabel('Cruise Speed (knots)')
    zlabel('Forest Loss (acres lost)')
    oldcolors = colormap;
    colormap(flipud(oldcolors))
    colorbar
    view(115,22)
    hold on
end
hold off
figure(4)
for i = 1:length(fleet)
    surf(X(:,:,i),Y(:,:,i),ZI(:,:,i))
    xlabel('Payload (tons)')
    ylabel('Cruise Speed (knots)')
    zlabel('Income (R$)')
    colormap parula
    colorbar
    view(115,22)
    hold on
end
% zlim([0,max(ZI(:,:,:),[],'all')])
% set(gca,'ColorScale','linear','CLim',[-6*10^5, max(ZI(:,:,i),[],'all')])
hold off
figure(5)
for i = 1:length(fleet)
    surf(X(:,:,i),Y(:,:,i),ZT(:,:,i))
    xlabel('Payload (tons)')
    ylabel('Cruise Speed (knots)')
    zlabel('Time Savings (hours)')
    colormap parula
    colorbar
    view(115,22)
    hold on
end
hold off

% % subplots
% figure(1)
% subplot(2,3,1);
% for i = 1:length(fleet)
%     zScaled = -100*ZB(:,:,i)/min(ZB(:,:,i),[],'all');
%     surf(X(:,:,i),Y(:,:,i),zScaled)
%     xlabel('Payload (tons)')
%     ylabel('Cruise Speed (knots)')
%     zlabel('Boat Job Loss (percent decrease))')
%     colormap parula
%     colorbar
%     view(115,22)
%     hold on
% end
% hold off
% % figure(2)
% subplot(2,3,2);
% for i = 1:length(fleet)
%     surf(X(:,:,i),Y(:,:,i),ZC(:,:,i))
%     xlabel('Payload (tons)')
%     ylabel('Cruise Speed (knots)')
%     zlabel('Crop Loss (tons crops saved)')
%     colormap parula
%     colorbar
%     view(115,22)
%     hold on
% end
% zlim([0,max(ZC(:,:,:),[],'all')])
% hold off
% % figure(3)
% subplot(2,3,3);
% for i = 1:length(fleet)
%     surf(X(:,:,i),Y(:,:,i),-2.29568e-5*ZF(:,:,i))
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
%     surf(X(:,:,i),Y(:,:,i),ZI(:,:,i))
%     xlabel('Payload (tons)')
%     ylabel('Cruise Speed (knots)')
%     zlabel('Income (R$)')
%     colormap parula
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
%     surf(X(:,:,i),Y(:,:,i),ZT(:,:,i))
%     xlabel('Payload (tons)')
%     ylabel('Cruise Speed (knots)')
%     zlabel('Time Savings (hours)')
%     colormap parula
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
