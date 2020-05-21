#print("test hellooooo")
#print("changes on the local computer 1")
#-------------------------------------------libraries--------------------------------
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
#import descartes
import pyodbc
import numpy as np
import sys
from copy import copy
from tkinter import *
import tkinter as tk
from tkinter import ttk

#-------------------------making the window------------------------

my_window=Tk()
my_canvas=Canvas(my_window, width=300, height=300,background='white')
my_canvas.grid(row=0, column=0)


# -------------function run_query()---------called by button 1--------


# (result1, result2) = choices.get(key, ('default1', 'default2'))

def run_query():
    variable = my_combobox.get()
    (result1, result2) = choices.get(variable, ('default1', 'default2'))
    print(result1)
    print(result2)

# ----------------------combo box------------------------


deases_lst = ['deases1', 'deases2', 'deases3', 'deases4', 'deases5', 'deases6'
              , 'deases7', 'deases8', 'deases9', 'deases10', 'deases11', 'deases12'
              , 'deases13', 'deases14', 'deases15', 'deases16', 'deases17', 'deases18']

choices = {'deases1': (1, 1399), 'deases2': (140, 2399), 'deases3': (240, 2799),
           'deases4': (280, 2899),'deases5': (290, 3199),'deases6': (320, 3599),
           'deases7': (360, 3899),'deases8': (390, 4599),'deases9': (460, 5199),
           'deases10': (520, 5799),'deases11': (580, 6299),'deases12': (630, 6799),
           'deases13': (680, 7099),'deases14': (710, 7399),'deases15': (740, 7599),
           'deases16': (760, 7799),'deases17': (780, 7999),'deases18': (800, 9999)
           }

my_str_var = tk.StringVar()
my_combobox = ttk.Combobox(my_window, textvariable=my_str_var, values=deases_lst)
my_combobox.grid(row=0, column=0)

# ----------------------button 1------------------------

button1 = ttk.Button(my_window, text="Show Query Results",
                     command=lambda: run_query())
button1.grid(row=1, column=0)

#---------------------------------------

conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=D:/WSU FY2012 OP.mdb;')
cursor = conn.cursor()

# ------------------------SQL command--------------------------------------
#example inputs to test the query:
a_v_min = "V140"
a_v_max = "V230"
a_e_min = "E140"
a_e_max = "E230"
a_min = 140
a_max = 230

sql_command = '''SELECT [FIPS County Code Table].[County Name], [WSU_OP_Diagnosis].[DIAG]  FROM 
(
    ([WSU_OP_Diagnosis] INNER JOIN [WSU_OP_Demographics] ON [WSU_OP_Diagnosis].[CNTRL] = [WSU_OP_Demographics].[CNTRL]) 
        INNER JOIN 
    [FIPS County Code Table] 
        ON [WSU_OP_Demographics].[statecounty] = [FIPS County Code Table].[FIPS_Code]
) 
WHERE 
(
    (
        ([WSU_OP_Diagnosis].[DIAG]) > ? & ([WSU_OP_Diagnosis].[DIAG]) < ?
    ) 
    & 
    (
        ([FIPS County Code Table].[State])='Kansas'
    )
) 
OR 
(
    (
        ([WSU_OP_Diagnosis].[DIAG])> ? & ([WSU_OP_Diagnosis].[DIAG])< ?
    ) 
    & 
    (
        ([FIPS County Code Table].[State])='Kansas'
    )
)
OR
(
    (
        ([WSU_OP_Diagnosis].[DIAG])> ? & ([WSU_OP_Diagnosis].[DIAG])< ?
    )  
    & 
    (
        ([FIPS County Code Table].[State])='Kansas'
    )
)
ORDER BY [FIPS County Code Table].[County Name]; '''



#------for the sake of time saving during test running, i comment this part for now:

#cursor.execute(sql_command, (a_v_min, a_v_max, a_e_min, a_e_max, a_min, a_max))

#for row in cursor.fetchall():
#    print(row)
#--------------------------------------------------------
gdf=gpd.read_file('GU_CountyOrEquivalent.shp')
df = pd.DataFrame(gdf)
df_seg=pd.read_csv("seg.csv")
new_df = df[df["State_Name"] == 'Kansas' ]
new_df.reset_index(drop=True, inplace=True)
merge_df=pd.merge(new_df, df_seg, left_on='County_Nam', right_on='County', how='inner')

gdf2 = gpd.GeoDataFrame(merge_df)

gdf2['coords'] = gdf2['geometry'].apply(lambda x: x.representative_point().coords[:])
gdf2['coords'] = [coords[0] for coords in gdf2['coords']]

#print(gdf.shape)
#print(gdf.head())
#gdf2.plot(column='County_Nam')

print(gdf2.head())
plt.rcParams['figure.figsize']=(20,15)
ax = gdf2.plot(column='Segment')
gdf2.apply(lambda x: ax.annotate(s=x.County_Nam, xy=x.geometry.centroid.coords[0], ha='center'),axis=1)
plt.show()

seg2=merge_df[['County_Nam','Segment']]
print(merge_df[['County_Nam','Segment']])
seg2.to_csv('seg2_out.csv',encoding='utf-8')
#new_df.to_csv('new-df.csv',encoding='utf-8')
print(new_df.head())


#----------------------running ----------------------

my_window.mainloop()