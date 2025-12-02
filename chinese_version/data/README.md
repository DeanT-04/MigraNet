# 数据目录说明

## 📂 目录结构

```
data/
├── input/          # 输入数据目录
│   └── README.md  # 输入数据说明
└── output/         # 输出结果目录
    └── README.md  # 输出文件说明
```

## 📥 输入数据 (input/)

存放原始PubMed导出的CSV文件。

**要求:**
- 格式: CSV文件
- 必需列: Manual Tags（手动标签）
- 编码: UTF-8或其他常见编码
- 来源: PubMed文献数据库

## 📤 输出数据 (output/)

存放脚本生成的网络分析结果文件。

**包含:**
- Gephi可视化文件（节点和边）
- 详细分析数据文件
- 所有文件使用UTF-8编码

## 🔄 数据流程

```
PubMed.csv (input/) 
    ↓
[脚本处理]
    ↓
网络文件 (output/)
    ↓
Gephi可视化
```

## 📋 数据要求

### 输入CSV格式示例:
```csv
Title,Authors,Year,Manual Tags,...
"Migraine study","Smith J",2023,"Depression; Anxiety; ...",...
```

### 关键字段:
- **Manual Tags**: 包含医学主题标签，用分号分隔

## 💾 数据大小参考

- 输入文件: 通常 5-50 MB
- 输出节点文件: ~15 KB
- 输出边文件: ~40-70 KB
- 详细数据文件: ~20-70 KB

## 🔒 数据安全

- 不要在输入目录放置敏感数据
- 输出文件仅包含聚合后的医学术语
- 不包含具体患者或研究者信息
