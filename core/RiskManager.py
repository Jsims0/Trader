class RiskManager:

    def __init__(self, api):
            self.api = api

    def approve_trade(self, symbol, signal):
        try:
            account = self.api.get_account()
            position = self.api.get_position(symbol)
            buying_power = float(account.buying_power)
            equity = float(account.equity)
            qty = int(position.qty) if position else 0

            # Get all current positions and calculate total market value
            positions = self.api.list_positions()
            total_exposure = sum(float(p.market_value) for p in positions)
        except Exception as e:
            print(f"Risk check failed: could not retrieve account or position data for {symbol}. Error: {e}")
            return False

        # Rules
        max_position_qty = 10
        max_position_value = 0.1 * equity  # max 10% of account in a single asset
        max_total_exposure = 0.5 * equity  # total exposure capped at 50%

        if signal == "buy":
            if qty >= max_position_qty:
                return False
            current_price = float(self.api.get_latest_trade(symbol).price)
            if current_price > buying_power:
                return False
            if qty * current_price > max_position_value:
                return False
            if total_exposure + current_price > max_total_exposure:
                return False

        return True
