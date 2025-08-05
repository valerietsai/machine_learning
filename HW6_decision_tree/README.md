# 🎾 Play Tennis 數據分析報告

## 📌 專案簡介

本專案旨在使用 Naive Bayes 分類器分析經典的「Play Tennis」資料集，並預測在特定天氣條件下是否適合打網球。透過資料前處理、模型訓練與評估，我們建立了一個能夠根據天氣特徵進行預測的機器學習模型。

---

## 📊 數據集概覽

資料集包含 14 筆樣本，每筆資料描述一組天氣條件與是否適合打網球的結果。特徵如下：

- `Outlook`: 天氣狀況（Sunny, Overcast, Rain）
- `Temperature`: 氣溫（Hot, Mild, Cool）
- `Humidity`: 濕度（High, Normal）
- `Wind`: 風力（Weak, Strong）
- `PlayTennis`: 是否打網球（Yes, No）

### 範例資料：

| Outlook  | Temperature | Humidity | Wind  | PlayTennis |
|----------|-------------|----------|-------|------------|
| Sunny    | Hot         | High     | Weak  | No         |
| Sunny    | Hot         | High     | Strong| No         |
| Overcast | Hot         | High     | Weak  | Yes        |
| Rain     | Mild        | High     | Weak  | Yes        |
| Rain     | Cool        | Normal   | Weak  | Yes        |

---

## 🧼 資料前處理

為了讓 Naive Bayes 模型能夠處理類別型資料，我們進行了以下處理：

- 使用 `pd.get_dummies()` 對類別特徵進行 One-Hot Encoding。
- 將目標變數 `PlayTennis` 轉換為數值型：`Yes` → 1，`No` → 0。
- 分離特徵 (`X`) 與目標 (`y`)。

---

## 🧪 模型訓練與測試

### 資料分割

由於資料集較小，我們仍進行了訓練集與測試集的分割：

- 訓練集：70%
- 測試集：30%
- 隨機種子：42

### 模型選擇

使用 `GaussianNB`（高斯 Naive Bayes）進行分類建模，適用於連續型特徵，但在此也能處理經 One-Hot 編碼後的類別特徵。

---

## 📈 模型評估結果

### 準確率 (Accuracy)

``` txt
Accuracy: 0.75
```

### 混淆矩陣 (Confusion Matrix)

``` txt
[[1 1]
[0 2]]
```

- TP: 2（正確預測為 Yes）
- TN: 1（正確預測為 No）
- FP: 1（錯誤預測為 Yes）
- FN: 0（錯誤預測為 No）

### 分類報告 (Classification Report)

``` txt
              precision    recall  f1-score   support

           0       1.00      0.50      0.67         2
           1       0.67      1.00      0.80         2

    accuracy                           0.75         4
   macro avg       0.83      0.75      0.73         4
weighted avg       0.83      0.75      0.73         4
```

- 類別 `1`（Yes）表現較好，召回率達 100%
- 類別 `0`（No）準確率高但召回率較低，可能因樣本不平衡

---

## 💾 模型儲存與載入

使用 `joblib` 將訓練好的模型儲存為 `naive_bayes_play_tennis.pkl`，方便未來載入並進行預測。

---

## 🔮 新樣本預測

針對以下天氣條件進行預測：

- Outlook: Sunny
- Temperature: Mild
- Humidity: Normal
- Wind: Weak

### 預測結果：

``` txt
可以打網球嗎？ Yes
```

模型判斷在此天氣條件下適合打網球。

---

## 🧠 結論與建議

- Naive Bayes 模型在小型資料集上表現良好，準確率達 75%。
- 類別不平衡可能影響模型對某些類別的預測能力。
- 若要提升模型效能，可考慮：
  - 擴充資料集
  - 使用其他分類模型（如 Decision Tree, Random Forest）
  - 進行交叉驗證以穩定評估結果

---