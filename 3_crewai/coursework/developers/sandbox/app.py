import gradio as gr
from backend import Account, get_share_price

# Global active account instance in sandbox session
current_account = Account(account_id="default_user", initial_deposit=10000.0)

def format_transactions(transactions):
    data = []
    for tx in transactions:
        data.append([
            tx.transaction_id,
            tx.timestamp,
            tx.tx_type,
            tx.symbol,
            tx.quantity,
            tx.price,
            tx.total_amount
        ])
    return data

def format_holdings(holdings):
    data = []
    for sym, qty in holdings.items():
        price = get_share_price(sym)
        val = qty * price
        data.append([sym, qty, price, val])
    return data

def get_current_metrics():
    cash = current_account.get_cash_balance()
    portfolio_val = current_account.get_portfolio_value()
    abs_pnl, pct_pnl = current_account.get_profit_loss()
    holdings = format_holdings(current_account.get_holdings())
    txs = format_transactions(current_account.get_transactions())
    return cash, portfolio_val, abs_pnl, pct_pnl, holdings, txs

def ui_deposit(amount: float) -> tuple[str, float, float, float, float, list, list]:
    try:
        current_account.deposit(amount)
        msg = f"Successfully deposited ${amount:,.2f}"
    except Exception as e:
        msg = f"Error: {e}"
    cash, p_val, abs_pnl, pct_pnl, holdings, txs = get_current_metrics()
    return msg, cash, p_val, abs_pnl, pct_pnl, holdings, txs

def ui_withdraw(amount: float) -> tuple[str, float, float, float, float, list, list]:
    try:
        current_account.withdraw(amount)
        msg = f"Successfully withdrew ${amount:,.2f}"
    except Exception as e:
        msg = f"Error: {e}"
    cash, p_val, abs_pnl, pct_pnl, holdings, txs = get_current_metrics()
    return msg, cash, p_val, abs_pnl, pct_pnl, holdings, txs

def ui_buy(symbol: str, quantity: float) -> tuple[str, float, float, float, float, list, list]:
    try:
        current_account.buy_shares(symbol, quantity)
        msg = f"Successfully bought {quantity} shares of {symbol.upper()}"
    except Exception as e:
        msg = f"Error: {e}"
    cash, p_val, abs_pnl, pct_pnl, holdings, txs = get_current_metrics()
    return msg, cash, p_val, abs_pnl, pct_pnl, holdings, txs

def ui_sell(symbol: str, quantity: float) -> tuple[str, float, float, float, float, list, list]:
    try:
        current_account.sell_shares(symbol, quantity)
        msg = f"Successfully sold {quantity} shares of {symbol.upper()}"
    except Exception as e:
        msg = f"Error: {e}"
    cash, p_val, abs_pnl, pct_pnl, holdings, txs = get_current_metrics()
    return msg, cash, p_val, abs_pnl, pct_pnl, holdings, txs

def ui_refresh_status() -> tuple[float, float, float, float, list, list]:
    return get_current_metrics()

def create_demo() -> gr.Blocks:
    with gr.Blocks(title="Trading Simulation Account Management") as demo:
        gr.Markdown("# 📈 Trading Simulation Account Management System")
        gr.Markdown("Manage your account cash, trade stocks (**AAPL**, **TSLA**, **GOOGL**), track portfolio value, and view transaction history.")

        with gr.Row():
            with gr.Column():
                cash_box = gr.Number(label="Cash Balance ($)", value=current_account.get_cash_balance(), interactive=False)
                portfolio_box = gr.Number(label="Total Portfolio Value ($)", value=current_account.get_portfolio_value(), interactive=False)
            with gr.Column():
                pnl_abs_box = gr.Number(label="Profit / Loss ($)", value=current_account.get_profit_loss()[0], interactive=False)
                pnl_pct_box = gr.Number(label="Profit / Loss (%)", value=current_account.get_profit_loss()[1], interactive=False)

        status_msg = gr.Textbox(label="System Status / Messages", value="System ready.", interactive=False)

        with gr.Tabs():
            with gr.TabItem("Cash Operations"):
                with gr.Row():
                    with gr.Column():
                        gr.Markdown("### Deposit Funds")
                        dep_input = gr.Number(label="Deposit Amount ($)", value=1000.0, minimum=0.01)
                        dep_btn = gr.Button("Deposit", variant="primary")
                    with gr.Column():
                        gr.Markdown("### Withdraw Funds")
                        with_input = gr.Number(label="Withdrawal Amount ($)", value=1000.0, minimum=0.01)
                        with_btn = gr.Button("Withdraw", variant="stop")

            with gr.TabItem("Trading Operations"):
                with gr.Row():
                    with gr.Column():
                        gr.Markdown("### Buy Shares")
                        buy_symbol = gr.Dropdown(choices=["AAPL", "TSLA", "GOOGL"], value="AAPL", label="Ticker Symbol")
                        buy_qty = gr.Number(label="Quantity", value=1.0, minimum=0.01)
                        buy_btn = gr.Button("Buy Shares", variant="primary")
                    with gr.Column():
                        gr.Markdown("### Sell Shares")
                        sell_symbol = gr.Dropdown(choices=["AAPL", "TSLA", "GOOGL"], value="AAPL", label="Ticker Symbol")
                        sell_qty = gr.Number(label="Quantity", value=1.0, minimum=0.01)
                        sell_btn = gr.Button("Sell Shares", variant="stop")

            with gr.TabItem("Holdings & Reports"):
                gr.Markdown("### Current Share Holdings")
                initial_holdings_data = format_holdings(current_account.get_holdings())
                holdings_table = gr.Dataframe(
                    headers=["Symbol", "Quantity", "Current Price ($)", "Market Value ($)"],
                    value=initial_holdings_data,
                    interactive=False
                )

                gr.Markdown("### Transaction History")
                initial_tx_data = format_transactions(current_account.get_transactions())
                tx_table = gr.Dataframe(
                    headers=["Tx ID", "Timestamp", "Type", "Symbol", "Quantity", "Price ($)", "Total Amount ($)"],
                    value=initial_tx_data,
                    interactive=False
                )
                refresh_btn = gr.Button("Refresh Reports")

        # Event wiring
        metrics_outputs = [cash_box, portfolio_box, pnl_abs_box, pnl_pct_box, holdings_table, tx_table]

        dep_btn.click(
            fn=ui_deposit,
            inputs=[dep_input],
            outputs=[status_msg] + metrics_outputs
        )

        with_btn.click(
            fn=ui_withdraw,
            inputs=[with_input],
            outputs=[status_msg] + metrics_outputs
        )

        buy_btn.click(
            fn=ui_buy,
            inputs=[buy_symbol, buy_qty],
            outputs=[status_msg] + metrics_outputs
        )

        sell_btn.click(
            fn=ui_sell,
            inputs=[sell_symbol, sell_qty],
            outputs=[status_msg] + metrics_outputs
        )

        refresh_btn.click(
            fn=ui_refresh_status,
            outputs=metrics_outputs
        )

    return demo

if __name__ == "__main__":
    demo = create_demo()
    demo.launch(server_name="0.0.0.0", server_port=7860)
