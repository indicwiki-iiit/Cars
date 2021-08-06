import pickle
from jinja2 import Environment, FileSystemLoader
import pandas as pd
from genXML_30k import tewiki, writePage

def getData(row):

	# reading and cleaning front & rear brake diameter and thickness
	if(str(row.Front_Brake_Rotor_Diam_x_Thickness_in.values[0]) not  in [""," "]):
		fbrake=str(row.Front_Brake_Rotor_Diam_x_Thickness_in.values[0]).split("x")
		if(len(fbrake)==1):
			if(fbrake[0]!=" - TBD -"):
				fdiam=fbrake[0]
				fthick=""
			else:
				fdiam=""
				fthick=""
		elif(len(fbrake)==2):
			if(fbrake[0]!=" - TBD -"):
				fdiam=fbrake[0]
			else:
				fdiam=""
			if(fbrake[1]!=" - TBD -"):
				fthick=fbrake[1]
			else:
				fthick=""
	else:
		fdiam=""
		fthick=""
	if(str(row.Rear_Brake_Rotor_Diam_x_Thickness_in.values[0]) not  in [""," "]):
		rbrake=str(row.Rear_Brake_Rotor_Diam_x_Thickness_in.values[0]).split("x")
		if(len(rbrake)==1):
			if(rbrake[0]!=" - TBD -"):
				rthick=""
				rdiam=rbrake[0]
			else:
				rthick=""
				rdiam=""
		elif(len(rbrake)==2):
			if(rbrake[0]!=" - TBD -"):
				rdiam=fbrake[0]
			else:
				rdiam=""
			if(rbrake[1]!=" - TBD -"):
				rthick=fbrake[1]
			else:
				rthick=""
		else:
			rdiam=""
			rthick=""
	name=str(row.Name_eng.values[0]).split("Specs:")#reading name in english and split it based on Specs:
	namet=str(row.Name.values[0]).split("స్పెక్స్:")#reading name in telugu and split it based on స్పెక్స్:
	#cleaning telugu and english name and transform into desired format and also obtaining brand and manufacturer data from name
	name_edit=name[0].split(" ")
	namet_edit=namet[0].split(" ")
	name_str=""
	for i in range(len(name_edit)):
		if i==0:
			year=name_edit[i]
		else:
			name_str+=name_edit[i]+ " "
	namet_str=""
	for i in range(len(namet_edit)):
		if i==0:
			yeart=namet_edit[i]
		else:
			namet_str+=namet_edit[i]+ " "
	Name=namet_str[:-1]+year+"("+namet[1][1:]+")" + "(<i>"+name_str[:-1]+yeart+"("+name[1][1:]+"</i>))"
	info_name=namet_str[:-1]+year+"("+namet[1][1:]+")"
	manufacturer=namet_str.split(" ")[0]
	brand=name_str.split(" ")[0]

	logos=pickle.load(open("./images/logos.pkl","rb"))#reading a dictionary with brand logos
	#edge case
	if (brand.upper()=="LAND"):
		brand="LAND ROVER"
	brand_logo=logos[brand.upper()]#loading brand image of this car
	intro=pickle.load(open("./data/brand_data.pkl","rb"))#reading a dictionary with brand introduction
	intro_data=intro[brand.upper()]#loading brand introduction of this car

	# converting weight, city mileage, highway mileage into indian units
	if(row.Base_Curb_Weight_lbs.values[0] != "#"):
		weight=round(float(row.Base_Curb_Weight_lbs.values[0])*0.454,2)
	else:
		weight="#"
	if(row.EPA_Fuel_Economy_Est__City_MPG.values[0] != "#"):
		citymil=round(float(row.EPA_Fuel_Economy_Est__City_MPG.values[0])*0.425143707,2)
	else:
		citymil="#"
	if(row.EPA_Fuel_Economy_Est__Hwy_MPG.values[0] != "#"):
		highmil=round(float(row.EPA_Fuel_Economy_Est__Hwy_MPG.values[0])*0.425143707,2)
	else:
		highmil="#"
	vers=pickle.load(open('./data/versions_30k.pkl', 'rb'))#versions dictionary used to render related models section in article

	# dictionary with external dimensions of car
	ext={
		'Wheelbase_in':str(row.Wheelbase_in.values[0]),
		'Length_Overall_in':str(row.Length_Overall_in.values[0]),
		'Height_Overall_in':str(row.Height_Overall_in.values[0]),
		'Width_Max_wo_mirrors_in':str(row.Width_Max_wo_mirrors_in.values[0]),
		'Track_Width_Front_in':str(row.Track_Width_Front_in.values[0]),
		'Track_Width_Rear_in':str(row.Track_Width_Rear_in.values[0])
	}
	# dictionary with internal dimensions of car
	int={
		'Passenger_Capacity':str(row.Passenger_Capacity.values[0]),
		'Passenger_Volume':str(row.Passenger_Volume.values[0]),
		'Front_Hip_Room_in':str(row.Front_Hip_Room_in.values[0]),
		'Front_Leg_Room_in':str(row.Front_Leg_Room_in.values[0]),
		'Second_Leg_Room_in':str(row.Second_Leg_Room_in.values[0]),
		'Second_Shoulder_Room_in':str(row.Second_Shoulder_Room_in.values[0]),
		'Front_Shoulder_Room_in':str(row.Front_Shoulder_Room_in.values[0]),
		'Second_Hip_Room_in':str(row.Second_Hip_Room_in.values[0]),
		'Front_Head_Room_in':str(row.Front_Head_Room_in.values[0]),
		'Second_Head_Room_in':str(row.Second_Head_Room_in.values[0])
	}
	# dictionary with tires data of car
	tires={
		'Front_Tire_Size':str(row.Front_Tire_Size.values[0]),
		'Rear_Tire_Size':str(row.Rear_Tire_Size.values[0]),
		'Spare_Tire_Size':str(row.Spare_Tire_Size.values[0]),
		'Front_Wheel_Size_in':str(row.Front_Wheel_Size_in.values[0]),
		'Rear_Wheel_Size_in':str(row.Rear_Wheel_Size_in.values[0]),
		'Spare_Wheel_Size_in':str(row.Spare_Wheel_Size_in.values[0]),
		'Front_Wheel_Material':(str(row.Front_Wheel_Material.values[0])),
		'Rear_Wheel_Material':(str(row.Rear_Wheel_Material.values[0])),
		'Spare_Wheel_Material':(str(row.Spare_Wheel_Material.values[0]))
	}
	# dictionary with gear ratios of car
	gear_ratios={
		'first_gear_ratio':row.First_Gear_Ratio_1.values[0],
        'second_gear_ratio':row.Second_Gear_Ratio_1.values[0],
        'third_gear_ratio':row.Third_Gear_Ratio_1.values[0],
        'fourth_gear_ratio':row.Fourth_Gear_Ratio_1.values[0],
        'fifth_gear_ratio':row.Fifth_Gear_Ratio_1.values[0],
        'reverse_ratio':row.Reverse_Ratio_1.values[0]
	}
	# list of airbags
	airbags=[row.Air_BagFrontalDriver.values[0],
		row.Air_BagFrontalPassenger.values[0],
		row.Air_BagSide_BodyFront.values[0],
		row.Air_BagSide_BodyRear.values[0],
		row.Air_BagSide_HeadFront.values[0],
		row.Air_BagSide_HeadRear.values[0],
		row.Air_BagPassenger_Switch_OnOff.values[0]
	]
	model=namet_str[:-1]+year#model vraiable used as key for versions dictionary
	airbags_len=len(airbags)#used in rendering airbags list
	#data dictionary
	data = {
		'introduction':intro_data,
		'img':brand_logo,
		'info_name':info_name,
		'airbags_len':airbags_len,
		'airbags':airbags,
		'year':year,
		'manufacturer':manufacturer,
		'len':len(model),
		'gear_ratios':gear_ratios,
		'ext':ext,
		'int':int,
		'tires':tires,
		'vers': vers,
		'name1': model,
		'Name':Name,
		'Fuel_System':(str(row.Fuel_System.values[0])),
		'Gas_Mileage':(str(row.Gas_Mileage.values[0])),
		'Engine_Type':(str(row.Engine_Type.values[0])),
		'Passenger_Capacity':str(row.Passenger_Capacity.values[0]),
		'EPA_Class':(str(row.EPA_Class.values[0])),
		'Body_Style':(str(row.Body_Style.values[0])),
		'Displacement':str(row.Displacement.values[0]),
		'Wheelbase_in':str(row.Wheelbase_in.values[0]),
		'Length_Overall_in':str(row.Length_Overall_in.values[0]),
		'Height_Overall_in':str(row.Height_Overall_in.values[0]),
		'Fuel_Tank_Capacity_Approx_gal':str(row.Fuel_Tank_Capacity_Approx_gal.values[0]),
		'Steering_Type':(row.Steering_Type.values[0]),
		'Basic_Mileskm':str(row.Basic_Mileskm.values[0]),
		'Passenger_Doors':str(row.Passenger_Doors.values[0]),
		'Passenger_Volume':str(row.Passenger_Volume.values[0]),
		'Front_Hip_Room_in':str(row.Front_Hip_Room_in.values[0]),
		'Front_Leg_Room_in':str(row.Front_Leg_Room_in.values[0]),
		'Second_Leg_Room_in':str(row.Second_Leg_Room_in.values[0]),
		'Second_Shoulder_Room_in':str(row.Second_Shoulder_Room_in.values[0]),
		'Front_Shoulder_Room_in':str(row.Front_Shoulder_Room_in.values[0]),
		'Second_Hip_Room_in':str(row.Second_Hip_Room_in.values[0]),
		'Front_Head_Room_in':str(row.Front_Head_Room_in.values[0]),
		'Second_Head_Room_in':str(row.Second_Head_Room_in.values[0]),
		'Width_Max_wo_mirrors_in':str(row.Width_Max_wo_mirrors_in.values[0]),
		'Track_Width_Front_in':str(row.Track_Width_Front_in.values[0]),
		'Track_Width_Rear_in':str(row.Track_Width_Rear_in.values[0]),
		'Front_Tire_Size':str(row.Front_Tire_Size.values[0]),
		'Rear_Tire_Size':str(row.Rear_Tire_Size.values[0]),
		'Spare_Tire_Size':str(row.Spare_Tire_Size.values[0]),
		'Front_Wheel_Size_in':str(row.Front_Wheel_Size_in.values[0]),
		'Rear_Wheel_Size_in':str(row.Rear_Wheel_Size_in.values[0]),
		'Spare_Wheel_Size_in':str(row.Spare_Wheel_Size_in.values[0]),
		'Front_Wheel_Material':(str(row.Front_Wheel_Material.values[0])),
		'Rear_Wheel_Material':(str(row.Rear_Wheel_Material.values[0])),
		'Spare_Wheel_Material':(str(row.Spare_Wheel_Material.values[0])),
		'rdiam':rdiam,
		'rthick':rthick,
		'fdiam':fdiam,
		'fthick':fthick,
		'Drivetrain':(str(row.Drivetrain.values[0])),
		'Drivetrain_Mileskm':str(row.Drivetrain_Mileskm.values[0]),
		'Drivetrain_Years':str(row.Drivetrain_Years.values[0]),
		'Trans_Description_Cont':(str(row.Trans_Description_Cont.values[0])),
		'Gears':str(row.Gears.values[0]),
		'Brake_Type':(str(row.Brake_Type.values[0])),
		'Brake_ABS_System':(str(row.Brake_ABS_System.values[0])),
		'Disc__Front_Yes_or___':row.Disc__Front_Yes_or___.values[0],
		'Disc__Rear_Yes_or___':row.Disc__Rear_Yes_or___.values[0],
		'Air_BagFrontalDriver':row.Air_BagFrontalDriver.values[0],
		'Air_BagFrontalPassenger':row.Air_BagFrontalPassenger.values[0],
		'Air_BagSide_BodyFront':row.Air_BagSide_BodyFront.values[0],
		'Air_BagSide_BodyRear':row.Air_BagSide_BodyRear.values[0],
		'Air_BagSide_HeadFront':row.Air_BagSide_HeadFront.values[0],
		'Air_BagSide_HeadRear':row.Air_BagSide_HeadRear.values[0],
		'Air_BagPassenger_Switch_OnOff':row.Air_BagPassenger_Switch_OnOff.values[0],
		'BackUp_Camera':str(row.BackUp_Camera.values[0]),
		'Base_Curb_Weight_lbs':str(weight),
		'SAE_Net_Torque_RPM':row.SAE_Net_Torque_RPM.values[0],
		'Suspension_Type__Front':(str(row.Suspension_Type__Front.values[0])),
		'Suspension_Type__Rear':(str(row.Suspension_Type__Rear.values[0])),
		'Trans_Type':str(row.Trans_Type.values[0]),
		'citymil':str(citymil),
        'highmil':str(highmil),
        'nethorsepower': str(row.Net_Horsepower_RPM.values[0]),
        'Transmission':(str(row.Trans_Description_Cont.values[0])),
        'displacement':str(row.Displacement_cc.values[0]),
        'gears':str(row.Gears.values[0]),
        'first_gear_ratio':str(row.First_Gear_Ratio_1.values[0]),
        'second_gear_ratio':str(row.Second_Gear_Ratio_1.values[0]),
        'third_gear_ratio':str(row.Third_Gear_Ratio_1.values[0]),
        'fourth_gear_ratio':str(row.Fourth_Gear_Ratio_1.values[0]),
        'fifth_gear_ratio':str(row.Fifth_Gear_Ratio_1.values[0]),
        'reverse_ratio':str(row.Reverse_Ratio_1.values[0]),
        'Traction_Control':row.Traction_Control.values[0],
        'fog_lamp':row.Fog_Lamps.values[0],
        'stability_control':row.Stability_Control.values[0],
        'curb_diam':str(row.Turning_Diameter__Curb_to_Curb.values[0]),
        'Tire_Pressure_Monitor':row.Tire_Pressure_Monitor.values[0],
        'Night_Vision':row.Night_Vision.values[0],
        'backup_cam':row.BackUp_Camera.values[0],
        'corrosion_years':row.Corrosion_Years.values[0],
        'Maximum_Alternator_Capacity_amps':str(row.Maximum_Alternator_Capacity_amps.values[0]),
	}
	return data

def main():
	file_loader = FileSystemLoader('./Templates')#loading folder with templates
	env = Environment(loader=file_loader)
	template = env.get_template('cars_30k.j2')#selecting template

	DF =pickle.load(open('./data/cars_30k.pkl', 'rb'))#reading pickle of final dataset
	ids = DF.Name_eng.tolist()#generating a list for an attribute which have all unique values
	#ids =ids[0:1]+ids[655:656]+ids[1649:1650]+ids[1668:1669]+ids[2953:2954]+ids[3307:3308]+ids[3735:3736]+ids[6661:6662]+ids[6811:6812]+ids[7248:7249]+ids[7313:7314]+ids[7531:7532]+ids[11254:11255]+ids[11300:11301]+ids[13469:13470]+ids[16036:16037]+ids[16459:16460]+ids[16482:16483]+ids[17249:17250]+ids[17973:17974]+ids[18603:18604]+ids[18749:18750]+ids[19398:19399]+ids[20337:20338]+ids[20499:20500]+ids[20600:20601]+ids[21269:21270]+ids[22899:22900]+ids[23199:23200]+ids[24470:24471]+ids[25335:25336]+ids[25767:25768]+ids[27348:27349]+ids[28779:28780]+ids[30269:30270]#remove this to generate articles for all movies281
	ids=ids[:20]#remove this to generate articles for all movies281
	# Initiate the file object
	fobj = open('cars_30k.xml', 'w', encoding="utf-8")
	fobj.write(tewiki+'\n')
	cur_page_id=950000#starting page id selected for rendering articles in tewiki
	for i, name in enumerate(ids):
		row = DF.loc[DF['Name_eng']==name]
		namet=str(row.Name.values[0]).split("స్పెక్స్:")
		namet_edit=namet[0].split(" ")
		namet_str=""
		for i in range(len(namet_edit)):
			if i==0:
				yeart=namet_edit[i]
			else:
				namet_str+=namet_edit[i]+ " "
		title=namet_str[:-1]+yeart+"("+namet[1][1:]+")"
		text = template.render(getData(row))
		writePage(title, text, fobj, cur_page_id)#adds current car data to .xml file
		cur_page_id+=1
		#print(text)

	fobj.write('</mediawiki>')
	fobj.close()#closing file

if __name__ == '__main__':
	main()