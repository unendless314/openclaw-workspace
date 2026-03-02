# Cron / Discord 發送問題調查摘要（2026-03-02）

## 背景
- 兩個 cron 任務：
  - **02:00** youtube_transcriber_daily_sync
  - **08:00** twitter_fetch_daily_push
- 實際結果：
  - 02:00 訊息在 Discord 有收到
  - 08:00 訊息在 Discord 沒收到

## 重要發現
1. **cron 顯示 error 不等於 Discord 一定沒送**
   - cron 的 error 多為 delivery/announce 通道失敗（pairing required / delivery target missing）
   - 任務本身可能仍有執行

2. **Gateway timeout 是 OpenClaw 端**
   - `gateway timeout after 30000ms` 是本機 gateway 連線逾時（ws://127.0.0.1:18789）
   - 非 Discord 端錯誤

3. **CLI timeout ≠ 任務中止**
   - CLI 超時只代表前端等不到回覆
   - 任務本身仍可能繼續跑並完成

4. **最可能導致 08:00 Discord 沒收到的原因：訊息過長**
   - Discord 單則訊息限制 2000 字
   - 08:00 任務輸出非常長（包含多領域詳細研究摘要/回覆建議），高機率超過限制
   - 02:00 任務內容較短，因此正常送出

## 任務設定差異（重點）
- 02:00 任務：內容短、timeoutSeconds=300、wakeMode=next-heartbeat
- 08:00 任務：內容長、包含 git add/commit/push 與大量摘要、wakeMode=now

## 測試/操作紀錄
- 嘗試手動 `openclaw cron run`：
  - 08:00 任務曾成功觸發
  - 02:00 任務曾因 gateway timeout 失敗
- 08:00 任務已暫停：
  - `openclaw cron disable aba725e2-0eda-442b-84fd-6db215c31338`

## 建議後續行動
1. 關閉 cron announce（避免 pairing/announce 造成誤判）
2. 08:00 任務改為：
   - 切段發送（每段 <2000 字）
   - 或輸出摘要 + 附檔（txt/md）
3. 若需驗證 Discord 端限制，可建立同內容 Telegram 測試版（待日後設定）

---
更新日期：2026-03-02
