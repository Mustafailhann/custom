import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import sys
import pandas as pd
import joblib
import json


str(sys.argv)


# Load the input data from command line arguments
input_data = json.loads(sys.argv[1])

# Veri yükleme
data = pd.read_csv('output.csv')

# Tarih ve Saat sütunlarını birleştirerek zaman bilgisi oluşturma
data['Datetime'] = pd.to_datetime(data['Tarih'] + ' ' + data['Saat'])

# Zaman bilgisini ay, gün, saat, dakika, saniye gibi bileşenlere ayırma
data['Month'] = data['Datetime'].dt.month
data['Day'] = data['Datetime'].dt.day
data['Hour'] = data['Datetime'].dt.hour
data['Minute'] = data['Datetime'].dt.minute
data['Second'] = data['Datetime'].dt.second

# Gereksiz sütunları düşürme
data = data.drop(columns=['Tarih', 'Saat', 'Datetime'])

# Özellikleri ve hedef değişkenleri belirleme
features = data[['Enlem(N)', 'Boylam(E)','Derinlik(km)' ,'Month', 'Day', 'Hour', 'Minute', 'Second']]
target_magnitude = data['ML']
# Eğitim verisinin sütun isimlerini kontrol edin
print(features.columns)

# Yeni verinin sütun isimlerini kontrol edin



# Veri setini eğitim ve test olarak bölme
X_train, X_test, y_train, y_test = train_test_split(features, target_magnitude, test_size=0.2, random_state=42)



"""# Random Forest Modeli
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)
y_pred_rf = rf_model.predict(X_test)
mae_rf = mean_absolute_error(y_test, y_pred_rf)
print(f'Random Forest - Magnitude MAE: {mae_rf}')
#print(y_pred_rf)"""


import lightgbm as lgb
from sklearn.metrics import mean_absolute_error

# LightGBM Modeli
lgb_model = lgb.LGBMRegressor(n_estimators=100, random_state=42)
lgb_model.fit(X_train, y_train)
y_pred_lgb = lgb_model.predict(X_test)
mae_lgb = mean_absolute_error(y_test, y_pred_lgb)
print(f'LightGBM - Magnitude MAE: {mae_lgb}')





import joblib

# Modeli kaydetme
joblib.dump(lgb_model, 'random_forest_model.pkl')

# Load the model
rf_model = joblib.load('random_forest_model.pkl')

# Prepare the new data
yeni_veri = pd.DataFrame({
    'Enlem(N)': [float(input_data['latitude'])],
    'Boylam(E)': [float(input_data['longitude'])],
    'Derinlik(km)': [float(input_data['depth'])],
    'Month': [int(input_data['month'])],
    'Day': [int(input_data['day'])],
    'Hour': [int(input_data['hour'])],
    'Minute': [int(input_data['minute'])],
    'Second': [int(input_data['second'])]
})

# Make sure the data types are correct
yeni_veri = yeni_veri.astype({
    'Enlem(N)': 'float',
    'Boylam(E)': 'float',
    'Derinlik(km)': 'float',
    'Month': 'int',
    'Day': 'int',
    'Hour': 'int',
    'Minute': 'int',
    'Second': 'int'
})

# Make the prediction
tahminler = rf_model.predict(yeni_veri)
tahmin_sonuc = round(tahminler[0], 2)

# Return the prediction result
result = {'prediction': tahmin_sonuc}
print(json.dumps(result, ensure_ascii=False))

# Write the prediction result to the file
with open('tahmin_sonucu.txt', 'w', encoding='utf-8') as dosya:
    dosya.write(f"Tahmin edilen büyüklük: {tahmin_sonuc}")

