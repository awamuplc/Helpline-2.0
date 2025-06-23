#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (
    unicode_literals,
    print_function)

import os
import markdown as md

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
from threading import (
    Thread)


bp = Blueprint(
    'aicore',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='assets'
    )

edir = os.path.dirname(os.path.realpath(__file__))

epath = edir + "/__init__.py"


def init():
    logger.debug("Initialize AI-Core")

    data = {}
    data['data'] = False
    data['error'] = False

    try:

        runtime = locate('models.aicore.runtime')

        if runtime is not None:
            logger.info("Initializing AI-Core Metadata")

            data['data'] = True
            x = Thread(target=runtime.indexinit, args=({},))
            x.daemon = True
            x.start()

    except Exception as e:
        data['error'] = "Error Index-Action AI-Core {}".format(e)
        logger.critical(data['error'])

    return data


"""
curl -X POST "localhost:50055/aicore/{create, data, action, stats, index}/item" \
-H "Content-Type: application/json" \
--data "{}"
"""
@bp.route("/", methods=['GET'])
@bp.route("/index", methods=['GET'])
def index():
    logger.debug("""AI Services-Data Web Pages""")

    try:

        data = {}
        x = request.args.to_dict()

        if x.get('userid') is None:
            logger.debug("""AI Services Web Page""")
            return render_template('sneat/index.html')

        x = dashboard.indexweb(x)
        
        if x.get('item') is not None:
            logger.debug("""AI Services Template""")
            return render_template('sneat/' + x.get(
                'item') + '.html', data=x.get('data'))

    except Exception as e:
        data['error'] = "Error Index-Template AI Services {}".format(e)
        logger.critical(data['error'])

    return render_template('errors/404.html')


@bp.route("/markdown/<item>", methods=['POST'])
def markdown(item=False):
    logger.debug("""AI Services Data Markdowns""")

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
        data['error'] = "Error Index-Data AI Services-Markdown {}".format(e)
        logger.critical(data['error'])

    return render_template('errors/404.html')


@bp.route("/data/<filename>", methods=['POST'])
@bp.route("/data/<filepath>/<filename>", methods=['POST'])
def data(filename, filepath=False):
    logger.debug("""AI Services Data """ + str(filepath))

    try:

        data = {}

        x = request.get_json()

        metadata = locate('models.aicore.' + filename)

        if filepath:
            logger.debug("AI Services Filepath " + filepath)
            metadata = locate('models.aicore.' + filepath + '.' + filename)

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
        data['error'] = "Error Index-Data AI Services {}".format(e)
        logger.critical(data['error'])

    return jsonify(data), 404


@bp.route("/action/<filename>", methods=['POST'])
@bp.route("/action/<filepath>/<filename>", methods=['POST'])
def action(filename, filepath=False):
    logger.debug("""AI Services Action: """ + filepath)

    try:

        data = {}
        x = request.get_json()

        metadata = locate('models.aicore.' + filename)
        if filepath:
            logger.debug("AI Services Filepath " + filepath)
            metadata = locate('models.aicore.' + filepath + '.' + filename)

        if metadata is not None:

            data['error'] = "Key-Values required: item and track or id"

            if x.get('item') is not None and any(v in x for v in ['id', 'track']):
                data = metadata.indexaction(x)
                if data.get('data'):
                    del data['error'], data['data']
                    return jsonify(data)

    except Exception as e:
        data['error'] = "Error Index-Action AI Services {}".format(e)
        logger.critical(data['error'])

    return jsonify(data), 404


@bp.route("/stats/<filename>", methods=['POST'])
@bp.route("/stats/<filepath>/<filename>", methods=['POST'])
def stats(filename, filepath=False):
    logger.debug("""AI Services Stats: """ + filepath)

    try:

        data = {}
        x = request.get_json()

        metadata = locate('models.aicore.' + filename)
        if filepath:
            logger.debug("AI Services Filepath " + filepath)
            metadata = locate('models.aicore.' + filepath + '.' + filename)

        if metadata is not None:
            data = metadata.indexstats(x)

            if data.get('data'):
                del data['error'], data['data']
                return jsonify(data)

    except Exception as e:
        data['error'] = "Error Index-Stats AI Services {}".format(e)
        logger.critical(data['error'])

    return jsonify(data), 404


@bp.route("/reset/<filename>", methods=['POST'])
@bp.route("/reset/<filepath>/<filename>", methods=['POST'])
def reset(filename, filepath=False):
    logger.debug("""AI Services Reset: """ + str(filepath))

    try:

        data = {}
        x = request.get_json()

        metadata = locate('models.aicore.' + str(filename))
        if filepath:
            logger.debug("AI Services Filepath " + str(filepath))
            metadata = locate('models.aicore.' + filepath + '.' + filename)

        if metadata is not None:

            data = metadata.indexreset(x)

            if data.get('data'):
                del data['error'], data['data']
                return jsonify(data)

    except Exception as e:
        data['error'] = "Error Index-Stats AI Services {}".format(e)
        logger.critical(data['error'])

    return jsonify(data), 404

