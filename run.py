from src.BUDA import start
from src.BUDA.utils.startup import reset_narratives_on_startup

app = start()

with app.app_context():
    reset_narratives_on_startup(app)
    
if __name__ == '__main__':
    app.run(debug=True)
