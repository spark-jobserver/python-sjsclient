import logging
import sys

from cliff.app import App
from cliff.commandmanager import CommandManager

logging.getLogger("requests").setLevel(logging.WARNING)


class CmdLineApp(App):

    def __init__(self):
        super(CmdLineApp, self).__init__(
            description='Spark Jobserver Command line client',
            version='0.1.0',
            command_manager=CommandManager('sjs.cmdline'),
            deferred_help=True,
            )

    def initialize_app(self, argv):
        self.LOG.debug('initialize_app')

    def prepare_to_run_command(self, cmd):
        self.LOG.debug('prepare_to_run_command %s', cmd.__class__.__name__)

    def clean_up(self, cmd, result, err):
        self.LOG.debug('clean_up %s', cmd.__class__.__name__)
        if err:
            self.LOG.debug('got an error: %s', err)


def main(argv=sys.argv[1:]):
    app = CmdLineApp()
    return app.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
