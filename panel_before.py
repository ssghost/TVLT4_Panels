import pandas as pd
import numpy as np
import plotly.figure_factory as ff
import plotly.offline as py
import plotly.graph_objs as go
import plotly.express as px
import datetime as dt
import plotly.io as pio
import datapane as dp

from symbols import *

def main() -> None:
    pio.templates.default = "ggplot2"

    data_dict = {}
    for sym in symbols:
        data = pd.read_csv("./zoom_stock_data.csv")
        data["date"] = pd.to_datetime(data["date"], format="%d/%m/%Y")
        data_dict[sym] = data
    
    fig_list = []
    for sym, data in data_dict.items:
        data["10-day MA"] = data["Close"].rolling(window=10).mean()
        data["20-day MA"] = data["Close"].rolling(window=20).mean()
        trace0 = go.Scatter(x=data.date, y=data.Close, name=sym)
        trace1 = go.Scatter(x=data.date, y=data["10-day MA"], name="10-day MA")
        trace2 = go.Scatter(x=data.date, y=data["20-day MA"], name="20-day MA")
        fig = go.Figure([trace0, trace1, trace2])
        fig.update_layout(title={"text": "{sym} Price", "x": 0.5, "xanchor": "center"})
        fig_list.append(fig)

    trace_list = []
    for sym, data in data_dict.items:
        trace = go.Scatter(x=data.date, y=data.close, name=sym)
        trace_list.append(trace)
    fig = go.Figure(trace_list)
    fig.update_layout(
        dict(
            title=dict({"text": "TVL Top4 Price Comparision", "x": 0.5, "xanchor": "center"}),
            xaxis=dict(
                rangeselector=dict(
                    buttons=list(
                        [
                            dict(count=1, label="1m", step="month", stepmode="backward"),
                            dict(count=3, label="3m", step="month", stepmode="backward"),
                            dict(count=6, label="6m", step="month", stepmode="backward"),
                            dict(count=12, label="12m", step="month", stepmode="backward"),
                        ]
                    )
                ),
                rangeslider=dict(visible=True),
                type="date",
            ),
        )
    )
    fig_list.append(fig)

    trace_list = []
    for sym, data in data_dict.items:
        trace = go.Scatterpolar(
            r=[data["close"].mean(), data["open"].mean(), data["low"].min(), data["high"].max()],
            theta=["Close", "Open", "Low", "High"],
            name=sym,
            fill="toself",
        )
        trace_list.append(trace)
    fig = go.Figure(trace_list)
    fig.update_layout(
        go.Layout(
            polar=dict(radialaxis=dict(visible=True)),
            title=dict({"text": "TVL Top4 Price Comparision (Radar Chart)", "x": 0.5, "xanchor": "center"}),
        )
    )
    fig_list.append(fig)

    eth = data_dict["ETH"][["open", "close"]]
    eth["index"] = np.arange(len(eth))
    fig_eth = go.Figure(
        ff.create_scatterplotmatrix(
            eth,
            diag="box",
            index="index",
            size=3,
            height=600,
            width=1150,
            colormap="RdBu",
            title={"text": "ETH Price (Scatterplot Matrix)", "x": 0.5, "xanchor": "center"},
        )
    )

    bignum_list = []
    for sym, data in data_dict.items:
        bignum = dp.BigNumber(
            heading="{sym} Performance",
                value="${:,.2f}".format(data.iloc[-1].close),
                prev_value="${:,.2f}".format(data.iloc[-1].open),
        )
        bignum_list.append(bignum)
    v = dp.View(
            dp.Page(
                title="Dashboard",
                blocks=[
                    dp.Group(
                        *bignum_list,
                        columns=2,
                    ),
                    dp.Group(
                        *fig_list,
                        columns=2,
                    ),
                    fig_eth,
                ],
            ),
        )

    dp.save_report(v, "report.html", open=True)

if '__name__' == '__main__':
    main()