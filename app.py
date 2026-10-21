from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Global DataFrame
df = None


@app.route('/')
def index():

    return render_template(
        'index.html',
        columns=None
    )


@app.route('/upload', methods=['POST'])
def upload():

    global df

    file = request.files['file']

    if file:

        filepath = os.path.join(
            app.config['UPLOAD_FOLDER'],
            file.filename
        )

        file.save(filepath)

        # Read CSV
        df = pd.read_csv(filepath)

        columns = df.columns.tolist()

        numerical_columns = df.select_dtypes(
            include=['int64', 'float64']
        ).columns.tolist()

        categorical_columns = df.select_dtypes(
            include=['object']
        ).columns.tolist()

        return render_template(
            'index.html',
            columns=columns,
            numerical_columns=numerical_columns,
            categorical_columns=categorical_columns
        )


@app.route('/graph', methods=['POST'])
def graph():

    global df

    x_column = request.form['x_column']
    y_column = request.form['y_column']
    graph_type = request.form['graph_type']

    fig = None

    # Graph Selection

    if graph_type == 'scatter':

        fig = px.scatter(
            df,
            x=x_column,
            y=y_column
        )

    elif graph_type == 'line':

        fig = px.line(
            df,
            x=x_column,
            y=y_column
        )

    elif graph_type == 'bar':

        fig = px.bar(
            df,
            x=x_column,
            y=y_column
        )

    elif graph_type == 'histogram':

        fig = px.histogram(
            df,
            x=x_column
        )

    elif graph_type == 'box':

        fig = px.box(
            df,
            x=x_column,
            y=y_column
        )

    elif graph_type == 'pie':

        fig = px.pie(
            df,
            names=x_column,
            values=y_column
        )

    graph_html = fig.to_html(full_html=False)

    columns = df.columns.tolist()

    numerical_columns = df.select_dtypes(
        include=['int64', 'float64']
    ).columns.tolist()

    categorical_columns = df.select_dtypes(
        include=['object']
    ).columns.tolist()

    return render_template(
        'index.html',
        columns=columns,
        numerical_columns=numerical_columns,
        categorical_columns=categorical_columns,
        graph_html=graph_html
    )


if __name__ == '__main__':

    app.run(debug=True)