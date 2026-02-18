#------------------------------IMPORTING ALL THE LIBRARIES THAT I WILL NEED----------------------
import pandas as pd
import os
import csv
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np




#------------------------------LOADING AND READING THE DATA-------------------------------------------------
pathname=''

#From station data get list to itterate through to load data
with open('c:\\Users\\u23948711\\Desktop\\CODES FOR GITHUB\\SAAQIS DATA\\Station Info.csv', #Please change to your directory
          mode='r') as csv_file:
    listofstat = []
    linec=0
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        if linec>0:
            listofstat.append(row)
        linec+=1

station_boxplot_data = []
#Loop through list of stations 
for bigcount in range(len(listofstat)):
    #Create a dataframe to work with
    stat_name= listofstat[bigcount][0]
    Prov_name=listofstat[bigcount][6]
    station_type = listofstat[bigcount][3]
    data_availability_NO2 = float(listofstat[bigcount][7])
    data_availability_O3 = float(listofstat[bigcount][10])
    Startyear=2022

    
    sheetname='Report'
    years_with_data =[]
  
    pathname = Prov_name+'_'+stat_name+'_'+str(Startyear)+'.xlsx'
    work_book = pd.read_excel(os.path.join('c:\\Users\\u23948711\\Desktop\\CODES FOR GITHUB\\SAAQIS DATA\\DATA', #Please change to your directory
        pathname),sheetname,index_col=0,skiprows=[0,1,3,2,4],header=None)

    work_book2 = work_book.iloc[:, [0,3]]


    #------------------------------FIXING THE DATE TIME-------------------------------------------------
    """
    THIS HERE FIXES INDEX AND CONVERT DATE TIME 24:00 TO 00:00
    SAAQIS REPORTS DATA AS 24:00, THUS WE CONVERT TO STANDARD TIME, WHICH IS 00:00 (HERE 00:00 GOES TO THE NEXT DAY)
    """

    def convert_to_valid_time(date_string):
        time_part, date_part = date_string.split(' ')

        date = datetime.strptime(date_part, "%d/%m/%Y")

        if time_part == "24:00":
            date = date + timedelta(days=1)
            time_part = "00:00"

        time = datetime.strptime(time_part, "%H:%M")

        return date.replace(hour=time.hour, minute=time.minute)

    # WE APPLY THE TIME CORRECTIONS TO THE DATA
    work_book2.index = work_book2.index.map(convert_to_valid_time)



    # -----------------------------YEARS AND DATA SELECTION--------------------------------------------------------
    """
    USE THIS LINE ONLY WHEN YOU NEED TO FOCUS ON A PARTICULAR YEAR (2023 IN THIS CASE)
    THE OTHER LINES ONLY SELECTS COLUMN FOR NO2 AND O3, CAN ALWAYS PRINT TO SEE IF YOU HAVE SELECTED THE CORRECT COLUMN
    """

    # work_book2 = work_book2[work_book2.index.year == 2023] #2023
    # work_book2 = work_book2.iloc[:, 0] #NO2
    work_book2 = work_book2.iloc[:, 1] #O3


    #-----------------------------DATA AVAILABILITY----------------------------------------------------
    """
    THIS HELPS YOU ANALYSE DATA THAT MEETS A PARTICULAR THRESHOLD, FOR THIS CODE, >60% DATA CAPTURE IS CONSIDERED
    """

    # Calculate the total number of data points
    total_data_points = len(work_book2)

    # Calculate the total number of non-null data points
    total_non_null_data_points = work_book2.count()

    # Calculate data availability percentage for the entire dataset
    data_availability = (total_non_null_data_points / total_data_points) * 100

    if data_availability >= 60:
        station_data = work_book2.dropna()
        station_boxplot_data.append((stat_name, station_data))


# --------------------------------BOX AND WHISKER ALL DATA --------------------------------------------

# Sort listofstat by province name in the desired order: GP, LP, MP, NW, WC
#This line takes your list of stations and creates a new list sorted alphabetically by province name (from A to Z)
sorted_listofstat = sorted(listofstat, key=lambda x: x[6], reverse=False)  

# Define colors for each province
province_colors = {'GP': 'blue', 'LP': 'green', 'MP': 'red', 'NW': 'gray', 'WC': 'orange'}



#----THIS HERE IS THE SAME AS THE ACTIVE CODE BELOW, BUT THIS ONE PLOTS THE ANNUAL NAAQS AS WELL---

# NO2 = plt.figure(figsize=(10, 6))
# positions = []
# x_labels = []

# mean_legend_handler = Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=8, label='Mean')


# for entry in sorted_listofstat:
#     stat_name = entry[0]
#     Prov_name = entry[6]
#     data = next((data for name, data in station_boxplot_data if name == stat_name), None)
#     if data is not None and float(entry[7]) >= 60:  # Only plot if data and meets criteria
#         positions.append(len(positions))
#         x_labels.append(f"{stat_name}_{Prov_name}")  # Adjust the order of labels
#         plt.boxplot(data, positions=[positions[-1]], labels=[x_labels[-1]], widths=0.6,
#                     boxprops=dict(linewidth=1.5, color=province_colors.get(Prov_name, 'gray')),  # Assign color based on province
#                     medianprops=dict(linewidth=1.5, color=province_colors.get(Prov_name, 'gray')),
#                     showfliers=False, capprops=dict(color=province_colors.get(Prov_name, 'gray')),
#                     whiskerprops=dict(linewidth=1.5, color=province_colors.get(Prov_name, 'gray')))

#         # Calculate and plot mean as dots inside the box plot
#         mean_val = np.mean(data)
#         print(stat_name)
#         print(mean_val)
#         # plt.plot(positions[-1], mean_val, 'ro')
#         plt.plot(positions[-1], mean_val, marker='o', markersize=5, color=province_colors.get(Prov_name, 'gray'))

# # Add legend
# # plt.legend(handles=[mean_legend_handler])


# # NAAQS
# NAAQS_NO2 = 21  #NAAQS value for NO2
# # Add NAAQS line to the box plot
# plt.axhline(y=NAAQS_NO2, color='k', linestyle='--', linewidth=3)
# # Add NAAQS line to the plot
# NAAQS_NO2_legend_handler = plt.axhline(y=NAAQS_NO2, color='k', linestyle='--', linewidth=3, label='NAAQS')


# # #WHO AQGs
# # WHO_NO2 = 5

# # # Add NAAQS line to the box plot
# # plt.axhline(y=WHO_NO2, color='k', linestyle='--', linewidth=3)

# # # Add NAAQS line to the plot
# # WHO_NO2_legend_handler = plt.axhline(y=WHO_NO2, color='k', linestyle='--', label='WHO')


# # Create handles and labels for the legend
# all_handles = [mean_legend_handler, NAAQS_NO2_legend_handler]
# all_labels = ['Mean', 'NAAQS']

# # Add legend
# plt.legend(handles=all_handles, labels=all_labels, loc='upper right')
# ----------------------------------------------------------------------------------------------------------------

# # Create a box plot for each station on the same plot
O3 = plt.figure(figsize=(10, 6))
positions = []
x_labels = []

mean_legend_handler = Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=8, label='Mean')

for entry in sorted_listofstat: # Looking through the station information
    stat_name = entry[0] # station names, first element in the csv file
    Prov_name = entry[6] # Province name, 7th element in the csv file
    data = next((data for name, data in station_boxplot_data if name == stat_name), None) # This here finds the data for each station

    if data is not None: # When the data is found, this builds the x axis, with station and province name
        positions.append(len(positions))
        x_labels.append(f"{stat_name}_{Prov_name}")  # Adjust the order of labels


        """
        THE NEXT LINE OF CODE DOES THE FOLLOWING:
        - Plots each box individually
        - Manually positions them
        - Colors them by province
        - Hides outliers
        """

        plt.boxplot(data, positions=[positions[-1]], labels=[x_labels[-1]], widths=0.6,
                    boxprops=dict(linewidth=1.5, color=province_colors.get(Prov_name, 'gray')),  
                    medianprops=dict(linewidth=1.5, color=province_colors.get(Prov_name, 'gray')),
                    showfliers=False, capprops=dict(color=province_colors.get(Prov_name, 'gray')),
                    whiskerprops=dict(linewidth=1.5, color=province_colors.get(Prov_name, 'gray')))

        # Calculate and plot mean as dots inside the box plot
        mean_val = np.mean(data)
        plt.plot(positions[-1], mean_val, marker='o', markersize=5, color=province_colors.get(Prov_name, 'gray'))

# Add legend
plt.legend(handles=[mean_legend_handler])

# For NO2
# # plt.title('SAAQIS STATIONS - NO$_2$', loc='center', fontweight='bold') #If you need to add title for your plot
# plt.xlabel('Station Names', weight='bold')
# plt.ylabel('NO$_2$, ppb', fontweight='bold')

# FOR O3
# plt.title('SAAQIS STATIONS - O$_3$', loc='center', fontweight='bold') #If you need to add title for your plot
plt.xlabel('Station Names', weight='bold')
plt.ylabel('O$_3$, ppb', fontweight='bold')

plt.xticks(ticks=np.arange(len(x_labels)), labels=x_labels, rotation=45, ha='right')
plt.yscale('linear') # Use a linear scale for the y-axis


plt.grid(color='gray', linestyle='-', linewidth=0.5)
plt.tight_layout()
# plt.savefig(('O3_2022_2023 MEAN Boxplots'), dpi=1000) # SAVE
# plt.pause(2)
# plt.close()
plt.show()