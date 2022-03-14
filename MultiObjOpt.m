
% Payload, Speed, Fleet Size
% MAYBE ADD loading rate, unloading rate, load threshold
lb = [1,   20, 1, 0]; % , 0.001,
ub = [30, 100, 5, 1];
options = optimset('Display','off');
disp("Beginning Optimization...")
for i = 1:1000 % run GA multiple times to determine result
%     [xGA_nl(:,i),fGA_nl(i)] = ga(@airship_surrogate_model, length(lb),[],[],[],[],lb,ub,@nlc);
    [xGA_nl(:,i),fGA_nl(i)] = ga(@airship_surrogate_model, length(lb),[],[],[],[],lb,ub,[],options); % seems reasonable
%     xGA_nl(:,i) = fmincon(@airship_surrogate_model,lb,[],[],[],[],lb,ub); % not good
end
MEANBEST = round(mean(xGA_nl,2))
meanbest2 = round(mean(round(xGA_nl),2))

% format bank
% nlc([5,59,2])

function f = airship_surrogate_model(x)
wB = -0.2; % minimize Impact to Boat Jobs (B/C it's already negative)
wC = -0.2; % maximize Impact to Crops
wF =  0.2; % minimize Impact to Forest
wI = -0.2; % maximize Impact to Farmer Income
wT = -0.2; % maximize Impact to Farmer Time
PAYLOAD = round(x(1));
CRUISESPEED = round(x(2));
FLEETSIZE = round(x(3));
LOADTHRESHOLD = x(4);

% Neural Models
H2_1 = tanh((-5.75603132300366 + 0.00479814454802907 * CRUISESPEED + 0.469920605021782 * FLEETSIZE + -0.0287355044167123 * LOADTHRESHOLD + 2.41628214675343 * PAYLOAD));

H2_2 = tanh((1.44838282939941 + 0.00909953660221097 * CRUISESPEED + 0.672631575632398 * FLEETSIZE + 0.0850169192130352 * LOADTHRESHOLD + -0.00103730098328378 * PAYLOAD));

H2_3 = tanh((-64.8768379274277 + 0.00440233229745275 * CRUISESPEED + 0.43625520152061 * FLEETSIZE + 62.833801508056 * LOADTHRESHOLD + -1.28703457330212 * PAYLOAD));

H2_4 = tanh((-0.959885991193005 + -0.00485241198481822 * CRUISESPEED + -0.105292598764789 * FLEETSIZE + 0.0401355453072585 * LOADTHRESHOLD + -0.149571919061724 * PAYLOAD));

H1_1 = tanh((-10.3850851332614 + -15.2057297918261 * H2_1 + -14.1536031484126 * H2_2 + 18.2230971766505 * H2_3 + 16.3379846998785 * H2_4));

H1_2 = tanh((-16.5642853935088 + 63.489164459487 * H2_1 + 0.210317299401058 * H2_2 + -84.157760853723 * H2_3 + 4.41782067538613 * H2_4));

H1_3 = tanh((-16.160655685465 + -12.3521581565424 * H2_1 + -2.74100471051557 * H2_2 + 19.1301378424478 * H2_3 + 4.65987178126424 * H2_4));

H1_4 = tanh((-96.4105848412762 + 0.367770316413491 * H2_1 + 91.1102687334951 * H2_2 + 8.90363011054483 * H2_3 + -15.8155116955356 * H2_4));

PREDICTED_BOAT_TRIP_LOSS = -1144.78694072882 + -643.769431991615 * H1_1 + -2614.08512536963 * H1_2 + -827.678048854795 * H1_3 + -1020.33783453748 * H1_4;


H2_1 = tanh((-0.773091641814244 + 0.00243699763138218 * CRUISESPEED + 0.241072843605256 * FLEETSIZE + 0.176756530701704 * LOADTHRESHOLD + -0.312273483176279 * PAYLOAD));

H2_2 = tanh((-1.96712666475144 + 0.0325457617552094 * CRUISESPEED + -0.330251814152188 * FLEETSIZE + 0.165140076234563 * LOADTHRESHOLD + -0.00698432002335753 * PAYLOAD));

H2_3 = tanh((0.501932372125631 + -0.00250327504309064 * CRUISESPEED + -0.232881276970301 * FLEETSIZE + 0.624513600267534 * LOADTHRESHOLD + -0.235941162208634 * PAYLOAD));

H2_4 = tanh((1.00603555951529 + -0.00998709975510537 * CRUISESPEED + -0.302607811624068 * FLEETSIZE + -0.0625184906364878 * LOADTHRESHOLD + -0.00294675403707748 * PAYLOAD));

H1_1 = tanh((1.55062666992885 + -1.3694437418225 * H2_1 + -0.301253733887449 * H2_2 + 1.43496386916848 * H2_3 + -1.66700097607852 * H2_4));

H1_2 = tanh((-0.721650481004815 + 3.01244265836738 * H2_1 + -0.06225431500437 * H2_2 + 3.3652428177009 * H2_3 + -0.889956324046573 * H2_4));

H1_3 = tanh((2.06794600234075 + 3.22028264903952 * H2_1 + 0.805525796119597 * H2_2 + -0.250922154651105 * H2_3 + 3.24005088157559 * H2_4));

H1_4 = tanh((0.0354671485455951 + -2.74259640584227 * H2_1 + -0.213254676952011 * H2_2 + -1.78045171962941 * H2_3 + 0.0365324330653902 * H2_4));

PREDICTED_CROP_LOSS = -1462.33915555233 + -2102.18603758528 * H1_1 + -6794.31565986378 * H1_2 + -1613.65797485278 * H1_3 + -4200.28960319683 * H1_4;


H2_1 = tanh((0.663303286844691 + 0.0000000233378808619 * CRUISESPEED + -0.066067907156015 * FLEETSIZE + 0.0000066036457104993 * LOADTHRESHOLD + -0.0396331815278092 * PAYLOAD));

H2_2 = tanh((1.79348665561358 + 0.0000007690226297241 * CRUISESPEED + -0.199320949978464 * FLEETSIZE + -0.0000788631033172107 * LOADTHRESHOLD + 0.117078495775262 * PAYLOAD));

H2_3 = tanh((-0.870155436270339 + 0.0000002250244975693 * CRUISESPEED + 0.0870408541453607 * FLEETSIZE + -0.0000254183134477584 * LOADTHRESHOLD + 0.0531330076096644 * PAYLOAD));

H2_4 = tanh((1.00224060408092 + 0.0000003640367841382 * CRUISESPEED + 0.0933040240073112 * FLEETSIZE + -0.0000136838612664491 * LOADTHRESHOLD + -0.0467132006768733 * PAYLOAD));

H1_1 = tanh((-2.93329490310406 + 1.29206760297898 * H2_1 + 3.51411320846103 * H2_2 + 1.36539282304386 * H2_3 + 1.40371478709301 * H2_4));

H1_2 = tanh((-1.15885588225526 + -2.46207595715428 * H2_1 + 0.422798924994942 * H2_2 + -0.990539997230518 * H2_3 + 0.270973985409323 * H2_4));

H1_3 = tanh((-0.581492315148716 + 6.44178760337716 * H2_1 + 1.9134574511266 * H2_2 + 4.5557459199104 * H2_3 + -0.458311914610254 * H2_4));

H1_4 = tanh((-3.27628100789887 + 5.10697084091407 * H2_1 + 2.12659767803016 * H2_2 + 3.78533978116357 * H2_3 + 0.936510928878754 * H2_4));

PREDICTED_FOREST_LOSS = 34391.8873053095 + 15488.3633363442 * H1_1 + 28343.9825289507 * H1_2 + -23105.8370988532 * H1_3 + 12025.6987608468 * H1_4;


H2_1 = tanh((2.36794657635359 + -0.00989722585319849 * CRUISESPEED + -0.350372207074847 * FLEETSIZE + -0.201240690906839 * LOADTHRESHOLD + 0.199620824822803 * PAYLOAD));

H2_2 = tanh((2.43423274676822 + -0.00977717951268109 * CRUISESPEED + -0.38152410300764 * FLEETSIZE + 0.064572680819742 * LOADTHRESHOLD + -0.0244960895648016 * PAYLOAD));

H2_3 = tanh((1.13967208971765 + -0.0135295894098759 * CRUISESPEED + 0.128889941928247 * FLEETSIZE + 0.376946585320654 * LOADTHRESHOLD + -0.0528018242060736 * PAYLOAD));

H2_4 = tanh((1.56188105641818 + -0.00949301442282156 * CRUISESPEED + -0.0788201389162313 * FLEETSIZE + -0.0652706368982341 * LOADTHRESHOLD + 0.00169919490194867 * PAYLOAD));

H1_1 = tanh((-2.53959672664952 + -3.50162275311638 * H2_1 + -0.286593201626918 * H2_2 + 1.13347415125413 * H2_3 + 8.55669957218313 * H2_4));

H1_2 = tanh((-0.0922688524778229 + -0.219838441109232 * H2_1 + -0.565060839152235 * H2_2 + 0.115009421165848 * H2_3 + 0.856340962247967 * H2_4));

H1_3 = tanh((1.05222021604082 + 18.5335283914523 * H2_1 + -16.0369393054512 * H2_2 + 1.53238673018533 * H2_3 + -4.48286171527013 * H2_4));

H1_4 = tanh((3.27957989755887 + -4.83950234956735 * H2_1 + 0.197789800408109 * H2_2 + 1.30908680809209 * H2_3 + 5.23862912259902 * H2_4));

PREDICTED_INCOME = -4427632.06800365 + 130328.826152438 * H1_1 + -586500.522045346 * H1_2 + 4932328.4312387 * H1_3 + 674772.659546848 * H1_4;


H2_1 = tanh((0.83378821832723 + -0.00209713091266587 * CRUISESPEED + -0.0688410374298678 * FLEETSIZE + -0.935811512098342 * LOADTHRESHOLD + 0.244690203302658 * PAYLOAD));

H2_2 = tanh((2.74881747160529 + -0.0721255482458542 * CRUISESPEED + -0.129405691047359 * FLEETSIZE + -0.713026534715612 * LOADTHRESHOLD + 0.0083265740175479 * PAYLOAD));

H2_3 = tanh((1.23233947514012 + -0.00297144410872564 * CRUISESPEED + -0.913381488469874 * FLEETSIZE + -0.0490418451269677 * LOADTHRESHOLD + -0.0109096715648858 * PAYLOAD));

H2_4 = tanh((-0.160091366745633 + 0.00147232954089439 * CRUISESPEED + 0.050852775875599 * FLEETSIZE + -0.260966002504825 * LOADTHRESHOLD + 0.326664557677971 * PAYLOAD));

H1_1 = tanh((0.280489269198527 + -0.498093028892304 * H2_1 + 0.243213123229474 * H2_2 + 0.555746407429308 * H2_3 + 0.163554720973274 * H2_4));

H1_2 = tanh((-1.11277236848422 + -3.05241196246005 * H2_1 + -0.0830783131578278 * H2_2 + -0.411314261464646 * H2_3 + -3.57832233227297 * H2_4));

H1_3 = tanh((0.685717233521692 + 0.577673245234402 * H2_1 + -0.135015757837441 * H2_2 + -0.248806285651413 * H2_3 + -0.765529813275076 * H2_4));

H1_4 = tanh((-0.432120710323035 + 0.187967079419757 * H2_1 + -0.2372027165703 * H2_2 + -0.609020206790501 * H2_3 + 0.491403630449268 * H2_4));

PREDICTED_TIME_SAVINGS = -31214.1946787699 + 38620.122078907 * H1_1 + -17955.9687222269 * H1_2 + 29868.4457088424 * H1_3 + 33785.5137234195 * H1_4;

% normalize impacts based on simulation max and mins
bshift = -595;
bnorm = 3260 + bshift;
cshift = 2554;
cnorm = cshift + 658;
fshift = -582;
fnorm = 25000 + fshift;
ishift = 442000;
inorm = ishift + 1384000;
tshift = 1588;
tnorm = 8732 + tshift;

BoatJobLoss = ((PREDICTED_BOAT_TRIP_LOSS) + bshift) /(bnorm);

Crops = ((PREDICTED_CROP_LOSS) + cshift)/(cnorm);

ForestLoss = ((PREDICTED_FOREST_LOSS) + fshift)/(fnorm);

Income = ((PREDICTED_INCOME) + ishift)/(inorm);

TimeSavings = ((PREDICTED_TIME_SAVINGS) + tshift)/ (tnorm);

% weight and sum impacts
f = wB * BoatJobLoss + wC * Crops + wF * ForestLoss + wI * Income + wT * TimeSavings;
end


function [c,ceq] = nlc(x)
% No constraints needed to define feasible space since cities are close
%   enough that all designs are feasible
Payload = round(x(1));
CruiseSpeed = round(x(2));
FleetSize = round(x(3));
PayloadFraction = 0.3;
FuelTankFraction = 0.05;
FinenessRatio = 3;
ConstraintSize = 81000;


% footprint constraint
totalLift_lb = 2000 * Payload / PayloadFraction;
liftLbPerCubicFoot = 0.06; % helium
specificDensity = 0.95; % at ~1500 ft
airshipVolume_ft3 = (totalLift_lb / liftLbPerCubicFoot) / specificDensity;
diameter_ft = 0.3048 * (4*airshipVolume_ft3 / (0.6 * pi * FinenessRatio))^(1/3) % m # not using percent cylinder
length_ft = diameter_ft * FinenessRatio % m
footprint_ft2 = length_ft * diameter_ft;

FootprintConstraint = footprint_ft2 * FleetSize * 1.1 - ConstraintSize; % this equivalent to forrestloss being below a size


c(:,1) = FootprintConstraint;
ceq = [];
end




















