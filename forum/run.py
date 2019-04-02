"""Run the application."""
from functional import create_app

app = create_app()  # returns app

if __name__ == '__main__':
    app.run(debug=True)
