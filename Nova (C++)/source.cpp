#include <iostream>
#include <time.h>
#include <fstream>
#include <string>
#include "Header.h"

using namespace std;

int* convertDate(char* date);
void writeToFile(ofstream& file, string* info);
void getDate(ofstream& file, bool firstTime = false, string weekDay = "");

void configure()
{
	ifstream readSettings("Settings.txt");
	ofstream writeSettings("Settings.txt");
	string info[4];
	if (!readSettings.is_open())
	{
		cout << "Awesome! This seems to be your first time using Nova." << endl;
		cout << "Nova is a virtual assistant that is going to help you keep track of your everyday schedule." << endl;
		cout << "Nova is something new, something better, Nova is the future" << endl;
		cout << endl;
		cout << "Before you can use Nova you must configure the application." << endl;
		cout << "So let's get started." << endl;
		cout << "What is your name?" << endl;
		cin >> info[0];
		cout << "What is your birthday? (Format: MM/DD/YYYY)" << endl;
		cin >> info[1];
		cout << "What is your age?" << endl;
		cin >> info[2];
		cout << "What is today's day of the week?" << endl;
		cin >> info[3];
		cout << "Cool! Everything is good to go. Nova is ready to be used" << endl;
		getDate(writeSettings, true, info[3]);
		writeToFile(writeSettings, info);
	}
}
void introduction()
{
	cout << "Hello. My name is Nova. I am your virtual assistant." << endl;
	//cout << "Today is " << weekday[dayWeek] << ": " << date << endl;
}


int* convertDate(char* date)
{
	int month = ((date[0] - '0') * 10) + (date[1] - '0');
	int day = ((date[3] - '0') * 10) + (date[4] - '0');
	int year = ((date[6] - '0') * 10) + (date[7] - '0') + 2000;
	static int mmddyy[3] = { month, day, year };
	return mmddyy;
}

void writeToFile(ofstream& file, string* info)
{
	file << "***********************************************************************************************************************" << endl;
	file << "PROFILE 1" << endl;
	file << "Name: " << info[0] << endl;
	file << "Birthday: " << info[1] << endl;
	file << "Age: " << info[2] << endl;
	file.close();
}

void getDate(ofstream& file, bool firstTime, string weekDay)
{
	string weekday[7] = { "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday" };
	string month[12] = { "January", "Feburary", "March", "April", "May", "June", "July", "August","September", "October", "November", "December" };
	char date[9];
	_strdate_s(date);
	int* mmddyy = convertDate(date);
	static string fullDate[4];

	if (firstTime)
	{
		fullDate[0] = weekDay;
		fullDate[1] = month[mmddyy[0] - 1];
		fullDate[2] = to_string( mmddyy[1]);
		fullDate[3] = to_string(mmddyy[2]);
		file << fullDate[0] << ": " << fullDate[1] << " " << fullDate[2] << ", " << fullDate[3] << endl;

	}

	else
	{
	}
}