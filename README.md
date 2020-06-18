# rotary-radio
Turn your rotary phone into an online radio !

This repo is meant to be used with the instructions that can be found here: ///Arduino Link here///.

## This repo consists of three parts:
### 🐍 Python script
A script for Raspberry pi that handles the rotary phone's input (such as numbers and detecting if the headset is picked up or put down.
### 📦 Chrome extension
This chrome extension is to be installed on the Raspberry Pi's Chromium browser. This is what enables the interfacing with the radiooooo.com website, without using the keyboard or mouse, but the telephone instead. 
#### Install the Chrome Extension
You can install the Chrome extension on your Raspberry Pi's Chromium browser. Here's how: <br>
- Make sure you have chromium installed for Raspberry Pi <br>
At first, we have to update our packages. Open a terminal and type in:<br>
```sudo apt-get update```
Then, you can install it also by using the packet manager:
```sudo apt-get install chromium-browser --yes```
### 🤖 Arduino code
The arduino code detects which country is selected on the map, and then sends the information via serial to the Raspberry Pi.

---

Each script has comments. 

Enjoy!

