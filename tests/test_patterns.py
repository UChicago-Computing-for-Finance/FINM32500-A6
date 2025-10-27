import unittest
import json
import os
import sys

# Ensure project root is importable when running tests
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from patterns.Factory_InstrumentTypes import InstrumentFactory, Stock, Bond, ETF
from patterns.Singleton_ConfigAccess import Config
from analytics import VolatilityDecorator, BetaDecorator, DrawdownDecorator


class TestFactorySingletonDecorators(unittest.TestCase):

    def test_factory_creates_types(self):
        s = InstrumentFactory.create_instrument({'symbol': 'X', 'type': 'stock', 'price': '10'})
        self.assertIsInstance(s, Stock)
        self.assertEqual(getattr(s, 'instrument_type', None), 'stock')

        b = InstrumentFactory.create_instrument({'symbol': 'Y', 'type': 'bond', 'price': '100', 'maturity': '2030-01-01'})
        self.assertIsInstance(b, Bond)
        self.assertEqual(getattr(b, 'instrument_type', None), 'bond')

        e = InstrumentFactory.create_instrument({'symbol': 'Z', 'type': 'etf', 'price': '50'})
        self.assertIsInstance(e, ETF)
        self.assertEqual(getattr(e, 'instrument_type', None), 'etf')

    def test_singleton_config(self):
        c1 = Config()
        c2 = Config()
        self.assertIs(c1, c2)

        # Compare loaded config with the file
        with open('inputs/config.json', 'r') as f:
            expected = json.load(f)
        self.assertEqual(c1.config, expected)

    def test_decorators_metrics_keys(self):
        stock = Stock({'symbol': 'AAPL', 'price': '169.89', 'type': 'stock'})
        decorated = DrawdownDecorator(BetaDecorator(VolatilityDecorator(stock)))
        metrics = decorated.get_metrics()
        self.assertIsInstance(metrics, dict)

        # ensure all three metrics are present and either float or None
        for key in ('volatility', 'beta', 'max_drawdown'):
            self.assertIn(key, metrics)
            self.assertTrue((metrics[key] is None) or isinstance(metrics[key], float))


if __name__ == '__main__':
    unittest.main()
