file = uigetfile('*.csv');
output = readtable(file);
file2 = uigetfile('*.csv');
output2 = readtable(file2);



figure(1)
plot(output.SimulationDay,output.CareiroVisits, 'r')
hold on
plot(output.SimulationDay,output.IrandubaVisits, 'g')
plot(output.SimulationDay,output.JutaiVisits, 'b')
plot(output.SimulationDay,output.ManaquiriVisits, 'c')

plot(output2.SimulationDay,output2.CareiroVisits, 'Color',[0.9290 0.6940 0.1250])
plot(output2.SimulationDay,output2.IrandubaVisits, 'k')
plot(output2.SimulationDay,output2.JutaiVisits, 'm')
plot(output2.SimulationDay,output2.ManaquiriVisits, 'Color',[0.8500 0.3250 0.0980])
legend('27-C','27-I','27-J','27-M','26-C','26-I','26-J','26-M')
hold off



figure(2)
plot(output.SimulationDay,output.CareiroFruitLoss, 'r','LineWidth',50)
hold on
plot(output.SimulationDay,output.IrandubaFruitLoss, 'g','LineWidth',40)
plot(output.SimulationDay,output.JutaiFruitLoss, 'b','LineWidth',30)
plot(output.SimulationDay,output.ManaquiriFruitLoss, 'c','LineWidth',20)

plot(output2.SimulationDay,output2.CareiroFruitLoss, 'Color',[0.9290 0.6940 0.1250],'LineWidth',10)
plot(output2.SimulationDay,output2.IrandubaFruitLoss, 'k','LineWidth',8)
plot(output2.SimulationDay,output2.JutaiFruitLoss, 'm','LineWidth',6)
plot(output2.SimulationDay,output2.ManaquiriFruitLoss,  'Color',[0.8500 0.3250 0.0980],'LineWidth',4)
legend('27-C','27-I','27-J','27-M','26-C','26-I','26-J','26-M')
hold off


figure(3)
plot(output.SimulationDay,output.CareiroLoadTime, 'r','LineWidth',2)
hold on
plot(output.SimulationDay,output.IrandubaLoadTime, 'g','LineWidth',2)
plot(output.SimulationDay,output.JutaiLoadTime, 'b','LineWidth',2)
plot(output.SimulationDay,output.ManaquiriLoadTime, 'c','LineWidth',2)

plot(output2.SimulationDay,output2.CareiroLoadTime, 'Color',[0.9290 0.6940 0.1250],'LineWidth',2)
plot(output2.SimulationDay,output2.IrandubaLoadTime, 'k','LineWidth',2)
plot(output2.SimulationDay,output2.JutaiLoadTime, 'm','LineWidth',2)
plot(output2.SimulationDay,output2.ManaquiriLoadTime, 'Color',[0.8500 0.3250 0.0980],'LineWidth',2)
legend('27-C','27-I','27-J','27-M','26-C','26-I','26-J','26-M')
hold off



figure(4)
plot(output.SimulationDay,output.CareiroLoadedGoods, 'r','LineWidth',50)
hold on
plot(output.SimulationDay,output.IrandubaLoadedGoods, 'g','LineWidth',40)
plot(output.SimulationDay,output.JutaiLoadedGoods, 'b','LineWidth',30)
plot(output.SimulationDay,output.ManaquiriLoadedGoods, 'c','LineWidth',25)

plot(output2.SimulationDay,output2.CareiroLoadedGoods, 'Color',[0.9290 0.6940 0.1250],'LineWidth',20)
plot(output2.SimulationDay,output2.IrandubaLoadedGoods, 'k','LineWidth',15)
plot(output2.SimulationDay,output2.JutaiLoadedGoods, 'm','LineWidth',10)
plot(output2.SimulationDay,output2.ManaquiriLoadedGoods,  'Color',[0.8500 0.3250 0.0980],'LineWidth',5)
legend('27-C','27-I','27-J','27-M','26-C','26-I','26-J','26-M')
hold off












