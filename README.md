# proj7-Gcal
First part of the MeetUp term project we are working on.

## Author
Jared Paeschke, contact me via paeschk@cs.uoregon.edu

## What is here

This application is just the first part of the larger MeetUp project we
are building in 16F CIS322 class.

## How to Install

When writing and testing this program, the test machine was a Raspberry Pi 3 running Raspian Jesse. 
This is the best sure fire way that the install will go smoothly. However you should have success 
as long as you have bash and make on your server machine. All but step four is done from command line.

1. git clone https://github.com/mahananaka/proj7-Gcal.git < install directory >
2. cd < install directory >
3. bash ./configure
4. You will need to create a a folder called secrets. Inside of secrets folder you will need two files
  * admin_secrets.py which will need 1 line, the quotes must be included.
    * google_key_file=“secrets/google_client_key.json” //this will point to the second file in secrets
  * your file with credentials generated with the google api manager
    * this file is created and downloaded following instructions [here](https://developers.google.com/google-apps/calendar/quickstart/python). Specifically the wizard in Step 1a.
5. make run

At this point the application should start, and inform you which port it is listening on. You may then
bring up this app in your preferred browser via http://serverdomain:port/. So if you’re on your dev
machine and running on port 5000 then the url would be http://localhost:5000/.

## Usage

From the main entry page you’ll have options to select a date range and a time range. Defaults are 
setup but if you wish to change them just click on the fields and a widget will appear for you to
choose new dates.

After this click the button, the date and time range will be set. Also retrieval of calendar data will begin. You 
will be redirect to a google page that will inform you of the data that the program wishes to have access to. After
you allow access then google will return you to the page you were at and now you’ll see that the calendars you have
are listed. Selected which ones you want to be considered when determining busy times and hit the button below.

Finally you are redirected to an events page which will list all events that are considered to block your time
and thus are busy times for you.

## Testing

Some tests were written for the program. You can see these tests in test_flask_main.py. If you wish to run these tests using nose, a nosetests recipe exists in the make file. From command line you can type `make test` to do the nosetests.
