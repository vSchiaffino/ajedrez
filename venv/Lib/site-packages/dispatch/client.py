from __future__ import absolute_import, print_function, unicode_literals
import json
import logging
import socket


class Client(object):
    host = '127.0.0.1'
    port = 5766
    
    def __init__(self, host=None, port=None):
        self.address = (
            host or self.host,
            int(port) if port else self.port,
        )
                
    def __getattr__(self, attr_name):
        """Return a method that, when called with keyword arguments,
        will send a request to the JSON messaging server."""
        
        def _send(action=attr_name, **kwargs):
            """Send a request, and return the response from the
            dispatch server."""
            
            # add the action to the keyword argument list
            kwargs['_action'] = action

            # create a socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            try:
                # connect to the server
                sock.connect(self.address)

                # send the requested message
                sock.sendall(json.dumps(kwargs))
                sock.shutdown(1)

                # receieve the response from the dispatch server
                # (which will then close the connection)
                response = ''
                chunk = sock.recv(2048)
                while len(chunk):
                    response += chunk
                    chunk = sock.recv(2048)
                return json.loads(response)

            except socket.error as ex:
                # something went wrong...close the connection,
                # log the error, and raise
                try:
                    sock.close()
                except:
                    pass

                # raise
                raise self.Error(six.text_type(ex))
        return _send
        
    class Error(Exception):
        pass
