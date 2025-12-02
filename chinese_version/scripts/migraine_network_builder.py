# PubMed_Gephi_Refined.py - 精炼版PubMed网络构建器
# 专门解决节点过多、分类不精确的问题

import pandas as pd
import re
import ast
from collections import defaultdict, Counter
import itertools
import os


class PubMedRefinedNetwork:
    def __init__(self):
        # 严格的医学停用词（大幅扩展）
        self.medical_stopwords = {
            "study",
            "studies",
            "research",
            "analysis",
            "effect",
            "effects",
            "patient",
            "patients",
            "group",
            "groups",
            "method",
            "methods",
            "result",
            "results",
            "conclusion",
            "conclusions",
            "objective",
            "background",
            "aim",
            "purpose",
            "significance",
            "review",
            "article",
            "paper",
            "their",
            "with",
            "the",
            "and",
            "or",
            "for",
            "from",
            "this",
            "that",
            "these",
            "those",
            "which",
            "what",
            "when",
            "where",
            "how",
            "why",
            "has",
            "have",
            "had",
            "was",
            "were",
            "is",
            "are",
            "be",
            "been",
            "being",
            "can",
            "could",
            "would",
            "should",
            "may",
            "might",
            "must",
            "author",
            "theory",
            "model",
            "system",
            "process",
            "approach",
            "perspective",
            "overview",
            "summary",
            "current",
            "future",
            "recent",
            "new",
            "novel",
            "various",
        }

        # 基于您论文框架的精确定义分类体系
        self.refined_categories = {
            # 1. 诱发机制（严格限定）
            "trigger_mechanisms": {
                "description": "诱发机制",
                "keywords": [
                    # 神经机制
                    "trigeminal",
                    "trigeminovascular",
                    "cortical spreading depression",
                    "central sensitization",
                    "neurogenic inflammation",
                    "neural mechanism",
                    # 血管机制
                    "vascular",
                    "cerebral blood flow",
                    "vasodilation",
                    "vasoconstriction",
                    # 激素机制
                    "hormonal",
                    "estrogen",
                    "progesterone",
                    "menstrual",
                    "menopause",
                    # 炎症机制
                    "inflammatory",
                    "cytokines",
                    "neuroinflammation",
                    "mast cells",
                    # 环境触发
                    "stress",
                    "sleep deprivation",
                    "weather",
                    "barometric",
                    "light sensitivity",
                ],
            },
            # 2. 确证共病（严格医学定义）
            "true_comorbidities": {
                "description": "确证共病",
                "keywords": [
                    # 精神类
                    "depression",
                    "anxiety",
                    "panic disorder",
                    "bipolar",
                    "ptsd",
                    # 神经类
                    "epilepsy",
                    "stroke",
                    "restless legs",
                    "parkinson",
                    "alzheimer",
                    # 疼痛类
                    "fibromyalgia",
                    "chronic pain",
                    "neuropathic pain",
                    # 自身免疫/过敏
                    "allergic rhinitis",
                    "asthma",
                    "irritable bowel",
                    "inflammatory bowel",
                    # 睡眠障碍
                    "insomnia",
                    "sleep apnea",
                    "circadian rhythm",
                    # 心血管
                    "hypertension",
                    "patent foramen ovale",
                    "stroke risk",
                ],
            },
            # 3. 社会影响
            "social_impact": {
                "description": "社会影响",
                "keywords": [
                    "quality of life",
                    "disability",
                    "work productivity",
                    "absenteeism",
                    "presenteeism",
                    "economic burden",
                    "healthcare cost",
                    "stigma",
                    "social isolation",
                    "family burden",
                    "daily functioning",
                ],
            },
            # 4. 干预措施
            "interventions": {
                "description": "干预措施",
                "keywords": [
                    # 药物
                    "triptans",
                    "CGRP",
                    "erenumab",
                    "fremanezumab",
                    "galcanezumab",
                    "propranolol",
                    "topiramate",
                    "amitriptyline",
                    "valproate",
                    "botulinum",
                    # 非药物
                    "cognitive behavioral therapy",
                    "biofeedback",
                    "acupuncture",
                    "physical therapy",
                    "relaxation",
                    "mindfulness",
                    "yoga",
                    # 生活方式
                    "diet",
                    "exercise",
                    "sleep hygiene",
                    "stress management",
                    # 新兴治疗
                    "neuromodulation",
                    "monoclonal antibodies",
                    "gene therapy",
                ],
            },
        }

        # 需要排除的研究方法术语（单独分类）
        self.research_methods = {
            "randomized controlled trial",
            "cohort study",
            "case control",
            "cross sectional",
            "systematic review",
            "meta analysis",
            "clinical trial",
            "observational study",
            "diagnostic criteria",
            "assessment scale",
            "statistical analysis",
            "epidemiology",
        }

    def load_pubmed_data(self, file_path):
        """加载数据"""
        try:
            # 尝试多种格式
            for encoding in ["utf-8", "latin-1", "cp1252"]:
                for sep in [",", "\t", ";"]:
                    try:
                        df = pd.read_csv(
                            file_path, encoding=encoding, sep=sep, quoting=1, on_bad_lines="skip"
                        )
                        if len(df.columns) > 3:
                            print(f"成功读取: {encoding}, 分隔符: '{sep}'")
                            return df
                    except:
                        continue
            return pd.read_csv(file_path, engine="python", on_bad_lines="skip")
        except Exception as e:
            print(f"读取失败: {e}")
            return None

    def strict_term_cleaning(self, term):
        """严格的术语清理"""
        if pd.isna(term) or not term.strip():
            return None

        term = str(term).strip()

        # 1. 去除所有特殊标记
        term = re.sub(r"^\*+|\*+$", "", term)  # 开头结尾星号
        term = re.sub(r"/\*.*", "", term)  # 斜杠星号后内容
        term = re.sub(r"\[.*?\]|\(.*?\)", "", term)  # 括号内容

        # 2. 转换为小写并分割
        term = term.lower()
        words = term.split()

        # 3. 严格过滤
        filtered_words = []
        for word in words:
            # 长度要求
            if len(word) < 3 or len(word) > 20:
                continue
            # 停用词过滤
            if word in self.medical_stopwords:
                continue
            # 数字过滤
            if word.isdigit():
                continue
            # 特殊字符检查
            if re.search(r"[^a-z\-]", word):
                continue

            filtered_words.append(word)

        if not filtered_words:
            return None

        term = " ".join(filtered_words)

        # 4. 标题化并返回
        return term.title()

    def precise_categorization(self, term):
        """精确分类"""
        term_lower = term.lower()

        # 首先检查是否是研究方法（需要排除）
        for research_term in self.research_methods:
            if research_term in term_lower:
                return "research_methods"  # 单独标记，后续过滤

        # 精确匹配分类
        for category, info in self.refined_categories.items():
            for keyword in info["keywords"]:
                if keyword in term_lower:
                    return category

        # 基于内容推断（更严格）
        trigger_words = ["mechanism", "pathophysiology", "etiology", "trigger", "sensitization"]
        comorbidity_words = ["comorbidity", "comorbid", "coexisting", "associated with"]
        impact_words = ["burden", "cost", "productivity", "quality", "disability"]
        intervention_words = ["therapy", "treatment", "medication", "management", "intervention"]

        if any(word in term_lower for word in trigger_words):
            return "trigger_mechanisms"
        elif any(word in term_lower for word in comorbidity_words):
            return "true_comorbidities"
        elif any(word in term_lower for word in impact_words):
            return "social_impact"
        elif any(word in term_lower for word in intervention_words):
            return "interventions"

        return "unclassified"  # 未分类的将被过滤

    def extract_high_quality_terms(self, tags_str, content_text=""):
        """提取高质量术语"""
        if pd.isna(tags_str):
            return []

        tags_str = str(tags_str)
        high_quality_terms = set()

        # 分割标签
        segments = re.split(r"[;,]", tags_str)

        for segment in segments:
            cleaned_term = self.strict_term_cleaning(segment)
            if not cleaned_term:
                continue

            # 分类检查
            category = self.precise_categorization(cleaned_term)

            # 只保留明确分类的术语
            if category != "unclassified" and category != "research_methods":
                high_quality_terms.add(cleaned_term)

        return list(high_quality_terms)

    def build_refined_network(self, df, min_frequency=3, min_weight=2):
        """构建精炼网络"""
        print("构建精炼网络（大幅减少节点数量）...")

        article_keywords = []

        for idx, row in df.iterrows():
            if idx % 200 == 0 and idx > 0:
                print(f"处理进度: {idx}/{len(df)}")

            # 提取高质量术语
            manual_tags = self.extract_high_quality_terms(row.get("Manual Tags", ""))

            # 限制每篇文章的术语数量（防止单篇文章贡献过多节点）
            if len(manual_tags) > 15:
                manual_tags = manual_tags[:15]

            if manual_tags:
                article_keywords.append(manual_tags)

        print(f"有效文章数: {len(article_keywords)}")

        # 计算节点频率
        node_frequency = Counter()
        for keywords in article_keywords:
            node_frequency.update(keywords)

        # 严格过滤：只保留高频术语
        filtered_terms = {
            term: freq for term, freq in node_frequency.items() if freq >= min_frequency
        }

        print(f"过滤后术语数: {len(filtered_terms)} (原: {len(node_frequency)})")

        # 计算边权重（只考虑过滤后的术语）
        edge_weights = defaultdict(int)
        for keywords in article_keywords:
            # 只考虑过滤后的术语
            filtered_keywords = [kw for kw in keywords if kw in filtered_terms]
            for kw1, kw2 in itertools.combinations(sorted(filtered_keywords), 2):
                edge_weights[(kw1, kw2)] += 1

        # 创建节点数据
        nodes_data = []
        for term, freq in filtered_terms.items():
            category = self.precise_categorization(term)
            nodes_data.append(
                {
                    "Id": re.sub(r"[^\w]", "_", term.lower())[:30],
                    "Label": term,
                    "Category": category,
                    "Frequency": freq,
                    "Category_Description": self.refined_categories.get(category, {}).get(
                        "description", "其他"
                    ),
                }
            )

        # 创建边数据（应用权重阈值）
        edges_data = []
        for (term1, term2), weight in edge_weights.items():
            if weight >= min_weight:  # 权重阈值
                source_id = next(
                    (node["Id"] for node in nodes_data if node["Label"] == term1), None
                )
                target_id = next(
                    (node["Id"] for node in nodes_data if node["Label"] == term2), None
                )

                if source_id and target_id:
                    edges_data.append(
                        {
                            "Source": source_id,
                            "Target": target_id,
                            "Weight": weight,
                            "Type": "Undirected",
                            "Source_Label": term1,
                            "Target_Label": term2,
                        }
                    )

        nodes_df = pd.DataFrame(nodes_data)
        edges_df = pd.DataFrame(edges_data)

        print(f"最终网络规模: {len(nodes_df)}节点, {len(edges_df)}边")
        print(f"节点减少: {(3645 - len(nodes_df)) / 3645 * 100:.1f}%")
        print(f"边减少: {(181245 - len(edges_df)) / 181245 * 100:.1f}%")

        return nodes_df, edges_df

    def analyze_refined_network(self, nodes_df, edges_df):
        """分析精炼网络"""
        print("\n" + "=" * 60)
        print("精炼网络分析报告")
        print("=" * 60)

        # 基本统计
        print(f"网络规模:")
        print(f"  - 节点数: {len(nodes_df):,} (原3,645个)")
        print(f"  - 边数: {len(edges_df):,} (原181,245条)")
        print(f"  - 网络密度: {len(edges_df) / (len(nodes_df) * (len(nodes_df) - 1) / 2):.6f}")

        # 类别分布
        print(f"\n节点分类分布:")
        category_stats = nodes_df["Category"].value_counts()
        for category, count in category_stats.items():
            desc = self.refined_categories.get(category, {}).get("description", "其他")
            percentage = (count / len(nodes_df)) * 100
            print(f"  - {desc}: {count}节点 ({percentage:.1f}%)")

        # 高频术语
        print(f"\nTop 20 高频术语:")
        top_terms = nodes_df.nlargest(20, "Frequency")
        for idx, row in top_terms.iterrows():
            desc = self.refined_categories.get(row["Category"], {}).get("description", "其他")
            print(f"  {idx + 1:2d}. {row['Label']:25s} (频率: {row['Frequency']:2d}, 类别: {desc})")

        # 强关联
        if not edges_df.empty:
            print(f"\nTop 10 强共现关系:")
            top_edges = edges_df.nlargest(10, "Weight")
            for idx, row in top_edges.iterrows():
                print(
                    f"  {idx + 1:2d}. {row['Source_Label']:20s} ←→ {row['Target_Label']:20s} (权重: {row['Weight']})"
                )


def main():
    """主函数"""
    converter = PubMedRefinedNetwork()

    # 文件路径
    file_path = r"C:\Users\29385\Desktop\大三\复杂网络\偏头痛2\PubMed.csv"

    if not os.path.exists(file_path):
        print(f"文件不存在: {file_path}")
        return

    # 加载数据
    print("加载PubMed数据...")
    df = converter.load_pubmed_data(file_path)

    if df is None or df.empty:
        print("数据加载失败")
        return

    print(f"数据规模: {len(df)}行 × {len(df.columns)}列")

    # 构建精炼网络（提高阈值）
    nodes_df, edges_df = converter.build_refined_network(df, min_frequency=3, min_weight=2)

    if nodes_df.empty:
        print("网络构建失败")
        return

    # 分析网络
    converter.analyze_refined_network(nodes_df, edges_df)

    # 保存文件
    output_dir = os.path.dirname(file_path)

    # Gephi文件
    nodes_df[["Id", "Label", "Category", "Frequency"]].to_csv(
        os.path.join(output_dir, "gephi_refined_nodes.csv"), index=False, encoding="utf-8-sig"
    )

    edges_df[["Source", "Target", "Weight", "Type"]].to_csv(
        os.path.join(output_dir, "gephi_refined_edges.csv"), index=False, encoding="utf-8-sig"
    )

    # 详细文件（用于分析）
    nodes_df.to_csv(
        os.path.join(output_dir, "detailed_refined_nodes.csv"), index=False, encoding="utf-8-sig"
    )
    edges_df.to_csv(
        os.path.join(output_dir, "detailed_refined_edges.csv"), index=False, encoding="utf-8-sig"
    )

    print(f"\n✅ 精炼网络文件已生成！")
    print(f"📊 预期网络规模: {len(nodes_df)}节点, {len(edges_df)}边")
    print(
        f"📉 规模减少: 节点-{(3645 - len(nodes_df)) / 3645 * 100:.1f}%, 边-{(181245 - len(edges_df)) / 181245 * 100:.1f}%"
    )

    # Gephi优化参数
    gephi_guide = """
    🎯 Gephi优化参数（针对精炼网络）:

    布局算法: ForceAtlas 2
    - 斥力强度: 2000 (原1000)
    - 重力: 50 (原5) 
    - 防止重叠: ✅ 开启
    - 边权重影响: 1.0
    - 运行时间: 3-5分钟

    外观设置:
    - 节点颜色: 按Category字段
    - 节点大小: 按Frequency字段 (2-15范围)
    - 标签: 只显示Frequency > 5的节点
    - 边透明度: 0.3 (提高可读性)
    """

    print(gephi_guide)

    # 保存指南
    with open(os.path.join(output_dir, "gephi_optimized_guide.txt"), "w", encoding="utf-8") as f:
        f.write(gephi_guide)


if __name__ == "__main__":
    main()
