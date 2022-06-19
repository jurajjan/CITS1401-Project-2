"""
Created on 10/05/2021

@author: Juraj Janekovic
"""


def input_format(country):
    """
    Function which capitalizes the country input
    """
    country = [country.capitalize() for country in country]
    
    return country
        
def read_file(csvfile):
    """
    Function reads and finds the amount of lines in the csv file inputted.
    """ 
    try:
        with open(csvfile) as myfile:
            my_lines = myfile.readlines()
            return my_lines
    except:
        return None
    

def find_indexes(header):
    """
    Function finds the indexes of the header and returns a list of indexes
    """
    header = header.strip('\n').split(',')
    header_col = ['continent','location','date','new_cases','new_deaths']
    indexes = []
    for s in header_col:
        if s not in header:
            return False
        indexes.append(header.index(s))
    return indexes

def get_all_list(my_lines, indexes):
    """
    Function which creates a list of all country values excluding ISO code
    """
    all_list = []
    for line in my_lines[1:]: 
        split_ln = line.strip('\n').split(',')   #splits and strips the line 
        tmp = [split_ln[i].lower() for i in indexes]  
        all_list.append(tmp)
    return all_list

def get_unique(all_list, index):
    """
    Function which finds unique countries or continents and appends to a list
    """
    data_list = []
    for x in all_list:
        x = x[index].lower()
        if x == 0:
            continue
        
        if x not in data_list:
            data_list.append(x)
    
    return data_list
        
        
def check_date(mydate):
    """
    Function validates date
    """
    if len(mydate) != 3:
        return False
    return True

def check_num_value(my_value):
    """
    Function validates the new cases and new deaths
    """
    try:
       tmp = int(my_value)             
    except ValueError:
        return 0
    if tmp < 0:
        return 0
    return tmp
            

def get_data(all_list, var, ind):
    """
    Functions returns a list of data from required header columns sorted by date (month)
    """
    tmp_list = [x[2:] for x in all_list if x[ind] == var]
    new_list = []
    for clist in tmp_list:
        mydate = clist[0].split('/')
        if not check_date(mydate):
            continue
        
        new_cases = check_num_value(clist[1])
        
        new_deaths = check_num_value(clist[2])
        new_list.append([mydate[1].zfill(2),new_cases,new_deaths])   #sets month to be at the front of string
        new_list.sort()
    return new_list
        

    return continent_list

def data_calculation(new_list, days_month=None):
    """
    Function performs all data calculations
    """
    total_new = []
    total_death = []
    avg_new = []
    avg_death = []
    
    for i in range (1,13):
        month = str(i).zfill(2)       #fills to 2 index spaces
        cases_new = [int(l[1])for l in new_list if l[0] == month]   # new cases per day
        if not cases_new:
            cases_new = [0]
        cases_death = [int(l[2])for l in new_list if l[0] == month]   # deaths cases per day
        if not cases_death:
            cases_death = [0]
        
        total_death.append(sum(cases_death))
        total_new.append(sum(cases_new))
        
        if not days_month: #calculates for country
            avg_values_death = sum(cases_death)/len(cases_death)
            avg_values_new = sum(cases_new)/len(cases_new)
        else: # calculates for continent to take account days in month
            avg_values_death = sum(cases_death)/days_month[i-1]
            avg_values_new =  sum(cases_new)/days_month[i-1]
            
        m_avg_deaths = greater_average(cases_death, avg_values_death)
        avg_death.append(m_avg_deaths)
               
        m_avg_new = greater_average(cases_new, avg_values_new)
        avg_new.append(m_avg_new)
        
    return(total_new, total_death, avg_new, avg_death)
    
    
def greater_average(mdata, avg):
    """
    Function returns counter for days larger than average
    """
    m_avg = 0
    for d in mdata:
        if d > avg:
            m_avg += 1
      
    return m_avg

    
def main(fname):
    """
    Main function of the program
    """
    country_dict = {}   #country dictionary
    continents_dict = {}  #continent dictionary
    if type(fname) != str:
        print ("Error: Main function invalid input")
        return (None,None)
    f_lines = read_file(fname)
    if f_lines == None:
        print("Error: File " "'{0}'" " not found".format(fname))
        return (None,None)
    if len(f_lines) < 2:
        print("Error: File " "'{0}'" " is empty".format(fname))
        return (None,None)
    header_idx = find_indexes(f_lines[0])
    if not header_idx:
        print("Error: Header columns not found in file " "'{0}'"  " or file is empty".format(fname))
        return(None,None)
    all_list = get_all_list(f_lines, header_idx)
    countries = get_unique(all_list, 1)
    continents = get_unique(all_list, 0)
    
    for country in countries:  # calculates data for country
        country_list = get_data(all_list, country, 1)
   
        total_new, total_deaths, avg_new, avg_death = data_calculation(country_list)
        country_dict[country] = [total_new,total_deaths,avg_new, avg_death]
    
     
    for continent in continents:   # calculates data for continent
        continent_list = get_data(all_list, continent, 0)
        days_month = [31,29,31,30,31,30,31,31,30,31,30,31]        # days in month table
        total_new, total_deaths, avg_new, avg_death = data_calculation(continent_list,days_month)
        continents_dict[continent] = [total_new,total_deaths,avg_new, avg_death]
       
    return country_dict, continents_dict
