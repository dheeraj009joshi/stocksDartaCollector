from multiprocessing import Process
from pytrends.request import TrendReq
import pandas as pd
import urllib3
from dateutil.parser import parse
from datetime import timedelta
import time as T
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
  


proxies = []
# read the CSV file into a DataFrame

def get_time():
    from datetime import datetime, timedelta

    current_time = datetime.now()- timedelta(hours=5)
    seven_days_before = current_time - timedelta(days=7)

    # Define the desired format
    format_string = "%Y-%m-%dT%H"

    # Initialize a list to store the timestamps
    timestamps = []

    # Loop through each hour from current_time to seven_days_before
    while current_time > seven_days_before:
        timestamp = current_time.strftime(format_string)
        timestamps.append(timestamp)
        current_time -= timedelta(hours=1)

    # Print the timestamps in reverse order (from recent to oldest)
    timestamps.reverse()
    # for timestamp in timestamps:
    #     print(timestamp)
    return timestamps
    # return "Ticket,"+",".join(timestamps)+"\n"

def get_interest(keyword,start,end):
    try:
        f=open('combine.csv',"a")
        # proxies = []
        # main_url = "http://gate.smartproxy.com:"
        # for index in range(10000, 10009):
        #     proxies.append(main_url + str(index))
        username = 'spbp08lpg9'
        password = '4URfpfvim1dsuaB3O2'
        proxy = f"http://{username}:{password}@gate.smartproxy.com:10000"
        # pytrends = TrendReq(hl='en-US', tz=360,proxies=["http://rajeshkumardevapp.gmail.com:zxamw8@gate2.proxyfuel.com:2000"],timeout=(200,300), retries=13, backoff_factor=0.5, requests_args={'verify':False})
        pytrends = TrendReq(hl='en-US', tz=360,proxies=proxies,timeout=(200,300), retries=13, backoff_factor=0.5, requests_args={'verify':False})
        pytrends.build_payload(kw_list=[keyword],  timeframe=f'{start} {end}')
        historical_interest = pytrends.interest_over_time()
        df=pd.DataFrame(historical_interest)
        df.to_csv(f"all_csv/{keyword}_data.csv")
        df_2 = pd.read_csv(f"all_csv/{keyword}_data.csv")
        # print(historical_interest)
        f.writelines(f"{keyword},"+",".join(map(str, df_2[keyword]))+"\n")
    except Exception as err:
        print(err)
if __name__ == '__main__':
    f=open('combine.csv',"a")
    data=pd.read_csv("nasdaq-listed.csv").head(1000)
    # print(data)
    kw_list = data['Symbol']
    
    processes = []
    time=get_time()
    start_time=time[0]
    end_time=time[-1]
    print(time)
    print(type(time))
    f.writelines("Ticket,"+",".join(time)+"\n")
    f.close()
    No_process=1
    for keyword in kw_list:
        print(f"Trying to get data for this {keyword} {No_process}")
        try:
            # get_interest(keyword,start_time,end_time)
            process = Process(target=get_interest, args=(keyword,start_time,end_time,))
            processes.append(process)
            process.start() 
            T.sleep(0.010)
            if No_process%20==0:
                T.sleep(20)
            No_process+=1
        except Exception as e :
            print(e)
            pass   
    for process in processes:
        try:
            process.join()
        except Exception as err:
            print(err)
            pass
        
    print("Work done check combine .csv")
