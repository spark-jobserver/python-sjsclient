import logging

from cliff.lister import Lister

from sjsclient.cmdline import utils


class List(Lister):
    """Show a list of context"""

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        client = utils.get_sjs_client()
        contexts = client.contexts.list()
        return (('Name', 'Time'),
                ((ctx.name, ctx.time) for ctx in contexts))
