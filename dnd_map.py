from flask import Flask, render_template, request
from flask_socketio import SocketIO
from PIL import Image, ImageDraw
import cv2
import os


app = Flask(__name__)
socketio = SocketIO(app)

PLAYERS = {}


@app.route('/update_map', methods=['POST'])
def update_map():
    global MAP_FILENAME, PLAYERS, TOKEN_WIDTH, HORIZONTAL_CELLS
    
    PLAYERS.clear()
    
    new_map = request.form['map']
    
    if new_map != "None":
        MAP_FILENAME = 'maps/' + new_map
    else:
        HORIZONTAL_CELLS = int(request.form['cells'])
    
    MESH = create_mesh("static/" + MAP_FILENAME)
    MESH.save("static/mesh.png")
    
    TOKEN_WIDTH = (MESH_WIDTH / MESH.size[1]) * 100
    
    socketio.emit('update_map', [MAP_FILENAME, TOKEN_WIDTH])
    
    return 'OK'


@app.route('/update_player_position', methods=['POST'])
def update_player_position():
    global PLAYERS
    
    player = request.form['p']
    
    if request.form['d'] == "True":
        del PLAYERS[player]
    else:
        if player == 'new':
            if len(PLAYERS) > 0:
                player = sorted(PLAYERS.keys())[-1] + '0'
            else:
                player = 'Player0'
                
        if player in PLAYERS:
            image_path = PLAYERS[player][2]
        else:
            image_path = request.form['image']
                
        x = float(request.form['x'])
        y = float(request.form['y'])
        max_x = float(request.form['max_x'])
        max_y = float(request.form['max_y'])

        PLAYERS[player] = [(x / max_x) * 100, (y / max_y) * 100, image_path]
    
    socketio.emit('update_players', [PLAYERS, TOKEN_WIDTH])
    
    return 'OK'


def files_in_directory(directory):
    try:
        files = os.listdir(directory)
        return files
    except OSError as e:
        print(f"Error: {e}")
        raise OSError


def create_mesh(filename):
    image = cv2.imread(filename)
    height, width = image.shape[0], image.shape[1]
    
    new_image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(new_image)
    
    global MESH_WIDTH
    MESH_WIDTH = int((width-1) / HORIZONTAL_CELLS)
    
    # Draw horizontal lines
    for i in range(0, height, MESH_WIDTH):
        draw.line([(0, i), (width, i)], fill=(255, 255, 255, 255), width=1)
        
    # Draw vertical lines
    for i in range(0, width, MESH_WIDTH):
        draw.line([(i, 0), (i, height)], fill=(255, 255, 255, 255), width=1)

    return new_image


@app.route('/')
def display_map():
    maps = files_in_directory('static/maps')
    avatars = files_in_directory('static/avatars')
    
    return render_template('display_map.html', map_filename=MAP_FILENAME, token_width=TOKEN_WIDTH, horizontal_cells=HORIZONTAL_CELLS, maps=maps, players=PLAYERS, avatars=avatars)


if __name__ == '__main__':
    HORIZONTAL_CELLS = 10

    MAP_FILENAME = 'maps/' + files_in_directory('static/maps')[0]
    MESH = create_mesh("static/" + MAP_FILENAME)
    MESH.save("static/mesh.png")
    
    TOKEN_WIDTH = (MESH_WIDTH / MESH.size[1]) * 100
    
    socketio.run(app, host="0.0.0.0", port="5000", allow_unsafe_werkzeug=True)