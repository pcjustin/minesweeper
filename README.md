# 踩地雷 (Minesweeper)

這是一個使用 Python 和 Pygame 開發的經典踩地雷遊戲。

## 遊戲操作

- 左鍵點擊：打開格子
- 右鍵點擊：插旗/取消旗子
- 在已打開的數字上左鍵點擊：如果周圍旗子數量正確，會自動打開其餘格子（chording）
- 按 R 鍵：重新開始

## 遊戲規則

- 找出所有不含地雷的格子即可獲勝
- 數字表示該格子周圍 8 個格子中不是地雷的數量
- 踩到地雷遊戲結束

## 配置

- 網格大小：16 x 16
- 地雷數量：40

## 安裝與執行

### 使用 Virtualenv（推薦）

1. 建立虛擬環境：
   ```
   python -m venv .venv
   ```

2. 啟動虛 - Linux/Mac:/bin/activate`
   - Windows: `.venv\Scripts `source .venv擬環境：
  \activate`

3. 安裝依賴：
   ```
   pip install -r requirements.txt
   ```

4. 執行遊戲：
   ```
   python minesweeper.py
   ```

### 直接安裝

1. 安裝依賴：
   ```
   pip install -r requirements.txt
   ```

2. 執行遊戲：
   ```
   python minesweeper.py
   ```
