# 📔 Open Notebook 私人 AI 知識庫操作手冊

> 本工具是 Google NotebookLM 的開源替代方案，已成功部署於 Ubuntu 系統中，採用「混合模式」（本地介面 + Google Gemini 雲端運算）。
> 
> 安裝日期：2026-02-07（由 Gemini Agent 協助完成）

---

## 🚀 1. 如何啟動與進入介面

目前服務已設定為後台執行。若重啟電腦後需要再次開啟：

1. **進入專案目錄：**
   ```bash
   cd ~/Projects/open-notebook
   ```

2. **啟動服務：**
   ```bash
   sudo docker compose -f docker-compose.full.yml start
   ```
   > 如果是第一次完全關閉後重啟，請使用 `up -d` 而不是 `start`

3. **開啟瀏覽器：**
   - 網址：`http://localhost:8502`

---

## 🛠️ 2. 安裝過程（技術回顧）

為了讓這台電腦能執行 Open Notebook，執行了以下標準化步驟：

1. **安裝 Docker 引擎**
   - 在 Ubuntu 24.04 上安裝了工業級的容器化工具（Docker），這是軟體的「地基」。

2. **下載原始碼**
   - 從 GitHub 複製 (git clone) 了 `lfnovo/open-notebook` 的完整專案到 `~/Projects` 資料夾。

3. **設定環境變數**
   - 建立並設定了 `docker.env` 檔案，將 Gemini API Key 安全地寫入其中，並配置為混合模式。

4. **自動化部署**
   - 使用 docker-compose 啟動了兩個容器：
     - `open-notebook-open_notebook-1`: 負責介面與 AI 邏輯
     - `open-notebook-surrealdb-1`: 負責存放筆記索引的資料庫

---

## 🔄 3. 如何更新軟體？

開源專案更新很快，若想獲取新功能：

1. **停止目前服務：**
   ```bash
   cd ~/Projects/open-notebook
   sudo docker compose -f docker-compose.full.yml down
   ```

2. **拉取最新代碼與鏡像：**
   ```bash
   git pull
   sudo docker compose -f docker-compose.full.yml pull
   ```

3. **重新啟動：**
   ```bash
   sudo docker compose -f docker-compose.full.yml up -d
   ```

---

## 🛑 4. 如何暫時關閉或徹底移除？

### 暫時關閉（釋放記憶體）

不使用時，建議關閉以節省系統資源（i5 CPU 與 16GB RAM 會更輕鬆）：

```bash
cd ~/Projects/open-notebook
sudo docker compose -f docker-compose.full.yml stop
```

### 徹底移除（不留痕跡）

如果你決定不再使用這個工具，想清空硬碟空間：

1. **刪除容器與網路：**
   ```bash
   cd ~/Projects/open-notebook
   sudo docker compose -f docker-compose.full.yml down --volumes
   ```

2. **刪除專案資料夾：**
   ```bash
   rm -rf ~/Projects/open-notebook
   ```

3. **(可選) 移除 Docker 軟體鏡像以釋放數 GB 空間：**
   ```bash
   sudo docker image prune -a
   ```

---

## 💡 5. 使用小提醒

- **API Key 額度**
  - 因為使用混合模式，對話會消耗 Gemini 免費額度。若發現 AI 不理你，請檢查 API Key 是否到期或超限。

- **檔案存放**
  - 雖然軟體有資料庫，但建議原始 Markdown 檔案依然保留在自己的資料夾中（例如 Obsidian 庫），只將複本上傳到 Open Notebook 進行分析。

- **本地運算**
  - 這台電腦沒有 NVIDIA GPU，請不要在設定中切換到「完全本地模式（Ollama）」，否則電腦會非常卡頓。

---

## 📁 檔案位置

| 項目 | 路徑 |
|------|------|
| 專案目錄 | `~/Projects/open-notebook` |
| 環境設定 | `~/Projects/open-notebook/docker.env` |
| 存取網址 | `http://localhost:8502` |

---

*本手冊由 Gemini Agent 生成，胖達 🐼 整理保存*
