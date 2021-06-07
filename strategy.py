def s101(df, trading, lists):
    """
    ema50 bounce off of ema100.
    Linear regression.
    """

    import numpy as np
    from sklearn.linear_model import LinearRegression

    buy_l = lists['buy_l']
    sel_l = lists['sel_l']

    # Span multiplier
    m = 4

    # data not sufficient, return
    w = 144 * m
    if len(df) < w:
        return [trading, lists]
    else:
        df = df[-w:]

    close = df['Close'].iloc

    # Exponential moving average
    ema50 = df[-48 * m:]['Close'].ewm(span=48).mean().iloc
    ema100 = df[-96 * m:]['Close'].ewm(span=96).mean().iloc
    ema150 = df[-144 * m:]['Close'].ewm(span=144).mean().iloc

    # Linear regression
    x = list(df.index[-12*8:])
    x = np.array(list(x)).reshape((-1, 1))
    # EMA50
    model50 = LinearRegression()
    model50.fit(x, ema50[-12*8:])
    coef50 = model50.coef_
    # EMA100
    model100 = LinearRegression()
    model100.fit(x, ema100[-12*8:])
    coef100 = model100.coef_
    # EMA150
    model150 = LinearRegression()
    model150.fit(x, ema150[-12*8:])
    coef150 = model150.coef_

    if not trading:
        c1 = (ema50[-1] > ema100[-1]) & (ema100[-1] > ema150[-1])
        c2 = (coef50 >= 0.5) & (coef100 >= 0.25) & (coef150 >= 0.25)
        c = c1 & c2
        if c:
            c1 = close[-1] > 1.001 * ema100[-1]
            c2 = close[-2] < 1.001 * ema100[-2]
            c3 = close[-2] > 0.999 * ema100[-2]
            c4 = close[-3] > ema100[-3]
            c5 = close[-4] > ema100[-4]
            c = c1 & c2 & c3 & c4 & c5
            if c:
                buy_time = df['Open time'].iloc[-1]
                buy_price = df['Close'].iloc[-1]
                buy = [buy_time, buy_price]
                buy_l.append(buy)
                trading = True
                lists = {'buy_l': buy_l, 'sel_l': sel_l}
        return [trading, lists]
    if trading:
        c1 = close[-1] / buy_l[-1][1] < 0.994
        c2 = close[-1] / buy_l[-1][1] > 1.02
        if c1 or c2:
            sel_time = df['Open time'].iloc[-1]
            sel_price = df['Close'].iloc[-1]
            sell = [sel_time, sel_price]
            sel_l.append(sell)
            trading = False
            lists = {'buy_l': buy_l, 'sel_l': sel_l}
        return [trading, lists]


def s102(df, trading, lists, emas):
    """
    ema48 bounce off of ema96.
    Linear regression.
    emas are calculated once in bt102 and passed in lists
    """

    import numpy as np
    from sklearn.linear_model import LinearRegression

    buy_l = lists['buy_l']
    sel_l = lists['sel_l']

    # data not sufficient, return
    w = 12*8
    if len(df) < w:
        return [trading, lists]
    else:
        df = df[-w:]

    close = df['Close'].iloc

    # Exponential moving average
    ema48 = emas['ema48'].iloc
    ema96 = emas['ema96'].iloc
    ema144 = emas['ema144'].iloc
    trend = emas['trend']

    # Linear regression
    x = list(df.index[-12*8:])
    x = np.array(list(x)).reshape((-1, 1))
    # EMA48
    model48 = LinearRegression()
    model48.fit(x, ema48[-12*8:])
    coef48 = model48.coef_
    # EMA96
    model96 = LinearRegression()
    model96.fit(x, ema96[-12*8:])
    coef96 = model96.coef_
    # EMA144
    model144 = LinearRegression()
    model144.fit(x, ema144[-12*8:])
    coef144 = model144.coef_

    if not trading:
        c1 = (ema48[-1] > ema96[-1]) & (ema96[-1] > ema144[-1])
        c2 = (coef48 > 0.5) & (coef96 > 0.25) & (coef144 > 0.25)
        c3 = trend[-1] >= 0.4
        c = c1 & c2 & c3
        if c:
            c1 = close[-1] > 1.001 * ema96[-1]
            c2 = close[-2] < 1.001 * ema96[-2]
            c3 = close[-2] > 0.999 * ema96[-2]
            c4 = close[-3] > ema96[-3]
            c5 = close[-4] > ema96[-4]
            c = c1 & c2 & c3 & c4 & c5
            if c:
                buy_time = df['Open time'].iloc[-1]
                buy_price = df['Close'].iloc[-1]
                buy = [buy_time, buy_price]
                buy_l.append(buy)
                trading = True
                lists = {'buy_l': buy_l, 'sel_l': sel_l}
        return [trading, lists]
    if trading:
        c1 = close[-1] / buy_l[-1][1] < 0.994
        c2 = close[-1] / buy_l[-1][1] > 1.02
        if c1 or c2:
            sel_time = df['Open time'].iloc[-1]
            sel_price = df['Close'].iloc[-1]
            sell = [sel_time, sel_price]
            sel_l.append(sell)
            trading = False
            lists = {'buy_l': buy_l, 'sel_l': sel_l}
        return [trading, lists]


def s102t(df, trading, lists, emas):
    """
    ema48 bounce off of ema96.
    Linear regression.
    emas are calculated once in bt102 and passed in lists
    """

    import numpy as np
    from sklearn.linear_model import LinearRegression

    buy_l = lists['buy_l']
    sel_l = lists['sel_l']

    # data not sufficient, return
    w = 12 * 8
    if len(df) < w:
        return [trading, lists]
    else:
        df = df[-w:]

    close = df['Close'].iloc

    # Exponential moving average
    ema48 = emas['ema48'].iloc
    ema96 = emas['ema96'].iloc
    ema144 = emas['ema144'].iloc
    trend = emas['trend']

    # Linear regression
    x = list(df.index[-12 * 8:])
    x = np.array(list(x)).reshape((-1, 1))
    # EMA48
    model48 = LinearRegression()
    model48.fit(x, ema48[-12 * 8:])
    coef48 = model48.coef_
    # EMA96
    model96 = LinearRegression()
    model96.fit(x, ema96[-12 * 8:])
    coef96 = model96.coef_
    # EMA144
    model144 = LinearRegression()
    model144.fit(x, ema144[-12 * 8:])
    coef144 = model144.coef_

    # Append
    lists['coef48'].append(coef48)
    lists['coef96'].append(coef96)
    lists['coef144'].append(coef144)

    if not trading:
        c1 = (ema48[-1] > ema96[-1]) & (ema96[-1] > ema144[-1])
        c2 = (coef48 > 0.5) & (coef96 > 0.25) & (coef144 > 0.25)
        c3 = trend[-1] >= 0.4
        c = c1 & c2 & c3
        if c:
            c1 = close[-1] > 1.001 * ema96[-1]
            c2 = close[-2] < 1.001 * ema96[-2]
            c3 = close[-2] > 0.999 * ema96[-2]
            c4 = close[-3] > ema96[-3]
            c5 = close[-4] > ema96[-4]
            c = c1 & c2 & c3 & c4 & c5
            if c:
                buy_time = df['Open time'].iloc[-1]
                buy_price = df['Close'].iloc[-1]
                buy = [buy_time, buy_price]
                buy_l.append(buy)
                trading = True
                lists = {'buy_l': buy_l, 'sel_l': sel_l}
        return [trading, lists]
    if trading:
        c1 = close[-1] / buy_l[-1][1] < 0.994
        c2 = close[-1] / buy_l[-1][1] > 1.02
        if c1 or c2:
            sel_time = df['Open time'].iloc[-1]
            sel_price = df['Close'].iloc[-1]
            sell = [sel_time, sel_price]
            sel_l.append(sell)
            trading = False
            lists = {'buy_l': buy_l, 'sel_l': sel_l}
        return [trading, lists]


def s103(df, trading, lists, emas):
    """
    ema48 bounce off of ema96.
    Linear regression.
    emas are calculated once in bt102 and passed in lists
    Relative values with std
    """

    import numpy as np
    from sklearn.linear_model import LinearRegression

    buy_l = lists['buy_l']

    # data not sufficient, return
    w = 12 * 8
    if len(df) < w:
        return [trading, lists]
    else:
        df = df[-w:]

    close = df['Close'].iloc

    # Exponential moving average
    ema48 = emas['ema48'].iloc
    ema96 = emas['ema96'].iloc
    ema144 = emas['ema144'].iloc
    trend = emas['trend']

    # Linear regression
    x = list(df.index[-12 * 8:])
    x = np.array(list(x)).reshape((-1, 1))
    # EMA48
    model48 = LinearRegression()
    model48.fit(x, ema48[-12 * 8:])
    coef48 = model48.coef_[0]
    # EMA96
    model96 = LinearRegression()
    model96.fit(x, ema96[-12 * 8:])
    coef96 = model96.coef_[0]
    # EMA144
    model144 = LinearRegression()
    model144.fit(x, ema144[-12 * 8:])
    coef144 = model144.coef_[0]

    # Append
    lists['coef144'].append(coef144)

    # Relative part
    if len(lists['coef144']) >= 1440:
        if len(lists['coef144']) < 1440*6:
            l144 = np.array(lists['coef144'])
            c144 = l144.std()
            p = np.array(trend).std()
        else:
            l144 = np.array(lists['coef144'][-1440*6:])
            c144 = l144.std()
            p = np.array(trend).std()
    else:
        return [trading, lists]

    if not trading:
        c1 = (ema48[-1] > ema96[-1]) & (ema96[-1] > ema144[-1])
        c2 = (coef48 > c144) & (coef96 > 0.5*c144) & (coef144 > 0.5*c144)
        c3 = c144 > 0
        c4 = (trend[-1] >= 2*p) & (p > 0)
        c = c1 & c2 & c3 & c4
        if c:
            c1 = close[-1] > (1 + 0.001) * ema96[-1]
            c2 = close[-2] < (1 + 0.001) * ema96[-2]
            c3 = close[-2] > (1 - 0.001) * ema96[-2]
            c4 = close[-3] > ema96[-3]
            c5 = close[-4] > ema96[-4]
            c = c1 & c2 & c3 & c4 & c5
            if c:
                buy_time = df['Open time'].iloc[-1]
                buy_price = df['Close'].iloc[-1]
                buy = [buy_time, buy_price]
                lists['buy_l'].append(buy)
                trading = True
        return [trading, lists]
    if trading:
        buy_time = buy_l[-1][0]
        open_time = df['Open time'].iloc[-1]
        if open_time - buy_time > 4 * 60*60*1000:
            c1 = close[-1] / buy_l[-1][1] > 1 + 0.006
            c2 = close[-1] / buy_l[-1][1] < 1 - 0.006
        else:
            c1 = close[-1] / buy_l[-1][1] > 1 + 0.015
            c2 = close[-1] / buy_l[-1][1] < 1 - 0.015
        if c1 or c2:
            sel_time = df['Open time'].iloc[-1]
            sel_price = df['Close'].iloc[-1]
            sell = [sel_time, sel_price]
            lists['sel_l'].append(sell)
            trading = False
        return [trading, lists]


def s104(df, trading, lists, emas):
    """
    ema48 bounce off of ema96.
    Linear regression.
    emas are calculated once in bt102 and passed in lists
    Relative values with std
    This one is to tinker with
    """

    import numpy as np
    from sklearn.linear_model import LinearRegression

    buy_l = lists['buy_l']

    # data not sufficient, return
    w = 12 * 8
    if len(df) < w:
        return [trading, lists]
    else:
        df = df[-w:]

    close = df['Close'].iloc

    # Exponential moving average
    ema48 = emas['ema48'].iloc
    ema96 = emas['ema96'].iloc
    ema144 = emas['ema144'].iloc
    trend = emas['trend']

    # Linear regression
    x = list(df.index[-12 * 8:])
    x = np.array(list(x)).reshape((-1, 1))
    # EMA48
    model48 = LinearRegression()
    model48.fit(x, ema48[-12 * 8:])
    coef48 = model48.coef_[0]
    # EMA96
    model96 = LinearRegression()
    model96.fit(x, ema96[-12 * 8:])
    coef96 = model96.coef_[0]
    # EMA144
    model144 = LinearRegression()
    model144.fit(x, ema144[-12 * 8:])
    coef144 = model144.coef_[0]

    # Append
    lists['coef144'].append(coef144)

    # Relative part
    if len(lists['coef144']) >= 1440:
        if len(lists['coef144']) < 1440*6:
            l144 = np.array(lists['coef144'])
            c144 = l144.std()
            p = np.array(trend).std()
        else:
            l144 = np.array(lists['coef144'][-1440*6:])
            c144 = l144.std()
            p = np.array(trend).std()
    else:
        return [trading, lists]

    # print(c144)

    if not trading:
        c1 = (ema48[-1] > ema96[-1]) & (ema96[-1] > ema144[-1])
        c2 = (coef48 > c144) & (coef96 > 0.5*c144) & (coef144 > 0.5*c144)
        c3 = c144 > 0
        c4 = (trend[-1] >= 2*p) & (p > 0)
        c = c1 & c2 & c3 & c4
        if c:
            c1 = close[-1] > (1 + 0.001) * ema96[-1]
            c2 = close[-2] < (1 + 0.001) * ema96[-2]
            c3 = close[-2] > (1 - 0.001) * ema96[-2]
            c4 = close[-3] > ema96[-3]
            c5 = close[-4] > ema96[-4]
            c = c1 & c2 & c3 & c4 & c5
            if c:
                buy_time = df['Open time'].iloc[-1]
                buy_price = df['Close'].iloc[-1]
                buy = [buy_time, buy_price]
                lists['buy_l'].append(buy)
                trading = True
        return [trading, lists]
    if trading:
        buy_time = buy_l[-1][0]
        open_time = df['Open time'].iloc[-1]
        if open_time - buy_time > 4 * 60*60*1000:
            c1 = close[-1] / buy_l[-1][1] > 1 + 0.006
            c2 = close[-1] / buy_l[-1][1] < 1 - 0.006
        else:
            c1 = close[-1] / buy_l[-1][1] > 1 + 0.02
            c2 = close[-1] / buy_l[-1][1] < 1 - 0.01
        if c1 or c2:
            sel_time = df['Open time'].iloc[-1]
            sel_price = df['Close'].iloc[-1]
            sell = [sel_time, sel_price]
            lists['sel_l'].append(sell)
            trading = False
        return [trading, lists]


def s201(df, trading, lists):
    """
    Buy when ema5 goes over max of window and last max wasn't too close.
    Sell when 0.997 under buy or when emas start to decrease and over buy
    :param df:
    :param trading:
    :param lists: {'buy_l': [], 'sel_l': [], 'peak_l': []}
    :return:
    """

    buy_l = lists['buy_l']
    sel_l = lists['sel_l']
    peak_l = lists['peak_l']

    # window not sufficient, return
    if len(df['Close']) < 360:
        lists = {'buy_l': buy_l, 'sel_l': sel_l, 'peak_l': peak_l}
        return [trading, lists]

    # ema5 and max of window
    ema5 = df['Close'].ewm(span=5).mean()
    window = ema5.iloc[-360:-1]
    peak = max(window)
    peak_l.append(peak)

    if not trading:
        c1 = peak != max(peak_l[-48:])
        c2 = ema5.iloc[-1] > 1.0014 * peak
        if c1 and c2:
            buy_time = df['Open time'].iloc[-1]
            buy_price = df['Close'].iloc[-1]
            buy = [buy_time, buy_price]
            buy_l.append(buy)
            trading = True
            lists = {'buy_l': buy_l, 'sel_l': sel_l, 'peak_l': peak_l}
            return [trading, lists]
    if trading:
        c1 = ema5.iloc[-1] < 0.997 * buy_l[-1][1]
        ema8 = df['Close'].ewm(span=8).mean()
        ema13 = df['Close'].ewm(span=13).mean()
        c2 = ema13.iloc[-2] - ema8.iloc[-2] > ema13.iloc[-1] - ema8.iloc[-1]
        c3 = ema8.iloc[-2] > ema8.iloc[-1]
        if c1 or (c2 and c3):
            sel_time = df['Open time'].iloc[-1]
            sel_price = df['Close'].iloc[-1]
            sell = [sel_time, sel_price]
            sel_l.append(sell)
            trading = False
            lists = {'buy_l': buy_l, 'sel_l': sel_l, 'peak_l': peak_l}
            return [trading, lists]

    lists = {'buy_l': buy_l, 'sel_l': sel_l, 'peak_l': peak_l}
    return [trading, lists]


def s301(df, trading, lists):
    """"""

    buy_l = lists['buy_l']
    sel_l = lists['sel_l']
    peak = lists['peak']
    over = lists['over']

    # window not sufficient, return
    if len(df['Close']) < 288:
        lists = {'buy_l': buy_l, 'sel_l': sel_l, 'peak_l': peak_l}
        return [trading, lists]

    # ema5 and max of window
    ema5 = df['Close'].ewm(span=5).mean()
    window = ema5.iloc[-288:-1]
    peak = max(window)
    peak_l.append(peak)

    if not trading:
        if not over:
            c = ema5.iloc[-1] > 1.0014 * peak
            if c:
                buy_time = df['Open time'].iloc[-1]
                buy_price = df['Close'].iloc[-1]
                buy = [buy_time, buy_price]
                buy_l.append(buy)
                trading = True
                lists = {'buy_l': buy_l, 'sel_l': sel_l, 'peak_l': peak_l}
                return [trading, lists]
    if trading:
        c1 = ema5.iloc[-1] < 0.997 * buy_l[-1][1]
        ema8 = df['Close'].ewm(span=8).mean()
        ema13 = df['Close'].ewm(span=13).mean()
        c2 = ema13.iloc[-2] - ema8.iloc[-2] > ema13.iloc[-1] - ema8.iloc[-1]
        c3 = ema8.iloc[-2] > ema8.iloc[-1]
        if c1 or (c2 and c3):
            sel_time = df['Open time'].iloc[-1]
            sel_price = df['Close'].iloc[-1]
            sell = [sel_time, sel_price]
            sel_l.append(sell)
            trading = False
            lists = {'buy_l': buy_l, 'sel_l': sel_l, 'peak_l': peak_l}
            return [trading, lists]

    lists = {'buy_l': buy_l, 'sel_l': sel_l, 'peak_l': peak_l}
    return [trading, lists]






