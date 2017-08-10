from __future__ import unicode_literals

from unittest import TestCase

from pysoa.client.client import Client


class TestClientRouter(TestCase):

    def setUp(self):
        expansions = {
            'type_routes': {
                'foo': {
                    'service': 'foo',
                    'action': 'get_foo',
                    'request_field': 'id',
                    'response_field': 'foo',
                },
                'bar': {
                    'service': 'bar',
                    'action': 'get_bar',
                    'request_field': 'id',
                    'response_field': 'bar',
                },
                'baz': {
                    'service': 'baz',
                    'action': 'get_baz',
                    'request_field': 'id',
                    'response_field': 'baz',
                },
                'qux': {
                    'service': 'qux',
                    'action': 'get_qux',
                    'request_field': 'id',
                    'response_field': 'qux',
                },
                'quas': {
                    'service': 'quas',
                    'action': 'get_quas',
                    'request_field': 'id',
                    'response_field': 'quas',
                },
                'wex': {
                    'service': 'wex',
                    'action': 'get_wex',
                    'request_field': 'id',
                    'response_field': 'wex',
                },
            },
            'type_expansions': {
                'foo': {
                    'bar': {
                        'type': 'bar',
                        'source_field': 'bar_id',
                        'dest_field': 'bar',
                    },
                    'baz': {
                        'type': 'baz',
                        'source_field': 'baz_id',
                        'dest_field': 'baz',
                    },
                },
                'baz': {
                    'qux': {
                        'type': 'qux',
                        'source_field': 'qux_id',
                        'dest_field': 'qux',
                    },
                },
                'quas': {
                    'wex': {
                        'type': 'wex',
                        'source_field': 'wex_id',
                        'dest_field': 'wex',
                    },
                },
            },
        }
        foo_transport_action_map = {
            'get_foo': {
                'body': {
                    'foo': {
                        '_type': 'foo',
                        'id': 1,
                        'bar_id': 2,
                        'baz_id': 3,
                    },
                },
            },
            'get_quas': {
                'body': {
                    'quas': {
                        '_type': 'quas',
                        'id': 5,
                        'wex_id': 6,
                    },
                }
            }
        }

        bar_transport_action_map = {
            'get_bar': {
                'body': {
                    'bar': {
                        '_type': 'bar',
                        'id': 2,
                    },
                }
            }
        }

        baz_transport_action_map = {
            'get_baz': {
                'body': {
                    'baz': {
                        '_type': 'baz',
                        'id': 3,
                        'qux_id': 4,
                    },
                }
            }
        }

        qux_transport_action_map = {
            'get_qux': {
                'body': {
                    'qux': {
                        '_type': 'qux',
                        'id': 4,
                    },
                }
            }
        }

        wex_transport_action_map = {
            'get_wex': {
                'body': {
                    'wex': {
                        '_type': 'wex',
                        'id': 6,
                    },
                }
            }
        }

        config = {
            'foo': {
                'transport': {
                    'path': 'pysoa.test.stub_service:StubClientTransport',
                    'kwargs': {
                        'action_map': foo_transport_action_map,
                    }
                }
            },
            'bar': {
                'transport': {
                    'path': 'pysoa.test.stub_service:StubClientTransport',
                    'kwargs': {
                        'action_map': bar_transport_action_map,
                    }
                }
            },
            'baz': {
                'transport': {
                    'path': 'pysoa.test.stub_service:StubClientTransport',
                    'kwargs': {
                        'action_map': baz_transport_action_map,
                    }
                }
            },
            'qux': {
                'transport': {
                    'path': 'pysoa.test.stub_service:StubClientTransport',
                    'kwargs': {
                        'action_map': qux_transport_action_map,
                    }
                }
            },
            'wex': {
                'transport': {
                    'path': 'pysoa.test.stub_service:StubClientTransport',
                    'kwargs': {
                        'action_map': wex_transport_action_map,
                    }
                }
            },
        }

        self.client = Client(config=config, expansions=expansions)

    def test_call_actions_with_expansions(self):
        expected_foo_response = {
            'foo': {
                '_type': 'foo',
                'id': 1,
                'bar': {
                    '_type': 'bar',
                    'id': 2,
                },
                'baz': {
                    '_type': 'baz',
                    'id': 3,
                    'qux': {
                        '_type': 'qux',
                        'id': 4,
                    },
                },
            },
        }
        expected_quas_response = {
            'quas': {
                '_type': 'quas',
                'id': 5,
                'wex': {
                    '_type': 'wex',
                    'id': 6,
                },
            },
        }

        response = self.client.call_actions(
            service_name='foo',
            actions=[
                {
                    'action': 'get_foo',
                    'body': {
                        'id': 1,
                    },
                },
                {
                    'action': 'get_quas',
                    'body': {
                        'id': 5,
                    }
                },
            ],
            expansions={
                'foo': ['bar', 'baz.qux'],
                'quas': ['wex'],
            },
        )

        self.assertEqual(
            response.actions[0].body,
            expected_foo_response,
        )

        self.assertEqual(
            response.actions[1].body,
            expected_quas_response,
        )

    def test_call_action_with_expansions(self):
        expected_response = {
            'foo': {
                '_type': 'foo',
                'id': 1,
                'bar': {
                    '_type': 'bar',
                    'id': 2,
                },
                'baz': {
                    '_type': 'baz',
                    'id': 3,
                    'qux': {
                        '_type': 'qux',
                        'id': 4,
                    },
                },
            },
        }

        response = self.client.call_action(
            service_name='foo',
            action='get_foo',
            body={
                'id': 1,
            },
            expansions={
                'foo': ['bar', 'baz.qux'],
            },
        )

        self.assertEqual(
            response.body,
            expected_response,
        )
