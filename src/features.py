import pandas as pd
import numpy as np

"""
This takes our cleaned data and extras featrures into dataframe suitable for modeling.
Data filtered Nov 2000 and onward, based on when Unified Rules adopted and more consistent data recording.
"""

def build_fights(fight_results, event_details, fighter_tott):
    df = fight_results.copy()  
    df[['FIGHTER_1', 'FIGHTER_2']] = df['BOUT'].str.split(' vs. ', expand=True)
    df = df.merge(event_details[['EVENT', 'DATE']], on='EVENT', how='left')
    df = df.drop(columns=['BOUT', 'OUTCOME', 'DETAILS', 'REFEREE', 'URL'])
    df = df.drop(columns=['TIME', 'TIME FORMAT'])
    df = df.sort_values('DATE').reset_index(drop=True)
    df = df[df['DATE'] >= '2000-11-01'].reset_index(drop=True)
    
    fighter_tott_f1 = fighter_tott.add_prefix('F1_')
    fighter_tott_f2 = fighter_tott.add_prefix('F2_')
    df = df.merge(fighter_tott_f1, left_on='FIGHTER_1', right_on='F1_FIGHTER', how='left')
    df = df.merge(fighter_tott_f2, left_on='FIGHTER_2', right_on='F2_FIGHTER', how='left')
    df = df.drop(columns=['F1_FIGHTER', 'F2_FIGHTER', 'F1_URL', 'F2_URL', 'EVENT'])

    df['F1_AGE'] = (df['DATE'] - df['F1_DOB']).dt.days / 365.25
    df['F2_AGE'] = (df['DATE'] - df['F2_DOB']).dt.days / 365.25
    df = df.drop(columns=['F1_DOB', 'F2_DOB'])
    return df

def add_outcome_label(fight_results, event_details):
    df = fight_results.copy()
    df[['FIGHTER_1', 'FIGHTER_2']] = df['BOUT'].str.split(' vs. ', expand=True)
    df = df.merge(event_details[['EVENT', 'DATE']], on='EVENT', how='left')
    df['OUTCOME_LABEL'] = df['OUTCOME'].map({'W/L': 1, 'L/W': 0, 'D/D': 2, 'NC/NC' : np.nan})
    return df[['FIGHTER_1', 'FIGHTER_2', 'DATE', 'OUTCOME_LABEL']]
    
