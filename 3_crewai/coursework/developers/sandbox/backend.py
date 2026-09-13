import datetime

def get_share_price(symbol: str) -> float:
    """Returns the current fixed price for a given ticker symbol.
    Defaults to $100.0 for unknown symbols.
    """
    prices = {
        "AAPL": 150.0,
        "TSLA": 200.0,
        "GOOGL": 2800.0
    }
    return prices.get(symbol.upper(), 100.0)

class Transaction:
    def __init__(self, transaction_id: str, timestamp: str, tx_type: str, symbol: str, quantity: float, price: float, total_amount: float):
        self.transaction_id = transaction_id
        self.timestamp = timestamp
        self.tx_type = tx_type  # e.g., "DEPOSIT", "WITHDRAW", "BUY", "SELL"
        self.symbol = symbol    # e.g., "AAPL" or "CASH"
        self.quantity = quantity
        self.price = price
        self.total_amount = total_amount

    def to_dict(self) -> dict:
        return {
            "transaction_id": self.transaction_id,
            "timestamp": self.timestamp,
            "tx_type": self.tx_type,
            "symbol": self.symbol,
            "quantity": self.quantity,
            "price": self.price,
            "total_amount": self.total_amount
        }

class Account:
    def __init__(self, account_id: str, initial_deposit: float = 0.0):
        self.account_id = account_id
        self.cash_balance = 0.0
        self.net_deposits = 0.0
        self.holdings = {}  # {symbol: quantity}
        self.transactions = []
        self._tx_counter = 0

        if initial_deposit > 0:
            self.deposit(initial_deposit)

    def _record_transaction(self, tx_type: str, symbol: str, quantity: float, price: float, total_amount: float):
        self._tx_counter += 1
        tx_id = f"TX-{self._tx_counter:04d}"
        timestamp = datetime.datetime.utcnow().isoformat()
        tx = Transaction(
            transaction_id=tx_id,
            timestamp=timestamp,
            tx_type=tx_type,
            symbol=symbol,
            quantity=quantity,
            price=price,
            total_amount=total_amount
        )
        self.transactions.append(tx)

    def deposit(self, amount: float) -> None:
        """Deposits funds into the account. Raises ValueError if amount <= 0."""
        if amount <= 0:
            raise ValueError("Deposit amount must be greater than zero.")
        self.cash_balance += amount
        self.net_deposits += amount
        self._record_transaction(
            tx_type="DEPOSIT",
            symbol="CASH",
            quantity=0.0,
            price=1.0,
            total_amount=amount
        )

    def withdraw(self, amount: float) -> None:
        """Withdraws funds. Raises ValueError if amount <= 0 or if resulting cash balance < 0."""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be greater than zero.")
        if amount > self.cash_balance:
            raise ValueError("Insufficient cash balance for withdrawal.")
        self.cash_balance -= amount
        self.net_deposits -= amount
        self._record_transaction(
            tx_type="WITHDRAW",
            symbol="CASH",
            quantity=0.0,
            price=1.0,
            total_amount=amount
        )

    def buy_shares(self, symbol: str, quantity: float) -> None:
        """Buys shares at current market price. Validates sufficient cash balance."""
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        sym = symbol.upper()
        price = get_share_price(sym)
        total_cost = price * quantity
        if total_cost > self.cash_balance:
            raise ValueError(f"Insufficient funds: cost {total_cost:.2f} exceeds cash balance {self.cash_balance:.2f}.")
        
        self.cash_balance -= total_cost
        self.holdings[sym] = self.holdings.get(sym, 0.0) + quantity
        self._record_transaction(
            tx_type="BUY",
            symbol=sym,
            quantity=quantity,
            price=price,
            total_amount=total_cost
        )

    def sell_shares(self, symbol: str, quantity: float) -> None:
        """Sells shares at current market price. Validates sufficient share holdings."""
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        sym = symbol.upper()
        current_holding = self.holdings.get(sym, 0.0)
        if quantity > current_holding:
            raise ValueError(f"Cannot sell {quantity} shares of {sym}; only {current_holding} owned.")

        price = get_share_price(sym)
        total_proceeds = price * quantity

        self.cash_balance += total_proceeds
        self.holdings[sym] -= quantity
        if self.holdings[sym] == 0:
            del self.holdings[sym]

        self._record_transaction(
            tx_type="SELL",
            symbol=sym,
            quantity=quantity,
            price=price,
            total_amount=total_proceeds
        )

    def get_cash_balance(self) -> float:
        """Returns current cash balance."""
        return self.cash_balance

    def get_holdings(self) -> dict:
        """Returns dictionary of {symbol: quantity} for shares currently held."""
        return self.holdings.copy()

    def get_portfolio_value(self) -> float:
        """Calculates total portfolio value (Cash + Market Value of all share holdings)."""
        shares_value = sum(qty * get_share_price(sym) for sym, qty in self.holdings.items())
        return self.cash_balance + shares_value

    def get_profit_loss(self) -> tuple[float, float]:
        """Calculates total profit/loss (absolute amount and percentage) relative to net deposits."""
        portfolio_val = self.get_portfolio_value()
        if self.net_deposits <= 0:
            # If net deposits is 0 or negative, absolute P&L is portfolio value - net_deposits
            abs_pnl = portfolio_val - self.net_deposits
            pct_pnl = 0.0 if self.net_deposits == 0 else (abs_pnl / abs(self.net_deposits)) * 100.0
        else:
            abs_pnl = portfolio_val - self.net_deposits
            pct_pnl = (abs_pnl / self.net_deposits) * 100.0
        return abs_pnl, pct_pnl

    def get_transactions(self) -> list[Transaction]:
        """Returns chronological list of transactions."""
        return list(self.transactions)
