# PR: 全新品牌首頁 + 後台導覽功能

## Summary

將 index.html 從舊版訓練計畫選擇器，完整重寫為專業健身教練個人品牌網站。同時為 admin.html 新增互動式功能導覽 (Guided Tour)。新增 FUTURE_FEATURES.md 記錄未來功能規劃。

---

## index.html — 全新品牌首頁

### 視覺設計
- **深色主題 + 金色強調色**：`#0a0a0a` 背景搭配 `#f5a623` 金色，建立專業健身品牌視覺
- **字體**：Oswald（標題/英文）+ Noto Sans TC（中文內文），font-weight 多為 300 呈現簡潔感
- **圓角元素**：所有卡片、照片、按鈕均使用 `border-radius`，避免 AI 生成的方塊感
- **Hover 效果**：所有互動元素都有 hover 動態回饋（顏色變化、位移、縮放）

### 動畫效果
- **Scroll Reveal**：使用 IntersectionObserver，元素滾入視窗時淡入 + 上移
- **Parallax 背景**：Hero 區塊背景圖隨滾動產生視差效果
- **浮動動畫**：Hero 標題使用 CSS `@keyframes float` 持續浮動

### 頁面結構（由上至下）
1. **Navbar**：固定頂部，滾動後加上半透明模糊背景
2. **Hero**：全螢幕背景圖 + 品牌名稱 + Slogan + CTA 按鈕 + IG/LINE 社群圖示
3. **Section Tabs**：`position: sticky` 吸頂導航列（HOME / ABOUT / SERVICES / STORIES / MILKY / CONTACT），`z-index: 999` 確保不被後方區塊覆蓋
4. **Stats Strip**：數據統計條（教學年資、學員數等）
5. **About**：三欄式佈局（照片 + 介紹 + 經歷列表），照片帶灰階濾鏡 hover 還原
6. **Banner Break 1**：全寬視差背景 + 勵志語錄
7. **Services**：三欄服務卡片 + 內嵌 BMR/TDEE 計算器
8. **Banner Break 2**：第二個視差橫幅
9. **Stories**：學員成功案例卡片
10. **Milky**：教練柴犬夥伴專區，含 IG 連結
11. **Contact**：聯繫方式（IG + LINE，LINE 點擊自動複製到剪貼簿並彈出 Toast）
12. **Footer**：版權資訊

### BMR/TDEE 計算器（內嵌於 Services 區塊）
- 使用 Mifflin-St Jeor 公式計算 BMR
- 活動量係數計算 TDEE
- 根據增肌/減脂目標計算每日建議攝取
- **5 週投射 CTA**：計算 5 週後的預估體重（基於 TDEE 與目標熱量差，7700 kcal/kg），顯示具體日期，引導聯繫教練

### 內容管理
- 所有文字內容由 `site-content.json` 動態載入，教練可直接編輯 JSON 更新網站內容
- 圖片路徑、社群連結、服務項目、學員故事等皆可透過 JSON 修改

### LOGIN 按鈕
- 從原本右上角的齒輪圖示（太小無法點擊），改為左下角固定定位的 "LOGIN" 文字按鈕
- `position: fixed; bottom: 1.5rem; left: 1.5rem; z-index: 100`
- 低透明度 (0.25) 不搶眼，hover 時亮起金色邊框

### RWD 響應式
- 768px 以下：單欄佈局、縮小間距、section-tab 縮小字體、背景改為 scroll（停用 parallax）

---

## admin.html — 互動式功能導覽 (Guided Tour)

### 功能說明
- 右下角「功能導覽」按鈕觸發（非自動彈出）
- 僅在學員 "Johnson" 的詳細頁面才會顯示觸發按鈕
- 10 個步驟的 step-by-step 導覽，涵蓋所有後台功能

### 導覽步驟
1. 主選單（學員列表 / 行程表 / 金流）
2. 學員卡片
3. 個人資料區
4. 課程資訊（堂數計算邏輯說明）
5. 運動參考（動作選擇器 + 複製功能）
6. 快速操作（預約 / 購買 / 體重記錄）
7. 體重趨勢圖
8. 近期預約
9. 上課紀錄
10. 危險區（刪除學員）

### 技術細節
- **Spotlight**：`position: fixed` + `box-shadow: 0 0 0 9999px rgba(0,0,0,0.7)` 遮罩，聚焦目標元素
- **自動滾動**：目標元素不在視窗內時，自動 `scrollIntoView`
- **非同步載入處理**：學員詳細頁需從 Firestore 載入，導覽在 1500ms 延遲後才定位
- **精確選擇器**：為 classRecordsHeader 新增 `id` 屬性避免 selector 衝突

---

## 新增檔案

| 檔案 | 說明 |
|------|------|
| `site-content.json` | 首頁所有文字內容的 JSON 資料檔 |
| `images/hero.jpg` | 教練照片（1200px，HEIC 轉換） |
| `images/milky.jpg` | Milky 柴犬照片（400px） |
| `FUTURE_FEATURES.md` | 未來功能規劃（學員端、教練端差異化、權限架構） |

---

## 修改檔案

| 檔案 | 變更 |
|------|------|
| `index.html` | 全面重寫為品牌首頁（+700 行） |
| `admin.html` | 新增 Guided Tour 功能（+214 行） |
