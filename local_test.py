import datetime
from pytrends.request import TrendReq
import time

# Set up pytrends
pytrends = TrendReq(hl='en-US', tz=360)

# Define the keywords
keywords = ['example keyword']

# Set the timeframe
current_time = datetime.datetime.now() - datetime.timedelta(hours=5)
five_days_before = current_time - datetime.timedelta(days=5)
timeframe = five_days_before.strftime('%Y-%m-%d') + ' ' + current_time.strftime('%Y-%m-%d')

# Initialize a list to store the data
data = []

# Loop through each 8-minute interval from current_time to five_days_before
while current_time > five_days_before:
    # Set the start and end time for the interval
    start_time = current_time - datetime.timedelta(minutes=8)
    end_time = current_time

    # Format the start and end time
    format_string = "%Y-%m-%dT%H"
    start_time_str = start_time.strftime(format_string)
    end_time_str = end_time.strftime(format_string)

    # Build the payload
    pytrends.build_payload(keywords, timeframe=start_time_str + ' ' + end_time_str, geo='')

    # Get the interest over time data
    interest_over_time_df = pytrends.interest_over_time()

    # Append the data to the list
    data.append(interest_over_time_df)

    # Pause for a few seconds to avoid hitting the rate limit
    time.sleep(5)

    # Update current_time for the next interval
    current_time = start_time

# Reverse the data list to have the most recent data first
data.reverse()

# Print the data
for df in data:
    print(df)
