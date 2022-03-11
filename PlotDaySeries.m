file11 = uigetfile('*.csv');
output11 = readtable(file11);
file22 = uigetfile('*.csv');
output22 = readtable(file22);
%%
DifferenceInDailyLossC = max(output11.CareiroFruitLoss - output22.CareiroFruitLoss)
DifferenceInDailyLossI = max(output11.IrandubaFruitLoss - output22.IrandubaFruitLoss)
DifferenceInDailyLossJ = max(output11.IrandubaFruitLoss - output22.IrandubaFruitLoss)
DifferenceInDailyLossM = max(output11.ManaquiriFruitLoss - output22.ManaquiriFruitLoss)
%%
figure(12)
plot(output11.SimulationDay,output11.CareiroVisits, 'r','LineWidth',5)
hold on
plot(output11.SimulationDay,output11.IrandubaVisits, 'g','LineWidth',4)
plot(output11.SimulationDay,output11.JutaiVisits, 'b','LineWidth',3)
% plot(output11.SimulationDay,output11.ManaquiriVisits, 'c','LineWidth',2)

plot(output22.SimulationDay,-output22.CareiroVisits, 'Color',[0.9290 0.6940 0.1250],'LineWidth',5)
plot(output22.SimulationDay,-output22.IrandubaVisits, 'k','LineWidth',4)
plot(output22.SimulationDay,-output22.JutaiVisits, 'm','LineWidth',3)
% plot(output22.SimulationDay,-output22.ManaquiriVisits, 'Color',[0.8500 0.3250 0.0980],'LineWidth',2)
% legend('27-C','27-I','27-J','27-M','26-C','26-I','26-J','26-M')
legend('27-C','27-I','27-J','26-C','26-I','26-J')
hold off



figure(22)
plot(output11.SimulationDay,output11.CareiroFruitLoss, 'r','LineWidth',8)
hold on
plot(output11.SimulationDay,output11.IrandubaFruitLoss, 'g','LineWidth',7)
plot(output11.SimulationDay,output11.JutaiFruitLoss, 'b','LineWidth',6)
% plot(output11.SimulationDay,output11.ManaquiriFruitLoss, 'c','LineWidth',5)

plot(output22.SimulationDay,output22.CareiroFruitLoss, 'Color',[0.9290 0.6940 0.1250],'LineWidth',4)
plot(output22.SimulationDay,output22.IrandubaFruitLoss, 'k','LineWidth',3)
plot(output22.SimulationDay,output22.JutaiFruitLoss, 'm','LineWidth',2)
% plot(output22.SimulationDay,output22.ManaquiriFruitLoss,  'Color',[0.8500 0.3250 0.0980],'LineWidth',1)
% legend('27-C','27-I','27-J','27-M','26-C','26-I','26-J','26-M')
legend('27-C','27-I','27-J','26-C','26-I','26-J')
hold off


figure(32)
plot(output11.SimulationDay,output11.CareiroLoadTime, 'r','LineWidth',2)
hold on
plot(output11.SimulationDay,output11.IrandubaLoadTime, 'g','LineWidth',2)
plot(output11.SimulationDay,output11.JutaiLoadTime, 'b','LineWidth',2)
% plot(output11.SimulationDay,output11.ManaquiriLoadTime, 'c','LineWidth',2)

plot(output22.SimulationDay,-output22.CareiroLoadTime, 'Color',[0.9290 0.6940 0.1250],'LineWidth',2)
plot(output22.SimulationDay,-output22.IrandubaLoadTime, 'k','LineWidth',2)
plot(output22.SimulationDay,-output22.JutaiLoadTime, 'm','LineWidth',2)
% plot(output22.SimulationDay,-output22.ManaquiriLoadTime, 'Color',[0.8500 0.3250 0.0980],'LineWidth',2)
% legend('27-C','27-I','27-J','27-M','26-C','26-I','26-J','26-M')
legend('27-C','27-I','27-J','26-C','26-I','26-J')
hold off



figure(42)
plot(output11.SimulationDay,output11.CareiroLoadedGoods, 'r','LineWidth',8)
hold on
plot(output11.SimulationDay,output11.IrandubaLoadedGoods, 'g','LineWidth',7)
plot(output11.SimulationDay,output11.JutaiLoadedGoods, 'b','LineWidth',6)
% plot(output11.SimulationDay,output11.ManaquiriLoadedGoods, 'c','LineWidth',5)

plot(output22.SimulationDay,output22.CareiroLoadedGoods, 'Color',[0.9290 0.6940 0.1250],'LineWidth',4)
plot(output22.SimulationDay,output22.IrandubaLoadedGoods, 'k','LineWidth',3)
plot(output22.SimulationDay,output22.JutaiLoadedGoods, 'm','LineWidth',2)
% plot(output22.SimulationDay,output22.ManaquiriLoadedGoods,  'Color',[0.8500 0.3250 0.0980],'LineWidth',1)
plot(output22.SimulationDay,0.642952587*output22.Production, 'Color','y','LineWidth',1)
% legend('27-C','27-I','27-J','27-M','26-C','26-I','26-J','26-M','I-Produced')
legend('27-C','27-I','27-J','26-C','26-I','26-J','I-Produced')
hold off











