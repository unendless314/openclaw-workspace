Loaded cached credentials.
Hook registry initialized with 0 hook entries
**Kimi CLI (kimi-cli)** 是一款由月之暗面 (Moonshot AI) 開發的智慧型命令行代理工具。

以下是您需要的重點整理：

**1. 這是什麼工具？**
這是一個結合了大型語言模型（Kimi K2/K2.5）的 AI 終端助手。它不僅能回答問題，還能像人類工程師一樣，自主地閱讀代碼、編輯文件、執行 Shell 指令、聯網搜索，並協助完成軟體開發任務。

**2. 主要功能有哪些？**
*   **AI 代理模式 (Agent Mode)：** 理解自然語言指令，自主規劃並執行複雜任務（如：重構代碼、修復 Bug、新增功能）。
*   **Shell 模式：** 支援直接執行傳統 Shell 指令，並提供智慧補全與建議。
*   **代碼理解與編輯：** 能夠深入分析專案結構，直接對文件進行增刪改查。
*   **擴展性：** 支援 MCP (Model Context Protocol) 協議，可連接外部工具與服務。

**3. 如何安裝？**
建議使用 `uv` 套件管理器進行安裝（需 Python 3.13+）：

1.  **安裝 uv (若未安裝)：**
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```
2.  **安裝 kimi-cli：**
    ```bash
    uv tool install --python 3.13 kimi-cli
    ```
3.  **初始化設定：**
    輸入 `kimi` 啟動，首次使用需執行 `/setup` 並輸入 Moonshot AI API Key。

**4. 基本使用方法**
*   **啟動：** 在專案目錄下輸入 `kimi` 進入互動介面。
*   **對話指令：** 直接用自然語言輸入需求，例如：「幫我解釋這個專案的架構」、「修復 main.py 裡的錯誤」、「新增一個登入功能的 API」。
*   **常用指令：**
    *   `/setup`：重新設定配置。
    *   `/compact`：壓縮上下文記憶以節省 Token。
    *   `/exit`：退出程式。
