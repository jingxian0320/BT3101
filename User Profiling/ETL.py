############################################################################
#                                                                          #
#                                  ETL                                     #
#                                                                          #
############################################################################

import pandas as pd
import csv

##########################################
#               reading csv              #
##########################################

# events
events_reader = pd.read_csv('../../Common Data/events.csv')
events = events_reader[['event_id','device_id']]

# app events
appevents_reader = pd.read_csv('../../Common Data/app_events.csv')
appevents = appevents_reader[['event_id','app_id','is_active']]

# app category
relabel_apps = []
with open('../Dataset/relabel_apps.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        if(row[0]!='app_id'):
            row[0]=int(row[0])
        relabel_apps.append(row)
del relabel_apps[0]
app_cat = pd.DataFrame(relabel_apps, columns=['app_id','cat'])

# gender age
demo_reader = pd.read_csv('../../Common Data/gender_age_train.csv')
demo_train = demo_reader[['device_id','gender','age']]

# device price 
model_reader = pd.read_csv('../Dataset/device_model_count.csv',sep=';', header=None)
model = model_reader[[0,1,2]]
model = model.rename(columns={0: "assigned_index", 1: "brand", 2:"model"})

specification = pd.read_csv('../Dataset/specification.csv', header=None)
price = specification[[0,10]]
price = price.rename(columns={0: "assigned_index", 10: "price"})
price = price.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)
price = price.groupby(['assigned_index'])['price'].mean().to_frame(name = 'price').reset_index()
device_price = model.merge(price, on='assigned_index')

device = pd.read_csv('../../Common Data/phone_brand_device_model.csv')
device = device.rename(columns={"phone_brand":"brand","device_model":"model"})


##########################################
#              joining table             #
##########################################

# device and price
device_info = device.merge(device_price, on = ["brand","model"])
device_info = device_info[['device_id','price']]

# device_info with gender_age
demographic = device_info.merge(demo_train, on='device_id')

# events, app_events and labels
appevent = appevents.merge(events,on='event_id')
appevent_label = appevent.merge(app_cat, on='app_id')


##########################################
#        aggregating and pivoting        #
##########################################
cols = list(appevent_label.columns.values)
appevent_label=appevent_label[['device_id','event_id','app_id','cat','is_active']]
cat_rate = appevent_label.groupby(['device_id','cat'])['is_active'].sum().to_frame(name = 'rate').reset_index()

cat_rate = cat_rate.pivot(index='device_id', columns='cat', values='rate')
cat_rate = cat_rate.fillna(0)
cat_rate['device_id'] = cat_rate.index

result = cat_rate.merge(demographic, on='device_id')
cols = list(result.columns.values)

cols = cols[len(cols)-4:len(cols)] + cols[0:len(cols)-4]
result = result[cols]

result[cols[4:len(cols)]] = result[cols[4:len(cols)]].astype(int)
result = result.drop_duplicates()
result['price']=result['price'].astype(int)

result.to_csv('data.csv', index=False) ## dataset for clustering

