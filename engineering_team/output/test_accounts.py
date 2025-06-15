import unittest

from accounts import Accounts, get_share_price

class TestAccounts(unittest.TestCase):

    def setUp(self):
        self.account = Accounts(user_id="user123", initial_deposit=1000.0)

    def test_initial_balance(self):
        self.assertEqual(self.account.balance, 1000.0)

    def test_deposit(self):
        self.account.deposit(500.0)
        self.assertEqual(self.account.balance, 1500.0)

    def test_withdraw(self):
        self.account.withdraw(200.0)
        self.assertEqual(self.account.balance, 800.0)

    def test_withdraw_insufficient_funds(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(1000.0)

    def test_negative_deposit(self):
        with self.assertRaises(ValueError):
            self.account.deposit(-100.0)

    def test_buy_shares(self):
        self.account.buy_shares("AAPL", 5)
        self.assertEqual(self.account.holdings["AAPL"], 5)
        self.assertEqual(self.account.balance, 1000.0 - 150.0 * 5)  # 150.0 is the price of AAPL

    def test_buy_shares_insufficient_funds(self):
        self.account.balance = 0  # Set balance to 0
        with self.assertRaises(ValueError):
            self.account.buy_shares("AAPL", 1)

    def test_sell_shares(self):
        self.account.buy_shares("AAPL", 5)
        self.account.sell_shares("AAPL", 2)
        self.assertEqual(self.account.holdings["AAPL"], 3)

    def test_sell_shares_insufficient(self):
        with self.assertRaises(ValueError):
            self.account.sell_shares("AAPL", 5)

    def test_get_portfolio_value(self):
        self.account.buy_shares("AAPL", 5)
        self.assertEqual(self.account.get_portfolio_value(), 1000.0 - 150.0 * 5 + 150.0 * 5)

    def test_get_profit_or_loss(self):
        self.account.deposit(500.0)
        self.account.buy_shares("AAPL", 5)
        self.assertEqual(self.account.get_profit_or_loss(), 500.0)

    def test_get_holdings(self):
        self.account.buy_shares("AAPL", 5)
        self.assertEqual(self.account.get_holdings(), {"AAPL": 5})

    def test_get_transactions(self):
        self.account.deposit(500.0)
        self.assertIn('Deposit: 500.0', self.account.get_transactions())

if __name__ == '__main__':
    unittest.main()