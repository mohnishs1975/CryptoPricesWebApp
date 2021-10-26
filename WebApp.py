import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from binance import ThreadedWebsocketManager
import time

import cbpro

###################################################################################################################
#############BINANCE CODE##########################################################################################
prev_token = {}
token_usdt = {}

def streaming_data_process_BTC(msg):
    global token_usdt
    if "BTCUSDT" in token_usdt:
        prev_token[msg['s']] = token_usdt['BTCUSDT']
    token_usdt[msg['s']] = msg['c']

def streaming_data_process_ETH(msg):
    global token_usdt
    if "ETHUSDT" in token_usdt:
        prev_token[msg['s']] = token_usdt['ETHUSDT']
    token_usdt[msg['s']] = msg['c']

bsm = ThreadedWebsocketManager()
bsm.start()
bsm.start_symbol_ticker_socket(callback=streaming_data_process_BTC, symbol = 'BTCUSDT')
bsm.start_symbol_ticker_socket(callback=streaming_data_process_ETH, symbol = 'ETHUSDT')
time.sleep(5)

###################################################################################################
##############COINBASE CODE########################################################################
cb_prices = {}
ETH_buy = ""
BTC_buy = ""
ETH_sell = ""
BTC_sell = ""
ETH_diff = 0
BTC_diff = 0

class myWebsocketClient_BTC(cbpro.WebsocketClient):
    def on_open(self):
        self.url = "wss://ws-feed.pro.coinbase.com/"
        self.products = ["BTC-USD"]
        self.channels=["ticker"]
    def on_message(self, msg):
        if 'price' in msg and 'type' in msg:
            if "BTC-USD" in cb_prices:
                prev_token['BTC-USD'] = cb_prices['BTC-USD']
            cb_prices["BTC-USD"] = msg["price"]
            if cb_prices['BTC-USD'] < token_usdt['BTCUSDT']:
                global BTC_buy
                global BTC_sell
                global BTC_diff
                BTC_buy = "Coinbase Pro"
                BTC_sell = "Binance"
                BTC_diff = float(token_usdt['BTCUSDT']) - float(cb_prices['BTC-USD'])
            else:
                BTC_buy = "Binance"
                BTC_sell = "Coinbase Pro"
                BTC_diff = float(cb_prices['BTC-USD']) - float(token_usdt['BTCUSDT'])
    def on_close(self):
        print("Closing")

wsClient1 = myWebsocketClient_BTC()
wsClient1.start()
time.sleep(5)

class myWebsocketClient_ETH(cbpro.WebsocketClient):
    def on_open(self):
        self.url = "wss://ws-feed.pro.coinbase.com/"
        self.products = ["ETH-USD"]
        self.channels=["ticker"]
    def on_message(self, msg):
        if 'price' in msg and 'type' in msg:
            if "ETH-USD" in cb_prices:
                prev_token['ETH-USD'] = cb_prices['ETH-USD']
            cb_prices["ETH-USD"] = msg["price"]
            if cb_prices['ETH-USD'] < token_usdt['ETHUSDT']:
                global ETH_buy
                global ETH_sell
                global ETH_diff
                ETH_buy = "Coinbase Pro"
                ETH_sell = "Binance"
                ETH_diff = float(token_usdt['ETHUSDT']) - float(cb_prices['ETH-USD'])
            else:
                ETH_buy = "Binance"
                ETH_sell = "Coinbase Pro"
                ETH_diff = float(cb_prices['ETH-USD']) - float(token_usdt['ETHUSDT'])
    def on_close(self):
        print("Closing")

wsClient2 = myWebsocketClient_ETH()
wsClient2.start()
time.sleep(5)



####################################################################################################
##############APP LAYOUT############################################################################
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

app.layout = html.Div([
    html.Div([
        dcc.Tabs([
            dcc.Tab(label = 'Bitcoin', children=[
                html.Div([
                    dcc.Graph(
                        id='figure-1',
                        figure={
                            'data': [
                                go.Indicator(
                                    mode="number+delta",
                                    value=float(token_usdt['BTCUSDT']),
                                    delta={'reference': float(prev_token['BTCUSDT']), 'valueformat': "f"},
                                    number={'valueformat': 'f'},
                                )
                            ],
                            'layout':
                                go.Layout(
                                    title = {"text": "Binance<br><span style='font-size:0.8em;color:gray'>Subtitle</span><br><span style='font-size:0.8em;color:gray'>Subsubtitle</span>"},
                                )
                        }
                )],
                style={'width': '50%', 'height': '300px', 'display': 'inline-block'}),
                html.Div([
                    dcc.Graph(
                        id='figure-2',
                        figure={
                            'data': [
                                go.Indicator(
                                    mode="number+delta",
                                    value=float(cb_prices['BTC-USD']),
                                    delta={'reference': float(prev_token['BTC-USD']), 'valueformat': "f"},
                                    number={'valueformat': 'f'}
                                )
                            ],
                            'layout':
                                go.Layout(
                                    title="Coinbase Pro"
                                )
                        }
                    )],

                style={'width': '50%', 'height': '300px', 'display': 'inline-block'}),
                html.Div([
                dcc.Graph(
                    id='figure-3',
                    figure={
                        'data': [
                                go.Indicator(
                                    mode="number",
                                    value=float(BTC_diff),
                                    number={'valueformat': 'f', 'font': {'size': 20}}
                                )
                            ],
                        'layout':
                            go.Layout(
                                title="<br><br>Recommended exchange to buy Bitcoin is {} and to sell is {}.<br><br>Difference".format(BTC_buy, BTC_sell),
                            )
                    }
                )],
                style={'width': '100%', 'height': '300px', 'display': 'inline-block'}),
            ]),
            dcc.Tab(label = 'Ethereum', children=[
                html.Div([
                    dcc.Graph(
                    id='figure-4',
                    figure={
                        'data': [
                            go.Indicator(
                                mode="number+delta",
                                value=float(token_usdt['ETHUSDT']),
                                delta={'reference': float(prev_token['ETHUSDT']), 'valueformat': "f"},
                                number={'valueformat': 'f'}
                            )
                        ],
                        'layout':
                            go.Layout(
                                title="Bitcoin"
                            )
                    }
                )],
                style={'width': '50%', 'height': '300px', 'display': 'inline-block'}),
                html.Div([
                    dcc.Graph(
                        id='figure-5',
                        figure={
                            'data': [
                                go.Indicator(
                                    mode="number+delta",
                                    value=float(cb_prices['ETH-USD']),
                                    delta={'reference': float(prev_token['ETH-USD']), 'valueformat': "f"},
                                    number={'valueformat': 'f'}
                                )
                            ],
                            'layout':
                                go.Layout(
                                    title="Coinbase Pro"
                                )
                        }
                    )],

                style={'width': '50%', 'height': '300px', 'display': 'inline-block'}),
                html.Div([
                dcc.Graph(
                    id='figure-6',
                    figure={
                        'data': [
                                go.Indicator(
                                    mode="number",
                                )
                            ],
                        'layout':
                            go.Layout(
                                title="<br><br>Recommended exchange to buy Ethereum is {} and to sell is {}.".format(ETH_buy, ETH_sell),
                            )
                    }
                )],
                style={'width': '100%', 'height': '300px', 'display': 'inline-block'}),
            ]),
        ]),
        dcc.Interval(
            id='1-second-interval',
            interval=1000,  # 1000 milliseconds
            n_intervals=0
        )
    ])
])

@app.callback(Output('figure-1', 'figure'), Output('figure-2', 'figure'), Output('figure-3', 'figure'), Output('figure-4', 'figure'), Output('figure-5', 'figure'), Output('figure-6', 'figure'), Input('1-second-interval', 'n_intervals'))

def update_layout(n):
    figure1 = {
        'data': [
            go.Indicator(
                mode="number+delta",
                value=float(token_usdt['BTCUSDT']),
                delta={'reference': float(prev_token['BTCUSDT']), 'valueformat': 'f'},
                number={'valueformat': 'f'},
            )
        ],
        'layout':
            go.Layout(
                title = {"text": "Binance"},
                font_color='#FFBF00',
                font_size=26
            )
    }
    figure2 = {
        'data': [
            go.Indicator(
                mode="number+delta",
                value=float(cb_prices['BTC-USD']),
                delta={'reference': float(prev_token['BTC-USD']), 'valueformat': "f"},
                number={'valueformat': 'f'},
            )
        ],
        'layout':
            go.Layout(
                title = {"text": "Coinbase Pro"},
                font_color='navy',
                font_size=26
            )
    }
    figure3={
        'data': [
            go.Indicator(
                mode="number",
                value=float(BTC_diff),
                number={'valueformat': 'f', 'font': {'size': 50}}
            )
        ],
        'layout':
            go.Layout(
                title= "<br><br><b>Recommended<b><br><br> Buy: {}<br> Sell: {}<br><br>Difference:".format(BTC_buy, BTC_sell),
            )
    }
    figure4 = {
        'data': [
            go.Indicator(
                mode="number+delta",
                value=float(token_usdt['ETHUSDT']),
                delta={'reference': float(prev_token['ETHUSDT']), 'valueformat': "f"},
                number={'valueformat': 'f'}
            )
        ],
        'layout':
            go.Layout(
                title = {"text": "Binance"},
                font_color='#FFBF00',
                font_size=26
            )
    }
    figure5 = {
        'data': [
            go.Indicator(
                mode="number+delta",
                value=float(cb_prices['ETH-USD']),
                delta={'reference': float(prev_token['ETH-USD']), 'valueformat': "f"},
                number={'valueformat': 'f'}
            )
        ],
        'layout':
            go.Layout(
                title = "Coinbase Pro",
                font_color='navy',
                font_size=26
            )
    }
    figure6 = {
        'data': [
            go.Indicator(
                mode="number",
                value=float(ETH_diff),
                number={'valueformat': 'f', 'font': {'size': 50}}
            )
        ],
        'layout':
            go.Layout(
                title="<br><br>Recommended<br><br> Buy: {}<br> Sell: {}.<br><br>Difference:".format(ETH_buy, ETH_sell)
            )
    }
    

    return figure1, figure2, figure3, figure4, figure5, figure6

if __name__ == '__main__':
    app.run_server(debug=True)