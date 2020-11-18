import threading
from functools import partial
from http.server import HTTPServer, SimpleHTTPRequestHandler

import click


class WebServer:

    def __init__(self, bind='localhost', port=8080, directory='.'):
        self.bind = bind
        self.port = port

        self.server_address = (self.bind, self.port)
        self.directory = directory

    def _target(self, server_address, directory):
        httpd = HTTPServer(server_address, partial(SimpleHTTPRequestHandler, directory=directory))
        httpd.serve_forever()

    def run(self):
        self.thread = threading.Thread(target=self._target, args=(self.server_address, self.directory), daemon=True)
        self.thread.start()

    def start(self):
        url = "http://{}:{}/".format(self.bind, self.port)

        click.secho("Serving on {}".format(click.style(url, fg="cyan")), bold=True, fg="bright_black")
        click.secho("Press Ctrl + C to stop...\n", bold=True, fg="bright_black")

        self.run()

    def stop(self):
        self.thread.join(0)
