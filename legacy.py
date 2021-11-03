#%% --------------------------------------------------------------------------
import pathlib
import pandas as pd
import random


# Config
AUTHOR = "elliott.phillips@ons.gov.uk"
DATA_DIR = pathlib.Path("data/")
SIGNUP_DATA = DATA_DIR / "signups.csv"
PREVIOUS_MATCHES = DATA_DIR / "previous_matches.csv"


# Import the list of members
collaborate_data = pd.read_csv(SIGNUP_DATA)


#%% --------------------------------------------------------------------------
# Import previous matches 
previous_matches = pd.read_csv(PREVIOUS_MATCHES, encoding="utf-8")

# Merge previously matched emails to create unquie indentifier
previous_matches['check_string'] = previous_matches["Email Address 1"] + previous_matches["Email Address 2"]

print(previous_matches["check_string"])

#%% --------------------------------------------------------------------------
# Cache all emails in a list
emails = list(collaborate_data['Email address (please use your ONS account)'])

# Print and remove duplicates.
if len(emails) != len(set(emails)):
    print(set([x for x in emails if emails.count(x) > 1]))
    emails=list(set(emails))

#%% --------------------------------------------------------------------------
# Initialise empty list for new matches
matches=[]

# Check even email count, remove author if odd
if len(emails) % 2 == 1:
    emails.remove(AUTHOR)

# Select email without replacement, then a second email
# Check if this pair is in previous cohort, if so, reselect
while len(emails) > 0:
    index1=random.randint(0,len(emails)-1)
    email1=emails[index1]
    emails.pop(index1)
    unique=False
    while unique==False:
        index2=random.randint(0,len(emails)-1)
        email2=emails[index2]
        email_pair=[email1,email2]
        UI=''.join(sorted(email_pair))
        unique=not any(n in UI for n in previous_matches.iloc[:,2])
    emails.pop(index2)
    matches.append(email_pair)
    

matches1=pd.DataFrame(matches, columns={'Email Address 1','Email Address 2'})
matches2=matches1.copy()
matches2.rename(columns={'Email Address 2':'Email Address 1','Email Address 1':'Email Address 2'},inplace=True);

#we now merge the 2 data frames, this creates a version with both orderings of the matches
frames=[matches2,matches1]
matches=pd.concat(frames).copy()

#make all emails lower case
matches['Email Address 1']=matches['Email Address 1'].str.lower()

#We now make it alphebetical order
matches.sort_values(by=['Email Address 1'],inplace=True)

#%% --------------------------------------------------------------------------
# We run old code to double check that this works
# This bit of code is preparing to see whether matches have occurred in previous months
# by checking it against the master collaborate matches spreadsheet


matches['check_string'] = matches.apply(lambda row: ''.join(sorted([row['Email Address 1'], row['Email Address 2']])), axis=1)
already_matched = matches.merge(previous_matches, on='check_string', how='left')
already_matched = already_matched.dropna()
#its empty which is good

#%% --------------------------------------------------------------------------
# New way of outputing
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows

# Outputing the new matches

Matches_table=load_workbook(DATA_DIR / "5_Collaborate_Matches_Table.xlsx")
del Matches_table['Python Output New']
Output_sheet=Matches_table.create_sheet('Python Output New')
Output_sheet.title='Python Output New'
for r in dataframe_to_rows(matches, index=True, header=True):
    Output_sheet.append(r)

# We also output the new collaborate list 
del Matches_table['Collaborate list']
Output_sheet=Matches_table.create_sheet('Collaborate list')
Output_sheet.title='Collaborate list'
for r in dataframe_to_rows(collaborate_data, index=True, header=True):
    Output_sheet.append(r)
Matches_table.save(filename=DATA_DIR / "5_Collaborate_Matches_Table.xlsx")   

# Add the new matches onto previous_matches
previous_matches=pd.read_excel(DATA_DIR + "2_Collaborate_previous_matches.xlsx")
previous_matches=pd.concat([previous_matches,matches1])
writer = pd.ExcelWriter(
    DATA_DIR / "2_Collaborate_previous_matches.xlsx",
    engine="xlsxwriter"
)
previous_matches.to_excel(writer)
writer.save()
writer.close()
