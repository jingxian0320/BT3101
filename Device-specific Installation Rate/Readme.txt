## Author: Liu Yue
## Date: 7/11/2016
## Python Version: Anaconda 4.2.0, python 3.5
## XAMPP Version: 3.2.1; MySQL Version: 5.6.21


S0_Data Cleaning_TalkingData.sql  (Operations on MySQL database)
Description: 
This script is to clean data to ensure each device is with recorded and labelled app events. List of device_model and list of brands are obtained.
Input file: 
events.csv; app_labels.csv; app_events.csv; phone_brand_device_model.csv
Output file: 
S0_device_model_count.csv; S0_tk_phone_brand.csv
*The entire database is saved in liuyue.sql

S1_TalkingData brands on ZOL_jupyter.ipynb(Data Scraping)
Description: 
ZOL is a Chinese cite for phone comparison/blogging/selling
On the phone-list page, we are able to get link to phone-homepage and specifications
This script gets the link to phone-list pages of various brands in TalkingData Kaggle Challenge dataset
Input file: 
S0_tk_phone_brand.csv
Output file: 
S1_zol phone brand link.csv

S2_zol phone model link_jupyter.ipynb(Data Scraping)
Description: 
This script gets the all names of and links to device models
Input file: 
S1_zol phone brand link.csv
Output file: 
S2_zol phone model link.csv; S2_zol tablet model link.csv

S3_zol match device model_jupyter.ipynb
Description: 
This script matches the names of device models on ZOL and on TalkingData  Input file: 
S0_device_model_count.csv; S2_zol phone model link.csv; S2_zol tablet model link.csv
Output file: 
S3_zol phone match device model_rough.csv

S4_zol match device model checked_jupyter.ipynb
Description:
This script describes the list of device models found on ZOL
Input file: 
S4_zol phone match device model.csv

S5_zol phone device specification_jupyter.ipynb(Data Scraping)
Description:
This script gets technical specifications of phones/tablets from web page link
Input file: 
S4_zol phone match device model.csv
Output file: 
S5_zol phone device specification.csv

S6_inital model_data merging_jupyter.ipynb
Description:
This script merges datasets from ZOL and from TalkIngData. Initial model is explored to test the feasibility of kNN and CF
Input file: 
S5_zol phone device specification.csv; S0_device_model_count.csv; tencent_game_device_id.csv; phone_brand_device_model.csv
Output file: 
S6_device model details.csv

S7_device model priotization_jupyter.ipynb
Description:
This script runs model for devce model prioritization, by checking the best cut-off for device_id_count with RMSE for only measuring top device models
Input file: 
S6_device model details.csv

S8_feature selection_jupyter.ipynb
Description:
This script runs feature selections from 511 subsets
Input file: 
S6_device model details.csv

S9_feature selected_device model priotization_jupyter.ipynb
This script runs model for devce model prioritization, by checking the best cut-off for device_id_count with RMSE for only measuring top device models, using results from S8, with 4 attributes
Input file: 
S6_device model details.csv
