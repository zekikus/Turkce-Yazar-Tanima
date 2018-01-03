import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from keras.utils import np_utils

# Veri dosya üzerinden okunur.
data = pd.read_csv('data/data.csv')

# Okunan veri girdi(X) ve çıktı(Y) olarak ayrıştırılır.
X = data.iloc[:,:20].values
Y = data.iloc[:,20].values

# Çıktı kategorik veri olduğundan sayısal hale dönüştürülür.
from sklearn.preprocessing import LabelEncoder
labelencoder_Y = LabelEncoder()
Y = labelencoder_Y.fit_transform(Y) 
Y = np_utils.to_categorical(Y)    

# Verinin %80'i train, %20'si test verisi olacak şekilde ayrılır. 
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = 0.2, random_state = 2)
          
# Z-Score normalizasyon işlemi yapılır.
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

import keras
from keras.models import Sequential
from keras.layers import Dense

def build_model():
    classifier = Sequential()
    classifier.add(Dense(units = 256, activation = 'relu', kernel_initializer = 'uniform', input_shape = (20,)))
    classifier.add(Dense(units = 256, activation = 'relu', kernel_initializer = 'uniform'))
    classifier.add(Dense(units = 6, activation = 'softmax', kernel_initializer = 'uniform'))
    classifier.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])
    return classifier

# Cross Validation #
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import cross_val_score
cv_classifier = KerasClassifier(build_fn=build_model,batch_size = 25,nb_epoch = 1000)
accuracies = cross_val_score(estimator = cv_classifier, X = X_train, y = y_train, cv = 10)

accuracySum = 0
for accuracy in accuracies:
    accuracySum += accuracy
 
print(accuracySum / accuracies.size)
# Cross Validation Son #

classifier = build_model()
# Oluşturulan model train verileri ile eğitilir. Yapay Sinir Ağı eğitilmeye başlar.
# nb_epoch: İterasyon sayısı
classifier.fit(X_train,y_train,nb_epoch=100)
# Train verileri ile model eğitildikten sonra test dataları ile doğruluk oranlarına bakılır.
loss,accuracy = classifier.evaluate(X_test,y_test)

# Rastgele bir veri seçilerek çıktı önizlenir.
tahmin = sc.transform(np.array([35,505,409,5,30,23,1,1,279,112,31,25,0,0,2,6,14,11,0,1])).reshape(1,20)
predict = classifier.predict(tahmin)
predict_class = classifier.predict_classes(tahmin)[0]

# Sınıflar: Sınıflarda bulunan veri sayısı arttırılarak doğruluk oranı çok daha iyi seviyelere getirilebilir.
# 0 - Ali Ece
# 1 - Gila BenMayor
# 2 - Gülse Birsel
# 3 - İlber Ortaylı
# 4 - Mehmet Barlas
# 5 - Mehmet Yaşin