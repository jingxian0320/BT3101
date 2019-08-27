############################################################################
#                                                                          #
#                           general population                             #
#                                                                          #
############################################################################

##########################################
#               reading csv              #
##########################################

# events
events_reader = pd.read_csv('../../Common Data/events.csv')
events = events_reader[['event_id','device_id']]

# app events
appevents_reader = pd.read_csv('../../Common Data/app_events.csv')
appevents = appevents_reader[['event_id','app_id','is_installed']]

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

##########################################
#        joining and aggregating         #
##########################################

appevent = appevents.merge(events,on='event_id')
appevent_label = appevent.merge(app_cat, on='app_id')
cols = list(appevent_label.columns.values)
appevent_label = appevent_label[['device_id','event_id','app_id','cat','is_installed']]
appevent_label = appevent_label.loc[appevent_label['is_installed'] == 1]
device_app_cat = appevent_label[['device_id','app_id','cat']]
device_app_cat = device_app_cat.drop_duplicates()
device_app_cat.to_csv('device_app_cat.csv',index=False)


############################################################################
#                                                                          #
#                               active user                                #
#                                                                          #
############################################################################

def sortBy(*args):
    data_sort = data
    for i in args:
        data_sort = data_sort[(data_sort[i]>X_quantile[i]) & (data_sort[i]>7)]
    return data_sort

X_quantile = X.quantile(.8)

cat_fin = sortBy('price','Finance').sort_index()['device_id']
cat_game = sortBy('Game').sort_index()['device_id']
cat_baby = sortBy('Babycare').sort_index()['device_id']
cat_edu = sortBy('Education').sort_index()['device_id']
cat_life = sortBy('Lifestyle').sort_index()['device_id']

data = pd.read_csv('../ETL output/device_app_cat.csv')

cat_fin = cat_fin.to_frame()
fin = cat_fin.merge(device_app_cat, on='device_id')
cat_game = cat_game.to_frame()
game = cat_game.merge(device_app_cat, on='device_id')
cat_baby = cat_baby.to_frame()
baby = cat_baby.merge(device_app_cat, on='device_id')
cat_edu = cat_edu.to_frame()
edu = cat_edu.merge(device_app_cat, on='device_id')
cat_life = cat_life.to_frame()
life = cat_life.merge(device_app_cat, on='device_id')

fin.to_csv('fin.csv', index=False)
game.to_csv('game.csv', index=False)
baby.to_csv('baby.csv', index=False)
edu.to_csv('edu.csv', index=False)
life.to_csv('life.csv', index=False)
