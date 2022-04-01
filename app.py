import json

from flask import Flask, render_template, request
import os
app = Flask(__name__)

aspect_sentiments = {}


@app.route('/')
def index():
    return render_template('index.html', asin_to_name=get_sorted_asin_to_name(), first=None, second=None)


@app.route('/compare', methods=['POST'])
def compare():
    first_phone = request.form['first_phone']
    second_phone = request.form['second_phone']

    first_data = aspect_sentiments[first_phone]
    second_data = aspect_sentiments[second_phone]

    return render_template('index.html', asin_to_name=get_sorted_asin_to_name(), first=first_phone, second=second_phone, first_data=first_data, second_data=second_data)

def get_sorted_asin_to_name():
    asin_to_name = {}
    for asin in aspect_sentiments:
        asin_to_name[asin] = aspect_sentiments[asin]['name']
    return {k: v for k, v in sorted(asin_to_name.items(), key=lambda item: item[1])}

@app.before_first_request
def load_data():
    aspect_sentiments_path = '%s/data/aspect_sentiments' %os.path.dirname(__file__)
    for filename in os.listdir(aspect_sentiments_path):
        file_path = os.path.join(aspect_sentiments_path, filename)
        aspect_sentiments_file = open(file_path, 'r')
        aspect_sentiments_dict = json.load(aspect_sentiments_file)
        aspect_sentiments_file.close()

        aspect_sentiments[aspect_sentiments_dict['asin']] = aspect_sentiments_dict

        total_positive = 0
        total_negative = 0
        aspect_to_sentiments = aspect_sentiments[aspect_sentiments_dict['asin']]['aspect_to_sentiments']
        for aspect in aspect_to_sentiments:
            total_positive += aspect_to_sentiments[aspect]['POSITIVE']
            total_negative += aspect_to_sentiments[aspect]['NEGATIVE']

        non_neutral_sentiments = total_positive+total_negative
        if non_neutral_sentiments != 0:
            aspect_sentiments[aspect_sentiments_dict['asin']]['general_score'] = round(total_positive / non_neutral_sentiments * 100, 0)
        else:
            aspect_sentiments[aspect_sentiments_dict['asin']]['general_score'] = 0


if __name__ == '__main__':
    app.run()
