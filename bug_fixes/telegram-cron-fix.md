# Telegram cron 投遞失敗 — 排查與修復（2026-03-05）

## 問題現象
- Cron 任務顯示執行 OK，但 Telegram **實際沒有收到訊息**。
- Log 反覆出現：`gateway closed (1008): pairing required`。

## 根因判斷
- `cron-bot` 使用 **announce delivery** 發送時，走的是 **gateway pairing gate**。
- 雖然主 agent 已配對，但 `cron-bot` 的 announce 路徑仍被判定為 **pairing required**。
- 因此訊息無法送達 Telegram。

## 最終修復策略（有效）
**不要用 announce delivery**，改成讓 cron payload 內 **明確使用 message 工具發送 Telegram**。

同時，將 Telegram DM policy 改為 allowlist，以避開 pairing gate：

- `channels.telegram.dmPolicy = allowlist`
- `channels.telegram.allowFrom = ["1882030013"]`

## 實作調整（已完成）
1) 修改 cron（`twitter_fetch_daily_push`）
- `delivery.mode = none`
- **payload 內改成用 exec 強制發送**（避免 cron-bot 不觸發 message tool）
  - `請使用 exec 工具執行：openclaw message send --channel telegram --target 1882030013 --message "<上面完整報告>"`

2) 修改 Telegram config
- `dmPolicy = allowlist`
- `allowFrom = ["1882030013"]`

## 驗證方式
- 手動觸發 cron：
  ```bash
  openclaw cron run <job_id> --expect-final --timeout 180000
  ```
- Telegram 實際收到「完整報告」即可視為成功。

## 結果（實測）
- 2026-03-05 已成功收到完整報告（此修復有效）。

## 備註
- `announce delivery` 仍可能因 pairing gate 失敗。
- 若要恢復 pairing 模式，需確保 cron-bot 的 outbound 路徑也被允許（目前仍不穩定）。
