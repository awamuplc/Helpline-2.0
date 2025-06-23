#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (
    unicode_literals,
    print_function
    )

import os
import markdown as md

from . import (
    aicore,
    chatbot,
    calldata,
    casedata,
    contacts,
    coredata,
    qcondata)

from pydoc import (
    locate)
from flask import (
    request,
    jsonify,
    Blueprint,
    render_template)
from flask.helpers import (
    send_file,
    url_for)
from logsdata import (
    logger)


bp = Blueprint(
    'datasets', __name__,
    )

edir = os.path.dirname(os.path.realpath(__file__))

epath = edir + "/__init__.py"


def init():
    logger.info("""Initialize Helpline Database""")

    data = {}

    try:

        metadata = locate('models.coredata.electoral')
        if metadata is not None:
            logger.debug("""Initialize Electoral Models-Data""")
            x = metadata.indexinit({})

        metadata = locate('models.coredata.schools')
        if metadata is not None:
            logger.debug("""Initialize Schools Models-Data""")
            x = metadata.indexinit({})

        metadata = locate('models.coredata.hospitals')
        if metadata is not None:
            logger.debug("""Initialize Hospitals Models-Data""")
            x = metadata.indexinit({})

        metadata = locate('models.coredata.police')
        if metadata is not None:
            logger.debug("""Initialize Police Models-Data""")
            x = metadata.indexinit({})

    except Exception as e:
        data['error'] = "Error Index-Action Models {}".format(e)
        logger.critical(data['error'])

    return data


"""
curl -X POST "localhost:50001/contacts/{create, data, action, stats, index}/item" \
-H "Content-Type: application/json" \
--data "{}"
"""
@bp.route("/", methods=['GET'])
@bp.route("/index", methods=['GET'])
def index():
    logger.debug("""Models Web Pages""")

    try:

        data = {}
        x = request.args.to_dict()

        if x.get('userid') is None:
            logger.debug("""Models Web Page""")
            return render_template('sneat/index.html')

        x = dashboard.indexweb(x)
        
        if x.get('item') is not None:
            logger.debug("""Models Template""")
            return render_template('sneat/' + x.get(
                'item') + '.html', data=x.get('data'))

    except Exception as e:
        data['error'] = "Error Index-Template Models {}".format(e)
        logger.critical(data['error'])

    return render_template('errors/404.html')


@bp.route("/markdown/<item>", methods=['POST'])
def markdown(item=False):
    logger.debug("""Models Data Markdowns""")

    try:

        data = {}
        x = request.get_json()

        mdfile = edir + "/README.md"
        if item:
            mdfile = edir + "/" + item + "/README.md"

        if os.path.isfile(edir + "/" + mkfile):
            with open(edir + "/" + mkfile, 'r') as f:
                file = f.read()

            return render_template(
                'markdown.html',
                data=data,
                markdown=md.markdown(file)
                )

    except Exception as e:
        data['error'] = "Error Index-Data Models-Markdown {}".format(e)
        logger.critical(data['error'])

    return render_template('errors/404.html')


@bp.route("/data/<filename>", methods=['POST'])
@bp.route("/data/<filepath>/<filename>", methods=['POST'])
def data(filename, filepath=False):
    logger.debug("""Models Data """ + str(filepath))

    try:

        data = {}

        x = request.get_json()

        metadata = locate('models.' + filename)

        if filepath:
            logger.debug("Models Filepath " + filepath)
            metadata = locate('models.' + filepath + '.' + filename)

        if metadata is not None:

            data = metadata.indexdata(x)
            if data.get('data'):
                del data['error'], data['data']

                if x.get('view') is not None:
                    return render_template(
                        'sneat/' + filename + '.html',
                        data=data,
                        title=filename.title() + " Datasets"
                        )
                return jsonify(data)

        if x.get('view') is not None:
            return render_template('errors/404.html')

    except Exception as e:
        data['error'] = "Error Index-Data Models {}".format(e)
        logger.critical(data['error'])

    return jsonify(data), 404


@bp.route("/action/<filename>", methods=['POST'])
@bp.route("/action/<filepath>/<filename>", methods=['POST'])
def action(filename, filepath=False):
    logger.debug("""Models Action: """ + filepath)

    try:

        data = {}
        x = request.get_json()

        metadata = locate('models.' + filename)
        if filepath:
            logger.debug("Models Filepath " + filepath)
            metadata = locate('models.' + filepath + '.' + filename)

        if metadata is not None:

            data['error'] = "Key-Values required: item and track or id"

            if x.get('item') is not None and any(v in x for v in ['id', 'track']):
                data = metadata.indexaction(x)
                if data.get('data'):
                    del data['error'], data['data']
                    return jsonify(data)

    except Exception as e:
        data['error'] = "Error Index-Action Models {}".format(e)
        logger.critical(data['error'])

    return jsonify(data), 404


@bp.route("/stats/<filename>", methods=['POST'])
@bp.route("/stats/<filepath>/<filename>", methods=['POST'])
def stats(filename, filepath=False):
    logger.debug("""Models Stats: """ + filepath)

    try:

        data = {}
        x = request.get_json()

        metadata = locate('models.' + filename)
        if filepath:
            logger.debug("Models Filepath " + filepath)
            metadata = locate('models.' + filepath + '.' + filename)

        if metadata is not None:
            data = metadata.indexstats(x)

            if data.get('data'):
                del data['error'], data['data']
                return jsonify(data)

    except Exception as e:
        data['error'] = "Error Index-Stats Models {}".format(e)
        logger.critical(data['error'])

    return jsonify(data), 404


@bp.route("/reset/<filename>", methods=['POST'])
@bp.route("/reset/<filepath>/<filename>", methods=['POST'])
def reset(filename, filepath=False):
    logger.debug("""Models Reset: """ + filepath)

    try:

        data = {}
        x = request.get_json()

        metadata = locate('models.' + filename)
        if filepath:
            logger.debug("Models Filepath " + filepath)
            metadata = locate('models.' + filepath + '.' + filename)

        if metadata is not None:

            data = metadata.indexreset(x)

            if data.get('data'):
                del data['error'], data['data']
                return jsonify(data)

    except Exception as e:
        data['error'] = "Error Index-Stats Models {}".format(e)
        logger.critical(data['error'])

    return jsonify(data), 404

