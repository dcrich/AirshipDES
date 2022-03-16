warning off
% how to optimize with jumps due to fleet size
% how to explain spikes due to stochastic natural of simulation
if false %exist('uniform12149.mat','file')
    load uniform12149.mat
else
    steps = [1,1,1,2];
%     steps = [2,2,1];
%     steps = [2,5,1];
%     steps = [5,10,1];
    file = uigetfile('*.csv');
    output = readtable(file);
    x = output.Payload;
    y = output.CruiseSpeed;
    f = output.FleetSize;
    l = output.LoadThreshold;
    all = [x,y,f];
    zI = output.Income;
    zT = output.TimeSavings;
    zC = output.CropLoss;
    zB = output.BoatTripLoss;
    zF = output.ForestLoss;
    zL = output.LoadThreshold;
    
    payloadrange = [min(output.Payload),max(output.Payload)];
    speedrange = [min(output.CruiseSpeed),max(output.CruiseSpeed)];
    fleetrange = [min(output.FleetSize),max(output.FleetSize)];
    loadthreshrange = [min(zL),max(zL)];
    payload = payloadrange(1):steps(1):payloadrange(2);
    speed = speedrange(1):steps(2):speedrange(2);
    fleet = fleetrange(1):steps(3):fleetrange(2);
    loadthresh = linspace(loadthreshrange(1),loadthreshrange(2),steps(4));

    [payloadG, speedG, loadthreshG] = meshgrid(payload, speed, loadthresh);

    ZB = zeros(length(loadthresh),length(speed),length(payload));
    ZC = ZB;
    ZF = ZB;
    ZI = ZB;
    ZT = ZB;
    X = ZB;
    Y = ZB;
    F = ZB;
    counter = 1;
    for i = 1:length(loadthresh)
        for j = 1:length(speed)
            for k = 1:length(payload)
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


sizeOut = size(X);
% individual thresh
figure(111)
for i = 1:length(loadthresh)%length(fleet)
    zScaled = -100*ZB(i,:,:)/min(ZB(i,:,:),[],'all');
    tempx = reshape(X(i,:,:),[sizeOut(2),sizeOut(3)]);
    surfc(reshape(X(i,:,:),[sizeOut(2),sizeOut(3)]),reshape(Y(i,:,:),[sizeOut(2),sizeOut(3)]),reshape(zScaled,[sizeOut(2),sizeOut(3)]))
    xlabel('Payload (tons)')
    ylabel('Cruise Speed (knots)')
    zlabel('Impact to Boat Jobs (percent decrease))')
    colormap parula
    colorbar
    view(115,22)
    hold on
end
hold off
figure(222)
for i = 1:length(loadthresh)%length(fleet)
    surfc(reshape(X(i,:,:),[sizeOut(2),sizeOut(3)]),reshape(Y(i,:,:),[sizeOut(2),sizeOut(3)]),reshape(ZC(i,:,:),[sizeOut(2),sizeOut(3)]))
    xlabel('Payload (tons)')
    ylabel('Cruise Speed (knots)')
    zlabel('Impact to Crops (tons crops saved)')
    colormap parula
    colorbar
    view(115,22)
    hold on
end
% zlim([0,max(ZC(:,:,:),[],'all')])
hold off
figure(333)
for i = 1:length(loadthresh)%length(fleet)
    surfc(reshape(X(i,:,:),[sizeOut(2),sizeOut(3)]),reshape(Y(i,:,:),[sizeOut(2),sizeOut(3)]),reshape(-2.29568e-5*ZF(i,:,:),[sizeOut(2),sizeOut(3)]))
    xlabel('Payload (tons)')
    ylabel('Cruise Speed (knots)')
    zlabel('Impact to Forest (acres lost)')
    oldcolors = colormap;
    colormap(flipud(oldcolors))
    colorbar
    view(115,22)
    hold on
end
hold off
figure(444)
for i = 1:length(loadthresh)%length(fleet)
    surfc(reshape(X(i,:,:),[sizeOut(2),sizeOut(3)]),reshape(Y(i,:,:),[sizeOut(2),sizeOut(3)]),reshape(ZI(i,:,:),[sizeOut(2),sizeOut(3)]))
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
figure(555)
for i = 1:length(loadthresh)%length(fleet)
    surfc(reshape(X(i,:,:),[sizeOut(2),sizeOut(3)]),reshape(Y(i,:,:),[sizeOut(2),sizeOut(3)]),reshape(ZT(i,:,:),[sizeOut(2),sizeOut(3)]))
    xlabel('Payload (tons)')
    ylabel('Cruise Speed (knots)')
    zlabel('Time Savings (hours)')
    colormap parula
    colorbar
    view(115,22)
    hold on
end
hold off
