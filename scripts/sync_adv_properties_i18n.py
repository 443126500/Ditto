# -*- coding: utf-8 -*-
"""Seed/sync Ditto_Adv_Properties + Adv string-table keys across Debug/Language/*.xml."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "Debug" / "Language"

# SETTING_* id -> English (must match AdvGeneral.cpp defaults)
PROPS: dict[int, str] = {
    1: "Amount of text to save for description",
    2: "Display icon in system tray",
    3: "Save multi-pastes",
    4: "Hide Ditto on hot key if Ditto is visible",
    5: "Paste clip in active window after selection",
    6: "Maximum clip size in bytes (0 for no limit)",
    7: "Multi-paste clip separator ([LF] = line feed)",
    8: "Ensure Ditto is always connected to the clipboard",
    9: "On copy play the sound",
    10: "Show text for first ten copy hot keys",
    11: "Show leading whitespace",
    12: "Text lines per clip",
    13: "Transparency enabled",
    14: "Show thumbnails(for CF_DIB and PNG types) (could increase memory usage and display speed)",
    15: "Draw RTF text in list (for RTF types) (could increase memory usage an display speed)",
    16: "Find as you type",
    17: "Ensure entire window is visible",
    18: "Show clips that are in groups in main list",
    19: "Prompt when deleting clips",
    20: "Always show scroll bar",
    21: "Elevated privileges to paste into elevated apps",
    22: "Show in taskbar",
    23: "Show indicator a clip has been pasted",
    24: "Diff application path",
    25: "Transparency percentage",
    26: "Update clip order on paste",
    27: "Allow duplicates",
    **{28 + i: f"{i + 1} Regex" for i in range(15)},
    **{43 + i: f"{i + 1} Process Name" for i in range(15)},
    58: "Show startup tooltip message",
    59: "Tooltip display time(ms) max of 32000 (-1 default (5 seconds), 0 to turn off)",
    60: "Selected index",
    61: "Save clipboard delay (ms, default: 100)",
    62: "Show message that we received a manual sent clip",
    63: "Multi-paste in reverse order",
    64: "Default paste string",
    65: "Default copy string",
    66: "Default cut string",
    67: "Revert to top level group on close",
    68: "Update clip Order on ctrl-c",
    69: "Tooltip maximum display lines",
    70: "Tooltip display characters",
    71: "Activate window delay (100ms default)",
    72: "Double shortcut keystroke timeout)",
    73: "Send keys delay (ms)",
    74: "First ten hot keys start index",
    75: "First ten hot keys font size",
    76: "Open to group same as active exe",
    77: "Add file drop when dragging clips",
    78: "Copy and save clipboard delay (ms)",
    79: "Editor default font size",
    80: "Move selection on open hot key",
    81: "Allow back to back duplicates (if allowing duplicates)",
    82: "Maintain search view",
    83: "Network send receive port (default: 23443)",
    84: "Write debug to file",
    85: "Write debug to OutputDebugString",
    86: "Network server bind IP (default: *)",
    87: "Disable friends",
    88: "Ignore copies faster than (ms) (default: 500)",
    89: "Refresh view after paste",
    90: "Slugify Separator (default: -)",
    91: "Fast thumbnails (True = fast / low quality (default). False = slow / high quality)",
    92: "Clipboard restore delay after copy buffer sent paste (ms, default: 750)",
    93: "Support all types ignoring supported type list (default: false))",
    94: "Ignore CF_DIB when a clip is detected as text content",
    95: "Regex case insensitive search",
    96: "Draw swatch for hex, RGB, and HSL colors",
    97: "Center window below cursor or caret",
    98: "Text editor path (empty for system mapping)",
    99: "RTF editor path",
    100: "Update description on clip edit",
    101: "QRCode Url",
    102: "Append Computer Name and IP when receiving clips",
    103: "Diff save compare files as utf8",
    104: "Image editor path (empty for system mapping)",
    105: "Clip edit save delay after load",
    106: "Clip edit save delay after Save",
    107: "Web Search Url",
    108: "Do not hide Ditto window on deactivate",
    109: "Hide taskbar icon when Ditto window closes",
    110: "Use modern scroll bar",
    111: "Enforce clipboard ignore formats",
}

# String table named IDs used by AdvGeneral.cpp
STRINGS_EN: dict[str, str] = {
    "AdvGroup_Ditto": "Ditto",
    "AdvGroup_RegexExclude": "Exclude clips by Regular Expressions",
    "AdvDesc_Process": "Process making the copy first must match this before the Regex will be applied (empty or * for all processes) (separate multiples by ;)",
    "AdvDesc_Regex": "If copied text matches this regular expression then the clip will not be saved to Ditto",
    "AdvDesc_IgnoreCFDIB": 'Case insensitive. Recommended option is "excel.exe; onenote.exe; powerpnt.exe" ',
    "AdvCopyScriptsTitle": "Copy Scripts",
    "AdvPasteScriptsTitle": "Paste Scripts",
    "AdvResetClipOrderTitle": "Select group to reset clip order",
}

PROPS_ZH: dict[int, str] = {
    1: "描述文本保存长度",
    2: "在系统托盘显示图标",
    3: "保存多次粘贴",
    4: "若 Ditto 已显示则热键时隐藏",
    5: "选择后粘贴到活动窗口",
    6: "最大剪贴大小（字节，0 表示不限制）",
    7: "多次粘贴分隔符（[LF] = 换行）",
    8: "确保 Ditto 始终连接到剪贴板",
    9: "复制时播放声音",
    10: "显示前十个复制热键文本",
    11: "显示前导空白",
    12: "每条剪贴显示行数",
    13: "启用透明度",
    14: "显示缩略图（CF_DIB 与 PNG）（可能增加内存占用并影响显示速度）",
    15: "在列表中绘制 RTF 文本（可能增加内存占用并影响显示速度）",
    16: "输入时即时查找",
    17: "确保整个窗口可见",
    18: "在主列表中显示分组内的剪贴",
    19: "删除剪贴时提示",
    20: "始终显示滚动条",
    21: "提升权限以粘贴到高权限应用",
    22: "在任务栏显示",
    23: "显示剪贴已粘贴标记",
    24: "差异比较程序路径",
    25: "透明度百分比",
    26: "粘贴时更新剪贴顺序",
    27: "允许重复项",
    **{28 + i: f"{i + 1} 正则表达式" for i in range(15)},
    **{43 + i: f"{i + 1} 进程名" for i in range(15)},
    58: "显示启动提示消息",
    59: "工具提示显示时间（毫秒，最大 32000；-1 默认约 5 秒，0 关闭）",
    60: "选中索引",
    61: "保存剪贴板延迟（毫秒，默认 100）",
    62: "收到手动发送的剪贴时显示消息",
    63: "多次粘贴按反向顺序",
    64: "默认粘贴按键串",
    65: "默认复制按键串",
    66: "默认剪切按键串",
    67: "关闭时回到顶层分组",
    68: "Ctrl-C 时更新剪贴顺序",
    69: "工具提示最大显示行数",
    70: "工具提示显示字符数",
    71: "激活窗口延迟（默认 100 毫秒）",
    72: "双击快捷键超时时间",
    73: "发送按键延迟（毫秒）",
    74: "前十个热键起始索引",
    75: "前十个热键字体大小",
    76: "打开到与活动程序相同的分组",
    77: "拖拽剪贴时添加文件投放",
    78: "复制并保存剪贴板延迟（毫秒）",
    79: "编辑器默认字体大小",
    80: "打开热键时移动选择",
    81: "允许连续重复（在允许重复时）",
    82: "保持搜索视图",
    83: "网络收发端口（默认 23443）",
    84: "将调试信息写入文件",
    85: "将调试信息写入 OutputDebugString",
    86: "网络服务器绑定 IP（默认 *）",
    87: "禁用好友",
    88: "忽略快于此时长的复制（毫秒，默认 500）",
    89: "粘贴后刷新视图",
    90: "Slugify 分隔符（默认 -）",
    91: "快速缩略图（True=快/低质量（默认）；False=慢/高质量）",
    92: "复制缓冲区粘贴后恢复剪贴板延迟（毫秒，默认 750）",
    93: "支持所有类型并忽略受支持类型列表（默认 false）",
    94: "当剪贴被识别为文本内容时忽略 CF_DIB",
    95: "正则搜索不区分大小写",
    96: "为十六进制、RGB、HSL 颜色绘制色块",
    97: "在光标或插入点下方居中窗口",
    98: "文本编辑器路径（空则使用系统关联）",
    99: "RTF 编辑器路径",
    100: "编辑剪贴时更新描述",
    101: "二维码 URL",
    102: "接收剪贴时附加计算机名和 IP",
    103: "差异比较时以 UTF-8 保存文件",
    104: "图像编辑器路径（空则使用系统关联）",
    105: "剪贴编辑加载后保存延迟",
    106: "剪贴编辑保存后保存延迟",
    107: "网页搜索 URL",
    108: "停用时不隐藏 Ditto 窗口",
    109: "关闭 Ditto 窗口时隐藏任务栏图标",
    110: "使用现代滚动条",
    111: "强制剪贴板忽略格式",
}

STRINGS_ZH: dict[str, str] = {
    "AdvGroup_Ditto": "Ditto",
    "AdvGroup_RegexExclude": "按正则表达式排除剪贴",
    "AdvDesc_Process": "复制来源进程须先匹配此项后才会应用正则（空或 * 表示全部进程；多个用 ; 分隔）",
    "AdvDesc_Regex": "若复制的文本匹配此正则表达式，则不会保存到 Ditto",
    "AdvDesc_IgnoreCFDIB": '不区分大小写。建议选项为 "excel.exe; onenote.exe; powerpnt.exe" ',
    "AdvCopyScriptsTitle": "复制时脚本",
    "AdvPasteScriptsTitle": "粘贴时脚本",
    "AdvResetClipOrderTitle": "选择要重置剪贴顺序的分组",
}

PROPS_ZH_TW: dict[int, str] = {
    1: "描述文字儲存長度",
    2: "在系統匣顯示圖示",
    3: "儲存多次貼上",
    4: "若 Ditto 已顯示則熱鍵時隱藏",
    5: "選擇後貼上到作用中視窗",
    6: "最大剪貼大小（位元組，0 表示不限制）",
    7: "多次貼上分隔符號（[LF] = 換行）",
    8: "確保 Ditto 始終連接到剪貼簿",
    9: "複製時播放聲音",
    10: "顯示前十個複製熱鍵文字",
    11: "顯示前導空白",
    12: "每則剪貼顯示行數",
    13: "啟用透明度",
    14: "顯示縮圖（CF_DIB 與 PNG）（可能增加記憶體並影響顯示速度）",
    15: "在清單中繪製 RTF 文字（可能增加記憶體並影響顯示速度）",
    16: "輸入時即時尋找",
    17: "確保整個視窗可見",
    18: "在主清單中顯示群組內的剪貼",
    19: "刪除剪貼時提示",
    20: "一律顯示捲軸",
    21: "提升權限以貼上到高權限應用程式",
    22: "在工作列顯示",
    23: "顯示剪貼已貼上標記",
    24: "差異比較程式路徑",
    25: "透明度百分比",
    26: "貼上時更新剪貼順序",
    27: "允許重複項目",
    **{28 + i: f"{i + 1} 正規表示式" for i in range(15)},
    **{43 + i: f"{i + 1} 程序名稱" for i in range(15)},
    58: "顯示啟動提示訊息",
    59: "工具提示顯示時間（毫秒，最大 32000；-1 預設約 5 秒，0 關閉）",
    60: "選取索引",
    61: "儲存剪貼簿延遲（毫秒，預設 100）",
    62: "收到手動傳送的剪貼時顯示訊息",
    63: "多次貼上依反向順序",
    64: "預設貼上按鍵字串",
    65: "預設複製按鍵字串",
    66: "預設剪下按鍵字串",
    67: "關閉時回到頂層群組",
    68: "Ctrl-C 時更新剪貼順序",
    69: "工具提示最大顯示行數",
    70: "工具提示顯示字元數",
    71: "啟用視窗延遲（預設 100 毫秒）",
    72: "雙擊快捷鍵逾時時間",
    73: "傳送按鍵延遲（毫秒）",
    74: "前十個熱鍵起始索引",
    75: "前十個熱鍵字型大小",
    76: "開啟到與作用中程式相同的群組",
    77: "拖曳剪貼時加入檔案投放",
    78: "複製並儲存剪貼簿延遲（毫秒）",
    79: "編輯器預設字型大小",
    80: "開啟熱鍵時移動選取",
    81: "允許連續重複（在允許重複時）",
    82: "保持搜尋檢視",
    83: "網路收發連接埠（預設 23443）",
    84: "將偵錯資訊寫入檔案",
    85: "將偵錯資訊寫入 OutputDebugString",
    86: "網路伺服器繫結 IP（預設 *）",
    87: "停用好友",
    88: "忽略快於此時間的複製（毫秒，預設 500）",
    89: "貼上後重新整理檢視",
    90: "Slugify 分隔符號（預設 -）",
    91: "快速縮圖（True=快/低品質（預設）；False=慢/高品質）",
    92: "複製緩衝區貼上後還原剪貼簿延遲（毫秒，預設 750）",
    93: "支援所有類型並忽略支援類型清單（預設 false）",
    94: "當剪貼被辨識為文字內容時忽略 CF_DIB",
    95: "正規表示式搜尋不區分大小寫",
    96: "為十六進位、RGB、HSL 色彩繪製色塊",
    97: "在游標或插入點下方置中視窗",
    98: "文字編輯器路徑（空則使用系統對應）",
    99: "RTF 編輯器路徑",
    100: "編輯剪貼時更新描述",
    101: "QR 碼 URL",
    102: "接收剪貼時附加電腦名稱與 IP",
    103: "差異比較時以 UTF-8 儲存檔案",
    104: "影像編輯器路徑（空則使用系統對應）",
    105: "剪貼編輯載入後儲存延遲",
    106: "剪貼編輯儲存後儲存延遲",
    107: "網頁搜尋 URL",
    108: "停用時不隱藏 Ditto 視窗",
    109: "關閉 Ditto 視窗時隱藏工作列圖示",
    110: "使用現代捲軸",
    111: "強制剪貼簿忽略格式",
}

STRINGS_ZH_TW: dict[str, str] = {
    "AdvGroup_Ditto": "Ditto",
    "AdvGroup_RegexExclude": "依正規表示式排除剪貼",
    "AdvDesc_Process": "複製來源程序須先符合此項後才會套用正規表示式（空或 * 表示全部程序；多個以 ; 分隔）",
    "AdvDesc_Regex": "若複製的文字符合此正規表示式，則不會儲存到 Ditto",
    "AdvDesc_IgnoreCFDIB": '不區分大小寫。建議選項為 "excel.exe; onenote.exe; powerpnt.exe" ',
    "AdvCopyScriptsTitle": "複製時指令碼",
    "AdvPasteScriptsTitle": "貼上時指令碼",
    "AdvResetClipOrderTitle": "選取要重設剪貼順序的群組",
}

ADV_OPTIONS_NEXT = ('>', '2124')


def xml_escape_attr(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace('"', "&quot;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def xml_escape_text(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def item_line(english: str, item_id: str, foreign: str) -> str:
    return (
        f'\t\t<Item English_Text = "{xml_escape_attr(english)}" '
        f'ID = "{xml_escape_attr(item_id)}">{xml_escape_text(foreign)}</Item>'
    )


def build_adv_properties(foreign_map: dict[int, str]) -> str:
    lines = ["\t<Ditto_Adv_Properties>"]
    for sid in sorted(PROPS):
        en = PROPS[sid]
        foreign = foreign_map.get(sid, en)
        lines.append(item_line(en, str(sid), foreign))
    lines.append("\t</Ditto_Adv_Properties>")
    return "\n".join(lines)


def ensure_string_items(text: str, foreign_map: dict[str, str]) -> str:
    for sid, en in STRINGS_EN.items():
        if f'ID = "{sid}"' in text or f'ID="{sid}"' in text:
            continue
        foreign = foreign_map.get(sid, en)
        insert = item_line(en, sid, foreign) + "\n"
        text = text.replace("\t</Ditto_String_Table>", insert + "\t</Ditto_String_Table>", 1)
    return text


def ensure_adv_options_next(text: str, foreign: str) -> str:
    # ID 2124 next-match button on Adv page only
    section = re.search(
        r"(<Ditto_Adv_Options>)(.*?)(</Ditto_Adv_Options>)",
        text,
        flags=re.DOTALL,
    )
    if not section:
        raise RuntimeError("Ditto_Adv_Options section missing")
    body = section.group(2)
    if re.search(r'ID\s*=\s*"2124"', body):
        return text
    en, iid = ADV_OPTIONS_NEXT
    line = "\n" + item_line(en, iid, foreign)
    new_section = section.group(1) + body.rstrip() + line + "\n\t" + section.group(3)
    return text[: section.start()] + new_section + text[section.end() :]


def upsert_adv_properties(text: str, section_xml: str) -> str:
    if "<Ditto_Adv_Properties>" in text:
        text = re.sub(
            r"\t?<Ditto_Adv_Properties>.*?</Ditto_Adv_Properties>\s*",
            "",
            text,
            count=1,
            flags=re.DOTALL,
        )
    marker = "</Ditto_Adv_Options>"
    idx = text.find(marker)
    if idx < 0:
        raise RuntimeError("Ditto_Adv_Options end marker missing")
    insert_at = idx + len(marker)
    return text[:insert_at] + "\n\n" + section_xml + "\n" + text[insert_at:]


def foreign_for_file(name: str) -> tuple[dict[int, str], dict[str, str], str]:
    if name == "Chinese Simplified.xml":
        return PROPS_ZH, STRINGS_ZH, ">"
    if name == "Chinese Traditional.xml":
        return PROPS_ZH_TW, STRINGS_ZH_TW, ">"
    # English and all others: English foreign body (required for LoadSection)
    return PROPS, STRINGS_EN, ">"


def main() -> int:
    missing = [sid for sid in range(1, 112) if sid not in PROPS]
    if missing:
        print("PROPS missing ids:", missing)
        return 1
    if set(PROPS_ZH) != set(PROPS) or set(PROPS_ZH_TW) != set(PROPS):
        print("Chinese prop maps must cover all SETTING ids")
        return 1

    files = sorted(ROOT.glob("*.xml"))
    if not files:
        print("No language files in", ROOT)
        return 1

    for path in files:
        props_map, str_map, next_foreign = foreign_for_file(path.name)
        text = path.read_text(encoding="utf-8")
        text = ensure_string_items(text, str_map)
        text = ensure_adv_options_next(text, next_foreign)
        text = upsert_adv_properties(text, build_adv_properties(props_map))
        path.write_text(text, encoding="utf-8", newline="\n")
        print("updated", path.name)

    # audit
    required_ids = {str(i) for i in range(1, 112)}
    required_strings = set(STRINGS_EN)
    errors = 0
    for path in files:
        text = path.read_text(encoding="utf-8")
        m = re.search(r"<Ditto_Adv_Properties>(.*?)</Ditto_Adv_Properties>", text, re.DOTALL)
        if not m:
            print("MISSING section", path.name)
            errors += 1
            continue
        ids = set(re.findall(r'ID\s*=\s*"(\d+)"', m.group(1)))
        miss = sorted(required_ids - ids, key=int)
        if miss:
            print(f"{path.name}: missing property ids {miss[:10]}... ({len(miss)})")
            errors += 1
        # LoadSection requires child text
        empty = re.findall(
            r'<Item English_Text\s*=\s*"[^"]*"\s*ID\s*=\s*"(\d+)"\s*/>',
            m.group(1),
        )
        empty += [
            i
            for i in re.findall(
                r'<Item English_Text\s*=\s*"[^"]*"\s*ID\s*=\s*"(\d+)"\s*></Item>',
                m.group(1),
            )
        ]
        if empty:
            print(f"{path.name}: empty foreign for ids {empty[:5]}")
            errors += 1
        for sid in required_strings:
            if f'ID = "{sid}"' not in text and f'ID="{sid}"' not in text:
                print(f"{path.name}: missing string {sid}")
                errors += 1
        adv = re.search(r"<Ditto_Adv_Options>(.*?)</Ditto_Adv_Options>", text, re.DOTALL)
        if not adv or not re.search(r'ID\s*=\s*"2124"', adv.group(1)):
            print(f"{path.name}: missing Adv Options 2124")
            errors += 1

    print("audit errors:", errors)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
