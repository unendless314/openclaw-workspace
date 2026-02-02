#!/bin/bash
# gemini-run.sh - 統一的 Gemini Agent 呼叫器（含自動重試）
# 位置: gemini-agent skill scripts/gemini-run.sh
# 
# 用法:
#   前景: bash command:"workspace/skills/gemini-agent/scripts/gemini-run.sh 'prompt' '/output/file.md'"
#   背景: bash background:true command:"workspace/skills/gemini-agent/scripts/gemini-run.sh 'prompt' '/output/file.md'"
#
# 特點:
#   - 強制輸出到檔案（避免執行方式錯誤導致的遺漏）
#   - 自動建立目錄
#   - 錯誤處理和狀態記錄（.status 檔案追蹤進度）
#   - 執行時間統計
#   - 🆕 自動重試機制（配額耗盡時自動等待重試）

set -e

# ========== 重試配置 ==========
MAX_RETRIES=3                      # 最大重試次數
INITIAL_RETRY_DELAY=3              # 初始重試延遲（秒）
MAX_RETRY_DELAY=30                 # 最大重試延遲（秒）
RETRY_MULTIPLIER=2                 # 指數退避乘數
# =============================

BACKGROUND=false
PROMPT=""
OUTPUT_FILE=""
WORK_DIR=""

# 解析參數
while [[ $# -gt 0 ]]; do
    case $1 in
        --background|-b)
            BACKGROUND=true
            shift
            ;;
        --work-dir|-w)
            WORK_DIR="$2"
            shift 2
            ;;
        --max-retries)
            MAX_RETRIES="$2"
            shift 2
            ;;
        --help|-h)
            echo "用法: $0 [選項] \"prompt\" \"output.md\""
            echo ""
            echo "選項:"
            echo "  --background, -b    背景執行模式"
            echo "  --work-dir, -w      工作目錄"
            echo "  --max-retries N     最大重試次數（預設: 3）"
            echo "  --help, -h          顯示說明"
            echo ""
            echo "重試策略:"
            echo "  - 自動檢測配額耗盡錯誤 ('exhausted your capacity')"
            echo "  - 指數退避：3s → 6s → 12s"
            echo "  - 最大重試次數: $MAX_RETRIES 次"
            echo ""
            echo "範例:"
            echo "  $0 \"研究 AI 趨勢\" \"./output/ai-trends.md\""
            echo "  $0 --background \"分析程式碼\" \"./output/analysis.md\""
            echo "  $0 --max-retries 5 \"重要任務\" \"./output/result.md\""
            exit 0
            ;;
        *)
            if [ -z "$PROMPT" ]; then
                PROMPT="$1"
            elif [ -z "$OUTPUT_FILE" ]; then
                OUTPUT_FILE="$1"
            fi
            shift
            ;;
    esac
done

# 驗證參數
if [ -z "$PROMPT" ] || [ -z "$OUTPUT_FILE" ]; then
    echo "❌ 錯誤: 缺少必要參數" >&2
    echo "用法: $0 \"你的 prompt\" \"/保存/路徑.md\"" >&2
    exit 1
fi

# 轉換為絕對路徑
if [[ "$OUTPUT_FILE" != /* ]]; then
    OUTPUT_FILE="$(pwd)/$OUTPUT_FILE"
fi

# 確保目錄存在
mkdir -p "$(dirname "$OUTPUT_FILE")"

# 建立狀態檔（用於追蹤執行狀態）
STATUS_FILE="${OUTPUT_FILE}.status"
echo "pending" > "$STATUS_FILE"

# 檢查回應是否為配額耗盡錯誤
is_quota_exhausted() {
    local response_file="$1"
    if grep -q "exhausted your capacity" "$response_file" 2>/dev/null; then
        return 0
    fi
    return 1
}

# 執行一次 gemini 呼叫
execute_gemini() {
    local prompt="$1"
    local temp_file="$2"
    gemini "$prompt" > "$temp_file" 2>&1
}

# 執行函數（含重試邏輯）
run_gemini_with_retry() {
    local prompt="$1"
    local output="$2"
    local start_time=$(date +%s)
    local attempt=1
    local retry_delay=$INITIAL_RETRY_DELAY
    local total_duration=0
    local last_error=""
    local all_attempts_log=""
    
    # 記錄開始時間
    echo "started_at: $(date -Iseconds)" > "$STATUS_FILE"
    echo "status: running" >> "$STATUS_FILE"
    echo "output_file: $output" >> "$STATUS_FILE"
    echo "max_retries: $MAX_RETRIES" >> "$STATUS_FILE"
    
    while [ $attempt -le $MAX_RETRIES ]; do
        local attempt_start=$(date +%s)
        local temp_response="${output}.tmp.$$"
        
        echo "🔄 嘗試 $attempt / $MAX_RETRIES..." >&2
        
        # 執行 gemini
        if execute_gemini "$prompt" "$temp_response"; then
            local attempt_end=$(date +%s)
            local attempt_duration=$((attempt_end - attempt_start))
            total_duration=$((attempt_end - start_time))
            
            # 寫入格式化的問答文件
            cat > "$output" << EOF
# Gemini Agent 對話記錄

---

## Prompt

$prompt

---

## Response

$(cat "$temp_response")

---

*生成時間: $(date -Iseconds)*  
*總耗時: ${total_duration}秒*  
*成功嘗試: 第 ${attempt} 次*
EOF
            
            rm -f "$temp_response"
            
            echo "status: completed" > "$STATUS_FILE"
            echo "completed_at: $(date -Iseconds)" >> "$STATUS_FILE"
            echo "duration_seconds: $total_duration" >> "$STATUS_FILE"
            echo "attempts: $attempt" >> "$STATUS_FILE"
            echo "exit_code: 0" >> "$STATUS_FILE"
            
            if [ $attempt -gt 1 ]; then
                echo "✅ Gemini 任務完成 (${total_duration}s，經過 $attempt 次嘗試)" >&2
            else
                echo "✅ Gemini 任務完成 (${total_duration}s)" >&2
            fi
            echo "   輸出: $output" >&2
            return 0
            
        else
            local exit_code=$?
            local attempt_end=$(date +%s)
            local attempt_duration=$((attempt_end - attempt_start))
            total_duration=$((attempt_end - start_time))
            
            # 記錄這次嘗試的錯誤
            last_error=$(cat "$temp_response" 2>/dev/null || echo "Unknown error")
            all_attempts_log="${all_attempts_log}\n\n--- 嘗試 $attempt (${attempt_duration}s) ---\nExit Code: $exit_code\n\n\`\`\`\n$last_error\n\`\`\`"
            
            # 檢查是否為配額耗盡錯誤
            if is_quota_exhausted "$temp_response"; then
                if [ $attempt -lt $MAX_RETRIES ]; then
                    echo "⚠️  配額已耗盡，等待 ${retry_delay} 秒後重試..." >&2
                    sleep $retry_delay
                    
                    # 指數退避
                    retry_delay=$((retry_delay * RETRY_MULTIPLIER))
                    if [ $retry_delay -gt $MAX_RETRY_DELAY ]; then
                        retry_delay=$MAX_RETRY_DELAY
                    fi
                    
                    attempt=$((attempt + 1))
                    rm -f "$temp_response"
                    continue
                else
                    echo "❌ 配額耗盡，已達最大重試次數 ($MAX_RETRIES)" >&2
                fi
            else
                echo "❌ 任務失敗（非配額錯誤），不再重試" >&2
            fi
            
            # 最終失敗，寫入所有嘗試記錄
            cat > "$output" << EOF
# Gemini Agent 對話記錄

---

## Prompt

$prompt

---

## Response

⚠️ **任務執行失敗（已嘗試 $attempt 次）**

### 錯誤摘要
\`\`\`
$last_error
\`\`\`

### 詳細嘗試記錄
$all_attempts_log

---

*最後嘗試時間: $(date -Iseconds)*  
*總耗時: ${total_duration}秒*  
*嘗試次數: $attempt / $MAX_RETRIES*
EOF
            
            rm -f "$temp_response"
            
            echo "status: failed" > "$STATUS_FILE"
            echo "failed_at: $(date -Iseconds)" >> "$STATUS_FILE"
            echo "duration_seconds: $total_duration" >> "$STATUS_FILE"
            echo "attempts: $attempt" >> "$STATUS_FILE"
            echo "exit_code: $exit_code" >> "$STATUS_FILE"
            
            echo "❌ Gemini 任務最終失敗 (exit code: $exit_code, ${total_duration}s)" >&2
            echo "   輸出: $output（包含錯誤訊息）" >&2
            return $exit_code
        fi
    done
}

# 執行模式選擇
if [ "$BACKGROUND" = true ]; then
    # 背景模式
    (
        if [ -n "$WORK_DIR" ]; then
            cd "$WORK_DIR" && run_gemini_with_retry "$PROMPT" "$OUTPUT_FILE"
        else
            run_gemini_with_retry "$PROMPT" "$OUTPUT_FILE"
        fi
    ) &
    PID=$!
    
    # 等待一下確保進程啟動
    sleep 0.1
    
    # 檢查進程是否真的在運行
    if kill -0 $PID 2>/dev/null; then
        echo "🔄 背景任務已啟動 (PID: $PID)"
        echo "   Prompt: ${PROMPT:0:50}..."
        echo "   輸出檔: $OUTPUT_FILE"
        echo "   狀態檔: $STATUS_FILE"
        echo "   重試策略: 最多 $MAX_RETRIES 次"
        echo ""
        echo "檢查進度:"
        echo "  cat $STATUS_FILE"
        echo "  cat $OUTPUT_FILE"
        echo ""
        echo "終止任務: kill $PID"
        
        # 更新狀態檔加入 PID
        echo "pid: $PID" >> "$STATUS_FILE"
    else
        echo "❌ 背景任務啟動失敗"
        exit 1
    fi
else
    # 前景模式
    if [ -n "$WORK_DIR" ]; then
        cd "$WORK_DIR" && run_gemini_with_retry "$PROMPT" "$OUTPUT_FILE"
    else
        run_gemini_with_retry "$PROMPT" "$OUTPUT_FILE"
    fi
fi
