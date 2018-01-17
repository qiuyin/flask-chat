from threading import Lock
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


@socketio.on('join', namespace='/chat')
def join(message):
    join_room(message['room'])


@socketio.on('my_room_event', namespace='/chat')
def send_room_message(message):
    emit('my_response',
         {'data': 'user ' + request.sid + ': ' + message['data'], 'room': message['room']},
         room=message['room'])


@socketio.on('inputing', namespace='/chat')
def send_typing_indicator(message):
    emit('inputing',
         {'room': message['room']},
         room=message['room'])

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", debug=True)
