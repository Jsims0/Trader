class ExecutionEngine:
    def __init__(self, api, strategies, risk_manager):
        self.api = api
        self.strategies = strategies  # Dict of symbol -> list of strategies
        self.risk_manager = risk_manager

    def execute_symbol(self, symbol):
        strategies = self.strategies.get(symbol, [])
        if not strategies:
            print(f"No strategies found for {symbol}")
            return

        signal_scores = {"buy": 0.0, "sell": 0.0}
        total_confidence = 0.0

        for strategy in strategies:
            result = strategy.generate_signal()
            signal = result["signal"]
            confidence = result["confidence"]

            if signal in signal_scores:
                signal_scores[signal] += confidence
                total_confidence += confidence

        if total_confidence == 0:
            print(f"Holding {symbol} (no strong signals)\n")
            return

        dominant_signal = max(signal_scores, key=signal_scores.get)
        confidence_ratio = signal_scores[dominant_signal] / total_confidence

        if confidence_ratio < 0.6:
            print(f"Holding {symbol} (weak consensus: {confidence_ratio:.2f})")
            return

        if not self.risk_manager.approve_trade(symbol, dominant_signal):
            print(f"Trade for {symbol} blocked by risk management.")
            return

        if dominant_signal == "buy":
            print(f"Executing BUY for {symbol} (aggregated confidence ratio: {confidence_ratio:.2f})")
            self.api.submit_order(symbol=symbol, qty=1, side='buy', type='market', time_in_force='gtc')
        elif dominant_signal == "sell":
            print(f"Executing SELL for {symbol} (aggregated confidence ratio: {confidence_ratio:.2f})")
            self.api.submit_order(symbol=symbol, qty=1, side='sell', type='market', time_in_force='gtc')