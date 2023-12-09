# sabis-ics

sabis-ics.py is a Python program to parse exported html files of Sabis Digital Platform into an .ics file to load into your preferred calendar client.

## Great. How?

To use sabis-ics.py, follow these steps:

- Using a web browser, log in to SDP.
- Click **Schedules and Timetables**.
- After fully loaded, export the page as full HTML.
- Clone this project using `git clone https://github.com/Windsun6688/sabis-ics`
- Put the exported HTML file under the same directory as the program. (Which is the clone destination)
- Adjust the timezone in the sabis-ics.py if you need to. The default timezone is UTC+8.
- Run the program. It should generate a `SABIS.ics` file in the same directory.
- Import `SABIS.ics` into any calendar client you prefer. Done and dusted.

## Known Limitations

Due to the reliance on the external library `ics.py`, sabis-ics.py cannot generate repeating events. It will only try to generate one-week of events for now.

> Shoutout to everyone behind `ics.py` . You are amazing.

## Privacy Concerns

This program will try to parse an exported html file of SDP, and which will require you to login.
This program is:

- Entirely local, no data transferred to external servers.
- Really Small (Actually <150 lines) so you can easily check on your own if any concern ever rises.

## Contribution

Suggestions and Pulling Requests are welcomed.

## Sure...But Why?

Simple. Because they said it was too hard.

SABIS is leading international school network. There're no doubts about that: their branches are all over the globe and they are present in education scenes everywhere. They deserved it: their journey out of the Lebanon mountains were awesome. Unique insights of technology and the dares of their choices allowed them to rock on till now, but the tradition is fading.

I asked for an .ics file exporting tool on their online digital platform, which already holds a calendar view. It shouldn't be hard for them, a global education network with cutting-edge technology and brilliant minds behind that, to implement this. (Actually, I created this handy little tool in less than 4 hours.) The answer I got from them was, "It was too hard". That's why I wrote this.

So, fellow SABIS alumnis and current students. If you are reading this, stand up, think, and see what 'too hard' things you can do. Being in all of this taught me nothing accept that I can create things that they say was too hard for them.

Ryan, if you are reading this, see? It wasn't that hard after all.

