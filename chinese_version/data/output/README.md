# 输出数据目录

## 📤 说明

此目录包含脚本生成的所有网络分析结果文件。

## 📋 文件列表

### Gephi可视化文件

#### 1. `gephi_refined_nodes.csv`
**节点文件 - 用于Gephi导入**

| 列名 | 说明 | 示例 |
|------|------|------|
| Id | 节点唯一标识符 | `quality_life` |
| Label | 显示标签 | `Quality Life` |
| Category | 分类 | `social_impact` |
| Frequency | 出现频率 | `645` |

**数据规模**: 238个节点

---

#### 2. `gephi_refined_edges.csv`
**边文件 - 用于Gephi导入**

| 列名 | 说明 | 示例 |
|------|------|------|
| Source | 起始节点ID | `quality_life` |
| Target | 目标节点ID | `treatment_outcome` |
| Weight | 边权重（共现次数） | `166` |
| Type | 边类型 | `Undirected` |

**数据规模**: 863条边

---

### 详细分析文件

#### 3. `detailed_refined_nodes.csv`
**完整节点数据 - 用于深入分析**

包含额外字段:
- `Category_Description`: 中文分类描述
- 完整的元数据信息

**用途**:
- 统计分析
- 分类研究
- 术语频率分析

---

#### 4. `detailed_refined_edges.csv`
**完整边数据 - 用于关系分析**

包含额外字段:
- `Source_Label`: 起始节点标签
- `Target_Label`: 目标节点标签
- 完整的关系元数据

**用途**:
- 共现模式分析
- 强关联识别
- 网络度量计算

---

## 📊 数据统计摘要

### 网络规模
- **节点数**: 238
- **边数**: 863
- **网络密度**: 0.000306
- **优化率**: 节点减少93.5%, 边减少99.5%

### 分类分布
```
干预措施 (Interventions)      : 131 节点 (55.0%)
社会影响 (Social Impact)       : 47 节点 (19.7%)
确证共病 (True Comorbidities)  : 40 节点 (16.8%)
诱发机制 (Trigger Mechanisms)  : 20 节点 (8.4%)
```

### 高频术语 Top 5
1. Quality Life - 645次
2. Treatment Outcome - 621次
3. Comorbidity - 473次
4. Migraine Therapy - 323次
5. Depression - 145次

## 🎨 Gephi导入步骤

### 1. 导入节点
```
数据实验室 → 导入电子表格 → 选择 gephi_refined_nodes.csv
选项: 作为节点表导入
```

### 2. 导入边
```
数据实验室 → 导入电子表格 → 选择 gephi_refined_edges.csv
选项: 作为边表导入
```

### 3. 应用布局
参考 `config/gephi_visualization_guide.txt`

## 📈 数据用途

### Gephi文件
- ✅ 网络可视化
- ✅ 布局算法应用
- ✅ 交互式探索

### 详细文件
- ✅ Python/R深度分析
- ✅ 统计报告生成
- ✅ 学术论文数据源

## 🔄 更新数据

重新运行脚本会覆盖这些文件。建议:
1. 保存当前版本到备份目录
2. 运行新的分析
3. 比较结果差异

## 🛠️ 数据格式

所有CSV文件:
- **编码**: UTF-8-sig（支持中文）
- **分隔符**: 逗号 (,)
- **引用**: 双引号 (" ") 用于包含逗号的字段

## 📖 进一步阅读

- 查看 `PROJECT_OVERVIEW.md` 了解完整项目说明
- 参考 `config/` 目录了解可视化配置
- 阅读 `scripts/README.md` 了解如何调整参数
