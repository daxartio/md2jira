import os
import sys
import getopt
import mistletoe
from .jira_renderer import JIRARenderer

usageString = '%s <markdownfile>' % os.path.basename(sys.argv[0])
helpString = """
Convert Markdown (CommonMark) to JIRA wiki markup
-h, --help                        help
-v, --version                     version
-o <outfile>, --output=<outfile>  output file, use '-' for stdout (default: stdout)
If no input file is specified, stdin is used.
"""

"""
Command-line utility to convert Markdown (CommonMark) to JIRA markup.
JIRA markup spec: https://jira.atlassian.com/secure/WikiRendererHelpAction.jspa?section=all
CommonMark spec: http://spec.commonmark.org/0.28/#introduction
"""


def main():
    try:
        optlist, args = getopt.getopt(sys.argv[1:], 'hvo:',
                                        ['help',
                                        'version',
                                        'output='])

    except getopt.GetoptError as err:
        sys.stderr.write(err.msg + '\n')
        sys.stderr.write(usageString + '\n')
        sys.exit(1)

    app = MarkdownToJIRA()
    app.run(optlist, args)


class MarkdownToJIRA:
    def __init__(self):
        self.version = "1.0.2"
        self.options = {}
        self.options['output'] = '-'

    def run(self, optlist, args):
        for o, i in optlist:
            if o in ('-h', '--help'):
                sys.stderr.write(usageString + '\n')
                sys.stderr.write(helpString + '\n')
                sys.exit(1)

            elif o in ('-v', '--version'):
                sys.stdout.write('%s\n' % self.version)
                sys.exit(0)

            elif o in ('-o', '--output'):
                self.options['output'] = i

        if len(args) < 1:
            sys.stderr.write(usageString + '\n')
            sys.exit(1)

        with open(args[0], 'r') if len(args) == 1 else sys.stdin as infile:
            rendered = mistletoe.markdown(infile, JIRARenderer)

        if self.options['output'] == '-':
            sys.stdout.write(rendered)
        else:
            with open(self.options['output'], 'w') as outfile:
                outfile.write(rendered)


if __name__ == '__main__':
    main()
