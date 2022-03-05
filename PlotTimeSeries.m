file = uigetfile('*.csv');
output = readtable(file);
file2 = uigetfile('*.csv');
output2 = readtable(file2);

airship10 = find(output.Airship == 0);
airship11 = find(output.Airship == 1);
SimulationTime_1 = output.SimulationTime(airship10);
SimulationTime_2 = output.SimulationTime(airship11);
airship20 = find(output2.Airship == 0);
airship21 = find(output2.Airship == 1);
SimulationTime_3 = output2.SimulationTime(airship20);
SimulationTime_4 = output2.SimulationTime(airship21);

PayloadLevel_1 = output.PayloadLevel(airship10);
PayloadLevel_2 = output.PayloadLevel(airship11);
PayloadLevel_3 = output2.PayloadLevel(airship20);
PayloadLevel_4 = output2.PayloadLevel(airship21);
Activity_1 = output.Activity(airship10);
Activity_2 = output.Activity(airship11);
Activity_3 = output2.Activity(airship20);
Activity_4 = output2.Activity(airship21);

figure(3)
plot(SimulationTime_1,PayloadLevel_1, 'r','LineWidth',5)
hold on
plot(SimulationTime_2,PayloadLevel_2, 'g','LineWidth',4)
plot(SimulationTime_3,PayloadLevel_3, 'b','LineWidth',3)
plot(SimulationTime_4,PayloadLevel_4, 'k','LineWidth',2)
legend('27-0','27-1','26-0','26-1')
hold off



figure(4)
plot(SimulationTime_1,Activity_1, 'r','LineWidth',5)
hold on
plot(SimulationTime_2,Activity_2, 'g','LineWidth',4)
plot(SimulationTime_3,Activity_3, 'b','LineWidth',3)
plot(SimulationTime_4,Activity_4, 'k','LineWidth',2)
legend('27-0','27-1','26-0','26-1')
hold off
%%
max(PayloadLevel_1 - PayloadLevel_3)
max(PayloadLevel_2 - PayloadLevel_4)
