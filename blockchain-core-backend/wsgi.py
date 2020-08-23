from app.main import app
import os

print(os.getpid())



if __name__ == "__main__":
    print('Hello log!')
    app.run(debug=True, port=5001)
