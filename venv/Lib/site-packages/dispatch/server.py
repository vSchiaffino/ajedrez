#!/usr/bin/env python
"""Simple messaging server to receieve queueing requests from distributed
clients, and save them in a pre-defined textual format in order to be picked
up by spiders (which will push responses back via. HTTP).
"""
from __future__ import absolute_import, print_function, unicode_literals
from .daemon import AbstractDaemon
from .handler import Handler
from six.moves import socketserver
import json
import logging
import logging.handlers
import os
import sys
import traceback
import warnings


class Server(AbstractDaemon):
    """A messaging server daemon."""
    
    # -------------------------------------------------------------------------
    # -- These are the most common/likely things for a subclass to want      --
    # -- to override; you really must* override service_name if you run more --
    # -- than one distinct one of these on a machine at a time .             --
    # -------------------------------------------------------------------------
    
    # Default interface to bind to, and default port.
    #
    # Override these in a subclass if desired, or send them explicitly
    # to `__init__`.
    bind_interface = '127.0.0.1'
    port = 5766
    
    # This is used for the name of the logger as well as some default paths:
    # override this in subclasses.
    service_name = 'messaging'
    
    # The handler class for requests made to this daemon.
    #
    # The default Handler class only has a ping method, so this must be
    # overridden for the messaging server to actually do anything important.
    handler = Handler
    
    # The version number for the service.
    version = '1.0'
    
    # ----------------------------------------------------
    # -- These are probably fine as is for most people. --
    # ----------------------------------------------------
    
    # Logging options
    # Note: If you override the path in a subclass, retain the trailing slash.
    request_log_level = logging.INFO
    error_log_level = logging.ERROR
    max_log_file_size = 10 ** 7
    rotating_log_file_max = 5
    log_file_path = property(lambda self: '/var/log/%s/' % self.service_name)
    
    # Set a default pid file name.
    pid_file = property(lambda self: '/tmp/%s.pid' % self.service_name)
    
    # ----------------------------------------------------------------------
    # -- Instance methods; these can be overridden as necessary, but      --
    # -- make sure their return signatures stay the same. For `__init__`, --
    # -- you should be sure and call the base class' __init__.            --
    # ----------------------------------------------------------------------
    
    def __init__(self, bind_interface=None, port=None, handler=None,
                       output_to_screen=False, **kwargs):
        """Daemon constructor."""
        
        # Call the superclass constructor.
        super(Server, self).__init__(
            pidfile=kwargs.get('pid_file', self.pid_file),
        )
        
        # Set the bind interface to the class default
        # unless it's explicitly set.
        self.address = (
            bind_interface or self.bind_interface,
            int(port) if port else self.port,
        )
        
        # Set the instance handler to the class handler,
        # or to the keyword argument if excplitly set.
        self.instance_handler = handler or self.handler
        
        # Save the `output_to_screen` variable.
        self.output_to_screen = output_to_screen
        
        # Save any additional keyword arguments, and make them
        # available on the server object.
        self.kw_options = kwargs
                        
    def setup_request_log(self, **kwargs):
        """Create and return a logging object to function as the
        request log for this daemon.
        """
        # Get my log file path; make sure it has a trailing slash.
        log_file_path = kwargs.get('log_file_path', self.log_file_path)
        if log_file_path[-1] != '/':
            log_file_path += '/'
        
        # Set up the request log.
        try:
            request_log_file = '{path}{service}.request.log'.format(
                path=log_file_path,
                service=self.service_name,
            )
            request_log = logging.getLogger(self.service_name)
            request_log.setLevel(kwargs.get('request_log_level',
                                            self.request_log_level))
            request_log.addHandler(
                logging.handlers.RotatingFileHandler(request_log_file,
                    backupCount=kwargs.get('rotating_log_file_max',
                                           self.rotating_log_file_max),
                    maxBytes=kwargs.get('max_log_file_size',
                                        self.max_log_file_size),
                ),
            )
        except:
            warnings.warn('Something went wrong with the request logger.\n'
                          'Does the executing user have write permission to '
                          'your request log file (%s)?'
                          % request_log_file, Warning)
        
        # Done; return back the request_log.
        return request_log
    
    def setup_error_log(self, **kwargs):
        """Create and return a logging object to function as the error
        log for this daemon.
        """
        # Get my log file path; make sure it has a trailing slash.
        log_file_path = kwargs.get('log_file_path', self.log_file_path)
        if log_file_path[-1] != '/':
            log_file_path += '/'
        
        # set up the error log
        try:
            error_log_file = '{path}{service}.error.log'.format(
                path=log_file_path,
                service=self.service_name,
            )
            error_log = logging.getLogger(self.service_name + '.errors')
            error_log.setLevel(kwargs.get('error_log_level',
                                          self.error_log_level))
            error_log.addHandler(
                logging.handlers.RotatingFileHandler(error_log_file,
                    backupCount=kwargs.get('rotating_log_file_max',
                                           self.rotating_log_file_max),
                    maxBytes=kwargs.get('max_log_file_size',
                                        self.max_log_file_size),
                ),
            )
        except:
            warnings.warn('Something went wrong with the error logger.\n'
                          'Does the executing user have write permission '
                          'to your error log file (%s)?' % error_log_file,
                          Warning)
            
        # Done, return back the error log.
        return error_log
    
    def run(self):
        """Actually run the daemon."""
        
        # Attach a few things to the handler class
        # so methods there have easy access to them.
        self.handler.request_log = self.setup_request_log(**self.kw_options)
        self.handler.error_log = self.setup_error_log(**self.kw_options)
        self.handler.output_to_screen = self.output_to_screen
        self.handler.version = self.version
        
        # If any additional options were sent in `__init__`,
        # set them to the handler also.
        for key, value in self.kw_options.iteritems():
            setattr(self.handler, key, value)
        
        # Get my server address as a tuple.
        server = socketserver.ThreadingTCPServer(self.address, self.handler)
        
        try:
            # Make the server accept commands.
            server.serve_forever()
        except KeyboardInterrupt:
            self.pre_shutdown()

            # Get the hell outta dodge...
            sys.exit(0)
            
    def pre_shutdown(self):
        """Code to run when the server is being shut down."""
        print('\n')
