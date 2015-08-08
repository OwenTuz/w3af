"""
test_sessions.py

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
import json

from w3af.core.ui.api.tests.utils.api_unittest import APIUnitTest


class SessionTest(APIUnitTest):

    def test_session_config(self):
        create_session = self.app.post('/sessions/',
                                       headers=self.HEADERS)

        session_id = json.loads(create_session.data)['id']
        self.assertEqual(create_session.status_code, 201)

        get_plugin_types = self.app.get('/sessions/%s/plugins/' % session_id,
                                       headers=self.HEADERS)
        plugin_types = json.loads(get_plugin_types.data)['entries']
        self.assertEqual(get_plugin_types.status_code, 200)
        self.assertIsInstance(plugin_types, list)
        self.assertTrue('audit' in plugin_types)

        get_plugin_list = self.app.get('/sessions/%s/plugins/%s/' %(
                                            session_id,
                                            plugin_types[0]),
                                        headers=self.HEADERS)
        plugin_list = json.loads(get_plugin_list.data)['entries']
        self.assertEqual(get_plugin_list.status_code, 200)
        self.assertIsInstance(plugin_list, list)

