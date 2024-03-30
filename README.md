# DnD Interactive Map

### Description

This is flask application that starts a web server within WiFi network. The app takes an image and creates interactive map, grid for it, and manages players on the board. Once set up you can connect to this server via browser on other devices. Idea of this app is to enable players to move on the virtual board using their phones, laptops, or w/e.

![](https://github.com/DefinitelyNotRandomNickname/DnD_Interactive_map/blob/main/static/resources/app.gif)

## Setting up the application

You need to install required libraries from `requirements.txt` file using `pip install -r requirements.txt`. Rest is pretty straightforward. Just run the `dnd_map.py` with python. After running the app, you'll see addresses like:

![](https://github.com/DefinitelyNotRandomNickname/DnD_Interactive_map/blob/main/static/resources/run_addresses.png)

The first one is localhost, so if you want to connect on a different device you need to use latter. Just connect to the (in my case) `http://192.168.1.11:5000`. You can change the port in python script.

## Features

### Map

Map is randomly pulled from directory `static/maps`. In browser you can change selected map via `Selected map` option. You can add new maps to the previously mentioned folder. Just drop some image in there. Feel free to zoom the map in the browser, but it may happen to fucking break. I have no idea why, but that's the problem for future me.

### Grid

Grid is created by app the the very start and when amount of cells in the app has changed. It's stored as image as `static/mesh.png`. You can manipulate density of it's cells and it's color in the browser.

### Players

At the start of the app there're 0 players, you can add a new player in the browser. At the top of UI is button for adding players and a dropbox for selecting their token(avatar). Players can move by clicking at the token on the map and clicking again at the position they want to move to. Player can delete token by moving it into the red bin at the bottom of UI. You can add new tokens by dropping some pics into `static/avatars` directory.

### UI

You can disable UI by clicking checkbox at the top of the map. I recommend disabling it if you don't need UI, but it doesn't matter much. UI as well as map scales with screen size, but on some wide-ass screens it can look weird.

## Note

This is early access so it kinda sucks, but hey it works. Feel free to use this project for your needs.

Also if you are struggling with BBEG I strongly recommend using `Gamer Mode`. It significantly increases your gaming performance.

