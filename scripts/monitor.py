from watchdog.events import LoggingEventHandler
from watchdog.observers import Observer

import click


class FileMonitor:

    def __init__(self, monitorpaths, callback):
        self.monitorpaths = monitorpaths
        self.callback = callback

    def _handler(self, *args, **kwargs):
        self.callback()

    def run(self):
        self.event_handler = LoggingEventHandler()

        self.event_handler.on_created = self._handler
        self.event_handler.on_deleted = self._handler
        self.event_handler.on_modified = self._handler

        self.observer = Observer()

        for path in self.monitorpaths:
            self.observer.schedule(self.event_handler, path, recursive=True)

        self.observer.start()

    def start(self):
        click.secho("Start monitoring:", bold=True, fg="bright_black")
        for path in self.monitorpaths:
            click.secho(" * {}".format(path), bold=True, fg="cyan")
        click.echo()

        self.run()

    def stop(self):
        self.observer.stop()
        self.observer.join()
