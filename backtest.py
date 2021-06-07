def bt(y0, m0, days, symbol, snum, lists, w=500, check_db=True):
    """
    Performs backtest for specified strategy over specified time.
    Returns buy dataframe and sell dataframe.
    :param y0: start year
    :param m0: start month
    :param days: number of days
    :param symbol: trading pair symbol
    :param snum: strategy function name
    :param lists: dict of strategy function input lists
    :param w: candle window
    :param check_db: Get candle data from api call or database
    :return: [buy pandas df, sell pandas df]
    """

    from database import get_database
    from api_calls import klines
    import importlib
    from tqdm import tqdm
    import pandas as pd

    # Collect candle data
    if check_db:
        candles = get_database(y0, m0, days, symbol)
    else:
        candles = klines(y0, m0, days, symbol)

    # Import strategy
    smod = importlib.import_module('strategy')
    strat = getattr(smod, snum)

    # Trade!
    tr = False
    print('Trading...')
    for i in tqdm(range(len(candles))):
        if i < w:
            ci = candles[0: i]
        else:
            ci = candles[i - w: i]

        tr, lists = strat(ci, tr, lists)

    # In case backtest finished on open trade
    if tr:
        lists['buy_l'].pop(-1)

    # Convert to pandas dataframe
    buy_df = pd.DataFrame(lists['buy_l'], columns=['Time', 'Buy'])
    buy_df['Symbol'] = symbol
    sel_df = pd.DataFrame(lists['sel_l'], columns=['Time', 'Sel'])
    sel_df['Symbol'] = symbol

    print('Done trading.')
    return [candles, buy_df, sel_df]


def bts(y0, m0, days, symbols, snum, lists, w=500, check_db=True):
    """
    Performs bt() for list or .csv of trading pair symbols.
    :param y0: start year
    :param m0: start month
    :param days: number of days
    :param symbols: list or .csv of trading pair symbols
    :param snum: strategy function name
    :param lists: dict of strategy function input lists
    :param w: candle window
    :param check_db: Get candle data from api call or database
    :return: [candles_list, bdf_list, sdf_list]
    """

    import csv
    from tqdm import tqdm
    import os
    import sys

    class HiddenPrints:
        def __enter__(self):
            self._original_stdout = sys.stdout
            self._original_stderr = sys.stderr
            sys.stdout = open(os.devnull, 'w')
            sys.stderr = open(os.devnull, 'w')

        def __exit__(self, exc_type, exc_val, exc_tb):
            sys.stdout.close()
            sys.stderr.close()
            sys.stdout = self._original_stdout
            sys.stderr = self._original_stderr

    # Check if symbols is a .csv file
    if isinstance(symbols, str):
        if symbols.endswith('.csv'):
            with open(symbols, newline='') as f:
                reader = csv.reader(f)
                symbols = list(reader)[0]

    candles_list = []
    bdf_list = []
    sdf_list = []
    for sym in tqdm(symbols):

        # Backtest
        with HiddenPrints():
            candles, bdf, sdf = bt(y0, m0, days, sym, snum, lists, w, check_db)

        # Append to list
        candles_list.append(candles)
        bdf_list.append(bdf)
        sdf_list.append(sdf)

    return [candles_list, bdf_list, sdf_list]


def bt1(y0, m0, days, symbol, lists, check_db=True):
    """
    Performs backtest for specified strategy 103, calculating emas and trend once.
    Returns buy dataframe and sell dataframe.
    :param y0: start year
    :param m0: start month
    :param days: number of days
    :param symbol: trading pair symbol
    :param lists: dict of strategy function input lists
    :param check_db: Get candle data from api call or database
    :return: [buy pandas df, sell pandas df]
    """

    from database import get_database
    from api_calls import klines
    from tqdm import tqdm
    import pandas as pd
    import numpy as np
    from strategy import s103 as s

    # Collect candle data
    if check_db:
        candles = get_database(y0, m0, days, symbol)
    else:
        candles = klines(y0, m0, days, symbol)

    # ema and trend
    ema48 = candles['Close'].ewm(span=48).mean()
    ema96 = candles['Close'].ewm(span=96).mean()
    ema144 = candles['Close'].ewm(span=144).mean()
    trend = np.diff(candles['Close'].ewm(span=1440).mean())

    # Trade!
    tr = False
    w = 12*8
    emas = {}
    print('Trading...')
    for i in tqdm(range(len(candles))):
        if i < w:
            continue
        else:
            ci = candles[i - w: i]
            emas['ema48'] = ema48[i - w: i]
            emas['ema96'] = ema96[i - w: i]
            emas['ema144'] = ema144[i - w: i]
            emas['trend'] = trend[i - w: i]

        tr, lists = s(ci, tr, lists, emas)

    # In case backtest finished on open trade
    if tr:
        lists['buy_l'].pop(-1)

    # Convert to pandas dataframe
    buy_df = pd.DataFrame(lists['buy_l'], columns=['Time', 'Buy'])
    buy_df['Symbol'] = symbol
    sel_df = pd.DataFrame(lists['sel_l'], columns=['Time', 'Sel'])
    sel_df['Symbol'] = symbol

    print('Done trading.')
    return [candles, buy_df, sel_df]


def bt_data(y0, m0, days, symbol, check_db=True):
    """"""

    from database import get_database
    from api_calls import klines
    from tqdm import tqdm
    import numpy as np
    from sklearn.linear_model import LinearRegression

    # Collect candle data
    if check_db:
        candles = get_database(y0, m0, days, symbol)
    else:
        candles = klines(y0, m0, days, symbol)

    # ema and trend
    ema48 = candles['Close'].ewm(span=48).mean()
    ema96 = candles['Close'].ewm(span=96).mean()
    ema144 = candles['Close'].ewm(span=144).mean()
    trend = np.diff(candles['Close'].ewm(span=1440).mean())

    # Get data
    w = 12*8
    coef48_l = []
    coef96_l = []
    coef144_l = []
    print('Collecting data...')
    for i in tqdm(range(len(candles))):
        if i < w:
            continue
        else:
            ci = candles[i - w: i]
            ema48i = ema48[i - w: i].iloc
            ema96i = ema96[i - w: i].iloc
            ema144i = ema144[i - w: i].iloc

            # Linear regression
            x = list(ci.index[-12 * 8:])
            x = np.array(list(x)).reshape((-1, 1))
            # EMA48
            model48 = LinearRegression()
            model48.fit(x, ema48i[-12 * 8:])
            coef48 = model48.coef_
            # EMA96
            model96 = LinearRegression()
            model96.fit(x, ema96i[-12 * 8:])
            coef96 = model96.coef_
            # EMA144
            model144 = LinearRegression()
            model144.fit(x, ema144i[-12 * 8:])
            coef144 = model144.coef_

            coef48_l.append(coef48)
            coef96_l.append(coef96)
            coef144_l.append(coef144)

    print('Done.')
    return [candles, coef48_l, coef96_l, coef144_l, trend]


def multi_bt1(y0, m0, days, symbols, lists, check_db=True):
    """
    Performs bt102() for list or .csv of trading pair symbols.
    :param y0: start year
    :param m0: start month
    :param days: number of days
    :param symbols: list or .csv of trading pair symbols
    :param lists: dict of strategy function input lists
    :param check_db: Get candle data from api call or database
    :return: [candles_list, bdf_list, sdf_list]
    """

    import csv
    from tqdm import tqdm
    import os
    import sys

    class HiddenPrints:
        def __enter__(self):
            self._original_stdout = sys.stdout
            self._original_stderr = sys.stderr
            sys.stdout = open(os.devnull, 'w')
            sys.stderr = open(os.devnull, 'w')

        def __exit__(self, exc_type, exc_val, exc_tb):
            sys.stdout.close()
            sys.stderr.close()
            sys.stdout = self._original_stdout
            sys.stderr = self._original_stderr

    # Check if symbols is a .csv file
    if isinstance(symbols, str):
        if symbols.endswith('.csv'):
            with open(symbols, newline='') as f:
                reader = csv.reader(f)
                symbols = list(reader)[0]

    candles_list = []
    bdf_list = []
    sdf_list = []
    for sym in tqdm(symbols):

        # Backtest
        print(sym)
        with HiddenPrints():
            candles, bdf, sdf = bt1(y0, m0, days, sym, lists, check_db)

        # Append to list
        candles_list.append(candles)
        bdf_list.append(bdf)
        sdf_list.append(sdf)

    return [candles_list, bdf_list, sdf_list]
