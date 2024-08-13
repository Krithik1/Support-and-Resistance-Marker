import os

from flask import Flask, render_template, request

from key_level_marker import getTickerInformation, plot_all

app = Flask(__name__)


with app.app_context():
    CHARTS_DIR = "static/charts/"
    if os.path.exists(CHARTS_DIR):
        for filename in os.listdir(CHARTS_DIR):
            file_path = os.path.join(CHARTS_DIR, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                    print(f"Deleted file: {file_path}")
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")
    else:
        print(f"Directory {CHARTS_DIR} does not exist.")


@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":
        ticker = request.form["ticker"]
        interval = request.form["interval"]
        start = request.form["start_date"]
        end = request.form["end_date"]
        df = getTickerInformation(ticker, interval, start, end)
        chart_filename = plot_all(df)
        return render_template("index.html", chart_url=chart_filename)

    return render_template("index.html", chart_url=None)


if __name__ == "__main__":
    app.run(debug=True)
