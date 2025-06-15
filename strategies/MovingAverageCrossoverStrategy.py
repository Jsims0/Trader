import math

class MovingAverageCrossoverStrategy:
    def __init__(self, api, symbol, short_window=5, long_window=20, timeframe='1Min'):
        self.api = api
        self.symbol = symbol
        self.short_window = short_window
        self.long_window = long_window
        self.timeframe = timeframe

    def get_moving_averages(self):
        bars = self.api.get_bars(self.symbol, self.timeframe, limit=self.long_window).df
        short_ma = bars['close'].tail(self.short_window).mean()
        long_ma = bars['close'].mean()
        return short_ma, long_ma

    def generate_signal(self):
        short_ma, long_ma = self.get_moving_averages()
        delta = abs(short_ma - long_ma)
        raw_conf = delta / long_ma if long_ma != 0 else 0
        confidence = 0.5 + 0.5 * math.tanh(raw_conf * 5)  # Smooth scaling from 0.5 to ~1.0

        if short_ma > long_ma:
            return {"symbol": self.symbol, "signal": "buy", "confidence": confidence}
        elif short_ma < long_ma:
            return {"symbol": self.symbol, "signal": "sell", "confidence": confidence}
        else:
            return {"symbol": self.symbol, "signal": "neutral", "confidence": 0.5}