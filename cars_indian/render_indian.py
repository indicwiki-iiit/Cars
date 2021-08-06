import pickle
from jinja2 import Environment, FileSystemLoader
import pandas as pd
  
from genXML_indian import tewiki, writePage

def getData(row):
	#versions dictionary used to render related models section in article
	versions=pickle.load(open("./data/versions_india.pkl","rb"))

	#to create model of car which used as key in versions dictionary to map to all variants of model
	if(row.Make.values[0]!="#"):
		model=row.Make.values[0]+" "+row.Model.values[0]
	else:
		model=row.Model.values[0]

	#car name
	if(row.Make.values[0]!="#"):
		Name=row.Make.values[0]+" "+row.Model.values[0]+" "+row.Variant.values[0]
	else:
		Name=row.Model.values[0]+" "+row.Variant.values[0]

	#cleaning power and torque values
	pow=row.Power.values[0].split("@")
	Tor=row.Torque.values[0].split("@")
	if(row.Power.values[0] != "#" and len(pow)>1):
		power=pow[1][:-3]
	else:
		power = "#"
	if(row.Torque.values[0] != "#" and len(pow)>1):
		Torque=Tor[1][:-3]
	else:
		Torque = "#"

	#features dictionary used to render a table in other features section in article
	features={
		'Power_Windows':row.Power_Windows.values[0],
		'Power_Steering':row.Power_Steering.values[0],
		'Audiosystem':row.Audiosystem.values[0],
		'Bluetooth':row.Bluetooth.values[0],
		'Fuel_lid_Opener':row.Fuel_lid_Opener.values[0],
		'Seats_Material':row.Seats_Material.values[0],
		'Child_Safety_Locks':row.Child_Safety_Locks.values[0],
		'Door_Pockets':row.Door_Pockets.values[0],
		'Voice_Recognition':row.Voice_Recognition.values[0],
		'USB_Compatibility':row.USB_Compatibility.values[0],
		'Navigation_System':row.Navigation_System.values[0],
		'iPod_Compatibility':row.iPod_Compatibility.values[0],
		'Turbocharger':row.Turbocharger.values[0],
		'Cup_Holders':row.Cup_Holders.values[0]
	}
	
	#car tyres specifications
	tyres={
		'Front_Tyre_Rim':row.Front_Tyre_Rim.values[0],
		'Rear_Tyre_Rim':row.Rear_Tyre_Rim.values[0],
		'Wheels_Size':row.Wheels_Size.values[0]
	}

	#car external dimensions
	ext={
		'Wheelbase':str(row.Wheelbase.values[0]),
		'Length':str(row.Length.values[0]),
		'Height':str(row.Height.values[0]),
		'Width':str(row.Width.values[0]),
		'Ground_Clearance':str(row.Ground_Clearance.values[0]),
		'Front_Track':str(row.Front_Track.values[0]),
		'Rear_Track':str(row.Rear_Track.values[0])
	}
	#reading a pickle file which contain logos of all car brands
	logos=pickle.load(open("./images/logos.pkl","rb"))
	#reading a pickle file which contain images of some notable cars
	car_img=pickle.load(open("./images/cars_images.pkl","rb"))
	#defining variables
	img=""
	manufacturer=""
	brand=""
	#defining img with car image if it is available in car_img dictionary
	if(row.Make.values[0]!="#"):
		if((row.eMake.values[0]+" "+row.eModel.values[0]) in car_img.keys()):
			img=car_img[row.eMake.values[0]+" "+row.eModel.values[0]]
	else:
		if(row.eModel.values[0] in car_img.keys()):
			img=car_img[row.eModel.values[0]]
	#if car_img dictionary does not have any entry of this car then car brand logo is defined as img and also dealing some edge cases
	if(img==""):
		if(row.eMake.values[0]!="#"):
			if(row.eMake.values[0]=="Land Rover Rover"):
				img=logos["LAND ROVER"]
			elif(row.eMake.values[0]=="Bugatti"):
				img=logos["BUGGATI"]
			else:
				img=logos[(row.eMake.values[0]).upper()]
		elif(row.eModel.values[0]=="Go+"):
			img=logos["DATSUN"]
		elif(row.eModel.values[0].split(" ")[0]=="Mercedes-Benz"):
			img=logos["MERCEDES-BENZ"]
		elif(row.eModel.values[0].split(" ")[0]=="Rolls-Royce"):
			img=logos["ROLLS-ROYCE"]
	#if both car_img and logo dictionaries doesn't have entry for this car then it is defined as empty
	if(img=="#"):
		img=""
	#reading brand in telugu as manufacturer
	manufacturer=row.Make.values[0]
	#reading brand in english as brand
	brand=row.eMake.values[0]
	#dealing with edge cases
	if(manufacturer=="#"):
		if(row.eModel.values[0]=="Go+"):
			manufacturer="డాట్సన్"
			brand="DATSUN"
		elif(row.eModel.values[0].split(" ")[0]=="Mercedes-Benz"):
			manufacturer="మెర్సిడెస్ బెంజ్"
			brand="Mercedes-Benz"
		elif(row.eModel.values[0].split(" ")[0]=="Rolls-Royce"):
			manufacturer="రోల్స్ రాయిస్"
			brand="Rolls-Royce"
	#reading a pickle file with introduction data as intro dictionary
	intro=pickle.load(open("./data/brand_data.pkl","rb"))
	#edge cases
	if(brand=="Land Rover Rover"):
		brand="Land Rover"
	if(brand=="Bugatti"):
		brand="BUGGATI"
	#reading introdution data for this car
	intro_data=intro[brand.upper()]
	#data dictionary send as an argument to .j2 file
	data ={
		'introduction':intro_data,
		'manufacturer':manufacturer,
		'img':img,
		'feat_len':len(features.keys()),
		'features':features,
		'len':len(versions[model]),
		'Name':Name,
		'model':model,
		'vers':versions,
		'tyres':tyres,
		'ext':ext,
		'Tachometer':row.Tachometer.values[0],
		'Keyless_Entry':row.Keyless_Entry.values[0],
		'Engine_Malfunction_light':row.Engine_Malfunction_Light.values[0],
		'Fuel_lid_Opener':row.Fuel_lid_Opener.values[0],
		'Child_Safety_Locks':row.Child_Safety_Locks.values[0],
		'High_Speed_Alert_System':row.High_Speed_Alert_System.values[0],
		'Walk_Away_Auto_Car_Lock':row.Walk_Away_Auto_Car_Lock.values[0],
		'Headlight_Reminder':row.Headlight_Reminder.values[0],
		'Automatic_Headlamps':row.Automatic_Headlamps.values[0],
		'Front_Tyre_Rim':row.Front_Tyre_Rim.values[0],
		'Rear_Tyre_Rim':row.Rear_Tyre_Rim.values[0],
		'Wheels_Size':row.Wheels_Size.values[0],
		'Make':row.Make.values[0],
		'Type':row.Type.values[0],
		'Power':power,
		'Fuel_Type':row.Fuel_Type.values[0],
		'Body_Type':row.Body_Type.values[0],
		'Wheelbase':row.Wheelbase.values[0],
		'Length':str(row.Length.values[0]),
		'Height':str(row.Height.values[0]),
		'Kerb_Weight':str(row.Kerb_Weight.values[0]),
		'Width':str(row.Width.values[0]),
		'Ex_Showroom_Price':row.Ex_Showroom_Price.values[0],
		'Seating_Capacity':row.Seating_Capacity.values[0],
		'Engine_Type':row.Engine_Type.values[0],
		'Torque':Torque,
		'Fuel_Tank_Capacity':str(row.Fuel_Tank_Capacity.values[0]),
		'Fuel_Type':row.Fuel_Type.values[0],
		'Airbags':row.Airbags.values[0],
		'Gears':str(row.Gears.values[0]),
		'Gear_Indicator':row.Gear_Indicator.values[0],
		'Minimum_Turning_Radius':row.Minimum_Turning_Radius.values[0],
		'Low_Fuel_Warning':row.Low_Fuel_Warning.values[0],
		'Compression_Ratio':row.Compression_Ratio.values[0],
		'Tyre_Pressure_Monitoring_System':row.Tyre_Pressure_Monitoring_System.values[0],
		'ASR_Traction_Control':row.ASR_Traction_Control.values[0],
		'Electric_Range':row.Electric_Range.values[0],
		'Odometer':row.Odometer.values[0],
		'Speedometer':row.Speedometer.values[0],
		'Fuel_Gauge':row.Fuel_Gauge.values[0],
		'Displacement':str(row.Displacement.values[0]),
		'City_Mileage':str(row.City_Mileage.values[0]),
		'Highway_Mileage':str(row.Highway_Mileage.values[0]),
		'ARAI_Certified_Mileage':str(row.ARAI_Certified_Mileage.values[0]),
		'ARAI_Certified_Mileage_for_CNG':str(row.ARAI_Certified_Mileage_for_CNG.values[0]),
		'Emission_Norm':row.Emission_Norm.values[0],
		'Rain_Sensing_Wipers':row.Rain_Sensing_Wipers.values[0],
		'Doors':row.Doors.values[0],
		'Seating_Capacity':row.Seating_Capacity.values[0],
		'Cylinders':row.Cylinders.values[0],
		'Valves_Per_Cylinder':row.Valves_Per_Cylinder.values[0],
		'Cylinder_Configuration':row.Cylinder_Configuration.values[0],
		'Engine_Location':row.Engine_Location.values[0],
		'Fuel_Tank_Capacity':row.Fuel_Tank_Capacity.values[0],
		'Drivetrain':row.Drivetrain.values[0],
		'Front_Brakes':row.Front_Brakes.values[0],
		'Rear_Brakes':row.Rear_Brakes.values[0],
		'ABS_Anti_lock_Braking_System':row.ABS_Anti_lock_Braking_System.values[0],
		'Rear_Suspension':row.Rear_Suspension.values[0],
		'Ventilation_System':row.Ventilation_System.values[0],
		'Handbrake':row.Handbrake.values[0],
		'Start_Stop_Button':row.Start_Stop_Button.values[0],
		'Paddle_Shifters':row.Paddle_Shifters.values[0],
		'Fuel_System':row.Fuel_System.values[0],
		'Front_Suspension':row.Front_Suspension.values[0]
	}
	return data
def main():
	#loading folder with templates
	file_loader = FileSystemLoader('./Templates')
	env = Environment(loader=file_loader)
	template = env.get_template('cars_indian.j2')#selecting template
	DF =pickle.load(open('./data/cars_india.pkl', 'rb'))#reading pickle of final dataset
	ids = DF.car_id.tolist()#generating a list for an attribute which have all unique values
	#ids =ids[:1]+ids[8:9]+ids[17:18]+ids[26:27]+ids[49:50]+ids[83:84]+ids[89:90]+ids[101:102]+ids[148:149]+ids[169:170]+ids[212:213]+ids[217:218]+ids[232:233]+ids[235:236]+ids[237:238]+ids[249:250]+ids[255:256]+ids[260:261]+ids[262:263]+ids[267:268]+ids[270:271]+ids[282:283]+ids[289:290]+ids[291:292]+ids[305:306]+ids[313:314]+ids[331:332]+ids[342:343]+ids[345:346]+ids[349:350]+ids[350:351]+ids[355:356]+ids[357:358]+ids[448:449]+ids[745:746]+ids[749:750]+ids[879:880]+ids[887:888]+ids[1145:1146] 
	ids=ids[:20]#remove this to generate articles for all movies281
	# Initiate the file object
	fobj = open('cars_indian.xml', 'w', encoding="utf-8")
	fobj.write(tewiki+'\n')
	cur_page_id=990000#starting page id selected for rendering articles in tewiki
	for i, name in enumerate(ids):
		row = DF.loc[DF['car_id']==name]
		if(row.Make.values[0]!="#"):
			title=row.Make.values[0]+" "+row.Model.values[0]+" "+row.Variant.values[0]
		else:
			title=row.Model.values[0]+" "+row.Variant.values[0]
		text = template.render(getData(row))
		writePage(title, text, fobj, cur_page_id)#adds current car data to .xml file
		cur_page_id+=1
		#print(text)
		
	fobj.write('</mediawiki>')
	fobj.close()#closing file
if __name__ == '__main__':
	main()