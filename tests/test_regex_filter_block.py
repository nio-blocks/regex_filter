from collections import defaultdict
from nio.testing.block_test_case import NIOBlockTestCase
from nio.signal.base import Signal
from ..regex_filter_block import RegExFilter


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
            "string": '{{ $val }}'
        })
        blk.start()
        blk.process_signals(signals)
        self.assert_num_signals_notified(3, blk, output_id='true')
        self.assert_num_signals_notified(0, blk, output_id='false')
        blk.stop()

    def test_false_output(self):
        signals = [DummySignal(v) for v in ['a', 'ba', 'AAbA']]
        blk = RegExFilter()
        self.configure_block(blk, {
            "pattern": 'a',
            "string": '{{ $val }}'
        })
        blk.start()
        blk.process_signals(signals)
        self.assert_num_signals_notified(2, blk, output_id='true')
        self.assert_num_signals_notified(1, blk, output_id='false')
        blk.stop()

    def test_filter_case_insensitive(self):
        signals = [DummySignal(v) for v in ['a', 'ba', 'AAbA']]
        blk = RegExFilter()
        self.configure_block(blk, {
            "log_level": "DEBUG",
            "pattern": 'a',
            "string": '{{ $val }}',
            "ignore_case": True
        })
        blk.start()
        blk.process_signals(signals)
        self.assert_num_signals_notified(3, blk, output_id='true')
        self.assert_num_signals_notified(0, blk, output_id='false')
        blk.stop()
