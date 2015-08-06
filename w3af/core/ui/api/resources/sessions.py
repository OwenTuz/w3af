"""
sessions.py

Copyright 2015 Andres Riancho

This file is part of w3af, http://w3af.org/ .

w3af is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

w3af is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with w3af; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""
from flask import jsonify, request

from w3af.core.ui.api import app
from w3af.core.ui.api.utils.error import abort
from w3af.core.ui.api.utils.routes import list_subroutes
from w3af.core.ui.api.utils.auth import requires_auth
from w3af.core.ui.api.db.master import SCANS
from w3af.core.ui.api.utils.scans import (get_scan_info_from_id,
                                          create_scan_helper,
                                          start_scan_helper,
                                          get_new_scan_id,
                                          create_temp_profile)
from w3af.core.data.parsers.doc.url import URL
from w3af.core.controllers.w3afCore import w3afCore
from w3af.core.controllers.exceptions import BaseFrameworkException


@app.route('/sessions/', methods=['POST'])
@requires_auth
def create_scan_session():
    """
    Creates a new w3af scan session.

    :return: A JSON containing:
        - The URL to the newly created session (eg. /sessions/0)
        - The newly created scan ID (eg. 0)
    """
    scan_id = create_scan_helper()

    return jsonify({'message': 'Success',
                    'id': scan_id,
                    'href': '/sessions/%s' % scan_id}), 201


@app.route('/sessions/<int:scan_id>', methods=['GET'])
@requires_auth
def session_info(scan_id):
    """
    Shows information about available actions for a session

    :return: 404 if scan does not exist.
             Otherwise, a list of possible routes under /sessions/<scan_id>/
    """
    if scan_id not in SCANS:
        return jsonify({
            'code': 404,
            'message': 'Session with ID %s does not exist' % scan_id
        }), 404
    else:
        urls = list_subroutes(request)
        return jsonify({'message': 'Session %s' % scan_id,
                        'available_endpoints': urls})

@app.route('/sessions/<int:scan_id>/plugins/', methods=['GET'])
@requires_auth
def list_plugin_types(scan_id):
    if scan_id not in SCANS:
        return jsonify({
            'code': 404,
            'message': 'Session with ID %s does not exist' % scan_id
        }), 404
    w3af = SCANS[scan_id].w3af_core
    return jsonify({ 'entries': w3af.plugins.get_plugin_types() })
