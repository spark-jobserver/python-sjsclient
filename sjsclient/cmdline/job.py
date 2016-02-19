import logging

from cliff.lister import Lister
from cliff.show import ShowOne

from sjsclient.cmdline import utils


class List(Lister):
    """Show a list of context"""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(List, self).get_parser(prog_name)
        parser.add_argument('-l', '--limit', nargs='?', default='50')
        return parser

    def take_action(self, parsed_args):
        client = utils.get_sjs_client()
        jobs = client.jobs.list(params={'limit': parsed_args.limit})
        columns = ('jobId',
                   'context',
                   'status',
                   'duration',
                   'classpath',
                   'result',)
        return (columns,
                ((j.jobId, j.context, j.status, j.duration,
                  j.classpath, j.result) for j in jobs))


class Show(ShowOne):
    "Show details about a job"

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(Show, self).get_parser(prog_name)
        parser.add_argument('-j', '--job-id', nargs='?')
        return parser

    def take_action(self, parsed_args):
        jobId = parsed_args.job_id
        client = utils.get_sjs_client()
        job = client.jobs.get(jobId)

        columns = ('Id',
                   'Context',
                   'Status',
                   'Result',
                   )
        data = (job.jobId,
                job.context,
                job.status,
                job.result,
                )

        return (columns, data)
