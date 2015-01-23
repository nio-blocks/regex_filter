import re

from nio.common.block.base import Block
from nio.common.discovery import Discoverable, DiscoverableType
from nio.metadata.properties import StringProperty, \
    ExpressionProperty, BoolProperty


class RegExFilter(Block):

    """ A block to match incoming signals agains a Regular Expression.

    Properties:
        pattern (str): The regular expression to search
        string (expr): Match against this expression.
        case_sensitive (bool): Is the match case sensitive.

    """

    pattern = StringProperty(title="Pattern (RegEx)")
    string = ExpressionProperty(title="Match String",
                                default='', attr_default=Exception)
    case_sensitive = BoolProperty(title="Case Sensitive", default=True)

    def __init__(self):
        super().__init__()
        self._compiled = None

    def configure(self, context):
        super().configure(context)
        if self.case_sensitive:
            self._compiled = re.compile(self.pattern)
        else:
            self._compiled = re.compile(self.pattern, re.I)

    def process_signals(self, signals):
        results = []
        for s in signals:
            try:
                match = self._compiled.search(str(self.string(s)))
                if match is not None:
                    results.append(s)
            except Exception as e:
                self._logger.debug(
                    "Evaluation failed: {}: {}".format(
                        type(e).__name__, str(e))
                )
        if results:
            self.notify_signals(results)
    
