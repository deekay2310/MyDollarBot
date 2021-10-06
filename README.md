# TrackMyDollar
<hr>
<p align="center">
<a><img  height=560 width=1000 
  src="https://github.com/deekay2310/MyDollarBot/blob/c56b4afd4fd5bbfffea0d0a4aade58596a5cb678/docs/0001-8711513694_20210926_212845_0000.png" alt="Expense tracking made easy!"></a>
</p>
<hr>

![MIT license](https://img.shields.io/badge/License-MIT-green.svg)
![GitHub](https://img.shields.io/badge/Language-Python-blue.svg)
![GitHub contributors](https://img.shields.io/github/contributors/deekay2310/SE21_HW2B_Group6)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5542548.svg)](https://doi.org/10.5281/zenodo.5542548)
[![Platform](https://img.shields.io/badge/Platform-Telegram-blue)](https://desktop.telegram.org/)
[![Build Status](https://app.travis-ci.com/deekay2310/MyDollarBot.svg?branch=main)](https://app.travis-ci.com/github/deekay2310/MyDollarBot)

<hr>

## About TrackMyDollar

TrackMyDollar is an easy-to-use Telegram Bot that assists you in recording your daily expenses on a local system without any hassle.  
With simple commands, this bot allows you to:
- Add/Record a new spending
- Show the sum of your expenditure for the current day/month
- Display your spending history
- Clear/Erase all your records
- Edit/Change any spending details if you wish to

## Demo
https://user-images.githubusercontent.com/15325746/135395315-e234dc5e-d891-470a-b3f4-04aa1d11ed45.mp4

## Installation guide

The below instructions can be followed in order to set-up this bot at your end in a span of few minutes! Let's get started:

1. This installation guide assumes that you have already installed Python (Python3 would be preferred)

2. Clone this repository to your local system at a suitable directory/location of your choice

3. Start a terminal session, and navigate to the directory where the repo has been cloned

4. Run the following command to install the required dependencies:
```
  pip install -r requirements.txt
```
5. Download and install the Telegram desktop application for your system from the following site: https://desktop.telegram.org/

6. Once you login to your Telegram account, search for "BotFather" in Telegram. Click on "Start" --> enter the following command:
```
  /newbot
```
7. Follow the instructions on screen and choose a name for your bot. Post this, select a username for your bot that ends with "bot" (as per the instructions on your Telegram screen)

8. BotFather will now confirm the creation of your bot and provide a TOKEN to access the HTTP API - copy this token for future use.

9. In the directory where this repo has been cloned, navigate to the "code" folder and open the "code.py" file. This file consists of a variable by the name "api_token". Paste the token copied in step 8 in the placeholder provided for this variable:
```
  api_token = "INSERT API KEY HERE"
```
10. In the Telegram app, search for your newly created bot by entering the username and open the same. Once this is done, go back to the terminal session. Navigate to the directory containing the "code.py" file and run the following command:
```
  python code.py
```
11. A successful run will generate a message on your terminal that says "TeleBot: Started polling." 
12. Post this, navigate to your bot on Telegram, enter the "/start" or "/menu" command, and you are all set to track your expenses!






<hr>
<p>--------------------------------------------------------------------------------------------------</p>
<p>Title:'Track My Dollar'</p>
<p>Version: '1.0'</p>
<p>Description: 'An easy to use Telegram Bot to track everyday expenses'</p>
<p>Authors:'Dev, Prakruthi, Radhika, Rohan, Sunidhi'</p>
<p>--------------------------------------------------------------------------------------------------</p>
