import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from binance.client import Client
from binance import ThreadedWebsocketManager
import configparser
from binance.client import Client
import time

import cbpro, time

###################################################################################################################
#############BINANCE CODE##########################################################################################
prev_token = {}
token_usdt = {}

def streaming_data_process_BTC(msg):
    global token_usdt
    if "BTCUSDT" in token_usdt:
        prev_token[msg['s']] = float(token_usdt['BTCUSDT'])
    token_usdt[msg['s']] = msg['c']

def streaming_data_process_ETH(msg):
    global token_usdt
    if "ETHUSDT" in token_usdt:
        prev_token[msg['s']] = float(token_usdt['ETHUSDT'])
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

class myWebsocketClient_BTC(cbpro.WebsocketClient):
    def on_open(self):
        self.url = "wss://ws-feed.pro.coinbase.com/"
        self.products = ["BTC-USD"]
        self.channels=["ticker"]
    def on_message(self, msg):
        if 'price' in msg and 'type' in msg:
            cb_prices["BTC-USD"] = msg["price"]
            if cb_prices['BTC-USD'] < token_usdt['BTCUSDT']:
                global BTC_buy
                global BTC_sell
                BTC_buy = "Coinbase Pro"
                BTC_sell = "Binance"
            else:
                BTC_buy = "Binance"
                BTC_sell = "Coinbase Pro"
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
            cb_prices["ETH-USD"] = msg["price"]
            if cb_prices['ETH-USD'] < token_usdt['ETHUSDT']:
                global ETH_buy
                global ETH_sell
                ETH_buy = "Coinbase Pro"
                ETH_sell = "Binance"
            else:
                ETH_buy = "Binance"
                ETH_sell = "Coinbase Pro"
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
                                    mode="number",
                                    value=float(token_usdt['BTCUSDT']),
                                    number={'valueformat': 'g'},
                                )
                            ],
                            'layout':
                                go.Layout(
                                    title="Binance"
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
                                    mode="number",
                                    value=float(cb_prices['BTC-USD']),
                                    number={'valueformat': 'g'}
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
                                )
                            ],
                        'layout':
                            go.Layout(
                                title="<br><br>Recommended exchange to buy Bitcoin is <font color=""green"">{}</font> and to sell is {}.".format(BTC_buy, BTC_sell),
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
                                mode="number",
                                value=float(token_usdt['ETHUSDT']),
                                number={'valueformat': 'g'}
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
                                    mode="number",
                                    value=float(cb_prices['ETH-USD']),
                                    number={'valueformat': 'g'}
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
                mode="number",
                value=float(token_usdt['BTCUSDT']),
                number={'valueformat': 'g'}
            )
        ],
        'layout':
            go.Layout(
                title="Binance"
            )
    }
    figure2 = {
        'data': [
            go.Indicator(
                mode="number",
                value=float(cb_prices['BTC-USD']),
                number={'valueformat': 'g'}
            )
        ],
        'layout':
            go.Layout(
                title="Coinbase Pro"
            )
    }
    figure3 = {
        'data': [
            go.Indicator(
                mode="number",
            )
        ],
        'layout':
            go.Layout(
                title="<br><br>Recommended exchange to buy Bitcoin is {} and to sell is {}.".format(BTC_buy, BTC_sell)
            )
    }
    figure4 = {
        'data': [
            go.Indicator(
                mode="number",
                value=float(token_usdt['ETHUSDT']),
                number={'valueformat': 'g'}
            )
        ],
        'layout':
            go.Layout(
                title="Binance"
            )
    }
    figure5 = {
        'data': [
            go.Indicator(
                mode="number",
                value=float(cb_prices['ETH-USD']),
                number={'valueformat': 'g'}
            )
        ],
        'layout':
            go.Layout(
                title="Coinbase Pro"
            )
    }
    figure6 = {
        'data': [
            go.Indicator(
                mode="number",
            )
        ],
        'layout':
            go.Layout(
                title="<br><br>Recommended exchange to buy Ethereum is {} and to sell is {}.".format(ETH_buy, ETH_sell)
            )
    }
    

    return figure1, figure2, figure3, figure4, figure5, figure6

if __name__ == '__main__':
    app.run_server(debug=True)