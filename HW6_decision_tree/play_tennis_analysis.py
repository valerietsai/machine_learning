import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 放置在與腳本相同的資料夾中
font_path = 'TaipeiSansTCBeta-Regular.ttf'

# 檢查檔案是否存在
try:
    with open(font_path, 'rb') as f:
        pass
except FileNotFoundError:
    print(f"錯誤：找不到字型檔案 '{font_path}'。請將字型檔案放置在腳本所在的資料夾中。")
    # 你可以選擇在此處退出程式或採取其他措施
    exit()

# 將字型添加到 font manager
fm.fontManager.addfont(font_path)

# 設定 matplotlib 的字型
plt.rc('font', family='Taipei Sans TC Beta')

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# 建立 Play Tennis 數據集
data = {
    'Outlook': ['Sunny', 'Sunny', 'Overcast', 'Rain', 'Rain', 'Rain', 'Overcast', 'Sunny', 'Sunny', 'Rain', 'Sunny', 'Overcast', 'Overcast', 'Rain'],
    'Temperature': ['Hot', 'Hot', 'Hot', 'Mild', 'Cool', 'Cool', 'Cool', 'Mild', 'Cool', 'Mild', 'Mild', 'Mild', 'Hot', 'Mild'],
    'Humidity': ['High', 'High', 'High', 'High', 'Normal', 'Normal', 'Normal', 'High', 'Normal', 'Normal', 'Normal', 'High', 'Normal', 'High'],
    'Wind': ['Weak', 'Strong', 'Weak', 'Weak', 'Weak', 'Strong', 'Strong', 'Weak', 'Weak', 'Weak', 'Strong', 'Strong', 'Weak', 'Strong'],
    'PlayTennis': ['No', 'No', 'Yes', 'Yes', 'Yes', 'No', 'Yes', 'No', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'No']
}

df = pd.DataFrame(data)

print("數據集概覽：")
print(df.head())
print("\n數據集資訊：")
print(df.info())

# 對類別型特徵進行 One-Hot Encoding
df_encoded = pd.get_dummies(df, columns=['Outlook', 'Temperature', 'Humidity', 'Wind'])

# 將目標變數 'PlayTennis' 轉換為 0 和 1
# 'Yes' -> 1, 'No' -> 0
df_encoded['PlayTennis'] = df_encoded['PlayTennis'].apply(lambda x: 1 if x == 'Yes' else 0)

# 分離特徵 (X) 和目標變數 (y)
X = df_encoded.drop('PlayTennis', axis=1)
y = df_encoded['PlayTennis']

print("\n經過 One-Hot Encoding 和標籤轉換後的數據：")
print(X.head())
print("\n目標變數：")
print(y.head())

# 製作堆疊長條圖
crosstab = pd.crosstab(df['Outlook'], df['PlayTennis'])
crosstab.plot(kind='bar', stacked=True, colormap='Set2')

plt.title('Outlook 與 PlayTennis 的關係')
plt.xlabel('Outlook')
plt.ylabel('筆數')
plt.tight_layout()
plt.savefig("圖表1_Outlook_PlayTennis.png")
plt.show()

# 分割訓練集和測試集
# 這裡由於數據集很小，我們通常會使用整個數據集來訓練，但為了展示流程，我們還是進行分割
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

print(f"\n訓練集大小: {X_train.shape}")
print(f"測試集大小: {X_test.shape}")

# 建立 Gaussian Naive Bayes 分類器
model = GaussianNB()

# 使用訓練集來訓練模型
model.fit(X_train, y_train)

print("\n模型訓練完成！")

# 使用測試集進行預測
y_pred = model.predict(X_test)

# 評估模型性能
accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)
class_report = classification_report(y_test, y_pred)

print(f"\n模型準確率 (Accuracy): {accuracy:.2f}")
print("\n混淆矩陣 (Confusion Matrix):")
print(conf_matrix)
print("\n分類報告 (Classification Report):")
print(class_report)

# 視覺化混淆矩陣
plt.figure(figsize=(5, 4))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues',
            xticklabels=['No', 'Yes'], yticklabels=['No', 'Yes'])
plt.title('混淆矩陣')
plt.xlabel('預測值')
plt.ylabel('實際值')
plt.tight_layout()
plt.savefig("圖表2_混淆矩陣.png")
plt.show()

import joblib

# 儲存模型
joblib.dump(model, 'naive_bayes_play_tennis.pkl')

print("\n模型已儲存為 naive_bayes_play_tennis.pkl")

# 假設我們有一個新的天氣狀況，並想要進行預測
new_data = pd.DataFrame({
    'Outlook_Sunny': [1], 'Outlook_Overcast': [0], 'Outlook_Rain': [0],
    'Temperature_Hot': [0], 'Temperature_Mild': [1], 'Temperature_Cool': [0],
    'Humidity_High': [0], 'Humidity_Normal': [1],
    'Wind_Weak': [1], 'Wind_Strong': [0]
})

# 載入儲存的模型
loaded_model = joblib.load('naive_bayes_play_tennis.pkl')

# 獲取訓練時的特徵順序
# 這是最關鍵的一步，因為它確保了新數據的欄位順序與訓練數據一致
# 假設你的 X_train 依然在記憶體中，如果不在，你可能需要從儲存的訓練數據中獲取
# 這裡我們直接從模型中獲取特徵名稱，這對於 scikit-learn >= 1.0 的版本是可行的
# 如果你的版本較舊，你可能需要手動定義或從 X_train 獲取
feature_names_order = X_train.columns

# 假設我們有一個新的天氣狀況，並想要進行預測
# 我們先定義新數據的字典，不考慮順序
new_data_dict = {
    'Outlook_Sunny': [1],
    'Outlook_Overcast': [0],
    'Outlook_Rain': [0],
    'Temperature_Hot': [0],
    'Temperature_Mild': [1],
    'Temperature_Cool': [0],
    'Humidity_High': [0],
    'Humidity_Normal': [1],
    'Wind_Weak': [1],
    'Wind_Strong': [0]
}

# 根據訓練時的特徵順序來建立新的 DataFrame
new_data = pd.DataFrame(new_data_dict, columns=feature_names_order)

# 進行預測
prediction = loaded_model.predict(new_data)

result = 'Yes' if prediction[0] == 1 else 'No'

print(f"\n對於新的天氣狀況，預測結果是：可以打網球嗎？ {result}")