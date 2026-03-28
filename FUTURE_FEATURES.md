# Future Features

## 學員端 — 學員查看自己的資料

### 認證方式（擇一）
- **Magic Link**：教練從後台發送專屬連結給學員，點開即可查看
- **LINE Login**：整合 LINE OAuth，學員用 LINE 帳號登入
- **Firebase Auth（Email）**：教練建立學員帳號，學員用 Email/密碼登入
- **簡易密碼**：每位學員設一組 PIN，搭配學員 ID 驗證（最簡單但安全性較低）

### 學員可查看的資料
- 個人體重趨勢圖表
- 訓練紀錄（每次上課的動作、重量、組數）
- 近期預約 / 下次上課時間
- 教練備註 / 課後建議
- 剩餘堂數

### 學員不可查看的資料
- 其他學員的任何資料
- 金流 / 價格資訊
- 教練內部備註

---

## 教練端 — 登入後的差異化介面

### 現有功能（維持）
- 學員管理（新增 / 編輯 / 查看詳情）
- 行程表（7天 / 30天 / 列表）
- 金流管理（購買紀錄 / 確認）
- 訓練紀錄與體重紀錄
- 運動動作選擇器

### 可擴展功能
- **Dashboard 儀表板**：本月營收、本週堂數、學員活躍度等統計
- **通知系統**：學員預約提醒、堂數快用完提醒
- **批量操作**：批量新增預約、批量匯出紀錄
- **訓練模板**：建立常用課表模板，快速套用到學員

---

## 權限架構

```
Firebase Auth
├── 教練帳號 (role: coach)
│   └── 可存取所有資料
├── 學員帳號 (role: student)
│   └── 只能存取自己的資料 (Firestore Security Rules)
```

### Firestore Security Rules 範例
```javascript
match /students/{studentId} {
  allow read, write: if request.auth.uid == coachUID;
  allow read: if request.auth.uid == resource.data.authUID;
}

match /bookings/{bookingId} {
  allow read, write: if request.auth.uid == coachUID;
  allow read: if request.auth.uid == resource.data.studentAuthUID;
}
```

---

## 實作優先順序建議
1. 教練端 Dashboard 儀表板（價值高、複雜度低）
2. 學員端查看訓練紀錄（核心需求）
3. 學員認證方式確定與實作
4. 通知系統
5. 訓練模板
