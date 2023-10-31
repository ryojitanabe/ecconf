#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pylab as plt
import numpy as np
import pandas as pd

# the width value w of bars should be large for biannual conferences    
width_vals = {'gecco':0.6, 'cec':0.6, 'eurogp':0.6, 'ppsn':1., 'emo':1., 'foga': 1., 'evocop':0.6, 'evomusart':0.6, 'evoapp':0.6, 'gecco_poster':0.6}
# this sets the y-limit for the acceptance rate. I notice that setting this kind of values manually is not efficient.
accrate_max_vals = {'gecco':55, 'cec':80, 'eurogp':80, 'ppsn':60, 'emo':90, 'foga':70, 'evocop':80, 'evomusart':90, 'evoapp':80, 'gecco_poster':90}
# this sets the offset value of the position of a text for the number of submission/acceptance papers
y_bar_offset_vals = {'gecco':30, 'cec':50, 'eurogp':3, 'ppsn':20, 'emo':8, 'foga':2, 'evocop':4, 'evomusart':2, 'evoapp':8, 'gecco_poster':30}

def plot_stats(conference):
    fig = plt.figure(figsize=(13, 6))
    ax = plt.subplot(111)
    ax.set_rasterization_zorder(1)    

    data_file = 'data/%s.csv' % (conference)
    df = pd.read_csv(data_file, index_col=False, delimiter=r",\s*", engine="python")
    df = df.rename(columns={'Year': 'year', 'Submission': 'submission', 'Acceptance': 'acceptance', 'Acceptance rate': 'arate', 'Place': 'place'})
    df['arate'] = df['arate'].str.replace('%', '')
    df['arate'] = pd.to_numeric(df['arate'])

    w = width_vals[conference]    
    ax.bar(df.year, df.submission, width=w, label='Submissions')
    ax.bar(df.year + w/5, df.acceptance, width=w, label='Acceptances')
    ax.set_xticks(df.year + 0)
    
    year_list = df.year.values.tolist()
    year_place = []
    for i, year in enumerate(year_list):
        year_place.append(str(year) + '\n' + df.place[i])
    ax.set_xticklabels(year_place, fontsize=10)
    labels = ax.get_xticklabels()
    plt.setp(labels, rotation=-90);

    y_pos_offset = y_bar_offset_vals[conference]    
    for x, y in zip(df.year, df.submission):
        tmp = 0
        if not np.isnan(y):
            tmp = int(y)
        plt.text(x, y-y_pos_offset, tmp, ha='center', va='bottom')
    for x, y in zip(df.year, df.acceptance):
        tmp = 0
        if not np.isnan(y):
            tmp = int(y)
        plt.text(x + w/5, y-y_pos_offset, tmp, ha='center', va='bottom')
    ax2 = ax.twinx()
    ax2.plot(df.year, df.arate.astype(float), '#2ca02c', marker='s', label='Acceptance rate')
    ax2.set_ylim(0, accrate_max_vals[conference])
    
    for x, y in zip(df.year, df.arate):
        tmp_str = '{:.0%}'.format(0.01*y)
        plt.text(x + 0, y+0.5, tmp_str, ha='center', va='bottom')
            
    ax.set_ylabel("Submissions / acceptances", fontsize=20)
    ax2.set_ylabel("Acceptance rate", fontsize=20, rotation=270, labelpad=30) 
    
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1+h2, l1+l2, fontsize=15, loc='upper right', bbox_to_anchor=(0.9, 1.13), ncol=3)

    #ax.set_rasterization_zorder(-5)
    
    fig_name = 'fig/stats_%s.png' % (conference)
    plt.savefig(fig_name, bbox_inches="tight")
    plt.close()
    
if __name__ == '__main__':
    #for conference in ['ppsn', 'gecco', 'cec', 'foga', 'emo', 'eurogp', 'evocop', 'evomusart', 'evoapp']:    
    for conference in ['cec']:
        plot_stats(conference)
