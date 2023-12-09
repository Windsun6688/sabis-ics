# An utility to generate iCal schedules from SABIS DIGITAL PLATFORM HTML
# They said it was too hard, so I did it.
# 19:12:36, December 8, 2023
# Allen WU

from bs4 import BeautifulSoup
from ics import Calendar, Event
from datetime import date,time,datetime,timedelta
from pytz import timezone

# Find and Clean Schedule Data with HTML Parsing
def html_2_schedule_data(fileLoc:str):
	with open(fileLoc) as f:
		courses = dict()
		soup = BeautifulSoup(f,"html.parser")

		html_events_table = soup.find('table',\
	{"ng-show":"!scheduleCtrl.isLoading && scheduleCtrl.schedule.length > 0",\
	"style":"", "class": ""})

		trs = html_events_table.find_all('tr')
		headerow = [td.get_text(strip = True) for td in trs[0].find_all('th')]
		stripped_rows = []

		for tr in trs:
			row = [td.get_text() for td in tr.find_all('td')]
			period_events_row = []
			for item in row:
				period_events_row.append(tuple([i.strip()\
								for i in item.split("\n")\
								if not i.isspace() and i]))
			stripped_rows.append(period_events_row)

		# Remove Empty Block
		headerow, stripped_rows = headerow[1:],stripped_rows[1:]
		return headerow, stripped_rows

# Generate iCal Event from event data
def schedule_data_2_ics_ev(tz:str,day:int, slot:tuple, info:tuple)-> Event():
	e = Event()
	# No Class
	if info == tuple():
		return None

	# Class
	if len(info) == 3:
		e.name = info[0]
		e.desciption = f"{info[1]}\nInstructor: {info[2]}"
	# Self Study / AMS
	elif len(info) == 1:
		e.name = info[0]
	# Unknown Class
	else:
		print(f"Unexpected Class Info Happened:\n{info}")
		return None

	# Get Time for the Event
	time_slot = slot[1].split(" - ")
	e.begin, e.end = get_ev_time(tz,day,time_slot[0],time_slot[1],slot[0])
	# print(f"{e.name}")
	# print(f"\tstarting at {e.begin.strftime('%Y-%m-%d-%H-%M')}")
	# print(f"\tending at {e.end.strftime('%Y-%m-%d-%H-%M')}")

	return e

# Helper Function to return the time for event
def get_ev_time(tz:str,ev_wk_day:int,start:str,end:str,period:str):
	today = datetime.today()
	curr_wk_day = today.weekday()

	# Get the date of the event day of current week
	d = timedelta(days = abs(ev_wk_day - curr_wk_day))
	if ev_wk_day <= curr_wk_day:
		curr_wk_start_day = today - d
	else:
		curr_wk_start_day = today + d

	period_num = int(period[6:])

	start_hr = int(start.split(':')[0])
	start_min = int(start.split(':')[1])
	end_hr = int(end.split(':')[0])
	end_min = int(end.split(':')[1])

	# 12hr Notation
	if period_num >= 6:
		if start_hr != 12:
			start_hr += 12
		end_hr += 12

	# Handle Timezones
	tz_info = timezone(tz)

	# Use .strftime("%Y-%m-%d-%H-%M") to see diff
	start_time = curr_wk_start_day.replace(hour = start_hr,\
									minute = start_min,\
									second = 0,\
									tzinfo = tz_info)
	end_time = curr_wk_start_day.replace(hour = end_hr,\
									minute = end_min,\
									second = 0,\
									tzinfo = tz_info)
	# Return two datetime objects
	return start_time,end_time

# Main Function
def generate_cal(html_loc:str,tz:str)-> Calendar():
	time_table = Calendar()
	time_table.creator = "WDS@AutoSabisCal"

	header, data = html_2_schedule_data(html_loc)
	for row in data:
		time_slot = row[0]
		for day in range(len(row)-1):
			wk_day = day + 1
			ev_info = row[wk_day]
			ev = schedule_data_2_ics_ev(tz, day, time_slot, ev_info)
			# If there is no class or unexpected class
			if not ev:
				continue
			time_table.events.add(ev)

	with open('SABIS.ics', 'w') as f:
	    f.writelines(time_table.serialize_iter())
	return time_table

if __name__ == "__main__":
	fileLoc = "./Schedules and Timetables.html"
	tz = "Asia/Shanghai"
	try:
		generate_cal(fileLoc,tz)
		print(".ics File Successfully Generated.")
	except Exception as e:
		print(f"Errors occured generating the .ics file.\n{e}")
		print("Please check the file name of the exported html.")
		print("If you think that this is a program malfunction, please submit an issue.")
