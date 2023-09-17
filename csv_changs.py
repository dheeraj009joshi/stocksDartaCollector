import pandas as pd

# read the CSV file into a DataFrame
f=open('combine.csv',"w")
df = pd.read_csv('UAL_data.csv')
print("Ticket,"+",".join(df['date']))
f.writelines("Ticket,"+",".join(df['date'])+"\n")
f.writelines("UAL,"+",".join(map(str, df['UAL'])))
print(",".join(map(str, df['UAL'])))
