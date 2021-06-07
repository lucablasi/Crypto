def klines(y0, m0, days, symbol):
    """
    Requests 5-minute candle data for trading pair over specified time interval.
    Time interval defined in year, month, and extension in days.
    Organizes into a pandas dataframe.
    :param y0: start year               :type y0: int
    :param m0: start month              :type m0: int
    :param days: number of days         :type days: int
    :param symbol: trading pair symbol  :type symbol: string
    :return: candle-data pandas dataframe
    """

    import datetime
    from tqdm import tqdm
    import requests
    import pandas

    # Start time
    st = datetime.datetime(y0, m0, 1)

    # Convert start time to milliseconds from epoch
    epoch = datetime.datetime.utcfromtimestamp(0)
    st = int((st - epoch).total_seconds() * 1000)

    # Determine total number of candles and number of calls to make
    n_candles = days * 24 * 60 / 5
    n_calls = int(n_candles // 1000)

    # Request candle data
    candles_list = []
    url = 'https://api.binance.com/api/v3/klines'
    params = {
        'symbol': symbol,
        'interval': '5m',
        'startTime': 0,
        'endTime': 0,
        'limit': 1000}
    print('Collecting candles...')
    for _ in tqdm(range(n_calls)):
        et = st + 1000*5 * 60 * 1000 - 1
        params['startTime'] = st
        params['endTime'] = et
        candles_i = requests.get(url, params).json()
        candles_list.append(candles_i)
        st += 1000*5 * 60 * 1000

    # Last request (different limit)
    last_limit = int(n_candles % 1000)
    if last_limit != 0:
        et = st + last_limit*5 * 60 * 1000 - 1
        params['startTime'] = st
        params['endTime'] = et
        params['limit'] = last_limit
        candles_i = requests.get(url, params).json()
        candles_list.append(candles_i)

    # Organize into dataframe
    candles_list = [item for subl in candles_list for item in subl]
    candles = pandas.DataFrame(candles_list)
    candles.columns = ['Open time', 'Open', 'High', 'Low', 'Close', 'Volume',
                       'Close time', 'Quote asset volume', 'Number of trades',
                       'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore']
    candles = candles.drop(columns='Ignore')
    candles['Symbol'] = symbol
    candles['Open'] = candles['Open'].apply(lambda x: float(x))
    candles['High'] = candles['High'].apply(lambda x: float(x))
    candles['Low'] = candles['Low'].apply(lambda x: float(x))
    candles['Close'] = candles['Close'].apply(lambda x: float(x))
    candles['Volume'] = candles['Volume'].apply(lambda x: float(x))
    print('Candle collection done.')

    return candles


def klines2(t0, t1, symbol):
    """
    Requests 5-minute candle data for trading pair over specified time interval.
    Time interval defined in milliseconds from epoch.
    Organizes into a pandas dataframe.
    :param t0: start time               :type t0: int
    :param t1: start time               :type t1: int
    :param symbol: trading pair symbol  :type symbol: string
    :return: candle-data pandas dataframe
    """

    import datetime
    from tqdm import tqdm
    import requests
    import pandas

    # Determine number of calls to make
    dt = t1 - t0
    n_calls = int((dt/300000) // 1000)   # 300000 is 5m in ms

    # Request candle data
    candles_list = []
    url = 'https://api.binance.com/api/v3/klines'
    params = {
        'symbol': symbol,
        'interval': '5m',
        'startTime': 0,
        'endTime': 0,
        'limit': 1000}
    st = t0
    print('Collecting candles...')
    for _ in tqdm(range(n_calls)):
        et = st + 1000 * 300000 - 1
        params['startTime'] = st
        params['endTime'] = et
        candles_i = requests.get(url, params).json()
        candles_list.append(candles_i)
        st += 1000 * 300000

    # Last request (different limit)
    last_limit = int((dt/300000) % 1000)
    if last_limit != 0:
        et = st + last_limit * 300000 - 1
        params['startTime'] = st
        params['endTime'] = et
        params['limit'] = last_limit
        candles_i = requests.get(url, params).json()
        candles_list.append(candles_i)

    # Organize into dataframe
    candles_list = [item for subl in candles_list for item in subl]
    candles = pandas.DataFrame(candles_list)
    candles.columns = ['Open time', 'Open', 'High', 'Low', 'Close', 'Volume',
                       'Close time', 'Quote asset volume', 'Number of trades',
                       'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore']
    candles = candles.drop(columns='Ignore')
    candles['Symbol'] = symbol
    candles['Open time'] = candles['Open time'].apply(lambda x: float(x))
    candles['Open'] = candles['Open'].apply(lambda x: float(x))
    candles['High'] = candles['High'].apply(lambda x: float(x))
    candles['Low'] = candles['Low'].apply(lambda x: float(x))
    candles['Close'] = candles['Close'].apply(lambda x: float(x))
    candles['Volume'] = candles['Volume'].apply(lambda x: float(x))
    candles['Close time'] = candles['Close time'].apply(lambda x: float(x))
    print('Candle collection done.')

    return candles
