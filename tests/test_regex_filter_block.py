from ..regex_filter_block import RegExFilter
from nio.util.support.block_test_case import NIOBlockTestCase
from nio.common.signal.base import Signal


class DummySignal(Signal):

    def __init__(self, val):
        super().__init__()
        self.val = val


class TestRegExFilter(NIOBlockTestCase):

    def test_pass(self):
        signals = [DummySignal(v) for v in ['a', 'ba', 'aaba']]

        blk = RegExFilter()
        self.configure_block(blk, {
            "pattern": '',
            "string": '{{$val}}'
        })
        blk.start()
        blk.process_signals(signals)
        self.assert_num_signals_notified(3, blk)
        blk.stop()

    def test_filter_case_sensitive(self):
        signals = [DummySignal(v) for v in ['a', 'ba', 'AAbA']]

        blk = RegExFilter()
        self.configure_block(blk, {
            "pattern": 'a',
            "string": '{{$val}}'
        })
        blk.start()
        blk.process_signals(signals)
        self.assert_num_signals_notified(2, blk)
        blk.stop()

    def test_filter_case_insensitive(self):
        signals = [DummySignal(v) for v in ['a', 'ba', 'AAbA']]

        blk = RegExFilter()
        self.configure_block(blk, {
            "log_level": "DEBUG",
            "pattern": 'a',
            "string": '{{$val}}',
            "ignore_case": True
        })
        blk.start()
        blk.process_signals(signals)
        self.assert_num_signals_notified(3, blk)
        blk.stop()
