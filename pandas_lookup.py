import pandas as pd
import numpy as np

 #functionfor converting number to grade. unnecessary but good to know
def Grade(value:float) ->str:
    if 0 <=value<=25:
        return "A1"
    elif 26 <=value<=50:
        return "A2"
    elif 51 <=value<=75:
        return "A3"
    elif 76<=value<=100:
        return "B1"
    elif 101<=value<=125:
        return "B2"
    elif 126<=value<=150:
        return "B3"
    elif 151<=value<=175:
        return "C1"
    elif 176<=value<=200:
        return "C2"
    elif 201<=value<=225:
        return "C3"
    elif 226<=value<=260:
        return "D1"
    elif 261<=value<=300:
        return "D2" 
    elif 301<=value<=345:
        return "E1"
    elif 346<=value<=390:
        return "E2"
    elif 391<=value<=440:
        return "F"
    elif value>440:
        return "G"
    else:
        return None   

#filepath
csv_path=r"C:\Users\ATU\OneDrive - Atlantic TU\Modules\smart teams\BER\ber.csv"

#Read chunk by chunk ie 100000 lines at a time
chunk_size=100000
chunks=[]

for chunk in pd.read_csv(
    csv_path,
    encoding="latin1",
    low_memory=False,
    chunksize=chunk_size,
    on_bad_lines='skip',
    usecols=lambda c:c in ['BerRating', 'CountyName']
):
    
    chunk=chunk[(chunk['BerRating']>=0) & (chunk['BerRating']<=500)]

    chunks.append(chunk)

#combine chunks

df=pd.concat(chunks, ignore_index=True)

#Convert BER ratings to numeric
df['BerRating']=pd.to_numeric(df['BerRating'], errors='coerce')

county=input("Select county: ")

#Create mask
mask=df['CountyName'].astype(str).str.contains(county, case=False, na=False)

#avg BER rating
mean_county=df.loc[mask, 'BerRating'].mean()

print("Average BER Rating for", county, ":", mean_county)   
print(Grade(mean_county))