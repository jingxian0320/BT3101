import pandas
import re
churner = pandas.read_csv('tencent_game_is_churner.csv')
data = pandas.read_csv('device_cat_rate.csv',sep = '\t').drop_duplicates('device_id')
device = pandas.read_csv('phone_brand_device_model.csv')

churner_data = pandas.merge(churner,data,how = 'inner',on='device_id')
churner_data_device = pandas.merge(churner_data,device,how = 'inner',on='device_id')




device_model_count = pandas.read_csv('device_model_count.csv',sep = ';',header=None,names = ['assigned index', 'phone_brand', 'device_model', 'count_devicde_id'])
device_spec = pandas.read_csv('S5_zol phone device specidication__13 error url.csv',header=None,names = ['assigned index', 'zol index', 'screen_size', 'screen_resolution', 'front_camera_pixel', 'back_camera_pixel', 'core_num', 'ram_mb', 'battery_mah', 'age_month', 'price_rmb', 'page_name'])

device_model = device_model_count[['assigned index','phone_brand','device_model']]
device_spec = device_spec[['assigned index','screen_size','screen_resolution','ram_mb']]
device_spec = device_spec.drop_duplicates('assigned index')
assigned_index = pandas.Series(index = device_spec.index)
for index, row in device_spec.iterrows():
    try:
        assigned_index[index] = int(row['assigned index'])
    except:
        print index, row['assigned index']

assigned_index[0] = 13
device_spec['assigned index'] = assigned_index
model_spec = pandas.merge(device_model,device_spec,how = 'inner',on='assigned index')

def extract_numeric_screen_size(string):
    try:
        return float(re.findall('\d+\.?\d*',string)[0])
    except:
        return 0

def extract_numeric(string):
    try:
        return int(re.findall('\A\d+',string)[0])
    except:
        return 0
def extract_ram(string):
    try:
        num = int(re.findall('\A\d+',string)[0])
        if 'GB' in string and 'MB' not in string:
            num = 1000*num
        if 'GB' not in string and 'MB' not in string:
            if num <= 10:
                num = 1000*num
        return num
    except:
        return 0
def is_male(string):
    if string == 'M':
        return 1
    else:
        return 0
training_data = pandas.merge(churner_data_device,model_spec,how = 'inner',on=['phone_brand','device_model'])

training_data['screen_size'] = pandas.to_numeric(training_data['screen_size'].apply(extract_numeric_screen_size))
training_data['screen_resolution'] = pandas.to_numeric(training_data['screen_resolution'].apply(extract_numeric))
training_data['ram_mb'] = pandas.to_numeric(training_data['ram_mb'].apply(extract_ram))
training_data['is_male'] = training_data['gender'].apply(is_male)

training_data = training_data.drop(['assigned index','phone_brand','device_model','price','gender'],1)
training_data = training_data.loc[training_data['screen_size'] != 999]
training_data = training_data.loc[training_data['screen_size'] != 0]
training_data = training_data.loc[training_data['screen_resolution'] != 0]
training_data = training_data.loc[training_data['ram_mb'] != 0]
training_data.to_csv('training_data.csv')