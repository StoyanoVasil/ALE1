from flask import render_template, request, Response, json
from src import app
from src.models.Tree import *
from src.models.Errors import ParserError


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/expression_image', methods=['POST'])
def get_expression_image():
    if request.method == 'POST':
        data = request.json
        try:
            t = Tree(data['expression'])
            return Response(json.dumps({'image': t.get_graph_image_name()}), 200)
        except ParserError as e:
            return Response(json.dumps({'error': e.message}), 200)
