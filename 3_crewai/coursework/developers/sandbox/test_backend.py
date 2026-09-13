import unittest
from backend import Account, Transaction, get_share_price

class TestAccountManagement(unittest.TestCase):
    def setUp(self):
        self.account = Account(account_id="test_user", initial_deposit=1000.0)

    def test_initial_deposit(self):
        self.assertEqual(self.account.get_cash_balance(), 1000.0)
        self.assertEqual(self.account.net_deposits, 1000.0)
        self.assertEqual(len(self.account.get_transactions()), 1)

    def test_deposit_funds(self):
        self.account.deposit(500.0)
        self.assertEqual(self.account.get_cash_balance(), 1500.0)
        with self.assertRaises(ValueError):
            self.account.deposit(0)
        with self.assertRaises(ValueError):
            self.account.deposit(-100)

    def test_withdraw_funds_success(self):
        self.account.withdraw(400.0)
        self.assertEqual(self.account.get_cash_balance(), 600.0)
        self.assertEqual(self.account.net_deposits, 600.0)

    def test_withdraw_funds_negative_balance_error(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(1500.0)
        with self.assertRaises(ValueError):
            self.account.withdraw(-50)
        with self.assertRaises(ValueError):
            self.account.withdraw(0)

    def test_buy_shares_success(self):
        # AAPL price is 150.0. Buy 2 shares = 300.0
        self.account.buy_shares("AAPL", 2.0)
        self.assertEqual(self.account.get_cash_balance(), 700.0)
        self.assertEqual(self.account.get_holdings(), {"AAPL": 2.0})

    def test_buy_shares_insufficient_funds(self):
        # Cash is 1000. TSLA is 200.0. Buy 6 shares = 1200.0 -> insufficient
        with self.assertRaises(ValueError):
            self.account.buy_shares("TSLA", 6.0)
        with self.assertRaises(ValueError):
            self.account.buy_shares("AAPL", -1.0)
        with self.assertRaises(ValueError):
            self.account.buy_shares("AAPL", 0.0)

    def test_sell_shares_success(self):
        self.account.buy_shares("AAPL", 4.0) # Cost 600, cash left 400
        self.assertEqual(self.account.get_cash_balance(), 400.0)
        
        self.account.sell_shares("AAPL", 2.0) # Proceeds 300, cash 700, holdings 2 AAPL
        self.assertEqual(self.account.get_cash_balance(), 700.0)
        self.assertEqual(self.account.get_holdings(), {"AAPL": 2.0})

    def test_sell_shares_exceeding_holdings(self):
        with self.assertRaises(ValueError):
            self.account.sell_shares("AAPL", 1.0)
        
        self.account.buy_shares("AAPL", 2.0)
        with self.assertRaises(ValueError):
            self.account.sell_shares("AAPL", 3.0)
        with self.assertRaises(ValueError):
            self.account.sell_shares("AAPL", -1.0)

    def test_portfolio_value_and_pnl(self):
        # Initial deposit 1000. Buy 2 AAPL (price 150 -> 300 total)
        self.account.buy_shares("AAPL", 2.0)
        # Cash = 700, Stock value = 300. Total Portfolio = 1000
        self.assertEqual(self.account.get_portfolio_value(), 1000.0)
        
        abs_pnl, pct_pnl = self.account.get_profit_loss()
        self.assertEqual(abs_pnl, 0.0)
        self.assertEqual(pct_pnl, 0.0)

        # Suppose AAPL price changes or simulate profit by selling or price lookup
        # Let's test with a mock price or custom symbol if needed, or check P&L calculation directly
        # If net deposits changes via withdrawal:
        self.account.withdraw(500.0) # net deposits now 500, cash 200, stock 300 -> portfolio 500
        abs_pnl, pct_pnl = self.account.get_profit_loss()
        self.assertEqual(abs_pnl, 0.0)

    def test_transaction_history(self):
        txs = self.account.get_transactions()
        self.assertEqual(len(txs), 1)
        self.assertEqual(txs[0].tx_type, "DEPOSIT")
        self.assertEqual(txs[0].total_amount, 1000.0)

        self.account.deposit(200.0)
        self.assertEqual(len(self.account.get_transactions()), 2)
        self.assertEqual(self.account.get_transactions()[1].tx_type, "DEPOSIT")

if __name__ == "__main__":
    unittest.main()
