def to_database(candles, folder='database'):
    """
    Saves candle data of a symbol (pandas dataframe) to a pickle file.
    If file exists merges candles.
    If merge has a time gap, gets time gap information and merges.

    :param candles:
    :param folder:
    :return:
    """

    from pathlib import Path
    import pickle
    import pandas as pd
    from api_calls import klines2

    # Check if directory exists
    db_dir = Path(folder)
    if not db_dir.is_dir():
        print('The directory does not exist.')
        return

    # Check if file exists and update
    symbol = candles['Symbol'][0]
    pathfile = folder + '/' + symbol + '.pkl'
    db_file = Path(pathfile)
    if db_file.is_file():   # If file exists: merge candle data

        db_candles = pickle.load(open(pathfile, 'rb'))
        t_start = db_candles['Open time'][0]
        t_end = db_candles['Open time'].iloc[-1] + 300000
        t0 = candles['Open time'][0]
        t1 = candles['Open time'].iloc[-1] + 300000

        #   |--db--|
        # |----|
        if (t0 < t_start) & (t_start <= t1 <= t_end):
            sub_candles = candles[candles['Open time'] < t_start]
            print('to1:', db_candles['Open time'].iloc[0] - sub_candles['Open time'].iloc[-1])
            db_candles = pd.concat([sub_candles, db_candles])
            db_candles = db_candles.reset_index(drop=True)
            pickle.dump(db_candles, open(pathfile, 'wb'))
            return

        #   |--db--|
        #       |----|
        if (t1 > t_end) & (t_start <= t0 <= t_end):
            sub_candles = candles[candles['Open time'] >= t_end]
            print('to2:', sub_candles['Open time'].iloc[0] - db_candles['Open time'].iloc[-1])
            db_candles = pd.concat([db_candles, sub_candles])
            db_candles = db_candles.reset_index(drop=True)
            pickle.dump(db_candles, open(pathfile, 'wb'))
            return

        #       |--db--|
        # |---|
        if (t0 < t_start) & (t1 <= t_start):
            sub_candles = klines2(t1, t_start, symbol)
            print('to3.1:', sub_candles['Open time'].iloc[0] - candles['Open time'].iloc[-1])
            print('to3.2:', db_candles['Open time'].iloc[0] - sub_candles['Open time'].iloc[-1])
            db_candles = pd.concat([candles, sub_candles, db_candles])
            db_candles = db_candles.reset_index(drop=True)
            pickle.dump(db_candles, open(pathfile, 'wb'))
            return

        #   |--db--|
        #            |---|
        if (t0 >= t_end) & (t1 > t_end):
            sub_candles = klines2(t_end, t0, symbol)
            print('to4.1:', sub_candles['Open time'].iloc[0] - db_candles['Open time'].iloc[-1])
            print('to4.2:', candles['Open time'].iloc[0] - sub_candles['Open time'].iloc[-1])
            db_candles = pd.concat([db_candles, sub_candles, candles])
            db_candles = db_candles.reset_index(drop=True)
            pickle.dump(db_candles, open(pathfile, 'wb'))
            return

        #     |--db--|
        #   |----------|
        if (t0 < t_start) & (t1 > t_end):
            sub_candles1 = candles[candles['Open time'] < t_start]
            sub_candles2 = candles[candles['Open time'] >= t_end]
            print('to5.1:', db_candles['Open time'].iloc[0] - sub_candles1['Open time'].iloc[-1])
            print('to5.2:', sub_candles2['Open time'].iloc[0] - db_candles['Open time'].iloc[-1])
            db_candles = pd.concat([sub_candles1, db_candles, sub_candles2])
            db_candles = db_candles.reset_index(drop=True)
            pickle.dump(db_candles, open(pathfile, 'wb'))
            return

    else:   # If file does not exist: create
        pickle.dump(candles, open(pathfile, 'wb'))

    return


def get_database(y0, m0, days, symbol, folder='database'):
    """"""

    from pathlib import Path
    import pickle
    import datetime
    from api_calls import klines2
    import pandas as pd

    # Check if directory exists
    db_dir = Path(folder)
    if not db_dir.is_dir():
        print('The directory does not exist.')
        return

    # t0 and t1 from y0, m0, days
    t0 = datetime.datetime(y0, m0, 1)
    epoch = datetime.datetime.utcfromtimestamp(0)
    t0 = int((t0 - epoch).total_seconds() * 1000)
    t1 = t0 + days * 24 * 60 * 60 * 1000

    # Check if file exists and get
    pathfile = folder + '/' + symbol + '.pkl'
    db_file = Path(pathfile)
    if db_file.is_file():

        db_candles = pickle.load(open(pathfile, 'rb'))
        t_start = db_candles['Open time'][0]
        t_end = db_candles['Open time'].iloc[-1] + 300000

        #   |--db--|
        # |----|
        if (t0 < t_start) & (t_start < t1 <= t_end):
            sub_candles1 = klines2(t0, t_start, symbol)
            sub_candles2 = db_candles[db_candles['Open time'] < t1]
            print('get1:', sub_candles2['Open time'].iloc[0] - sub_candles1['Open time'].iloc[-1])
            candles = pd.concat([sub_candles1, sub_candles2])
            candles = candles.reset_index(drop=True)
            to_database(sub_candles1)
            return candles

        #   |--db--|
        #       |----|
        if (t1 > t_end) & (t_start <= t0 < t_end):
            sub_candles1 = db_candles[db_candles['Open time'] >= t0]
            sub_candles2 = klines2(t_end, t1, symbol)
            print('get2:', sub_candles2['Open time'].iloc[0] - sub_candles1['Open time'].iloc[-1])
            candles = pd.concat([sub_candles1, sub_candles2])
            candles = candles.reset_index(drop=True)
            to_database(sub_candles2)
            return candles

        #       |--db--|
        # |---|
        if (t0 < t_start) & (t1 < t_start):
            candles = klines2(t0, t1, symbol)
            sub_candles = klines2(t1, t_start, symbol)
            print('get3.1:', sub_candles['Open time'].iloc[0] - candles['Open time'].iloc[-1])
            print('get3.2:', db_candles['Open time'].iloc[0] - sub_candles['Open time'].iloc[-1])
            db_candles = pd.concat([candles, sub_candles, db_candles])
            db_candles = db_candles.reset_index(drop=True)
            to_database(db_candles)
            return candles

        #   |--db--|
        #            |---|
        if (t0 > t_end) & (t1 > t_end):
            candles = klines2(t0, t1, symbol)
            sub_candles = klines2(t_end, t0, symbol)
            print('get4.1:', sub_candles['Open time'].iloc[0] - db_candles['Open time'].iloc[-1])
            print('get4.2:', candles['Open time'].iloc[0] - sub_candles['Open time'].iloc[-1])
            db_candles = pd.concat([db_candles, sub_candles, candles])
            db_candles = db_candles.reset_index(drop=True)
            to_database(db_candles)
            return candles

        #     |--db--|
        #   |----------|
        if (t0 < t_start) & (t1 > t_end):
            sub_candles1 = klines2(t0, t_start, symbol)
            sub_candles2 = klines2(t_end, t1, symbol)
            print('get5.1:', db_candles['Open time'].iloc[0] - sub_candles1['Open time'].iloc[-1])
            print('get5.2:', sub_candles2['Open time'].iloc[0] - db_candles['Open time'].iloc[-1])
            db_candles = pd.concat([sub_candles1, db_candles, sub_candles2])
            db_candles = db_candles.reset_index(drop=True)
            to_database(db_candles)
            return db_candles

        #     |--db--|
        # |---|
        if (t0 < t_start) & (t1 == t_start):
            candles = klines2(t0, t1, symbol)
            print('get6:', db_candles['Open time'].iloc[0] - candles['Open time'].iloc[-1])
            db_candles = pd.concat([candles, db_candles])
            db_candles = db_candles.reset_index(drop=True)
            to_database(db_candles)
            return candles

        #   |--db--|
        #          |---|
        if (t1 > t_end) & (t0 == t_end):
            candles = klines2(t0, t1, symbol)
            print('get7:', candles['Open time'].iloc[0] - db_candles['Open time'].iloc[-1])
            db_candles = pd.concat([db_candles, candles])
            db_candles = db_candles.reset_index(drop=True)
            to_database(db_candles)
            return candles

        #   |----db----|
        #      |----|
        if (t0 >= t_start) & (t1 <= t_end):
            mask = (db_candles['Open time'] >= t0) & (db_candles['Open time'] < t1)
            candles = db_candles[mask]
            return candles

    else:  # If file does not exist: create
        candles = klines2(t0, t1, symbol)
        to_database(candles)
        return candles
