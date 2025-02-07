from app import create_app
from app.utils.startup import reset_narratives_on_startup


app = create_app()

with app.app_context():
    reset_narratives_on_startup(app)
    
if __name__ == '__main__':
    app.run(debug=True)
