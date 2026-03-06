# Discord cron 投遞失敗 — 排查與修復（2026-03-06）

## 問題現象
- youtube_transcriber_daily_sync cron 在 02:00 執行，但 Discord 有時沒收到訊息。
- cron runs 顯示 `cron announce delivery failed`，即使任務本體成功。

## 根因判斷
- `announce delivery` 路徑不穩定，會造成 cron 被標記為 error，且可能導致訊息未送達。
- 另有一次是轉錄模型被刪除，導致沒有新的轉錄稿（非 cron 本身問題）。

## 最終修復策略（有效）
**不要使用 announce delivery**，改成在 cron payload 內直接使用 `message` 工具發送 Discord。

## 具體調整
- cron job: `youtube_transcriber_daily_sync`（ID: c10f5a4c-4f07-4c16-84f6-289c7995a553）
- 修改內容：
  - `delivery.mode = none`
  - payload 明確要求：`message` 工具直接送 Discord（channel=discord, target=1467426282580217998），**不要詢問允許**。

## 手動驗證
- 2026-03-06 10:52 手動觸發 cron 測試成功。
- cron log 顯示 status: ok，Discord 實際收到訊息。

## 備註
- 若未來仍有未送達，可查看 cron runs summary 與 Discord message logs。
