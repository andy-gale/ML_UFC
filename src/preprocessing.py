import pandas as pd
import numpy as np
import os

"""
This contains methods for cleaning CSV files individually prior to merging and feature engineering.
run_all method will read in all CSVs, clean them, and return cleaned dataframes.

"""

def replace_placeholders(df): # Helper Function
    return df.replace(['--', '---'], np.nan)

def clean_event_details(df):
    df = replace_placeholders(df)
    df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce')
    return df

def clean_fight_details(df):
    df = replace_placeholders(df)
    df['EVENT'] = df['EVENT'].str.strip()
    return df

def clean_fight_results(df):
    df = replace_placeholders(df)
    df['EVENT'] = df['EVENT'].str.strip()
    df['WEIGHTCLASS'] = df['WEIGHTCLASS'].str.replace(' Bout', '')
    df['TIME'] = df['TIME'].str.split(':').apply(lambda x: int(x[0]) * 60 + int(x[1]) if isinstance(x, list) and len(x) == 2 else np.nan)
    df['TOTAL_TIME'] = (df['ROUND'] - 1) * 300 + df['TIME']
    return df

def clean_fight_stats(df):
    df = replace_placeholders(df)
    df['EVENT'] = df['EVENT'].str.strip()
    X_of_Y_cols = ['SIG.STR.', 'TOTAL STR.', 'TD', 'HEAD', 'BODY', 'LEG', 'DISTANCE', 'CLINCH', 'GROUND']
    for col in X_of_Y_cols:
        df[f'{col}_LANDED'] = df[col].str.split(' of ').apply(lambda x: int(x[0]) if isinstance(x, list) and len(x) == 2 else np.nan)
        df[f'{col}_ATT'] = df[col].str.split(' of ').apply(lambda x: int(x[1]) if isinstance(x, list) and len(x) == 2 else np.nan)
    df = df.drop(columns=X_of_Y_cols)
    df['CTRL'] = df['CTRL'].str.split(':').apply(lambda x: int(x[0]) * 60 + int(x[1]) if isinstance(x, list) and len(x) == 2 else np.nan)
    df['SIG.STR. %'] = pd.to_numeric(df['SIG.STR. %'].str.strip('%'), errors='coerce').fillna(0) / 100
    df['TD %'] = pd.to_numeric(df['TD %'].str.strip('%'), errors='coerce').fillna(0) / 100
    return df

def clean_fighter_details(df):
    df = replace_placeholders(df)
    return df

def clean_fighter_tott(df):
    df = replace_placeholders(df)
    df['HEIGHT'] = pd.to_numeric(df['HEIGHT'].str.replace('"', '').str.split("' ").apply(lambda x: int(x[0]) * 12 + int(x[1]) if isinstance(x, list) and len(x) == 2 else np.nan), errors='coerce')
    df['WEIGHT'] = pd.to_numeric(df['WEIGHT'].str.replace(' lbs.', ''), errors='coerce')
    df['REACH'] = pd.to_numeric(df['REACH'].str.replace('"', ''), errors='coerce')
    df['DOB'] = pd.to_datetime(df['DOB'], errors='coerce')
    # leaving 'STANCE' as is for now
    return df

def run_all(data_dir='../scraped_data/', save_dir='../cleaned_data/'): 
    event_details   = pd.read_csv(f'{data_dir}ufc_event_details.csv')
    fight_details   = pd.read_csv(f'{data_dir}ufc_fight_details.csv')
    fight_results   = pd.read_csv(f'{data_dir}ufc_fight_results.csv')
    fight_stats     = pd.read_csv(f'{data_dir}ufc_fight_stats.csv')
    fighter_details = pd.read_csv(f'{data_dir}ufc_fighter_details.csv')
    fighter_tott    = pd.read_csv(f'{data_dir}ufc_fighter_tott.csv')

    event_details   = clean_event_details(event_details)
    fight_details = clean_fight_details(fight_details)
    fight_results   = clean_fight_results(fight_results)
    fight_stats     = clean_fight_stats(fight_stats)
    fighter_details = clean_fighter_details(fighter_details)
    fighter_tott    = clean_fighter_tott(fighter_tott)

    os.makedirs(save_dir, exist_ok=True)
    
    event_details.to_csv(f'{save_dir}event_details.csv', index=False)
    fight_details.to_csv(f'{save_dir}fight_details.csv', index=False)
    fight_results.to_csv(f'{save_dir}fight_results.csv', index=False)
    fight_stats.to_csv(f'{save_dir}fight_stats.csv', index=False)
    fighter_details.to_csv(f'{save_dir}fighter_details.csv', index=False)
    fighter_tott.to_csv(f'{save_dir}fighter_tott.csv', index=False)

    return event_details, fight_details, fight_results, fight_stats, fighter_details, fighter_tott