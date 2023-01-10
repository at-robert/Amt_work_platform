import os
import sys

# pwd_path = os.path.expanduser('~') + '/'

import send_line as sl
import datetime
from tkinter.tix import MAX
import pandas as pd
from cal_setup import get_calendar_service
import fw3_day_off as fw3

# How to get Google Calendar ID, please refer to the following Evernote "Google Calendar Read" article
CAL_ID_FINISH_TASK = '5h3ema8s5bbua11vdh1vcopfpk@group.calendar.google.com'

FILE_PATH_TIMESTAMP_CAL = r"D:\work_platform\fw3_day_off\once_day_cal.txt"

#----------------------------------------------------------------------
def out_to_csv(date_in, sum_):

    cal_dict = {
        "date": date_in,
        "events": sum_,
        }
    cal_dict_df = pd.DataFrame(cal_dict)

    cal_dict_df.sort_values(by=['date'],ascending=True,inplace=True)
    # To output to csv file
    cal_dict_df.to_csv('cal_.csv', encoding='utf-8', index=False)
    
# To obtain Google Calender Events 
#----------------------------------------------------------------------
def parser_google_cal():
    cal_id = ['primary',CAL_ID_FINISH_TASK]
    date_ = []
    summary_ = []
    MAX_OUT = 500
    act_out = 0

    service = get_calendar_service()
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time{}

    d = datetime.datetime.utcnow().date()
    print("Month = {} ".format(d.month))

    tomorrow = datetime.datetime(d.year, d.month, d.day - 1, 0)
    now = tomorrow.isoformat() + 'Z'

    # print('Getting List to 10 events')

    for i in range(0,2):
        events_result = service.events().list(calendarId=cal_id[i], timeMin=now,
                                            maxResults=MAX_OUT, singleEvents=True,
                                            orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            start = start[0:10]
            dt_start = datetime.datetime.strptime(start, "%Y-%m-%d")

            if( dt_start <  datetime.datetime.utcnow()):
                print(start, event['summary'])
                # To store to pandas dataframe
                date_.append(start)
                summary_.append(event['summary'])
                act_out = act_out + 1

                if(event['summary'] == '[CHECK] 輪值' ):
                    out_msg = " 輪值 on {} , Get Key from Willie , Give key to Tommy on the next day!!".format(start)
                    print(out_msg)
                    sl.lineNotify_one_to_one(out_msg)
    
    out_to_csv(date_, summary_)

    if act_out >= MAX_OUT:
        print (" The actual output {} is larger than {}".format(act_out,MAX_OUT))


#----------------------------------------------------------------------
if __name__ == "__main__":
    # sl.lineNotify_one_to_one("Hello again!!")

    if fw3.check_timestamp_file(FILE_PATH_TIMESTAMP_CAL) == True:
        sys.exit()
    else:
        parser_google_cal()