from logging import debug
from Bonfire import app, socketio

if __name__ == '__main__':
    # socketio.run(app.run(debug=True))
    socketio.run(app, debug=True)
