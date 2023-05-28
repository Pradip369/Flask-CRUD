from crud import app
from dotenv import load_dotenv

if __name__ == '__main__':
    load_dotenv('.env')
    app.run()

# set FLASK_ENV=development  run in console