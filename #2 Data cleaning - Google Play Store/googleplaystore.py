#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 22:13:52 2019

@author: archanavillalba
"""


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


category=input('Enter an app caterory from the list below: FAMILY, GAME, TOOLS, MEDICAL, BUSINESS, PRODUCTIVITY, PERSONALIZATION, COMMUNICATION, SPORTS, LIFESTYLE, FINANCE, HEALTH_AND_FITNESS, PHOTOGRAPHY, SOCIAL, NEWS_AND_MAGAZINES, SHOPPING, TRAVEL_AND_LOCAL,DATING, BOOKS_AND_REFERENCE, VIDEO_PLAYERS, EDUCATION, ENTERTAINMENT, MAPS_AND_NAVIGATION, FOOD_AND_DRINK, HOUSE_AND_HOME, LIBRARIES_AND_DEMO, AUTO_AND_VEHICLES, WEATHER, ART_AND_DESIGN, EVENTS, COMICS, PARENTING, BEAUTY : ')
title='Top 10 App Install in Google Play for the category '+ str(category)

def acquisition():
    data=pd.read_csv(r'/Users/archanavillalba/Data/Data-cleaning-project/googleplaystore.csv')
    return data

def wrangling(df):
    
    df['Rating']=df['Rating'].fillna(0)
    df['Type']=df['Type'].fillna(0)
    df.loc[df.Type==0,'Type']='Free'
    df['Content Rating']=df['Content Rating'].fillna(0)
    df['Current Ver']=df['Current Ver'].fillna(0)
    df['Android Ver']=df['Android Ver'].fillna(0)
    df.loc[df.Category=='1.9','Category']='LIFESTYLE'
    df=df.drop(['Genres'], axis=1)
    df.loc[df.Rating==19.0,'Rating']=2.5
    df.drop(df.loc[(df.Installs=='0+') | (df.Installs=='Free') | (df.Installs=='0')].index, axis=0, inplace=True)
    df['Installs'].replace(regex=True,inplace=True,to_replace=r'[,*+]',value=r'')
    df['Installs'] = df['Installs'].astype('int')
    df['Price'].replace(regex=True,inplace=True,to_replace=r'[$]',value=r'')
    df['Price'] = df['Price'].astype('float64')
    df['Android Ver'].replace(regex=True,inplace=True,to_replace=r'\s[a-z]{3}\s[a-z]{2}',value=r'')
    df['Android Ver'].replace(regex=True,inplace=True,to_replace=r'\s\D\s[0-9]\D[0-9]?\D?[0-9]',value=r'')
    df.loc[df['Android Ver']=='4.4W','Android Ver']='4.4'
    df=df.drop(['Price'], axis=1)
    df['Size'].replace(regex=True,inplace=True,to_replace=r'[k]',value=r'000')
    df['Size'].replace(regex=True,inplace=True,to_replace=r'[M]',value=r'000000')
    df['Size'].replace(regex=True,inplace=True,to_replace=r'[A-Za-z]{6}\s[a-z]{4}\s[A-Za-z]{6}',value=r'0')
    df['Size'].replace(regex=True,inplace=True,to_replace=r'\D',value=r'')
    df['Size']=df['Size'].astype('int')
    mpg_labels=['Very Small','Small','Moderate','Big','Very Big']
    bins=pd.cut(df.Size,[0,100000,2000000,10000000,25000000,50000000],labels=mpg_labels)
    df['Size bins']=pd.cut(df.Size,5,labels=mpg_labels)
    df.loc[df.Size==0,'Size']='Varies with device'
    df.drop_duplicates(inplace=True)
    df.drop_duplicates(subset =['App','Installs'],inplace = True)
    
    filtered=df[df.Category==category].copy()
    return filtered

def analyze(df):
    result=filtered.sort_values(by=['Installs'],ascending=False).head(10)
    return result

def viz(df):
    fig,ax=plt.subplots(figsize=(6,15))
    barchart=sns.barplot(data=result,x='Installs',y='App')
    plt.title(title+'\n',fontsize=16)
    sns.set_style('white')
    plt.show()
    return barchart

def save_viz(chart):
    fig=barchart.get_figure()
    fig.savefig(title+'.png')
    
if __name__=='__main__':
    data=acquisition()
    filtered=wrangling(data)
    result=analyze(filtered)
    barchart=viz(result)
    save_viz(barchart)