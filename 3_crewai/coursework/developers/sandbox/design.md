# System Architecture & Engineering Design: Trading Simulation Account Management System

## 1. System Overview & Architecture

The system is a Python-based trading simulation account management and portfolio tracking platform. It consists of three core components running in a single flat directory under a `uv`-managed Python environment with `gradio` installed:

1. **Backend Module (`backend.py`)**: Manages state, accounts, balances, portfolio holdings, transactions, validations (no negative balance, no over-buying, no short-selling without shares), and pricing (`get_share_price`).
2. **Frontend UI (`app.py`)**: A Gradio 6 web interface allowing users to manage accounts, deposit/withdraw cash, buy/sell shares, view portfolio valuations, holdings reports, profit/loss statements, and transaction history.
3. **Test Suite (`test_backend.py`)**: Comprehensive unit tests covering all edge cases, financial calculations, and validation checks.

---

## 2. Module & Class Specifications

### 2.1 Backend Module (`backend.py`)

#### Global / Utility Functions
* `get_share_price(symbol: str) -> float`
  * Returns the current fixed or dynamic price for a given ticker symbol (e.g., AAPL: $150.0, TSLA: $200.0, GOOGL: $2800.0). Defaults to $100.0 for unknown symbols.

#### Classes & Methods

##### `Transaction`
Represents a single immutable record of account activity.
```python
class Transaction:
    def __init__(self, transaction_id: str, timestamp: str, tx_type: str, symbol: str, quantity: float, price: float, total_amount: float):
        pass
    
    def to_dict(self) -> dict:
        pass
```

##### `Account`
Manages user cash balance, initial deposits, holdings, and transaction history.
```python
class Account:
    def __init__(self, account_id: str, initial_deposit: float = 0.0):
        pass

    def deposit(self, amount: float) -> None:
        """Deposits funds into the account. Raises ValueError if amount <= 0."""
        pass

    def withdraw(self, amount: float) -> None:
        """Withdraws funds. Raises ValueError if amount <= 0 or if resulting cash balance < 0."""
        pass

    def buy_shares(self, symbol: str, quantity: float) -> None:
        """Buys shares at current market price. Validates sufficient cash balance."""
        pass

    def sell_shares(self, symbol: str, quantity: float) -> None:
        """Sells shares at current market price. Validates sufficient share holdings."""
        pass

    def get_cash_balance(self) -> float:
        """Returns current cash balance."""
        pass

    def get_holdings(self) -> dict:
        """Returns dictionary of {symbol: quantity} for shares currently held."""
        pass

    def get_portfolio_value(self) -> float:
        """Calculates total portfolio value (Cash + Market Value of all share holdings)."""
        pass

    def get_profit_loss(self) -> tuple[float, float]:
        """Calculates total profit/loss (absolute amount and percentage) relative to net deposits."""
        pass

    def get_transactions(self) -> list[Transaction]:
        """Returns chronological list of transactions."""
        pass
```

---

### 2.2 Frontend Module (`app.py`)

> **Gradio 6 API Guidance for Frontend Engineer:**
> * Use `gr.Blocks()` as the context manager for building interactive layouts.
> * Use standard layout components (`gr.Row`, `gr.Column`, `gr.Tabs`, `gr.TabItem`, `gr.Markdown`).
> * Input/Output components include `gr.Textbox`, `gr.Number`, `gr.Dropdown`, `gr.Dataframe`.
> * Event binding uses `.click(fn=..., inputs=[...], outputs=[...])`.
> * Gradio 6 features clean event handling without deprecated arguments; ensure all outputs match the expected return types of handler functions.

#### UI Layout & Functions (`app.py`)
```python
import gradio as gr
from backend import Account, get_share_price

# Global active account instance in sandbox session
current_account = Account(account_id="default_user", initial_deposit=10000.0)

def ui_deposit(amount: float) -> tuple[str, float, float, float, list]:
    pass

def ui_withdraw(amount: float) -> tuple[str, float, float, float, list]:
    pass

def ui_buy(symbol: str, quantity: float) -> tuple[str, float, float, float, list, list]:
    pass

def ui_sell(symbol: str, quantity: float) -> tuple[str, float, float, float, list, list]:
    pass

def ui_refresh_status() -> tuple[float, float, float, float, list, list]:
    pass

def create_demo() -> gr.Blocks:
    pass
```

---

### 2.3 Test Suite (`test_backend.py`)

Unit tests written using standard `unittest` library.

```python
import unittest
from backend import Account, Transaction, get_share_price

class TestAccountManagement(unittest.TestCase):
    def setUp(self):
        pass

    def test_initial_deposit(self):
        pass

    def test_deposit_funds(self):
        pass

    def test_withdraw_funds_success(self):
        pass

    def test_withdraw_funds_negative_balance_error(self):
        pass

    def test_buy_shares_success(self):
        pass

    def test_buy_shares_insufficient_funds(self):
        pass

    def test_sell_shares_success(self):
        pass

    def test_sell_shares_exceeding_holdings(self):
        pass

    def test_portfolio_value_and_pnl(self):
        pass

    def test_transaction_history(self):
        pass

if __name__ == "__main__":
    unittest.main()
```

---

## 3. Work Assignments

### 🛠️ Backend Engineer (`backend_engineer`)
* **File to create**: `backend.py`
* **Responsibilities**:
  * Implement `get_share_price(symbol)` with mock prices for `AAPL`, `TSLA`, `GOOGL`.
  * Implement `Transaction` class for logging trade and cash events.
  * Implement `Account` class encapsulating cash management, share holdings dictionary, transaction logs, and financial calculations (portfolio value, profit/loss).
  * Implement strict validation rules preventing negative cash balances, overdrafts during share purchases, and selling unowned shares.

### 🎨 Frontend Engineer (`frontend_engineer`)
* **File to create**: `app.py`
* **Responsibilities**:
  * Implement a clean Gradio 6 `gr.Blocks` interface.
  * Provide tabs or clear sections for:
    1. Account Summary (Cash Balance, Portfolio Value, Profit/Loss).
    2. Cash Operations (Deposit / Withdraw forms with validation messaging).
    3. Trading Operations (Buy / Sell forms with ticker dropdown `AAPL`, `TSLA`, `GOOGL` and quantity input).
    4. Holdings Report & Transaction History Dataframes.
  * Wire all UI buttons to call backend account methods and refresh display components seamlessly using Gradio event handlers.

### 🧪 Test Engineer (`test_engineer`)
* **File to create**: `test_backend.py`
* **Responsibilities**:
  * Write comprehensive unit tests covering standard operations as well as edge cases (zero/negative deposits, exact balance withdrawals, partial share sales, multi-stock portfolios, P&L calculations).
  * Ensure tests execute successfully via `python -m unittest test_backend.py` within the `uv` sandbox environment.