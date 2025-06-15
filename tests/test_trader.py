import unittest
from unittest.mock import MagicMock
import asyncio
import concurrent.futures
import pandas as pd
import numpy
from alpaca_trade_api.rest import REST
from strategies.MovingAverageCrossoverStrategy import MovingAverageCrossoverStrategy
from core.ExecutionEngine import ExecutionEngine
from core.RiskManager import RiskManager

class TestMovingAverageCrossoverStrategy(unittest.TestCase):
    def setUp(self):
        self.api_mock = MagicMock()
        self.symbol = 'AAPL'
        self.strategy = MovingAverageCrossoverStrategy(self.api_mock, self.symbol)

    def test_generate_signal_buy(self):
        self.api_mock.get_bars.return_value.df = pd.DataFrame({
            'close': [100 + i for i in range(20)]
        })
        signal = self.strategy.generate_signal()
        self.assertEqual(signal['signal'], 'buy')
        self.assertTrue(0.5 <= signal['confidence'] <= 1.0)

    def test_generate_signal_sell(self):
        self.api_mock.get_bars.return_value.df = pd.DataFrame({
            'close': [120 - i for i in range(20)]
        })
        signal = self.strategy.generate_signal()
        self.assertEqual(signal['signal'], 'sell')
        self.assertTrue(0.5 <= signal['confidence'] <= 1.0)