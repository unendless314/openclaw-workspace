#!/bin/bash
# gemini-run.sh - 統一的 Gemini Agent 呼叫器
# 位置: gemini-agent skill scripts/gemini-run.sh
# 
# 用法:
#   前景: bash command:"workspace/skills/gemini-enhanced/scripts/gemini-run.sh 'prompt' '/output/file.md'"
#   背景: bash background:true command:"workspace/skills/gemini-enhanced/scripts/gemini-run.sh 'prompt' '/output/file.md'"
#
# 特點:
#   - 強制輸出到檔案（避免執行方式錯誤導致的遺漏）
#   - 自動建立目錄
#   - 錯誤處理和狀態記錄（.status 檔案追蹤進度）
#   - 執行時間統計

set -e

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
        --help|-h)
            echo "用法: $0 [選項] \"prompt\" \"output.md\""
            echo ""
            echo "選項:"
            echo "  --background, -b    背景執行模式"
            echo "  --work-dir, -w      工作目錄"
            echo "  --help, -h          顯示說明"
            echo ""
            echo "範例:"
            echo "  $0 \"研究 AI 趨勢\" \"./output/ai-trends.md\""
            echo "  $0 --background \"分析程式碼\" \"./output/analysis.md\""
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

# 執行函數
run_gemini() {
    local prompt="$1"
    local output="$2"
    local start_time=$(date +%s)
    
    # 記錄開始時間
    echo "started_at: $(date -Iseconds)" > "$STATUS_FILE"
    echo "status: running" >> "$STATUS_FILE"
    echo "output_file: $output" >> "$STATUS_FILE"
    
    # 建立臨時檔案存放回應
    local temp_response="${output}.tmp.$$"
    
    # 執行 gemini（包含 stderr）
    if gemini "$prompt" > "$temp_response" 2>&1; then
        local end_time=$(date +%s)
        local duration=$((end_time - start_time))
        
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
*耗時: ${duration}秒*
EOF
        
        # 清理臨時檔案
        rm -f "$temp_response"
        
        echo "status: completed" > "$STATUS_FILE"
        echo "completed_at: $(date -Iseconds)" >> "$STATUS_FILE"
        echo "duration_seconds: $duration" >> "$STATUS_FILE"
        echo "exit_code: 0" >> "$STATUS_FILE"
        
        echo "✅ Gemini 任務完成 (${duration}s)" >&2
        echo "   輸出: $output" >&2
        return 0
    else
        local exit_code=$?
        local end_time=$(date +%s)
        local duration=$((end_time - start_time))
        
        # 即使失敗也寫入問答格式（包含錯誤訊息）
        cat > "$output" << EOF
# Gemini Agent 對話記錄

---

## Prompt

$prompt

---

## Response

⚠️ **任務執行失敗**

\`\`\`
$(cat "$temp_response")
\`\`\`

---

*嘗試時間: $(date -Iseconds)*  
*耗時: ${duration}秒*  
*Exit Code: $exit_code*
EOF
        
        # 清理臨時檔案
        rm -f "$temp_response"
        
        echo "status: failed" > "$STATUS_FILE"
        echo "failed_at: $(date -Iseconds)" >> "$STATUS_FILE"
        echo "duration_seconds: $duration" >> "$STATUS_FILE"
        echo "exit_code: $exit_code" >> "$STATUS_FILE"
        
        echo "❌ Gemini 任務失敗 (exit code: $exit_code, ${duration}s)" >&2
        echo "   輸出: $output（包含錯誤訊息）" >&2
        return $exit_code
    fi
}

# 執行模式選擇
if [ "$BACKGROUND" = true ]; then
    # 背景模式
    (
        if [ -n "$WORK_DIR" ]; then
            cd "$WORK_DIR" && run_gemini "$PROMPT" "$OUTPUT_FILE"
        else
            run_gemini "$PROMPT" "$OUTPUT_FILE"
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
        cd "$WORK_DIR" && run_gemini "$PROMPT" "$OUTPUT_FILE"
    else
        run_gemini "$PROMPT" "$OUTPUT_FILE"
    fi
fi