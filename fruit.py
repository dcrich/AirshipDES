import numpy as np

class fruit:
    def __init__(self,numberOfNewCities):
        if numberOfNewCities == 0:
            # data from FarmerDataAdjusted.xls, distrubution of daily fruit production through the year, in imperial tons
            metricTonsToImperialTons = 1.10231
            self.DailyFruitProduction = metricTonsToImperialTons * np.array([4.90117687168451, 4.91031646930524, 4.92437011183630, 4.93649279501228, 4.95014157960967, 4.96548161903437, 4.98887208640314, 5.00886212676615, 5.03117066199798, 5.05600535878424, 5.09341863947534, 5.12498775571930, 5.15980990055501, 5.19810410208063, 5.25493282298304, 5.30214551151104, 5.35350350085848, 5.40917640799240, 5.49036914967390, 5.55663374228312, 5.62758889511747, 5.70327273359316, 5.81152660834755, 5.89814788676384, 5.98929888492371, 6.11757749333149, 6.21853999173363, 6.32324829337238, 6.43134580653531, 6.58002929731689, 6.69434512056264, 6.81468431373320, 6.93240654668110, 7.09029876996453, 7.20858786635470, 7.32603341952800, 7.44212189854525, 7.59303472294466, 7.70285556018058, 7.80899200936550, 7.91105389761043, 8.03905686559711, 8.12887744152224, 8.21304978253074, 8.29074320341420, 8.38388155379347, 8.44638287240029, 8.50177121098050, 8.56467914067670, 8.60428251211838, 8.63777808576929, 8.66468944135223, 8.69105757182629, 8.70531406007943, 8.71427607126381, 8.71889054793876, 8.71922739723006, 8.71585762074335, 8.71002859601729, 8.70232053173004, 8.69010104640178, 8.68018568286068, 8.79641764525067, 8.80188475451504, 8.81098514890519, 8.82168927618986, 8.83658100766846, 8.85434771104593, 8.88342447166076, 8.91100951241923, 8.94422956914249, 8.98273954280306, 9.03719551301618, 9.08692107475378, 9.14060417879011, 9.20353773040584, 9.28551469637137, 9.35595429405062, 9.43130669372908, 9.53789658547303, 9.62577339205677, 9.71688729730981, 9.81252687275417, 9.94692434840426, 10.0527645841621, 10.1628330396960, 10.2787026015753, 10.4356790611307, 10.5593183576528, 10.6886474066959, 10.8626323835578, 10.9996179392250, 11.1399759909746, 11.2644899869009, 11.4651976631350, 11.6207195769662, 11.7812606691477, 11.9429936355499, 12.1614611853255, 12.3322360243090, 12.5039971615745, 12.6785934176291, 12.9136137039360, 13.0962631390646, 13.2792620727526, 13.5399233692091, 13.7139958648582, 13.9029867768846, 14.0931429338479, 14.3667504984261, 14.5393828129662, 14.7307732365473, 14.9216304437154, 15.1959386167682, 15.3622377486374, 15.5478323030820, 15.7323351470418, 15.9693882178411, 16.1437678314555, 16.3149874576192, 16.5555475843450, 16.6883834085801, 16.8384732954013, 16.9825594449637, 17.1836624071526, 17.2835026618100, 17.3991814945023, 17.5041681055582, 17.6507922614321, 17.7087314398468, 17.7779501116961, 17.8354788798306, 17.9149621724938, 17.9221882831579, 17.9382289689717, 17.9598674747818, 17.9449329352021, 17.8965398768752, 17.8549686859129, 17.7972524176287, 17.7054818210361, 17.6190712118903, 17.5189896047721, 17.3828973571260, 17.2367972294205, 17.0948368445982, 16.9016969832747, 16.7318566931879, 16.5373588425709, 16.3455452856680, 16.0893074406968, 15.8757061303309, 15.6408220949549, 15.4111538995484, 15.1054365982389, 14.8594027236372, 14.5967737940760, 14.3404527009703, 14.0021165551219, 13.7348189663589, 13.4589372584850, 13.1075361192536, 12.8339409867402, 12.5554162231432, 12.2837883277497, 11.9304493362788, 11.6595840035298, 11.3879666237278, 11.1243055384152, 10.7821702621831, 10.5266568481150, 10.2718061563049, 10.0237047776344, 9.70870232615360, 9.47484353422856, 9.24409215375906, 8.95243468645942, 8.73907217127155, 8.53229564651996, 8.32832575097253, 8.07617411289909, 7.89220903882371, 7.71339230530407, 7.54198585251137, 7.32947009180552, 7.13552181575183, 6.99044600989788, 6.85363001386365, 6.68283280120711, 6.55918784160174, 6.44334744706939, 6.29976188267278, 6.19617583878672, 6.09977051551468, 6.00883137899447, 5.89576573852370, 5.81686124707095, 5.74279425367783, 5.67336811560199, 5.58767645129208, 5.52830774799423, 5.47291943701574, 5.40492203256548, 5.35806451291012, 5.31454615287620, 5.27320279242196, 5.22496200837776, 5.19126976498829, 5.16015413635332, 5.13062279600295, 5.09667820285009, 5.07302338712695, 5.05056809746531, 5.03065934040337, 5.00733671860512, 4.99046935435742, 4.86242386343084, 4.86068229749055, 4.85902039357234, 4.85692430194841, 4.85543894899568, 4.85402524539498, 4.85224760213348, 4.85099173529582, 4.84979953921729, 4.84830492106332, 4.84725217788743, 4.84625536574897, 4.84531223417146, 4.84413441322140, 4.84330801239217, 4.84252809312706, 4.84155695510773, 4.84087757624426, 4.84023801831665, 4.83944397198689, 4.83889010403169, 4.83836999878516, 4.83788196166270, 4.83727830807370, 4.83685882988355, 4.83646618701218, 4.83598191684974, 4.83564636642917, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461])
            self.TotalFruitProduction = np.sum(self.DailyFruitProduction)
            # self.TotalProductionValue = 4205000.0 # in brazilian reals
            self.AverageFruitProduction = np.mean(self.DailyFruitProduction)

            # fraction of daily production from each city, fractions from FarmerDataAdjusted.xls, fraction = fraction of production from that city
            CareiroProduction = 0.104346379 * self.DailyFruitProduction
            IrandubaProduction = 0.642952587 * self.DailyFruitProduction
            JutaiProduction = 0.094446983 * self.DailyFruitProduction
            ManaquiriProduction = 0.158254051 * self.DailyFruitProduction
            # fruit available at each city each day
            self.DailyCityFruitProduction_TonsPerDay = np.round(np.array([CareiroProduction, IrandubaProduction, JutaiProduction, ManaquiriProduction]),decimals=3)
            self.DailyCityFruitProduction_TonsPerDay[self.DailyCityFruitProduction_TonsPerDay < 0.0] = 0.0
            # daily value in reals per ton of fruit produced in each city, from FarmerDataAdjusted.xls, value = production value from that city / all goods produced in that city
            # in brazilian reals
            CareiroValue = 1000 * 1.873830294
            IrandubaValue = 1000 * 2.099050572
            JutaiValue = 1000 * 2.034181964
            ManaquiriValue = 1000 * 2.474721974
            # average fruit value per ton for each city
            self.AverageFruitValueCity_RealsPerTon = np.array([CareiroValue, IrandubaValue, JutaiValue, ManaquiriValue])

            self.TotalGoodsSoldFraction = 1.0 - 0.205
            self.TotalLossFraction = 0.205 
            self.CitySoldFraction = np.array(  [0.693590376,
                                                0.846035343,
                                                0.708805859,
                                                0.70518231])
        else:
            randomseed = 96
            scaleFactor = 1 + 0.25 * numberOfNewCities
            # data from FarmerDataAdjusted.xls, distrubution of daily fruit production through the year, in imperial tons
            metricTonsToImperialTons = 1.10231
            self.DailyFruitProduction = scaleFactor * metricTonsToImperialTons * np.array([4.90117687168451, 4.91031646930524, 4.92437011183630, 4.93649279501228, 4.95014157960967, 4.96548161903437, 4.98887208640314, 5.00886212676615, 5.03117066199798, 5.05600535878424, 5.09341863947534, 5.12498775571930, 5.15980990055501, 5.19810410208063, 5.25493282298304, 5.30214551151104, 5.35350350085848, 5.40917640799240, 5.49036914967390, 5.55663374228312, 5.62758889511747, 5.70327273359316, 5.81152660834755, 5.89814788676384, 5.98929888492371, 6.11757749333149, 6.21853999173363, 6.32324829337238, 6.43134580653531, 6.58002929731689, 6.69434512056264, 6.81468431373320, 6.93240654668110, 7.09029876996453, 7.20858786635470, 7.32603341952800, 7.44212189854525, 7.59303472294466, 7.70285556018058, 7.80899200936550, 7.91105389761043, 8.03905686559711, 8.12887744152224, 8.21304978253074, 8.29074320341420, 8.38388155379347, 8.44638287240029, 8.50177121098050, 8.56467914067670, 8.60428251211838, 8.63777808576929, 8.66468944135223, 8.69105757182629, 8.70531406007943, 8.71427607126381, 8.71889054793876, 8.71922739723006, 8.71585762074335, 8.71002859601729, 8.70232053173004, 8.69010104640178, 8.68018568286068, 8.79641764525067, 8.80188475451504, 8.81098514890519, 8.82168927618986, 8.83658100766846, 8.85434771104593, 8.88342447166076, 8.91100951241923, 8.94422956914249, 8.98273954280306, 9.03719551301618, 9.08692107475378, 9.14060417879011, 9.20353773040584, 9.28551469637137, 9.35595429405062, 9.43130669372908, 9.53789658547303, 9.62577339205677, 9.71688729730981, 9.81252687275417, 9.94692434840426, 10.0527645841621, 10.1628330396960, 10.2787026015753, 10.4356790611307, 10.5593183576528, 10.6886474066959, 10.8626323835578, 10.9996179392250, 11.1399759909746, 11.2644899869009, 11.4651976631350, 11.6207195769662, 11.7812606691477, 11.9429936355499, 12.1614611853255, 12.3322360243090, 12.5039971615745, 12.6785934176291, 12.9136137039360, 13.0962631390646, 13.2792620727526, 13.5399233692091, 13.7139958648582, 13.9029867768846, 14.0931429338479, 14.3667504984261, 14.5393828129662, 14.7307732365473, 14.9216304437154, 15.1959386167682, 15.3622377486374, 15.5478323030820, 15.7323351470418, 15.9693882178411, 16.1437678314555, 16.3149874576192, 16.5555475843450, 16.6883834085801, 16.8384732954013, 16.9825594449637, 17.1836624071526, 17.2835026618100, 17.3991814945023, 17.5041681055582, 17.6507922614321, 17.7087314398468, 17.7779501116961, 17.8354788798306, 17.9149621724938, 17.9221882831579, 17.9382289689717, 17.9598674747818, 17.9449329352021, 17.8965398768752, 17.8549686859129, 17.7972524176287, 17.7054818210361, 17.6190712118903, 17.5189896047721, 17.3828973571260, 17.2367972294205, 17.0948368445982, 16.9016969832747, 16.7318566931879, 16.5373588425709, 16.3455452856680, 16.0893074406968, 15.8757061303309, 15.6408220949549, 15.4111538995484, 15.1054365982389, 14.8594027236372, 14.5967737940760, 14.3404527009703, 14.0021165551219, 13.7348189663589, 13.4589372584850, 13.1075361192536, 12.8339409867402, 12.5554162231432, 12.2837883277497, 11.9304493362788, 11.6595840035298, 11.3879666237278, 11.1243055384152, 10.7821702621831, 10.5266568481150, 10.2718061563049, 10.0237047776344, 9.70870232615360, 9.47484353422856, 9.24409215375906, 8.95243468645942, 8.73907217127155, 8.53229564651996, 8.32832575097253, 8.07617411289909, 7.89220903882371, 7.71339230530407, 7.54198585251137, 7.32947009180552, 7.13552181575183, 6.99044600989788, 6.85363001386365, 6.68283280120711, 6.55918784160174, 6.44334744706939, 6.29976188267278, 6.19617583878672, 6.09977051551468, 6.00883137899447, 5.89576573852370, 5.81686124707095, 5.74279425367783, 5.67336811560199, 5.58767645129208, 5.52830774799423, 5.47291943701574, 5.40492203256548, 5.35806451291012, 5.31454615287620, 5.27320279242196, 5.22496200837776, 5.19126976498829, 5.16015413635332, 5.13062279600295, 5.09667820285009, 5.07302338712695, 5.05056809746531, 5.03065934040337, 5.00733671860512, 4.99046935435742, 4.86242386343084, 4.86068229749055, 4.85902039357234, 4.85692430194841, 4.85543894899568, 4.85402524539498, 4.85224760213348, 4.85099173529582, 4.84979953921729, 4.84830492106332, 4.84725217788743, 4.84625536574897, 4.84531223417146, 4.84413441322140, 4.84330801239217, 4.84252809312706, 4.84155695510773, 4.84087757624426, 4.84023801831665, 4.83944397198689, 4.83889010403169, 4.83836999878516, 4.83788196166270, 4.83727830807370, 4.83685882988355, 4.83646618701218, 4.83598191684974, 4.83564636642917, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461])
            self.TotalFruitProduction = np.sum(self.DailyFruitProduction)
            self.AverageFruitProduction = np.mean(self.DailyFruitProduction)

            # fruit available at each city each day
            self.DailyCityFruitProduction_TonsPerDay = np.array([])
            fruitFractions = np.random.default_rng(randomseed).uniform(0,1 , 4+numberOfNewCities)
            fruitFractions = (1/np.sum(fruitFractions)) * fruitFractions
            checkthis = np.sum(fruitFractions)

            # daily value in reals per ton of fruit produced in each city, from FarmerDataAdjusted.xls, value = production value from that city / all goods produced in that city
            # in brazilian reals
            CareiroValue = 1000 * 1.873830294
            IrandubaValue = 1000 * 2.099050572
            JutaiValue = 1000 * 2.034181964
            ManaquiriValue = 1000 * 2.474721974
            # average fruit value per ton for each city
            self.AverageFruitValueCity_RealsPerTon = np.array([CareiroValue, IrandubaValue, JutaiValue, ManaquiriValue])
            averageValueNewCityM = np.mean(self.AverageFruitValueCity_RealsPerTon)
            averageValueNewCityS =np.std(self.AverageFruitValueCity_RealsPerTon)
            for fruitfrac in fruitFractions:
                averageValueNewCity = np.abs(np.random.default_rng(randomseed).normal(averageValueNewCityM,averageValueNewCityS))
                self.AverageFruitValueCity_RealsPerTon = np.append(self.AverageFruitValueCity_RealsPerTon,averageValueNewCity)
                self.DailyCityFruitProduction_TonsPerDay = np.append(self.DailyCityFruitProduction_TonsPerDay,
                                                                     fruitfrac * self.DailyFruitProduction)
            self.DailyCityFruitProduction_TonsPerDay = np.round(self.DailyCityFruitProduction_TonsPerDay,decimals=3)
            self.DailyCityFruitProduction_TonsPerDay[self.DailyCityFruitProduction_TonsPerDay < 0.0] = 0.0
            
            self.TotalGoodsSoldFraction = 1.0 - 0.205
            self.TotalLossFraction = 0.205 
            self.CitySoldFraction = np.array(  [0.693590376,
                                                0.846035343,
                                                0.708805859,
                                                0.70518231])

# class fruit:
#     def __init__(self):
#         # data from FarmerDataAdjusted.xls, distrubution of daily fruit production through the year, in imperial tons
#         metricTonsToImperialTons = 1.10231
#         self.DailyFruitProduction = metricTonsToImperialTons * np.array([4.90117687168451, 4.91031646930524, 4.92437011183630, 4.93649279501228, 4.95014157960967, 4.96548161903437, 4.98887208640314, 5.00886212676615, 5.03117066199798, 5.05600535878424, 5.09341863947534, 5.12498775571930, 5.15980990055501, 5.19810410208063, 5.25493282298304, 5.30214551151104, 5.35350350085848, 5.40917640799240, 5.49036914967390, 5.55663374228312, 5.62758889511747, 5.70327273359316, 5.81152660834755, 5.89814788676384, 5.98929888492371, 6.11757749333149, 6.21853999173363, 6.32324829337238, 6.43134580653531, 6.58002929731689, 6.69434512056264, 6.81468431373320, 6.93240654668110, 7.09029876996453, 7.20858786635470, 7.32603341952800, 7.44212189854525, 7.59303472294466, 7.70285556018058, 7.80899200936550, 7.91105389761043, 8.03905686559711, 8.12887744152224, 8.21304978253074, 8.29074320341420, 8.38388155379347, 8.44638287240029, 8.50177121098050, 8.56467914067670, 8.60428251211838, 8.63777808576929, 8.66468944135223, 8.69105757182629, 8.70531406007943, 8.71427607126381, 8.71889054793876, 8.71922739723006, 8.71585762074335, 8.71002859601729, 8.70232053173004, 8.69010104640178, 8.68018568286068, 8.79641764525067, 8.80188475451504, 8.81098514890519, 8.82168927618986, 8.83658100766846, 8.85434771104593, 8.88342447166076, 8.91100951241923, 8.94422956914249, 8.98273954280306, 9.03719551301618, 9.08692107475378, 9.14060417879011, 9.20353773040584, 9.28551469637137, 9.35595429405062, 9.43130669372908, 9.53789658547303, 9.62577339205677, 9.71688729730981, 9.81252687275417, 9.94692434840426, 10.0527645841621, 10.1628330396960, 10.2787026015753, 10.4356790611307, 10.5593183576528, 10.6886474066959, 10.8626323835578, 10.9996179392250, 11.1399759909746, 11.2644899869009, 11.4651976631350, 11.6207195769662, 11.7812606691477, 11.9429936355499, 12.1614611853255, 12.3322360243090, 12.5039971615745, 12.6785934176291, 12.9136137039360, 13.0962631390646, 13.2792620727526, 13.5399233692091, 13.7139958648582, 13.9029867768846, 14.0931429338479, 14.3667504984261, 14.5393828129662, 14.7307732365473, 14.9216304437154, 15.1959386167682, 15.3622377486374, 15.5478323030820, 15.7323351470418, 15.9693882178411, 16.1437678314555, 16.3149874576192, 16.5555475843450, 16.6883834085801, 16.8384732954013, 16.9825594449637, 17.1836624071526, 17.2835026618100, 17.3991814945023, 17.5041681055582, 17.6507922614321, 17.7087314398468, 17.7779501116961, 17.8354788798306, 17.9149621724938, 17.9221882831579, 17.9382289689717, 17.9598674747818, 17.9449329352021, 17.8965398768752, 17.8549686859129, 17.7972524176287, 17.7054818210361, 17.6190712118903, 17.5189896047721, 17.3828973571260, 17.2367972294205, 17.0948368445982, 16.9016969832747, 16.7318566931879, 16.5373588425709, 16.3455452856680, 16.0893074406968, 15.8757061303309, 15.6408220949549, 15.4111538995484, 15.1054365982389, 14.8594027236372, 14.5967737940760, 14.3404527009703, 14.0021165551219, 13.7348189663589, 13.4589372584850, 13.1075361192536, 12.8339409867402, 12.5554162231432, 12.2837883277497, 11.9304493362788, 11.6595840035298, 11.3879666237278, 11.1243055384152, 10.7821702621831, 10.5266568481150, 10.2718061563049, 10.0237047776344, 9.70870232615360, 9.47484353422856, 9.24409215375906, 8.95243468645942, 8.73907217127155, 8.53229564651996, 8.32832575097253, 8.07617411289909, 7.89220903882371, 7.71339230530407, 7.54198585251137, 7.32947009180552, 7.13552181575183, 6.99044600989788, 6.85363001386365, 6.68283280120711, 6.55918784160174, 6.44334744706939, 6.29976188267278, 6.19617583878672, 6.09977051551468, 6.00883137899447, 5.89576573852370, 5.81686124707095, 5.74279425367783, 5.67336811560199, 5.58767645129208, 5.52830774799423, 5.47291943701574, 5.40492203256548, 5.35806451291012, 5.31454615287620, 5.27320279242196, 5.22496200837776, 5.19126976498829, 5.16015413635332, 5.13062279600295, 5.09667820285009, 5.07302338712695, 5.05056809746531, 5.03065934040337, 5.00733671860512, 4.99046935435742, 4.86242386343084, 4.86068229749055, 4.85902039357234, 4.85692430194841, 4.85543894899568, 4.85402524539498, 4.85224760213348, 4.85099173529582, 4.84979953921729, 4.84830492106332, 4.84725217788743, 4.84625536574897, 4.84531223417146, 4.84413441322140, 4.84330801239217, 4.84252809312706, 4.84155695510773, 4.84087757624426, 4.84023801831665, 4.83944397198689, 4.83889010403169, 4.83836999878516, 4.83788196166270, 4.83727830807370, 4.83685882988355, 4.83646618701218, 4.83598191684974, 4.83564636642917, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461, 4.83144354438461])
#         self.TotalFruitProduction = np.sum(self.DailyFruitProduction)
#         # self.TotalProductionValue = 4205000.0 # in brazilian reals

#         # fraction of daily production from each city, fractions from FarmerDataAdjusted.xls, fraction = fraction of production from that city
#         CareiroProduction = 0.33333333* self.DailyFruitProduction
#         IrandubaProduction = 0.33333333 * self.DailyFruitProduction
#         JutaiProduction = 0.33333333 * self.DailyFruitProduction
#         ManaquiriProduction = 0.25 * self.DailyFruitProduction
#         # fruit available at each city each day
#         self.DailyCityFruitProduction_TonsPerDay = np.round(np.array([CareiroProduction, IrandubaProduction, JutaiProduction, ManaquiriProduction]),decimals=3)
#         self.DailyCityFruitProduction_TonsPerDay[self.DailyCityFruitProduction_TonsPerDay < 0.0] = 0.0
#         # daily value of fruit produced in each city, fractions from FarmerDataAdjusted.xls, fraction = fraction of value from that city * value of all goods / all goods
#         # in brazilian reals
#         CareiroValue = 1000 * 1.873830294 #* self.DailyFruitProduction 
#         IrandubaValue = 1000 * 2.099050572 #* self.DailyFruitProduction
#         JutaiValue = 1000 * 2.034181964 #* self.DailyFruitProduction
#         ManaquiriValue = 1000 * 2.474721974 #* self.DailyFruitProduction
#         # average fruit value per ton for each city
#         self.AverageFruitValueCity_RealsPerTon = np.array([CareiroValue, IrandubaValue, JutaiValue, ManaquiriValue])

#         self.TotalGoodsSoldFraction = 1.0 - 0.205
#         self.TotalLossFraction = 0.205 
#         self.CitySoldFraction = np.array(  [0.795,
#                                             0.795,
#                                             0.795,
#                                             0.795])

# fruits = fruit()

