from app import config
from app.main import app

if __name__ == '__main__':
    debugMode = False
    if(hasattr(config, 'debugMode')):
        if(config.debugMode == True):
            debugMode = True
    app.run(debug=debugMode)
    