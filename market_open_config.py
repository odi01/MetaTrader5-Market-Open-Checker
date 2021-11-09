from markets_open_checker import today_date
from markets_open_checker import date_and_time_to_utc_timestamp

# Middle East Nine
middle_east_nine_s = ["TADAWUL", "SABIC", "STC", "Aramco"]
middle_east_nine_open_time = "09:00"
middle_east_nine_date = today_date + " " + middle_east_nine_open_time
middle_east_nine_timestamp = date_and_time_to_utc_timestamp(middle_east_nine_date)

# JSE-DATE
jse_s = ["JSE-DEC21"]
jse_open_time = "09:35"
jse_date = today_date + " " + jse_open_time
jse_timestamp = date_and_time_to_utc_timestamp(jse_date)

# Europe Market
europe_s = ["AIRBUS", "BAYER", "ADS", "CREDIT", "HM", "IBER", "INTEX", "GAZPROM", "TELITA", "HSBC", "VODAFONE",
            "CAC40", "DAX40", "NDA", "TA35"]  # "NDA"
europe_open_time = "10:00"
europe_date = today_date + " " + europe_open_time
europe_timestamp = date_and_time_to_utc_timestamp(europe_date)

# SUG11-DATE
sug11 = ["SUG11-MAR22"]
sug11_open_time = "10:30"
sug11_date = today_date + " " + sug11_open_time
sug11_timestamp = date_and_time_to_utc_timestamp(sug11_date)

# COFFE-DATE
coffee = ["COFFE-DEC21"]
coffee_open_time = "11:15"
coffee_date = today_date + " " + coffee_open_time
coffee_timestamp = date_and_time_to_utc_timestamp(coffee_date)

# COCOA-DATE
cocoa = ["COCOA-DEC21"]
cocoa_open_time = "11:45"
cocoa_date = today_date + " " + cocoa_open_time
cocoa_timestamp = date_and_time_to_utc_timestamp(cocoa_date)

# ORANG-DATE
orange = ["ORANG-NOV21"]
orange_open_time = "15:00"
orange_date = today_date + " " + orange_open_time
orange_timestamp = date_and_time_to_utc_timestamp(orange_date)

# USA Market Open
us_market_open_time = "16:30"
us_symbols = ["APPLE", "AMAZON", "3M", "TESLA", "MSFT", "INTEL", "DOW30", "SPX500", "NASDAQ100"]
us_date_n_time = today_date + " " + us_market_open_time  # str
us_timestamp = date_and_time_to_utc_timestamp(us_date_n_time)
