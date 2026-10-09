import time
import pandas as pd
from  ddgs import DDGS



input_file="eyecarelists.csv"
output_file="eyecare_data_with_websites.csv"

df=pd.read_csv(input_file)
df.columns=df.columns.str.lower()


#show colums from the csv-input file
print("CSV Columns Found:",df.columns.tolist())
print("")
NAME_COL="name"
CITY_COL="city"

# Process only the first 60 rows for testing
batch_df=df.head(11).copy() 

IGNORE_DOMAINS =[ "yelp.com","yellowpages.com","facebook.com","healthgrades.com","mapquest.com", "linkedin.com" ]

print("Starting Website Search...\n")

results=[]
ddgs=DDGS()


for index, row in df.iterrows():
    
    business=row[NAME_COL]
    city=row[CITY_COL]


    query=f"{business} {city} official website"
    print(f"Searching for: {query}")
    
    found_url="Not Found"
   

    try:
        #handle th etime out exception if the search takes too long
        with DDGS(timeout=10) as ddgs:

            #fetch top results from duckduckgo search
            search_results = list(ddgs.text(query,  backend="html"))

         
            for result in search_results:
                url=result.get("href","")


                #check if url belongs to the directory site
                if not any(domain in url.lower() for domain in IGNORE_DOMAINS):

                    found_url=url

                    break

    except Exception as e:
        print(f"Error {business}:{e}")

    results.append(found_url)
    #print the found URL
    print(f" -->Found URL: {found_url}\n")

    time.sleep(2)  # Sleep to avoid hitting  too quickly


#add the results to the dataframe and save to a new CSV file
df["Website"]   = results


#save the updated dataframe to a new CSV file
df.to_csv("eyecare_data_with_websites.csv",index=False)

print("Done file output in eyecare_data_with_websites.csv")