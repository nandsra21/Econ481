# Exercise 0
def github() -> str:
    """
    my github repo
    """

    return "https://github.com/nandsra21/Econ481/blob/main/Problem_Set_3.py"

# Exercise 1
import pandas as pd

def import_yearly_data(years: list) -> pd.DataFrame:
    """
    Some docstrings.
    """
    df_list = []
    
    for year in years:
        temp = pd.read_excel(f"ghgp_data_{year}.xlsx", sheet_name="Direct Emitters", header=3, index_col=None)
        temp['year'] = year
        df_list.append(temp)

    final_df = pd.concat(df_list, ignore_index=True)
        
    return final_df

emissions_df = import_yearly_data([2019, 2020, 2021, 2022])

# Exercise 2

def import_parent_companies(years: list) -> pd.DataFrame:
    """
    Some docstrings.
    """
    df_list = []
    for year in years:
        temp = pd.read_excel("ghgp_data_parent_company_09_2023.xlsb", sheet_name=f"{year}", header=0, index_col=None, engine='pyxlsb')
        
        temp['year'] = year
        df_list.append(temp)

    final_df = pd.concat(df_list, ignore_index=True)
    
    final_df = final_df.dropna(subset=final_df.columns.difference(['year']), how="all")
    
    return final_df

parent_df = import_parent_companies([2019, 2020, 2021, 2022])

# Exercise 3

def n_null(df: pd.DataFrame, col: str) -> int:
    """
    Some docstrings
    """
    return df[col].isnull().sum()

n_null(parent_df, 'FRS ID (FACILITY)')
n_null(parent_df, 'GHGRP FACILITY ID')

# Exercise 4
def clean_data(emissions_data: pd.DataFrame, parent_data: pd.DataFrame) -> pd.DataFrame:
    """
    Some docstrings.
    """
    new_parent_df = parent_data.rename(columns={'GHGRP FACILITY ID': 'Facility Id'})
    
    merged_data = pd.merge(emissions_data, new_parent_df, how='left', 
                           left_on=['year', 'Facility Id'], 
                           right_on=['year', 'Facility Id'])

    
    # Subset the data to the specified variables
    subset_data = merged_data[['Facility Id', 'year', 'State', 'Industry Type (sectors)',
                               'Total reported direct emissions', 'PARENT CO. STATE',
                               'PARENT CO. PERCENT OWNERSHIP']]
    
    # Convert column names to lower case
    subset_data.columns = subset_data.columns.str.lower()
    
    return subset_data

cleaned_df = clean_data(emissions_df, parent_df)

# Exercise 5
def aggregate_emissions(df: pd.DataFrame, group_vars: list) -> pd.DataFrame:
    """
    Some docstrings.
    """
    
    agg_df = df.groupby(group_vars).agg(
        min_total_reported_direct_emissions=('total reported direct emissions', 'min'),
        median_total_reported_direct_emissions=('total reported direct emissions', 'median'),
        mean_total_reported_direct_emissions=('total reported direct emissions', 'mean'),
        max_total_reported_direct_emissions=('total reported direct emissions', 'max'),
        mean_parent_co_percent_ownership=('parent co. percent ownership', 'mean')
    ).reset_index()  # Resetting index to make group_vars columns again

    agg_df.sort_values(by='mean_total_reported_direct_emissions', ascending=False, inplace=True)

    return agg_df

aggregate_emissions(cleaned_df, ['state'])