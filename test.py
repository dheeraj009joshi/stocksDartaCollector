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

# Test the get_time function
get_time()
