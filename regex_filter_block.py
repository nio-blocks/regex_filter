import re

from nio.common.block.base import Block
from nio.common.discovery import Discoverable, DiscoverableType
from nio.metadata.properties import StringProperty, \
    ExpressionProperty, BoolProperty


@Discoverable(DiscoverableType.block)
class RegExFilter(Block):

    """ A block to match incoming signals agains a Regular Expression.

    Properties:
        pattern (str): The regular expression to search
        string (expr): Match against this expression.
        ignore_case (bool): Is the match case insensitive.

    """

    pattern = StringProperty(title="Pattern (RegEx)")
    string = ExpressionProperty(title="Match String",
                                default='', attr_default=Exception)
    ignore_case = BoolProperty(title="Ignore Case", default=False)
    inverse = BoolProperty(title="Inverse Matching", default=False)

    def __init__(self):
        super().__init__()
        self._compiled = None

    def configure(self, context):
        super().configure(context)
        if self.ignore_case:
            self._compiled = re.compile(self.pattern, re.I)
        else:
            self._compiled = re.compile(self.pattern)

    def process_signals(self, signals):
        results = []
        for s in signals:
            try:
                match = self._compiled.search(str(self.string(s)))
                if match is not None and not self.inverse:
                    # signal matched
                    results.append(s)
                elif match is None and self.inverse:
                    # signal didn't match,
                    # but we want inverse (i.e. non-matching signals)
                    results.append(s)
            except Exception as e:
                self._logger.debug(
                    "Evaluation failed: {}: {}".format(
                        type(e).__name__, str(e))
                )
        if results:
            self.notify_signals(results)

