from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse 
from pycel import ExcelCompiler
import pickle
import json

# csrf exemption required for external requests since Django requires csrf tokens
@csrf_exempt 

# create views here
def myAPI(request):
    
    if request.method == 'POST':
        
        # load JSON POST request as a python dictionary (raw JSON)
        jsonRequest = json.loads(request.body.decode("utf-8"))
        
    if request.method == 'GET':
        
        # load JSON GET request as a python dictionary (URL encoded JSON)
        if 'jsonRequest' in request.GET:
            jsonRequest = json.loads(request.GET['jsonRequest'])
    
    
    
    # intialize variables
    jsonResponse = {}
    costs = {}
    menu = {}
    packages= []
    
    
    
    # load attributes portion of algorithm
    with open('static/pickledAlgorithmAttributes', 'rb') as f:
        excel = pickle.load(f)
        
    # calculate default price before making changes based off selections
    defaultPrice = excel.evaluate('Attributes Inputs and Outputs!C1')
    defaultPrice = str(int(defaultPrice))
    
        
    # check for/insert general attribute selections
    if 'BedroomCount' in jsonRequest:
        excel.set_value('Attributes Inputs and Outputs!B8', int(jsonRequest['BedroomCount']))
        
    if 'BathroomCount' in jsonRequest:
        excel.set_value('Attributes Inputs and Outputs!C8', int(jsonRequest['BathroomCount']))
        
    if 'Sqft' in jsonRequest:
        excel.set_value('Attributes Inputs and Outputs!D8', jsonRequest['Sqft'])
        
    if 'StoriesCount' in jsonRequest:
        excel.set_value('Attributes Inputs and Outputs!J8', int(jsonRequest['StoriesCount']))
        
    if 'GaragePortCount' in jsonRequest:
        excel.set_value('Attributes Inputs and Outputs!I8', int(jsonRequest['GaragePortCount']))
        
    if 'FramingType' in jsonRequest:
        excel.set_value('Attributes Inputs and Outputs!F8', jsonRequest['FramingType'])
        
    if 'BasementType' in jsonRequest:
        excel.set_value('Attributes Inputs and Outputs!E8', jsonRequest['BasementType'])
        
        
        
    # check for/insert other rooms and attributes selections
    if 'HasDiningRoom' in jsonRequest:
        excel.set_value('Attributes Inputs and Outputs!H8', jsonRequest['HasDiningRoom'])
       
    if 'HasExtraFamilyRoom' in jsonRequest:
        excel.set_value('Attributes Inputs and Outputs!H9', jsonRequest['HasExtraFamilyRoom'])
            
    if 'HasOffice' in jsonRequest:
        excel.set_value('Attributes Inputs and Outputs!H10', jsonRequest['HasExtraFamilyRoom'])
          
    if 'HasMudRoom' in jsonRequest:
        excel.set_value('Attributes Inputs and Outputs!H11', jsonRequest['HasMudRoom'])
        
    if 'HasSunRoom' in jsonRequest:
        excel.set_value('Attributes Inputs and Outputs!H12', jsonRequest['HasSunRoom'])
        
    if 'HasBreakfastRoom' in jsonRequest:
        excel.set_value('Attributes Inputs and Outputs!H13', jsonRequest['HasBreakfastRoom'])
        
    if 'HasTheaterRoom' in jsonRequest:
        excel.set_value('Attributes Inputs and Outputs!H14', jsonRequest['HasTheaterRoom'])
        
    if 'HasWineCellar' in jsonRequest:
        excel.set_value('Attributes Inputs and Outputs!H15', jsonRequest['HasWineCellar'])
            
    if 'HasExtraLaundryRoom' in jsonRequest:
        excel.set_value('Attributes Inputs and Outputs!H16', jsonRequest['HasExtraLaundryRoom'])
            
    if 'HasLoft' in jsonRequest:
        excel.set_value('Attributes Inputs and Outputs!H17', jsonRequest['HasLoft'])
            
    if 'HasElevatorShaft' in jsonRequest:
        excel.set_value('Attributes Inputs and Outputs!H18', jsonRequest['HasElevatorShaft'])
         
    if 'HasDeckOrPatio' in jsonRequest:
        excel.set_value('Attributes Inputs and Outputs!H19', jsonRequest['HasDeckOrPatio'])
           
    if 'HasSolarPanels' in jsonRequest:
        excel.set_value('Attributes Inputs and Outputs!H20', jsonRequest['HasSolarPanels'])
            
    if 'HasPluginVehicle' in jsonRequest:
        excel.set_value('Attributes Inputs and Outputs!H21', jsonRequest['HasPluginVehicle'])
            
    if 'HasGenerator' in jsonRequest:
        excel.set_value('Attributes Inputs and Outputs!H22', jsonRequest['HasGenerator'])
    
    # check for/insert floor height attribute selections
    if 'BasementFloorHeight' in jsonRequest:
        excel.set_value('Attributes Inputs and Outputs!K10', int(jsonRequest['BasementFloorHeight']))
        
    if 'FirstFloorHeight' in jsonRequest:
        excel.set_value('Attributes Inputs and Outputs!L8', int(jsonRequest['FirstFloorHeight']))
        
    if 'SecondFloorHeight' in jsonRequest:
        excel.set_value('Attributes Inputs and Outputs!M10', int(jsonRequest['SecondFloorHeight']))
    
    # check for/insert other attribute selections
    if 'SqftEfficiency' in jsonRequest:
        excel.set_value('Attributes Inputs and Outputs!U8', jsonRequest['SqftEfficiency'])
        
    if 'LargeRoomsCount' in jsonRequest:
        excel.set_value('Attributes Inputs and Outputs!N8', int(jsonRequest['LargeRoomsCount']))
        
    if 'AnglesCurvesType' in jsonRequest:
        excel.set_value('Attributes Inputs and Outputs!O8', jsonRequest['AnglesCurvesType'])
        
    if 'RoofStyle' in jsonRequest:
        excel.set_value('Attributes Inputs and Outputs!P8', jsonRequest['RoofStyle'])
        
    if 'GarageEntry' in jsonRequest:
        excel.set_value('Attributes Inputs and Outputs!S8', jsonRequest['GarageEntry'])
        
    if 'VaultedCeiling' in jsonRequest:
        excel.set_value('Attributes Inputs and Outputs!T8', jsonRequest['VaultedCeiling'])
    
    # check for/insert plans and engineering selections
    if ('Engineering' in jsonRequest) and ('HousePlans' in jsonRequest):
        if (jsonRequest['Engineering'] == 'No'):
            excel.set_value('Attributes Inputs and Outputs!Q8', 'Neither')
        elif (jsonRequest['HousePlans'] == 'No'):
            excel.set_value('Attributes Inputs and Outputs!Q8', 'Engineering Only')
        else:
            excel.set_value('Attributes Inputs and Outputs!Q8', 'Both')
        
    if 'InteriorDesigner' in jsonRequest:
        excel.set_value('Attributes Inputs and Outputs!R8', jsonRequest['InteriorDesigner'])
    
    
    
    # calculate home/default (above) total price
    homePrice = excel.evaluate('Attributes Inputs and Outputs!C1')
    homePrice = str(int(homePrice))
    costs['YourPrice'] = homePrice
    costs['DefaultPrice'] = defaultPrice
    
    
    
    # calculate attribute granular costs
    bedroomPrice = excel.evaluate('Attributes Inputs and Outputs!B30')
    bedroomPrice = str(int(bedroomPrice))
    costs['BedroomCost'] = bedroomPrice
    
    bathroomPrice = excel.evaluate('Attributes Inputs and Outputs!C30')
    bathroomPrice = str(int(bathroomPrice))
    costs['BathCost'] = bathroomPrice
    
    sqftPrice = excel.evaluate('Attributes Inputs and Outputs!D30')
    sqftPrice = str(int(sqftPrice))
    costs['SqftCost'] = sqftPrice
    
    basementPrice = excel.evaluate('Attributes Inputs and Outputs!E30')
    basementPrice = str(int(basementPrice))
    costs['BasementCost'] = basementPrice
    
    framingPrice = excel.evaluate('Attributes Inputs and Outputs!F30')
    framingPrice = str(int(framingPrice))
    costs['FramingCost'] = framingPrice
    
    diningRoomPrice = excel.evaluate('Attributes Inputs and Outputs!H30')
    diningRoomPrice = str(int(diningRoomPrice))
    costs['DiningRoomCost'] = diningRoomPrice
    
    extraFamilyRoomPrice = excel.evaluate('Attributes Inputs and Outputs!H31')
    extraFamilyRoomPrice = str(int(extraFamilyRoomPrice))
    costs['ExtraFamilyRoomCost'] = extraFamilyRoomPrice
    
    officePrice = excel.evaluate('Attributes Inputs and Outputs!H32')
    officePrice = str(int(officePrice))
    costs['OfficeCost'] = officePrice
    
    mudRoomPrice = excel.evaluate('Attributes Inputs and Outputs!H33')
    mudRoomPrice = str(int(mudRoomPrice))
    costs['MudRoomCost'] = mudRoomPrice
    
    sunRoomPrice = excel.evaluate('Attributes Inputs and Outputs!H34')
    sunRoomPrice = str(int(sunRoomPrice))
    costs['SunRoomCost'] = sunRoomPrice
    
    breakfastRoomPrice = excel.evaluate('Attributes Inputs and Outputs!H35')
    breakfastRoomPrice = str(int(breakfastRoomPrice))
    costs['BreakfastRoomCost'] = breakfastRoomPrice
    
    theaterRoomPrice = excel.evaluate('Attributes Inputs and Outputs!H36')
    theaterRoomPrice = str(int(theaterRoomPrice))
    costs['TheaterRoomCost'] = theaterRoomPrice
    
    wineCellarPrice = excel.evaluate('Attributes Inputs and Outputs!H37')
    wineCellarPrice = str(int(wineCellarPrice))
    costs['WineCellarCost'] = wineCellarPrice
    
    extraLaundryRoomPrice = excel.evaluate('Attributes Inputs and Outputs!H38')
    extraLaundryRoomPrice = str(int(extraLaundryRoomPrice))
    costs['ExtraLaundryRoomCost'] = extraLaundryRoomPrice
    
    loftPrice = excel.evaluate('Attributes Inputs and Outputs!H39')
    loftPrice = str(int(loftPrice))
    costs['LoftCost'] = loftPrice
    
    elevatorShaftPrice = excel.evaluate('Attributes Inputs and Outputs!H40')
    elevatorShaftPrice = str(int(elevatorShaftPrice))
    costs['ElevatorShaftCost'] = elevatorShaftPrice
    
    deckPatioPrice = excel.evaluate('Attributes Inputs and Outputs!H41')
    deckPatioPrice = str(int(deckPatioPrice))
    costs['DeckOrPatioCost'] = deckPatioPrice
    
    solarPanelsPrice = excel.evaluate('Attributes Inputs and Outputs!H42')
    solarPanelsPrice = str(int(solarPanelsPrice))
    costs['SolarPanelsCost'] = solarPanelsPrice
    
    pluginVehiclePrice = excel.evaluate('Attributes Inputs and Outputs!H43')
    pluginVehiclePrice = str(int(pluginVehiclePrice))
    costs['PluginVehicleCost'] = pluginVehiclePrice
    
    generatorPrice = excel.evaluate('Attributes Inputs and Outputs!H44')
    generatorPrice = str(int(generatorPrice))
    costs['GeneratorCost'] = generatorPrice
    
    garagePrice = excel.evaluate('Attributes Inputs and Outputs!I30')
    garagePrice = str(int(garagePrice))
    costs['GaragePortCost'] = garagePrice
    
    storiesPrice = excel.evaluate('Attributes Inputs and Outputs!J30')
    storiesPrice = str(int(storiesPrice))
    costs['StoriesCost'] = storiesPrice
    
    basementHeightPrice = excel.evaluate('Attributes Inputs and Outputs!K30')
    basementHeightPrice = str(int(basementHeightPrice))
    costs['BasementHeightCost'] = basementHeightPrice
    
    firstFloorHeightPrice = excel.evaluate('Attributes Inputs and Outputs!L30')
    firstFloorHeightPrice = str(int(firstFloorHeightPrice))
    costs['FirstFloorHeightCost'] = firstFloorHeightPrice
    
    secondFloorHeightPrice = excel.evaluate('Attributes Inputs and Outputs!M30')
    secondFloorHeightPrice = str(int(secondFloorHeightPrice))
    costs['SecondFloorHeightCost'] = secondFloorHeightPrice
    
    sqftEfficiencyPrice = excel.evaluate('Attributes Inputs and Outputs!U30')
    sqftEfficiencyPrice = str(int(sqftEfficiencyPrice))
    costs['SqftEfficiencyCost'] = sqftEfficiencyPrice
    
    largeRoomsPrice = excel.evaluate('Attributes Inputs and Outputs!N30')
    largeRoomsPrice = str(int(largeRoomsPrice))
    costs['LargeRoomsCost'] = largeRoomsPrice
    
    anglesCurvesPrice = excel.evaluate('Attributes Inputs and Outputs!O30')
    anglesCurvesPrice = str(int(anglesCurvesPrice))
    costs['AnglesCurvesCost'] = anglesCurvesPrice
    
    roofStylePrice = excel.evaluate('Attributes Inputs and Outputs!P30')
    roofStylePrice = str(int(roofStylePrice))
    costs['RoofStyleCost'] = roofStylePrice
    
    housePlansEngineeringPrice = excel.evaluate('Attributes Inputs and Outputs!Q30')
    housePlansEngineeringPrice = str(int(housePlansEngineeringPrice))
    costs['HousePlansEngineeringCost'] = housePlansEngineeringPrice
    
    interiorDesignerPrice = excel.evaluate('Attributes Inputs and Outputs!R30')
    interiorDesignerPrice = str(int(interiorDesignerPrice))
    costs['InteriorDesignerCost'] = interiorDesignerPrice
    
    garageEntryPrice = excel.evaluate('Attributes Inputs and Outputs!S30')
    garageEntryPrice = str(int(garageEntryPrice))
    costs['GarageEntryCost'] = garageEntryPrice
    
    vaultedCeilingPrice = excel.evaluate('Attributes Inputs and Outputs!T30')
    vaultedCeilingPrice = str(int(vaultedCeilingPrice))
    costs['VaultedCeilingCost'] = vaultedCeilingPrice
    
    
    
    sqftAboveGrade = excel.evaluate('Attributes Inputs and Outputs!D19')
    sqftAboveGrade = str(int(sqftAboveGrade))
    menu['SqftAboveGrade'] = sqftAboveGrade
    
    sqftBasemenet = excel.evaluate('Attributes Inputs and Outputs!D21')
    sqftBasemenet = str(int(sqftBasemenet))
    menu['SqftBasement'] = sqftBasemenet
    
    sqftLoft = excel.evaluate('Attributes Inputs and Outputs!D23')
    sqftLoft = str(int(sqftLoft))
    menu['SqftLoft'] = sqftLoft
    
    sqftTotal = excel.evaluate('Attributes Inputs and Outputs!D25')
    sqftTotal = str(int(sqftTotal))
    menu['SqftTotal'] = sqftTotal
    
    
    
    # load packages portion of algorithm
    with open('static/pickledAlgorithmPackages', 'rb') as f:
        excel = pickle.load(f)
    
    
    
    packageOptions = ['Kitchen', 'Master Bedroom', 'Bedroom 2', 'Bedroom 3', 'Bedroom 4', 'Bedroom 5', 
                      'Bedroom 6', 'Bedroom 7', 'Bedroom 8', 'Master Bath', 'Powder Room', 'Bath 2', 
                      'Bath 3', 'Bath 4', 'Bath 5', 'Bath 6', 'Bath 7', 'Bath 8', 'Main Living Area', 
                      'Laundry Room', 'Garage', 'Finished Basement', 'Unfinished Basement', 'Dining Room', 
                      'Additional Family/Living', 'Office', 'Mud Room', 'Sun Room', 'Breakfast Room', 
                      'Theater Room', 'Wine Cellar', 'Additional Laundry Room', 'Loft', 
                      'Flooring - Main Living Areas', 'Stairs', 'Windows', 'Interior Doors',
                      'Timber Frame Wood and Joint Type', 'Deck/Patio, Porch', 'Exterior Doors', 
                      'Exterior Walls and Trim', 'Exterior Trim', 'Exterior Lighting', 'Landscaping', 
                      'Driveway', 'Front Path', 'Roof', 'Heat & Cooling', 'Energy Efficiency', 
                      'Home Technology', 'Warranty', 'Generator', 'Elevator Shaft', 
                      'Baseboards & Window & Door Trim', 'Plug-in Vehicle Ready', 'Solar Panels', 
                      'Interior Designer', 'Paint Level']
    
    # calculate package granular costs following packageOptions (above) - must be in order of xlsx/xlsm
    for i in range(len(packageOptions)):
        info = {}
        info['Name'] = packageOptions[i]
        i = str(i + 8)
        info['Type'] = ''
        info['BronzePrice'] = str(int(excel.evaluate('Packages Inputs and Outputs!G' + i)))
        info['SilverPrice'] = str(int(excel.evaluate('Packages Inputs and Outputs!H' + i)))
        info['GoldPrice'] = str(int(excel.evaluate('Packages Inputs and Outputs!I' + i)))
        info['PlatinumPrice'] = str(int(excel.evaluate('Packages Inputs and Outputs!J' + i)))
        packages.append(info)


    
    # assemble/format json response
    jsonResponse['costs'] = costs
    jsonResponse['menu'] = menu
    jsonResponse['packages'] = packages
    response = json.dumps(jsonResponse, indent = 4, separators=(',', ':'))
    
    return HttpResponse(response, content_type = 'text/json')