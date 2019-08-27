import pandas
# load data
labels = pandas.read_csv("../Common Data/label_categories.csv")
app_labels = pandas.read_csv("../Common Data/app_labels.csv")
app_events = pandas.read_csv('../Common Data/app_events.csv')
events = pandas.read_csv('../Common Data/events.csv')
print 'Data loading completed!'

#label_id category
#     794  Tencent

cat_id = set([794])
tencent_game_cate = labels[labels['label_id'].isin(cat_id)]
print tencent_game_cate

# find app_ids containing 'Tencent'
tencent_game_app_ids = app_labels[app_labels['label_id'].isin(cat_id)]
tencent_game_app_ids = tencent_game_app_ids['app_id']
tencent_game_app_ids = tencent_game_app_ids.drop_duplicates()
print 'no. of distinct tencent_game app ids: '
print tencent_game_app_ids.shape[0]
tencent_game_app_ids.to_csv('tencent_game_app_ids.csv',index=False)

# find all app events having tencent apps installed
tencent_game_app_events = app_events[app_events['app_id'].isin(tencent_game_app_ids)]
tencent_game_event_ids = tencent_game_app_events['event_id'].drop_duplicates()
print 'no. of distinct tencent_game events: '
print tencent_game_event_ids.shape[0]
tencent_game_app_events.to_csv('tencent_game_installed_app_events.csv',index=False)

# installed_app_events: all app_events having tencent_game installed
installed_app_events = tencent_game_app_events
print 'installed_app_events'
print installed_app_events.shape[0]

# active_app_events: all app_events having active tencent_game
active_app_events = installed_app_events.loc[installed_app_events['is_active'] == 1]
print 'active_app_events'
print active_app_events.shape[0]

# find all event_ids having tencent apps installed
tencent_game_device_ids = events[events['event_id'].isin(tencent_game_event_ids)]

# according to event_id, find all distinct device that installed tencent apps
tencent_game_device_ids = tencent_game_device_ids['device_id'].drop_duplicates()
print 'no. of distinct tencent_game decives: '
print tencent_game_device_ids.shape[0]
tencent_game_device_ids.to_csv('tencent_game_device_id.csv',index=False)

# tencent_game_events: all events belonging to tencent_game devices (containing those not inside app_events)
tencent_game_events = events.loc[events['device_id'].isin(tencent_game_device_ids)]
# tencent_game_events: [device_id, event_id,timestamp]
tencent_game_events = tencent_game_events[['device_id','event_id','timestamp']]
print 'tencent_game_events:'
print tencent_game_events.shape[0]

tencent_game_app_events = app_events.loc[app_events['event_id'].isin(tencent_game_events['event_id'])]
print 'tencent_game_app_events:'
print tencent_game_app_events.shape[0]

# tencent_game_events: all events belonging to tencent_game devices (excluding those not inside app_events)
tencent_game_events = tencent_game_events.loc[tencent_game_events['event_id'].isin(tencent_game_app_events['event_id'])]
print 'tencent_game_events(excluding those not inside app_events):'
print tencent_game_events.shape[0]


# find the last event of each device
tencent_game_events_sorted = tencent_game_events.sort_values(by = ['timestamp'],ascending = False)
tencent_game_events_last = tencent_game_events_sorted.drop_duplicates(subset = ['device_id'], keep = 'first')
print 'tencent_game_events_last'
print tencent_game_events_last.shape[0]

# check number of apps installed in the first event
tencent_game_events_first = tencent_game_events_sorted.drop_duplicates(subset = ['device_id'], keep = 'last')
first_app_events = app_events[app_events['event_id'].isin(tencent_game_events_first['event_id'].values)]
first_count_app_events = first_app_events['event_id'].value_counts()
first_count_app_events = first_count_app_events.to_frame(name = 'installed_app_count')
first_count_app_events['event_id'] = first_count_app_events.index
tencent_game_events_first = pandas.merge(tencent_game_events_first, first_count_app_events, on = 'event_id')
tencent_game_events_first = tencent_game_events_first[['device_id','installed_app_count']]

# check if the last event has tencent_games installed
tencent_game_events_last['is_churner_uninstalled'] = -tencent_game_events_last['event_id'].isin(installed_app_events['event_id'])

tencent_game_is_churn = tencent_game_events_last[['device_id','is_churner_uninstalled']]
tencent_game_is_churn = pandas.merge(tencent_game_is_churn, tencent_game_events_first, on = 'device_id')
print tencent_game_is_churn.head()

tencent_game_is_churn['is_churner_inactive'] = pandas.Series()

def check_inactive(row):
    row['is_churner_inactive'] = True
    device_tencent_game_events = tencent_game_events.loc[tencent_game_events['device_id'] == row['device_id']]
    for event in device_tencent_game_events['event_id']:
        if event in active_app_events['event_id']:
            row['is_churner_inactive'] = False
            break
    return row
tencent_game_is_churn = tencent_game_is_churn.apply(check_inactive, axis = 1)
print tencent_game_is_churn.head()
#tencent_game_is_churn.drop(['is_churner_inactive','in_churner_uninstalled'],1)
tencent_game_is_churn.to_csv('tencent_game_is_churner.csv')
