#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 16:44:25 2020

@author: baharehharandizadeh
"""

#change to json format

import json 
import typer



    
def merge_items(index,links):
    new_index = []
    new_links = []
    if(len(links)==1):
      new_index = index
      new_links = links
    elif(len(links)==0):
      new_index = []
      new_links = []
    else:

      previous_link = links[0]
      first = index[0][0]
      last = index[0][1]
      for indx in range(1,len(index)):
        if (index[indx][0] == index[indx-1][1]+1) and (links[indx]==links[indx-1]):
              last = index[indx][1]
              previous_link = links[indx]
        else:
          new_index.append([first,last])
          new_links.append(previous_link)
          first = index[indx][0]
          last = index[indx][1]
          previous_link = links[indx]
      new_index.append([first,last])
      new_links.append(previous_link)
      
    return new_index,new_links
    


def main()-> None:
    
    with open('Tweeki_gold') as f:
        ff = f.read().strip()
        sentences = ff.split('\n\n')
         
    with open('Tweeki_gold.jsonl' ,'w') as f:
       id = 1000
       for sen in sentences:     
           lines = sen.split('\n')
           sen_j={}
           index = []
           links = []
           words = []
           w_ind = 0

           for l in lines[2:]:
              segment = l.split('\t')
              words.append(str(segment[1]))
              if(segment[3]!='-'):
                  links.append(str(segment[3]))
                  index.append([w_ind,w_ind+len(segment[1])])
              w_ind+=len(segment[1])+1

           
           sen_j["id"] = id
           sen_j["sentence"] = ' '.join(words)
           index, links = merge_items(index,links)
           sen_j["index"] = index
      
           sen_j["link"] = links
           json.dump(sen_j,f)

           f.write('\n')
           id+=1
    
    


if __name__ == "__main__":
    typer.run(main)

