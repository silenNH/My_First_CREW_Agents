class Accounts:
    def __init__(self, user_id: str, initial_deposit: float):
        if initial_deposit < 0:
            raise ValueError("Initial deposit cannot be negative.")
        self.user_id = user_id
        self.balance = initial_deposit
        self.initial_deposit = initial_deposit
        self.holdings = {}
        self.transactions = [f'Deposit: {initial_deposit}']

    def deposit(self, amount: float) -> None:
        if amount < 0:
            raise ValueError("Deposit amount cannot be negative.")
        self.balance += amount
        self.transactions.append(f'Deposit: {amount}')

    def withdraw(self, amount: float) -> bool:
        if amount < 0:
            raise ValueError("Withdrawal amount cannot be negative.")
        if amount > self.balance:
            raise ValueError("Insufficient funds for withdrawal.")
        self.balance -= amount
        self.transactions.append(f'Withdrawal: {amount}')
        return True

    def buy_shares(self, symbol: str, quantity: int) -> bool:
        if quantity <= 0:
            raise ValueError("Quantity must be positive.")
        total_cost = get_share_price(symbol) * quantity
        if total_cost > self.balance:
            raise ValueError("Insufficient funds to buy shares.")
        self.balance -= total_cost
        if symbol in self.holdings:
            self.holdings[symbol] += quantity
        else:
            self.holdings[symbol] = quantity
        self.transactions.append(f'Bought {quantity} shares of {symbol}')
        return True

    def sell_shares(self, symbol: str, quantity: int) -> bool:
        if quantity <= 0:
            raise ValueError("Quantity must be positive.")
        if symbol not in self.holdings or self.holdings[symbol] < quantity:
            raise ValueError("Not enough shares to sell.")
        total_sale_value = get_share_price(symbol) * quantity
        self.balance += total_sale_value
        self.holdings[symbol] -= quantity
        if self.holdings[symbol] == 0:
            del self.holdings[symbol]
        self.transactions.append(f'Sold {quantity} shares of {symbol}')
        return True

    def get_portfolio_value(self) -> float:
        total_value = self.balance
        for symbol, quantity in self.holdings.items():
            total_value += get_share_price(symbol) * quantity
        return total_value

    def get_profit_or_loss(self) -> float:
        return self.get_portfolio_value() - self.initial_deposit

    def get_holdings(self) -> dict:
        return self.holdings.copy()

    def get_transactions(self) -> list:
        return self.transactions.copy()


def get_share_price(symbol: str) -> float:
    prices = {'AAPL': 150.0, 'TSLA': 800.0, 'GOOGL': 2800.0}
    return prices.get(symbol, 0.0)

# Example Usage
if __name__ == '__main__':
    account = Accounts(user_id="user123", initial_deposit=1000.0)
    account.deposit(500.0)
    account.withdraw(200.0)
    account.buy_shares("AAPL", 5)
    print('Portfolio Value:', account.get_portfolio_value())
    print('Profit or Loss:', account.get_profit_or_loss())
    print('Holdings:', account.get_holdings())
    print('Transactions:', account.get_transactions())