# MetaTrader5 Market Open Checker Automation
### Check Prices of world markets on MT5 platform at specific time, then send WhatsApp message with market status.

#### Using Rest API to connect to Meta Trader platform, then check at specific time for a specific market, if all conidiation are met then send a WhatsApp message to group with custom text message at fix time.

This automation script uses three files: <br />
The main one is markets_open_checker.py in which there are most the functions of the algorithm. <br />
The second one is market_open_config.py which is set what kind of market to check and calculate the timestamp automatically for the relevant day. <br />
The third file is send_whatsapp_message.py which set the kind of message to send and then use Selenium to open WhatsApp web at the background and send a message.

All the dates and times in this script are calculated automatically and convert to timestamp to work with the API. The functions are running at fix time and waiting until the next check to run again, The script also saves coockies to not make you relogin to WhatsApp Web everytime.
