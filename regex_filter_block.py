import re

from nio.block.terminals import output
from nio.block.base import Block
from nio.properties import (StringProperty, Property, BoolProperty,
                            VersionProperty)


@output('false')
@output('true')
class RegExFilter(Block):

    """ A block to match incoming signals against a Regular .

    Properties:
        pattern (str): The regular expression to search
        string (expr): Match against this expression.
        ignore_case (bool): Is the match case insensitive.

    """

    pattern = StringProperty(title="Pattern (RegEx)", default='')
    string = Property(title="Match String", default='')
    ignore_case = BoolProperty(title="Ignore Case", default=False)
    version = VersionProperty("0.1.0")

    def __init__(self):
        super().__init__()
        self._compiled = None

    def configure(self, context):
        super().configure(context)
        if self.ignore_case():
            self._compiled = re.compile(self.pattern(), re.I)
        else:
            self._compiled = re.compile(self.pattern())

    def process_signals(self, signals):
        true_result = []
        false_result = []
        for s in signals:
            try:
                match = self._compiled.search(str(self.string(s)))
                if match is not None:
                    # signal matched
                    true_result.append(s)
                else:
                    false_result.append(s)
            except Exception as e:
                self.logger.debug(
                    "Evaluation failed: {}: {}".format(
                        type(e).__name__, str(e))
                )

        self.logger.debug("Emitting {} true signals".format(
            len(true_result)))
        if len(true_result):
            self.notify_signals(true_result, 'true')

        self.logger.debug("Emitting {} false signals".format(
            len(false_result)))
        if len(false_result):
            self.notify_signals(false_result, 'false')
