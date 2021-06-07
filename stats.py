def performance(bdf, sdf):
    """
    Analyze performance of a strategy given the buy/sel dataframes
    :param bdf:
    :param sdf:
    :return:
    """

    import pandas as pd
    from numpy import nan

    if len(bdf) == 0:
        p = [[1, nan, nan, 0, nan, 0, nan, 0]]
        p_df = pd.DataFrame(p, columns=[
            'G', 't', 'Gt', 'N',
            'good_g', 'good_n', 'bad_g', 'bad_n',
        ])
        return p_df

    gain_y = [sdf['Sel'][i] / bdf['Buy'][i] for i in range(len(bdf['Buy']))]
    gain_t = [(sdf['Time'][i] - bdf['Time'][i]) * (1/1000) * (1/60)**2 for i in range(len(bdf['Time']))]

    gain_y = [i * 0.999 ** 2 for i in gain_y]

    gain_df = pd.DataFrame(gain_y, columns=['G'])
    mask = gain_df['G'] >= 1
    good = gain_df[mask]
    good_g = good['G'].mean()
    good_n = len(good)
    bad = gain_df[mask == False]
    bad_g = bad['G'].mean()
    bad_n = len(bad)

    g = sum(gain_y) / len(gain_y)
    t = sum(gain_t) / len(gain_t)
    gt = (g ** (1 / t) - 1)
    t = round(t, 2)
    n = len(bdf)

    p = [[g, t, gt, n, good_g, good_n, bad_g, bad_n]]
    p_df = pd.DataFrame(p, columns=[
        'G', 't', 'Gt', 'N',
        'good_g', 'good_n', 'bad_g', 'bad_n',
    ])
    return p_df


def graphit(candles, bdf, sdf, emas):
    """
    Graph Close prices, emas, and buy and sell points
    :param candles: candles dataframe
    :param bdf: buy dataframe
    :param sdf: sell dataframe
    :param emas: list of ema spans
    :return:
    """

    import plotly.graph_objects as go

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=candles['Open time'], y=candles['Close'], name='Close'))

    for i in emas:
        ema_i = candles['Close'].ewm(span=i).mean()
        name_i = 'ema' + str(i)
        fig.add_trace(go.Scatter(x=candles['Open time'], y=ema_i, name=name_i))

    fig.add_trace(go.Scatter(x=bdf['Time'], y=bdf['Buy'], mode='markers', name='Buy'))
    fig.add_trace(go.Scatter(x=sdf['Time'], y=sdf['Sel'], mode='markers', name='Sell'))

    return fig
