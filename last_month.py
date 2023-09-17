from multiprocessing import Process
from pytrends.request import TrendReq
import pandas as pd
import urllib3
from dateutil.parser import parse
from datetime import timedelta
import time as T
from config import username,password
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


proxies = []
# read the CSV file into a DataFrame

from datetime import datetime, timedelta

def get_time():
    # Get the current date and time
    current_time = datetime.now() - timedelta(hours=5)

    # Calculate the first day of the current month
    first_day_of_current_month = current_time.replace(day=1)

    # Calculate the first day of the previous month
    first_day_of_previous_month = (first_day_of_current_month - timedelta(days=1)).replace(day=1)

    # Initialize a list to store the timestamps
    timestamps = []

    # Define the desired format
    format_string = "%Y-%m-%dT%H"

    # Loop through each hour from the first hour of the previous month to the last hour of the previous month
    current_hour = first_day_of_previous_month.replace(hour=0, minute=0, second=0)
    last_hour_of_previous_month = first_day_of_current_month - timedelta(hours=1)
    
    while current_hour <= last_hour_of_previous_month:
        timestamp = current_hour.strftime(format_string)
        timestamps.append(timestamp)
        current_hour += timedelta(hours=1)

    print(len(timestamps))
    return timestamps

get_time()

def get_interest(keyword, start, end):
    try:
        f=open('combine.csv',"a")
        proxies = []
        # main_url = "http://gate.smartproxy.com:"
        # for index in range(10000, 10009):
        #     proxies.append(main_url + str(index))
        
        print(start, end)
        
        proxy = f"http://{username}:{password}@gate.smartproxy.com:10000"
        pytrends = TrendReq(hl='en-US', tz=360, proxies=[proxy], timeout=(200,300), retries=13, backoff_factor=0.5, requests_args={'verify':False})
        pytrends.build_payload(kw_list=[keyword],  timeframe=f'{start} {end}')
        historical_interest = pytrends.interest_over_time()
        df=pd.DataFrame(historical_interest)
        df.to_csv("data.csv")
        print(df)
        print(len(df))
        return df
        # df.to_csv(f"all_csv/{keyword}_data.csv")
    except Exception as err:
        print(err)

if __name__ == '__main__':
    f=open('combine.csv',"a")
    # data=pd.read_csv("nasdaq-listed.csv").head(1000)
    # kw_list = data['Symbol']
    kw_list = ['AAPL','MSFT','GOOG','GOOGL','AMZN','NVDA','BRK/B','TSLA','META','HSBC']
    
    processes = []
    time=get_time()
    print(len(time))
    # f.writelines("Ticket,"+",".join(time)+"\n")
    # f.close()
    No_process = 1

    for keyword in kw_list:
        print(f"Trying to get data for {keyword} - Process {No_process}")
        try:
            t__=0
            times__=[]
            FINAL_DF_SINGLE_STOKE=[]
            for req in range(1,6):
                try:
                    start_time=time[t__]
                    if t__+168<=len(time):
                        end_time=time[t__+168]
                    else:
                        end_time=time[len(time)-1]
                    print(end_time)
                    data__= get_interest(keyword,start_time,end_time)
                    data__.to_csv("time.csv")
                    a=pd.read_csv("time.csv")
                    for timm in a['date']:
                        times__.append(timm)
                    FINAL_DF_SINGLE_STOKE.append(data__)
            

                except Exception as err:
                    print(err)
                    pass
                
                t__+=168
            
            # print(times__)
            times__= [str(num) for num in times__]
            FINAL_DF_SINGLE_STOKE_df = pd.concat(FINAL_DF_SINGLE_STOKE)
            print(FINAL_DF_SINGLE_STOKE_df)
            print(len(FINAL_DF_SINGLE_STOKE_df))
            # Reset the index of the concatenated dataframe
            FINAL_DF_SINGLE_STOKE_df.reset_index(drop=True, inplace=True)
            if No_process==1:
                
                # f.writelines("Ticket,"+",".join(FINAL_DF_SINGLE_STOKE_df['date'])+"\n")
                f.writelines("Ticket,"+",".join(times__)+"\n")
                f.writelines(f"{keyword},"+",".join(FINAL_DF_SINGLE_STOKE_df[keyword].astype(str))+"\n")
            else: 
                f.writelines(f"{keyword},"+",".join(FINAL_DF_SINGLE_STOKE_df[keyword].astype(str))+"\n")
            # FINAL_DF_SINGLE_STOKE_df.to_csv("output_5_days_each_minute.csv",index=False)
            No_process+=1
        except Exception as e :
            print(e)
            pass   
        
    
        
    print("Work done. Check combine.csv")
