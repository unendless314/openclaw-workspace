# 📔 Open Notebook 私人 AI 知識庫操作手冊

> 本工具是 Google NotebookLM 的開源替代方案，已成功部署於 Ubuntu 系統中，採用「混合模式」（本地介面 + Google Gemini 雲端運算）。
> 
> **部署模式**：Docker Dev 模式（含本地 TTS 服務）
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
   docker compose -f docker-compose.dev.yml up -d
   ```
   > 此模式包含 TTS (語音合成) 服務，支援本地 Podcast 生成

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
   docker compose -f docker-compose.dev.yml down
   ```

2. **拉取最新代碼與映像：**
   ```bash
   git pull
   docker compose -f docker-compose.dev.yml build --pull
   ```

3. **重新啟動：**
   ```bash
   docker compose -f docker-compose.dev.yml up -d
   ```

---

## 🛑 4. 如何暫時關閉或徹底移除？

### 暫時關閉（釋放記憶體）

不使用時，建議關閉以節省系統資源（i5 CPU 與 16GB RAM 會更輕鬆）：

```bash
cd ~/Projects/open-notebook
docker compose -f docker-compose.dev.yml stop
```

### 徹底移除（不留痕跡）

如果你決定不再使用這個工具，想清空硬碟空間：

1. **刪除容器與網路：**
   ```bash
   cd ~/Projects/open-notebook
   docker compose -f docker-compose.dev.yml down --volumes
   ```

2. **刪除專案資料夾：**
   ```bash
   rm -rf ~/Projects/open-notebook
   ```

3. **(可選) 移除 Docker 軟體映像以釋放數 GB 空間：**
   ```bash
   docker image prune -a
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

## 🎙️ 6. TTS (語音合成) 設定

本部署已整合本地 TTS 服務（Speaches + Kokoro-82M），支援 Podcast 多人對話生成。

⚠️ **重要**：Docker Dev 模式必須修改 `docker.env`，不是 `.env`！

### 環境變數設定
在 `docker.env` 檔案中確保有以下設定（**兩組都要**）：
```bash
# ✅ 必須：通用設定（讓 UI 顯示 Openai-Compatible 已啟用）
OPENAI_COMPATIBLE_BASE_URL=http://speaches:8000/v1
OPENAI_COMPATIBLE_API_KEY=sk-local

# ✅ 必須：TTS 專用設定
OPENAI_COMPATIBLE_BASE_URL_TTS=http://speaches:8000/v1
OPENAI_COMPATIBLE_API_KEY_TTS=sk-local

# ✅ 建議：CPU 環境批次大小設為 1
TTS_BATCH_SIZE=1
```

修改後記得重啟：
```bash
docker compose -f docker-compose.dev.yml restart open_notebook
```

### 首次啟動時下載模型
Speaches 服務啟動後，需要手動下載 Kokoro 語音模型：
```bash
docker compose -f docker-compose.dev.yml exec speaches \
  uv tool run speaches-cli model download speaches-ai/Kokoro-82M-v1.0-ONNX
```

### 在 UI 中註冊 TTS 模型
1. 進入 **Settings** → **Models**
2. 確認「AI 提供商」區塊中「Openai-Compatible」顯示 ✅ 已設定
3. 在 **Text-to-Speech** 區塊點擊 **Add Model**
4. 設定：
   - **Provider**: `openai_compatible`
   - **Model ID**: `speaches-ai/Kokoro-82M-v1.0-ONNX`
   - **Display Name**: `Kokoro Local`

⚠️ **如果 UI 無法選擇 Provider**：使用 API 方式建立
```bash
curl -X POST http://localhost:5055/api/models \
  -H "Content-Type: application/json" \
  -d '{
    "name": "speaches-ai/Kokoro-82M-v1.0-ONNX",
    "provider": "openai_compatible",
    "type": "text_to_speech",
    "is_default": true
  }'
```

### 建立 Speaker Profiles
1. 進入 **Podcasts** → **Speaker Profiles**
2. 建立發言人，設定不同的 Voice ID：
   - `af_bella`：美式女聲（柔和）
   - `af_sarah`：美式女聲（專業）
   - `am_michael`：美式男聲（沉穩）
   - `am_adam`：美式男聲（有力）
   - `bf_emma`：英式女聲
   - `bm_george`：英式男聲

## 📁 檔案位置

| 項目 | 路徑 |
|------|------|
| 專案目錄 | `~/Projects/open-notebook` |
| 環境設定 | `~/Projects/open-notebook/docker.env` |
| 存取網址 | `http://localhost:8502` |

---

## 📝 更新記錄

| 日期 | 更新內容 |
|------|----------|
| 2026-02-07 | 初次建立，使用 single 模式 |
| 2026-02-08 | 更新為 Dev 模式，整合 TTS 服務 |

**本次更新重點**：
- 切換至 Docker Dev 模式（支援本地 TTS）
- 新增 Speaches + Kokoro-82M 本地語音合成設定
- 釐清 `docker.env` 與 `.env` 的區別
- 新增 UI Provider 無法選擇時的 API 繞過方法

---

*本手冊由 Gemini Agent 生成，胖達 🐼 整理保存*
