from flask import Flask, render_template, request
from db_utility import get_filtered_cars_details, validate_form_submitted_data
import pandas as pd
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route("/formSubmissionStatus", methods=["POST"])
def formSubmissionStatus():
    output_list = []
    input_values = {}
    keys_from_forms = request.form.keys()
    for key in keys_from_forms:
        input_values[key] = request.form.get(key)
   
    message = validate_form_submitted_data(input_values)
    return render_template("./formSubmissionStatus.html",message=message)


@app.route("/viewCar")
def viewCar():
    return render_template('./viewCar.html')


@app.route("/home")
def home():
    return render_template('./home.html')


@app.route("/form_preferences", methods=["POST"])
def form_preferences():
    output_list = []
    keys_from_forms = request.form.keys()
    for key in keys_from_forms:
        output_list.append([key, request.form.get(key)])
    x = get_filtered_cars_details(request.form)

    df = pd.DataFrame(x)
    if "main_picture_url" in df:
        df.drop("main_picture_url", inplace=True, axis=1)
    table = df.to_html(index=False)

    if len(df)==0:
        return render_template("./vctable.html",table="oops..!! Sorry there is no matching data")
   
    print(df) 
    return render_template("./vctable.html", table=table)


if __name__ == '__main__':
    app.run(debug=False)