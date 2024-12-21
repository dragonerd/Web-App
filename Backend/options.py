import datetime

def time():
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d %H:%M:%S")
    return date
        