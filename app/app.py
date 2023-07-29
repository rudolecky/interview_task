from flask import Flask, render_template
from scraper import scrape_into_db

class FlaskApp:
    def __init__(self):
        self.flats = scrape_into_db()
   

    def render_flats(self):
        return render_template("index.html", flats=self.flats)

app = Flask(__name__)
fl = FlaskApp()

@app.route('/')
def hello():
    return fl.render_flats()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)