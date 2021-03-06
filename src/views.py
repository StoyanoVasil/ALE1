from flask import render_template, request, Response, json, session
from src import app
from src.models.TruthTable import *
from src.models.Errors import ParserError


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/create_truth_table', methods=['POST'])
def create_truth_table():
    if request.method == 'POST':
        data = request.json
        try:
            t = TruthTable(data['expression'])
            return Response(json.dumps({'image': t.tree.get_graph_image_name(),
                                        'table': t.table,
                                        'identification': t.identification,
                                        'nand': str(t.tree.nandify()),
                                        'normalization': t.normalization}), 200)
        except ParserError as e:
            return Response(json.dumps({'error': e.message}), 200)


@app.route('/simplify', methods=['POST'])
def simplify():
    if request.method == 'POST':
        data = request.json
        try:
            t = TruthTable(data['expression'])
            t.simplify()
            return Response(json.dumps({'table': t.simplified_table,
                                        'identification': t.simplified_identification,
                                        'nand': str(t.tree.nandify()),
                                        'normalization': t.simplified_normalization}), 200)
        except ParserError as e:
            return Response(json.dumps({'error': e.message}), 200)


@app.route('/render_table', methods=['POST'])
def render_table():
    if request.method == 'POST':
        data = request.json
        return render_template('table.html',
                               table=data['table'],
                               identification=data['identification'],
                               nand=data['nand'],
                               normalization=data['normalization'])
