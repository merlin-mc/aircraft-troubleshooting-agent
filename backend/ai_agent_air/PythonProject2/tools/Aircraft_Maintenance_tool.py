"""
ATA章节速查工具模块，提供常见ATA章节编号与定义的快速查询
"""
from langchain_core.tools import tool
@tool
def ata_chapter_lookup(chapter: str) -> str:
    """
    根据ATA章节编号查询该章节的定义和涵盖范围。
    例如输入 "21" 返回 "空调系统 (Environmental Control System)"
    支持2位数字查询（如"21"、"24"、"27"、"29"、"32"、"49"等）

    :param chapter: ATA章节编号（2位数字字符串），如 "21"、"ATA24"
    :return: 章节定义及相关说明
    """
    ata_database = {
        "21": "ATA 21 - 空调系统 (Air Conditioning)：包括座舱增压、温度控制、空气分配、PACK组件等。",
        "22": "ATA 22 - 自动飞行系统 (Auto Flight)：包括自动驾驶、飞行指引、偏航阻尼、FAC/FCU等。",
        "23": "ATA 23 - 通信系统 (Communications)：包括VHF/HF通信、SATCOM、客舱广播、内话系统等。",
        "24": "ATA 24 - 电源系统 (Electrical Power)：包括发电机(IDG)、TRU、电瓶、GCU、发电机控制等。",
        "25": "ATA 25 - 设备/装饰 (Equipment/Furnishings)：包括客舱座椅、厨房、洗手间、灯光装饰等。",
        "26": "ATA 26 - 防火系统 (Fire Protection)：包括发动机火警探测、APU火警、货舱烟雾探测、灭火瓶等。",
        "27": "ATA 27 - 飞行操纵系统 (Flight Controls)：包括副翼、升降舵、方向舵、缝翼/襟翼、扰流板等。",
        "28": "ATA 28 - 燃油系统 (Fuel System)：包括燃油泵、燃油计量、加油/放油、燃油交输等。",
        "29": "ATA 29 - 液压系统 (Hydraulic Power)：包括液压泵(EDP/ACMP)、蓄压器、PTU、电动泵、管路等。",
        "32": "ATA 32 - 起落架系统 (Landing Gear)：包括起落架收放、刹车、前轮转弯、舱门等。",
        "34": "ATA 34 - 导航系统 (Navigation)：包括IRS、ADR、VOR/ILS、DME、GNSS等。",
        "36": "ATA 36 - 引气系统 (Pneumatic)：包括发动机引气、APU引气、预冷器、PRV活门等。",
        "49": "ATA 49 - 辅助动力装置 (APU)：包括APU启动、供气、供电、ECU控制等。",
        "51": "ATA 51 - 标准实践与结构-总体 (Standard Practices - General)",
        "52": "ATA 52 - 舱门 (Doors)：包括客舱门、货舱门、应急出口、增压舱门等。",
        "53": "ATA 53 - 机身 (Fuselage)：包括机身结构、框架、蒙皮、地板等。",
        "54": "ATA 54 - 短舱/吊舱 (Nacelles/Pylons)：包括发动机短舱、反推整流罩等。",
        "55": "ATA 55 - 安定面 (Stabilizers)：包括水平安定面、垂直安定面等。",
        "56": "ATA 56 - 窗户 (Windows)：包括驾驶舱窗、客舱窗、应急窗等。",
        "57": "ATA 57 - 机翼 (Wings)：包括机翼结构、翼梢小翼、翼身整流罩等。",
        "70": "ATA 70 - 标准实践-发动机 (Standard Practices - Engine)",
        "71": "ATA 71 - 动力装置 (Power Plant)：包括发动机安装、吊架等。",
        "72": "ATA 72 - 发动机 (Engine)：包括CFM56/V2500/LEAP发动机本体结构。",
        "73": "ATA 73 - 发动机燃油与控制 (Engine Fuel & Control)：包括燃油泵、燃油计量组件等。",
        "74": "ATA 74 - 点火系统 (Ignition)：包括点火激励器、点火线、选择电门等。",
        "75": "ATA 75 - 空气系统 (Air)：包括发动机引气、空调、增压等空气管路。",
        "76": "ATA 76 - 发动机控制 (Engine Controls)：包括FADEC、EEC、燃油控制组件等。",
        "77": "ATA 77 - 发动机指示 (Engine Indicating)：包括EPR、N1/N2、EGT、振动指示等。",
        "78": "ATA 78 - 排气系统 (Exhaust)：包括尾喷管、反推排气、排气活门等。",
        "79": "ATA 79 - 发动机滑油系统 (Engine Oil)：包括滑油箱、滑油管路、滑油冷却器等。",
    }
    ch = chapter.strip().upper()
    if ch.startswith("ATA"):
        ch = ch.replace("ATA", "").strip()

    if ch in ata_database:
        return f"✅ {ata_database[ch]}"
    else:
        return f"⚠️ 未找到ATA {chapter} 章节的定义。支持的章节：21-29, 32, 34, 36, 49-57, 70-79。建议通过知识库工具(query_knowledge)检索详细内容。"

tools = [ata_chapter_lookup]
