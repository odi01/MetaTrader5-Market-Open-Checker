import datetime as dt
import hashlib
import sys
from datetime import date
from datetime import datetime

import pytz
import requests
import schedule
from urllib3 import disable_warnings, exceptions

sys.path.insert(1, 'C:/Code/dealing-tools')  # For the config file path
from config import *
from market_open_config import *
from send_whatsapp_message import *


# Disable RFC 2818 Error message
disable_warnings(exceptions.SecurityWarning)

# dd/mm/YY
today_date = date.today()
today_date = today_date.strftime("%d/%m/%Y")


def mt5_auth(login, password):
    # get authentication start
    s = requests.Session()
    auth_start_response = s.get("{}/api/auth/start?version=1985&agent=WebManager&type=manager&login={}".
                                format(mt5_url, login), # From config.py file
                                verify='/mt5-dev.pem').json()
    srv_rand = auth_start_response['srv_rand']
    password_hash = hashlib.md5(password.encode('utf-16le')).digest()
    password_hash_total = hashlib.md5(password_hash + b'WebAPI').digest()
    srv_rand_answer = hashlib.md5(password_hash_total + bytearray.fromhex(srv_rand)).hexdigest()
    auth_answer_response = s.get("{}/api/auth/answer?srv_rand_answer={}&cli_rand=677ab515ac4682ecb15f4ee0e0c2847b".
                                 format(mt5_url, srv_rand_answer),
                                 verify='/mt5-dev.pem')
    # print(auth_answer_response.json())
    return s


def history_chart(auth_func, url, symbols_list, from_time, to_time, open_time, quote_date=today_date):
    result = []

    for symbol in symbols_list:
        try:  # Try to fetch data for the symbol
            res_dict = auth_func.get("{0}/api/chart/get?symbol={1}&from={2}&to={3}&data=do".
                                     format(url, symbol, from_time, to_time)).json()
            # res_dict = json.loads(json.dumps(res_dict))
            res_list = res_dict['answer']

        except (KeyError, ValueError) as e:  # Symbol isn't exists
            result.append("ERROR: {0} wasn't found".format(symbol))

        else:
            if res_list:
                for line in res_list:
                    open_price = "{:g}".format(line[1])  # Using :g to remove zeros at the end
                    timestamp = line[0]
                    dt_object = datetime.utcfromtimestamp(timestamp)  # Convert to regular time in UTC/GMT
                    c_time = dt_object.strftime("%H:%M")
                    hour = int(c_time[:2])
                    minute = int(c_time[3:])
                    c_date = dt_object.strftime("%d/%m/%Y")

                    if c_date == quote_date and hour == int(open_time[:2]) and minute >= int(open_time[3:]):
                        result.append(
                            "{0} was successfully opened at {1} in price of {2}".format(symbol, c_time, open_price))
                        break
                    else:
                        result.append('ERROR:')
            else:  # Empty list = not quotes
                result.append("ERROR: {} was not opened from five minute since it should be open".format(symbol))
    return result


def date_and_time_to_utc_timestamp(date_and_time):
    """
    :param date_and_time: (str) The date and the time (dd/mm/yy hh/mm) which you want to get UTC timestamp of.
    :return: (int) from_timestamp - The date and the time in timestamp.
    to_timestamp - The date and the time in timestamp plus five minutes from the original time.
    """
    # UTC timezone
    utc_timezone = pytz.timezone('Etc/Greenwich')

    # Convert The date of today and the market open time from string to datetime format,
    # than convert it to gmt time to match the server time, and at the end convert it to timestamp.
    from_date_time = datetime.strptime(date_and_time, '%d/%m/%Y %H:%M')  # Today date and market open time in datetime
    from_utc_dt = utc_timezone.localize(from_date_time)  # Convert local time to UTC time
    from_timestamp = round(datetime.timestamp(from_utc_dt))  # Convert UTC to timestamp

    # Do the same as the above but adding plus five minutes to the market open time.
    to_date_time = from_date_time + dt.timedelta(minutes=5)  # Adding five minutes to the original time
    to_utc_dt = utc_timezone.localize(to_date_time)  # Convert local time to UTC time
    to_timestamp = round(datetime.timestamp(to_utc_dt))  # Convert UTC to timestamp

    return from_timestamp, to_timestamp


def valid_market_open(history_chart_fun):
    quotes = history_chart_fun

    for line in quotes:  # Print checked symbols list
        print(line)

    split_list_to_words = [word for line in quotes for word in
                           line.split()]  # Split symbols line to words to find error keyword

    if 'ERROR:' in split_list_to_words:
        print("~ ERROR: Market Didn't Opened Correctly ~")
        return False
    else:
        print(" ~ Market Opened Successfully ~")
        return True


def sending_whatsapp_sms(history_chart_func, message):
    check_quotes = history_chart_func

    if valid_market_open(check_quotes):
        send_message(message)
    else:
        return "Something Went Wrong"


def all_tasks(symbol, timestamp_list, symbol_opentime, sms_content):
    auth = mt5_auth(mt5_login, mt5_password)
    history_func = history_chart(auth, mt5_url, symbol, timestamp_list[0], timestamp_list[1], symbol_opentime, today_date)
    sending_whatsapp_sms(history_func, sms_content)


def main():
    print("~~ Running ~~")

    # Calling sending_whatsapp_sms function with two parameters.
    schedule.every().day.at("09:05").do(lambda: all_tasks(middle_east_nine_s, middle_east_nine_timestamp,
                                                          middle_east_nine_open_time, MiddleEastNine_txt))
    schedule.every().day.at("09:37").do(lambda: all_tasks(jse_s, jse_timestamp, jse_open_time, JSE_txt))
    # Summer DST
    # schedule.every().day.at("10:02").do(lambda: all_tasks(middle_east_ten_s, middle_east_ten_timestamp,
    #                                                       middle_east_ten_open_time, MiddleEastTen_txt))
    schedule.every().day.at("10:04").do(lambda: all_tasks(europe_s, europe_timestamp, europe_open_time, Europe_txt))
    schedule.every().day.at("10:32").do(lambda: all_tasks(sug11, sug11_timestamp, sug11_open_time, SUG11_txt))
    schedule.every().day.at("11:17").do(lambda: all_tasks(coffee, coffee_timestamp, coffee_open_time, COFFEE_txt))
    schedule.every().day.at("11:47").do(lambda: all_tasks(cocoa, cocoa_timestamp, cocoa_open_time, COCOA_txt))
    schedule.every().day.at("15:02").do(lambda: all_tasks(orange, orange_timestamp, orange_open_time, ORANGE_txt))
    schedule.every().day.at("16:32").do(lambda: all_tasks(us_symbols, us_timestamp, us_market_open_time, UsMarket_txt))

    while True:
        schedule.run_pending()
        next_run_delta = (schedule.next_run() - datetime.now()).total_seconds()
        if next_run_delta <= 0:
            continue
        elif next_run_delta >= 18000:
            print("\n~~ DONE ~~")
            break
        else:
            print("\n" + "The next check will be in {} minutes".format(round(next_run_delta / 60)))
            time.sleep(next_run_delta + 1)


if __name__ == '__main__':
    main()
