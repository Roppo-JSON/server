import json
from logging import getLogger
from logging import INFO

from flask import Blueprint
from flask import jsonify
from flask import make_response


# Make Logger
logger = getLogger(__name__)
logger.setLevel(INFO)


bp_constitution = Blueprint('constitution', __name__)

data = None
with open('./Lows/constitution.json') as f:
    logger.info({
        'action': 'Load file',
        'File': 'constitution.json',
        'status': 'run'
    })

    data = json.load(f)

    logger.info({
        'action': 'Load file',
        'File': 'constitution.json',
        'status': 'success'
    })


@bp_constitution.route('/')
def all_constitution():
    """Get all provision of Japanese constitution"""
    res = make_response(jsonify(data))
    logger.info({
        'action': 'Get all constitution',
        'status': 'success'
    })
    return res


@bp_constitution.route('/<int:low_number>')
def get_provision(low_number):
    """Get a specific provision of Japanese constitution by low_number"""
    res = make_response(jsonify(data[low_number]))
    logger.info({
        'action': 'Get provision',
        'status': 'success',
        'low_number': low_number
    })
    return res


@bp_constitution.route('<int:low_number>/<int:term_number>')
def get_term(low_number, term_number):
    """Get specific term of provision in Japanese constitution by low_number and term_number"""
    provision = data[low_number]
    if len(provision) < term_number:
        logger.error({
            'action': 'Get term',
            'status': 'fail',
            'message': 'Not found specified term',
            'low_number': low_number,
            'term_number': term_number
        })
        return make_response({
            'error': {
                'status': 404,
                'message': f"日本国憲法 第{low_number}条 第{term_number}項 は見つかりませんでした。"
            }
        }), 404
    res = make_response(jsonify(provision[term_number]))
    logger.info({
        'action': 'Get term',
        'status': 'success',
        'low_number': low_number,
        'term_number': term_number
    })

    return res


@bp_constitution.after_request
def add_custom_header(res):
    """レスポンスにカスタムヘッダーを追加する。
    """
    res.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    res.headers['Expires'] = '0'
    res.headers['Server'] = 'Roppo-JSON'
    return res
