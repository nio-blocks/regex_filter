import re
from nio.common.block.attribute import Output
from nio.common.versioning.dependency import DependsOn
from nio.common.block.base import Block
from nio.common.discovery import Discoverable, DiscoverableType
from nio.metadata.properties import StringProperty, \
    ExpressionProperty, BoolProperty, VersionProperty


@Output('false')
@Output('true')
@DependsOn('nio', '1.5.2')
@Discoverable(DiscoverableType.block)
class RegExFilter(Block):

    """ A block to match incoming signals against a Regular Expression.

    Properties:
        pattern (str): The regular expression to search
        string (expr): Match against this expression.
        ignore_case (bool): Is the match case insensitive.

    """

    version = VersionProperty(version="0.1.0")
    pattern = StringProperty(title="Pattern (RegEx)")
    string = ExpressionProperty(title="Match String",
                                default='', attr_default=Exception)
    ignore_case = BoolProperty(title="Ignore Case", default=False)

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
                self._logger.debug(
                    "Evaluation failed: {}: {}".format(
                        type(e).__name__, str(e))
                )

        self._logger.debug("Emitting {} true signals".format(
            len(true_result)))
        if len(true_result):
            self.notify_signals(true_result, 'true')

        self._logger.debug("Emitting {} false signals".format(
            len(false_result)))
        if len(false_result):
            self.notify_signals(false_result, 'false')
