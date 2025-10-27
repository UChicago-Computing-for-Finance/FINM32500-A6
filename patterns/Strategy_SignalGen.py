import json
from models import MarketDataPoint

# Problem: Support interchangeable trading strategies.
# Expectations:
# Create abstract Strategy.generate_signals(tick: MarketDataPoint) -> int.
# Implement:
# MeanReversionStrategy
# BreakoutStrategy
# Each maintains internal state and uses parameters from strategy_params.json.
# Demonstrate strategy interchangeability and signal generation.
# Returns: 1 for BUY, -1 for SELL, 0 for NO ACTION

from abc import ABC, abstractmethod

class Strategy(ABC):
    @abstractmethod
    def generate_signals(self, tick: MarketDataPoint) -> int:
        pass

class MeanReversionStrategy(Strategy):
    def __init__(self, lookback_window: int = 20, threshold: float = 0.02):
        self.lookback_window = lookback_window
        self.threshold = threshold
        self.price_history = {}  # Internal state: {symbol: [prices]}
    
    def load_params(self, filepath: str = 'inputs/strategy_params.json'):
        with open(filepath, 'r') as f:
            params = json.load(f)
        
        self.lookback_window = params['MeanReversionStrategy'].get('lookback_window', 20)
        self.threshold = params['MeanReversionStrategy'].get('threshold', 0.02)
    
    def generate_signals(self, tick: MarketDataPoint) -> int:
        """
        Generate signals based on mean reversion strategy.
        Buy when price is significantly below the mean.
        Sell when price is significantly above the mean.
        Returns: 1 (BUY), -1 (SELL), or 0 (NO ACTION)
        """
        symbol = tick.symbol
        price = tick.price
        
        # Initialize price history for this symbol if needed
        if symbol not in self.price_history:
            self.price_history[symbol] = []
        
        # Update price history
        self.price_history[symbol].append(price)
        
        # Only generate signals if we have enough data
        if len(self.price_history[symbol]) < self.lookback_window:
            return 0  # NO ACTION - not enough data
        
        # Keep only the last lookback_window prices
        self.price_history[symbol] = self.price_history[symbol][-self.lookback_window:]
        
        # Calculate mean price over lookback window
        mean_price = sum(self.price_history[symbol]) / len(self.price_history[symbol])
        
        # Calculate deviation from mean
        deviation = (price - mean_price) / mean_price
        
        # Generate signals based on threshold
        if deviation < -self.threshold:  # Price is significantly below mean - BUY
            return 1
        elif deviation > self.threshold:  # Price is significantly above mean - SELL
            return -1
        else:
            return 0  # NO ACTION


class BreakoutStrategy(Strategy):
    def __init__(self, lookback_window: int = 15, threshold: float = 0.03):
        self.lookback_window = lookback_window
        self.threshold = threshold
        self.price_history = {}  # Internal state: {symbol: [prices]}
    
    def load_params(self, filepath: str = 'inputs/strategy_params.json'):
        with open(filepath, 'r') as f:
            params = json.load(f)
        
        self.lookback_window = params['BreakoutStrategy'].get('lookback_window', 15)
        self.threshold = params['BreakoutStrategy'].get('threshold', 0.03)
    
    def generate_signals(self, tick: MarketDataPoint) -> int:
        """
        Generate signals based on breakout strategy.
        Buy when price breaks above recent high.
        Sell when price breaks below recent low.
        Returns: 1 (BUY), -1 (SELL), or 0 (NO ACTION)
        """
        symbol = tick.symbol
        price = tick.price
        
        # Initialize price history for this symbol if needed
        if symbol not in self.price_history:
            self.price_history[symbol] = []
        
        # Update price history
        self.price_history[symbol].append(price)
        
        # Only generate signals if we have enough data
        if len(self.price_history[symbol]) < self.lookback_window:
            return 0  # NO ACTION - not enough data
        
        # Keep only the last lookback_window prices
        recent_prices = self.price_history[symbol][-self.lookback_window:]
        self.price_history[symbol] = recent_prices
        
        # Calculate high and low over lookback window
        high_price = max(recent_prices)
        low_price = min(recent_prices)
        
        # Calculate breakout thresholds
        upward_breakout = high_price * (1 + self.threshold)
        downward_breakout = low_price * (1 - self.threshold)
        
        # Generate signals based on breakout
        if price > upward_breakout:  # Price breaks above resistance - BUY
            return 1
        elif price < downward_breakout:  # Price breaks below support - SELL
            return -1
        else:
            return 0  # NO ACTION