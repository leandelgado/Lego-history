#!/usr/bin/env python
# coding: utf-8

# ## # Introduction
# <p><img src="https://assets.datacamp.com/production/project_981/img/lego_unsplash.jpg" alt="A picture of Lego characters!"></p>
# <h3 id="letslookatlegosets">Let's look at Lego sets!</h3>
# <p>Lego is a household name across the world, supported by a diverse toy line, hit movies, and a series of successful video games. In this project, we are going to explore a key development in the history of Lego: the introduction of licensed sets such as Star Wars, Super Heroes, and Harry Potter.</p>
# <p>It may not be widely known, but Lego has had its share of ups and downs since its inception in the early 20th century. This includes a particularly rough period in the late 90s. As described in <a href="https://www.businessinsider.com/how-lego-made-a-huge-turnaround-2014-2?r=US&IR=T">this article</a>, Lego was only able to survive due to a successful internal brand (Bionicle) and the introduction of its first licensed series: Star Wars. In the instructions panel are the two questions you will need to answer to complete this project.</p>
# <p>Before diving into our analysis though, let's become familiar with the two datasets that will help you with this project:<br><br></p>
# <div style="background-color: #ebf4f7; color: #595959; text-align:left; vertical-align: middle; padding: 15px 25px 15px 25px; line-height: 1.6;">
#     <div style="font-size:20px"><b>datasets/lego_sets.csv</b></div>
# <ul>
#     <li><b>set_num:</b> A code that is unique to each set in the dataset. <b><i>This column is critical, and a missing value indicates the set is a duplicate or invalid!</i></b></li>
#     <li><b>set_name:</b> A name for every set in the dataset (note that this can be the same for different sets).</li>
#     <li><b>year:</b> The date the set was released.</li>
#     <li><b>num_parts:</b> The number of parts contained in the set.<b><i> This column is not central to our analyses, so missing values are acceptable.</i></b></li>
#         <li><b>theme_name:</b> The name of the sub-theme of the set.</li>
#     <li><b>parent_theme:</b> The name of the parent theme the set belongs to. Matches the `name` column of the `parent_themes` csv file.</li>
# </ul>
# 
# <div style="font-size:20px"><b>datasets/parent_themes.csv</b></div>
# <ul>
#     <li><b>id:</b> A code that is unique to every theme.</li>
#     <li><b>name:</b> The name of the parent theme.</li>
#     <li><b>is_licensed:</b> A Boolean column specifying whether the theme is a licensed theme.</li>
# </ul>
#     </div>
# <p>From here on out, it will be your task to explore and manipulate the existing data until you are able to answer the two questions described in the instructions panel. Feel free to add as many cells as necessary. Finally, remember that you are only tested on your answer, not on the methods you use to arrive at the answer!</p>
# <p><em><strong>Note:</strong> If you haven't completed a DataCamp project before you should check out the <a href="https://projects.datacamp.com/projects/33">Intro to Projects</a> first to learn about the interface. In this project, you also need to know your way around <code>pandas</code> DataFrames and it's recommended that you take a look at the course <a href="https://www.datacamp.com/courses/data-manipulation-with-pandas">Data Manipulation with pandas</a>.</em></p>

# In[30]:


import pandas as pd
import numpy as np

sets=pd.read_csv("datasets/lego_sets.csv")
parent=pd.read_csv("datasets/parent_themes.csv")

#Count Na values and check uniques from "set_num"
display(sets.set_num.isna().sum())
display(sets.set_num.value_counts().sort_values(ascending=False))

#Drop missing values (duplicate or invalid) and drop "num_parts" column
sets.drop(columns="num_parts", inplace=True)
sets.dropna(subset=["set_num"], inplace=True)
display(sets.set_num.isna().sum())

#Joining sets
sets_parent = sets.merge(parent, how="left", left_on="parent_theme",                          right_on="name")

#Calculating % Star Wars themed
sets_parent_lic = sets_parent[sets_parent["is_licensed"] == True]
the_force = sets_parent_lic[sets_parent_lic["name_y"].str.            contains("Star Wars")].shape[0] / sets_parent_lic.shape[0]
the_force = int(the_force * 100)


#Grouping and counting
unique_years = pd.DataFrame(sets_parent_lic["year"].unique()).                            sort_values(by=0, ignore_index=True)
unique_years.columns = ["Year"]

for count, year in enumerate(unique_years["Year"]):
    SW = sets_parent_lic[(sets_parent_lic["year"] == year) &         (sets_parent_lic["name_y"].str.contains("Star Wars"))].shape[0] 
    Total = sets_parent_lic[sets_parent_lic["year"] == year].shape[0]
    unique_years.loc[count, "pctg"] = SW / Total 

min = unique_years["pctg"].min()
new_era = int(unique_years[unique_years["pctg"] == min]["Year"])

#Results
display(the_force, new_era)
    


    


# In[ ]:





# In[31]:


get_ipython().run_cell_magic('nose', '', '\ndef test_force():\n    assert(int(the_force) != 45), \\\n        "Have you properly inspected your data and dealt with missing values appropriately?"\n    assert(int(the_force) != 50), \\\n        "Have you dropped the relevant missing rows? Remember, not all rows with missing values need to be dropped!"\n    assert int(the_force) == 51 or int(the_force) == 52, \\\n        "Have you correctly calculated the percentage of licensed sets that belonged to the Star Wars theme?"\n\ndef test_new_era():\n    assert((type(new_era)==int) & (len(str(new_era))==4)), \\\n        "Have you entered the year in which Star Wars was not the most popular theme as a four digit integer?"\n    assert int(new_era) == 2017, \\\n        "Have you correctly calculated the year in which Star Wars was no longer the most popular set?"')

