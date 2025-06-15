import gradio as gr
from accounts import Accounts, get_share_price

account = Accounts(user_id="user123", initial_deposit=1000.0)

def deposit_funds(amount):
    try:
        account.deposit(amount)
        return f"Deposited {amount}. New balance: {account.balance}"
    except ValueError as e:
        return str(e)

def withdraw_funds(amount):
    try:
        account.withdraw(amount)
        return f"Withdrew {amount}. New balance: {account.balance}"
    except ValueError as e:
        return str(e)

def buy_shares(symbol, quantity):
    try:
        account.buy_shares(symbol, quantity)
        return f"Bought {quantity} shares of {symbol}. New holdings: {account.get_holdings()}"
    except ValueError as e:
        return str(e)

def sell_shares(symbol, quantity):
    try:
        account.sell_shares(symbol, quantity)
        return f"Sold {quantity} shares of {symbol}. New holdings: {account.get_holdings()}"
    except ValueError as e:
        return str(e)

def get_portfolio_info():
    return {
        "Total Portfolio Value": account.get_portfolio_value(),
        "Profit or Loss": account.get_profit_or_loss(),
        "Holdings": account.get_holdings(),
        "Transactions": account.get_transactions()
    }

with gr.Blocks() as demo:
    gr.Markdown("## Simple Trading Account Management")
    with gr.Row():
        deposit_input = gr.Number(label="Deposit Amount")
        deposit_button = gr.Button("Deposit")
        deposit_output = gr.Textbox(label="Deposit Result", interactive=False)

    with gr.Row():
        withdraw_input = gr.Number(label="Withdraw Amount")
        withdraw_button = gr.Button("Withdraw")
        withdraw_output = gr.Textbox(label="Withdraw Result", interactive=False)

    with gr.Row():
        symbol_input = gr.Textbox(label="Share Symbol (AAPL, TSLA, GOOGL)")
        buy_quantity_input = gr.Number(label="Buy Quantity")
        buy_button = gr.Button("Buy Shares")
        buy_output = gr.Textbox(label="Buy Result", interactive=False)

    with gr.Row():
        sell_quantity_input = gr.Number(label="Sell Quantity")
        sell_button = gr.Button("Sell Shares")
        sell_output = gr.Textbox(label="Sell Result", interactive=False)

    portfolio_button = gr.Button("Get Portfolio Info")
    portfolio_output = gr.Textbox(label="Portfolio Info", interactive=False)

    deposit_button.click(deposit_funds, inputs=deposit_input, outputs=deposit_output)
    withdraw_button.click(withdraw_funds, inputs=withdraw_input, outputs=withdraw_output)
    buy_button.click(buy_shares, inputs=[symbol_input, buy_quantity_input], outputs=buy_output)
    sell_button.click(sell_shares, inputs=[symbol_input, sell_quantity_input], outputs=sell_output)
    portfolio_button.click(get_portfolio_info, outputs=portfolio_output)

demo.launch(share=True)