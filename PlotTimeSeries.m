file = uigetfile('*.csv');
output = readtable(file);
file2 = uigetfile('*.csv');
output2 = readtable(file2);
%%
airship10 = find(output.Airship == 0);
airship11 = find(output.Airship == 1);
SimulationTime1 = output.SimulationTime(airship10);
SimulationTime2 = output.SimulationTime(airship11);
airship20 = find(output2.Airship == 0);
airship21 = find(output2.Airship == 1);
SimulationTime3 = output2.SimulationTime(airship20);
SimulationTime4 = output2.SimulationTime(airship21);

PayloadLevel1 = output.PayloadLevel(airship10);
PayloadLevel2 = output.PayloadLevel(airship11);
PayloadLevel3 = output2.PayloadLevel(airship20);
PayloadLevel4 = output2.PayloadLevel(airship21);
Activity1 = output.Activity(airship10);
Activity2 = output.Activity(airship11);
Activity3 = output2.Activity(airship20);
Activity4 = output2.Activity(airship21);

figure(1)
plot(SimulationTime1,PayloadLevel1, 'k','LineWidth',5)
hold on
% plot(SimulationTime2,PayloadLevel2, 'g','LineWidth',4)
plot(SimulationTime3,PayloadLevel3, ':','Color', [0.5 0.5 0.5],'LineWidth',4)
% plot(SimulationTime4,PayloadLevel4, 'Color', [0.4660 0.6740 0.1880],'LineWidth',2)
% legend('27-0','27-1','26-0','26-1')
xlabel('Simulation Time (hours)')
ylabel('Payload Level (tons)')
labels = {'A','B','C'};
xline([2074.92,2076.27,2077.54],'--',labels,'Color',[0.5,0,0],...
    'LineWidth',1,'LabelVerticalAlignment','top','LabelOrientation','horizontal','FontSize',16)
legend('Larger Payload','Smaller Payload','Events','Location','southwest')
set(gca,'FontSize',18)
hold off
xlim([2070,2081])
Activity1(889) = -3;
Activity3(897) = -3;
figure(2)
plot(SimulationTime1,Activity1, 'k','LineWidth',5)
hold on
% plot(SimulationTime2,Activity2, 'g','LineWidth',4)
plot(SimulationTime3,Activity3, ':','Color', [0.5 0.5 0.5],'LineWidth',4)
labels = {'A','B','C'};
xline([2074.92,2076.27,2077.54],'--',labels,'Color',[0.5,0,0],...
    'LineWidth',1,'LabelVerticalAlignment','bottom','LabelOrientation','horizontal','FontSize',16)
% plot(SimulationTime4,Activity4, 'Color', [0.4660 0.6740 0.1880],'LineWidth',2)
% legend('27-0','27-1','26-0','26-1')
legend('Larger Payload','Smaller Payload','Events','Location','southwest')
xlabel('Simulation Time (hours)')
ylabel('Airship Status')
xlim([2070,2081])
ylim([-3.2,3.2])
names = {'Manaus (EOD)'; ''; 'Manus (Unload)'; 'Careiro'; 'Iranduba'; 'Jutaí'; 'Mantaquiri';''};
set(gca,'ytick',-3:4,'yticklabel',names,'FontSize',18)
hold off
%%
max(PayloadLevel1(1:length(PayloadLevel3)) - PayloadLevel3)
max(PayloadLevel2(1:length(PayloadLevel4)) - PayloadLevel4)
figure(4)
plot(1:length(Activity4),Activity1(1:length(Activity4))-Activity4)
%%
listActivities1 = Activity1(find(SimulationTime1 == 2335):find(SimulationTime1 == 2359));
listActivities2 = Activity2(find(SimulationTime2 == 2335):find(SimulationTime2 == 2359));
listActivities3 = Activity3(find(SimulationTime3 == 2335):find(SimulationTime3 == 2359));
listActivities4 = Activity4(find(SimulationTime4 == 2335):find(SimulationTime4 == 2359));
listActivities1(find(listActivities1==-2)) = [];
listActivities2(find(listActivities2==-2)) = [];
listActivities3(find(listActivities3==-2)) = [];
listActivities4(find(listActivities4==-2)) = [];




































