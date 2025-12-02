"""
Test Suite for Migraine Network Analysis

This module contains comprehensive tests for the PubMed network builder.
Tests cover data loading, term cleaning, categorization, and network construction.

Usage:
    pytest tests/test_main.py -v
    pytest tests/test_main.py --cov=english_version/scripts
"""

import pytest
import pandas as pd
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "english_version" / "scripts"))

# Import the class after path is set
from main import PubMedRefinedNetworkV2  # noqa: E402


class TestPubMedRefinedNetworkV2:
    """Test suite for the main PubMed network builder"""

    @pytest.fixture
    def network_builder(self):
        """Fixture to create a network builder instance"""
        return PubMedRefinedNetworkV2()

    @pytest.fixture
    def sample_data(self):
        """Fixture to create sample PubMed data"""
        return pd.DataFrame(
            {
                "Manual Tags": [
                    "Migraine; Depression; Anxiety; CGRP",
                    "Stress; Quality of Life; Triptans",
                    "Epilepsy; Comorbidity; Treatment Outcome",
                ],
                "Abstract Note": [
                    "This study examines the relationship between migraine and depression.",
                    "Stress is a major trigger mechanism for migraine attacks.",
                    "Epilepsy commonly co-occurs with migraine as a comorbidity.",
                ],
                "Keywords": [
                    "migraine, mental health, intervention",
                    "stress management, quality of life",
                    "neurological comorbidities",
                ],
            }
        )

    # ==================== INITIALIZATION TESTS ====================

    def test_initialization(self, network_builder):
        """Test that the network builder initializes correctly"""
        assert network_builder is not None
        assert hasattr(network_builder, "medical_stopwords")
        assert hasattr(network_builder, "refined_categories")
        assert len(network_builder.refined_categories) == 4

    def test_stopwords_exist(self, network_builder):
        """Test that medical stopwords are defined"""
        assert "study" in network_builder.medical_stopwords
        assert "patient" in network_builder.medical_stopwords
        assert "research" in network_builder.medical_stopwords
        assert len(network_builder.medical_stopwords) > 20

    def test_categories_structure(self, network_builder):
        """Test that categories have required structure"""
        required_categories = [
            "trigger_mechanisms",
            "true_comorbidities",
            "social_impact",
            "interventions",
        ]
        for cat in required_categories:
            assert cat in network_builder.refined_categories
            assert "description" in network_builder.refined_categories[cat]
            assert "keywords" in network_builder.refined_categories[cat]
            assert len(network_builder.refined_categories[cat]["keywords"]) > 0

    # ==================== TERM CLEANING TESTS ====================

    def test_strict_term_cleaning_basic(self, network_builder):
        """Test basic term cleaning functionality"""
        # Normal term
        assert network_builder.strict_term_cleaning("migraine") == "Migraine"
        # Term with spaces
        assert network_builder.strict_term_cleaning("quality of life") == "Quality Life"
        # Term with special characters
        result = network_builder.strict_term_cleaning("migraine*")
        assert result == "Migraine" or result is None

    def test_strict_term_cleaning_stopwords(self, network_builder):
        """Test that stopwords are removed"""
        assert network_builder.strict_term_cleaning("study") is None
        assert network_builder.strict_term_cleaning("research patient") is None
        assert network_builder.strict_term_cleaning("the patient study") is None

    def test_strict_term_cleaning_edge_cases(self, network_builder):
        """Test edge cases in term cleaning"""
        assert network_builder.strict_term_cleaning("") is None
        assert network_builder.strict_term_cleaning(None) is None
        assert network_builder.strict_term_cleaning("   ") is None
        assert network_builder.strict_term_cleaning("a") is None  # Too short
        assert network_builder.strict_term_cleaning("x" * 25) is None  # Too long

    def test_strict_term_cleaning_numbers(self, network_builder):
        """Test that pure numbers are filtered"""
        assert network_builder.strict_term_cleaning("123") is None
        assert network_builder.strict_term_cleaning("2024") is None

    # ==================== CATEGORIZATION TESTS ====================

    def test_precise_categorization_triggers(self, network_builder):
        """Test categorization of trigger mechanism terms"""
        assert network_builder.precise_categorization("stress") == "trigger_mechanisms"
        assert network_builder.precise_categorization("hormonal") == "trigger_mechanisms"
        assert network_builder.precise_categorization("inflammatory") == "trigger_mechanisms"
        assert network_builder.precise_categorization("vascular") == "trigger_mechanisms"

    def test_precise_categorization_comorbidities(self, network_builder):
        """Test categorization of comorbidity terms"""
        assert network_builder.precise_categorization("depression") == "true_comorbidities"
        assert network_builder.precise_categorization("anxiety") == "true_comorbidities"
        assert network_builder.precise_categorization("epilepsy") == "true_comorbidities"
        assert network_builder.precise_categorization("stroke") == "true_comorbidities"

    def test_precise_categorization_impact(self, network_builder):
        """Test categorization of social impact terms"""
        assert network_builder.precise_categorization("quality of life") == "social_impact"
        assert network_builder.precise_categorization("disability") == "social_impact"
        assert network_builder.precise_categorization("economic burden") == "social_impact"

    def test_precise_categorization_interventions(self, network_builder):
        """Test categorization of intervention terms"""
        assert network_builder.precise_categorization("triptans") == "interventions"
        assert network_builder.precise_categorization("acupuncture") == "interventions"
        assert network_builder.precise_categorization("cgrp") == "interventions"
        assert network_builder.precise_categorization("botulinum") == "interventions"

    def test_precise_categorization_unclassified(self, network_builder):
        """Test that unknown terms are marked as unclassified"""
        assert network_builder.precise_categorization("random unknown term") == "unclassified"
        assert network_builder.precise_categorization("xyz123") == "unclassified"

    # ==================== TERM EXTRACTION TESTS ====================

    def test_extract_high_quality_terms_basic(self, network_builder):
        """Test basic term extraction from tags"""
        tags = "Migraine; Depression; Anxiety"
        terms = network_builder.extract_high_quality_terms(tags)
        assert len(terms) > 0
        assert "Anxiety" in terms

    def test_extract_high_quality_terms_with_abstract(self, network_builder):
        """Test term extraction including abstract text"""
        tags = "Migraine"
        abstract = "This study examines depression and anxiety in migraine patients."
        terms = network_builder.extract_high_quality_terms(tags, abstract_text=abstract)
        assert len(terms) >= 1
        # Should extract at least migraine, possibly depression/anxiety

    def test_extract_high_quality_terms_filters_research(self, network_builder):
        """Test that research methodology terms are filtered"""
        tags = "Stress; Randomized Controlled Trial; Meta Analysis"
        terms = network_builder.extract_high_quality_terms(tags)
        assert "Stress" in terms
        # Research terms should be filtered
        assert not any("trial" in t.lower() or "meta" in t.lower() for t in terms)

    def test_extract_high_quality_terms_empty_input(self, network_builder):
        """Test extraction with empty input"""
        assert network_builder.extract_high_quality_terms("") == []
        assert network_builder.extract_high_quality_terms(None) == []

    # ==================== NETWORK BUILDING TESTS ====================

    def test_build_refined_network_structure(self, network_builder, sample_data):
        """Test that network building returns correct structure"""
        nodes_df, edges_df = network_builder.build_refined_network(
            sample_data, min_frequency=1, min_weight=1
        )

        # Check DataFrames exist and have correct columns
        assert isinstance(nodes_df, pd.DataFrame)
        assert isinstance(edges_df, pd.DataFrame)

        assert "Id" in nodes_df.columns
        assert "Label" in nodes_df.columns
        assert "Category" in nodes_df.columns
        assert "Frequency" in nodes_df.columns

        assert "Source" in edges_df.columns
        assert "Target" in edges_df.columns
        assert "Weight" in edges_df.columns
        assert "Type" in edges_df.columns

    def test_build_refined_network_nonempty(self, network_builder, sample_data):
        """Test that network building produces results"""
        nodes_df, edges_df = network_builder.build_refined_network(
            sample_data, min_frequency=1, min_weight=1
        )

        assert len(nodes_df) > 0, "Nodes dataframe should not be empty"
        # Edges may be empty with small sample data

    def test_build_refined_network_frequency_filter(self, network_builder, sample_data):
        """Test that frequency filtering works"""
        # With low threshold
        nodes_low, _ = network_builder.build_refined_network(
            sample_data, min_frequency=1, min_weight=1
        )

        # With high threshold
        nodes_high, _ = network_builder.build_refined_network(
            sample_data, min_frequency=10, min_weight=1
        )

        # Higher threshold should produce fewer or equal nodes
        assert len(nodes_high) <= len(nodes_low)

    def test_build_refined_network_categories_valid(self, network_builder, sample_data):
        """Test that all nodes have valid categories"""
        nodes_df, _ = network_builder.build_refined_network(
            sample_data, min_frequency=1, min_weight=1
        )

        valid_categories = list(network_builder.refined_categories.keys())
        for category in nodes_df["Category"]:
            assert category in valid_categories, f"Invalid category: {category}"

    # ==================== INTEGRATION TESTS ====================

    def test_full_pipeline_sample_data(self, network_builder, sample_data):
        """Test complete pipeline with sample data"""
        # Build network
        nodes_df, edges_df = network_builder.build_refined_network(
            sample_data, min_frequency=1, min_weight=1
        )

        # Verify output
        assert len(nodes_df) > 0
        assert all(nodes_df["Frequency"] >= 1)

        # Run analysis (should not crash)
        try:
            network_builder.analyze_refined_network(nodes_df, edges_df)
        except Exception as e:
            pytest.fail(f"Analysis should not raise exception: {e}")

    # ==================== DATA VALIDATION TESTS ====================

    def test_node_ids_unique(self, network_builder, sample_data):
        """Test that node IDs are unique"""
        nodes_df, _ = network_builder.build_refined_network(
            sample_data, min_frequency=1, min_weight=1
        )

        assert len(nodes_df["Id"]) == len(nodes_df["Id"].unique()), "Node IDs should be unique"

    def test_edge_references_valid(self, network_builder, sample_data):
        """Test that edges reference valid nodes"""
        nodes_df, edges_df = network_builder.build_refined_network(
            sample_data, min_frequency=1, min_weight=1
        )

        if len(edges_df) > 0:
            node_ids = set(nodes_df["Id"])
            for _, edge in edges_df.iterrows():
                assert edge["Source"] in node_ids, f"Edge source {edge['Source']} not in nodes"
                assert edge["Target"] in node_ids, f"Edge target {edge['Target']} not in nodes"


# ==================== PERFORMANCE TESTS ====================


@pytest.mark.slow
def test_large_dataset_performance():
    """Test performance with larger dataset (marked as slow)"""
    # Create larger sample
    large_data = pd.DataFrame(
        {
            "Manual Tags": ["Migraine; Depression"] * 100,
            "Abstract Note": ["Sample abstract text"] * 100,
            "Keywords": ["test keywords"] * 100,
        }
    )

    builder = PubMedRefinedNetworkV2()

    import time

    start = time.time()
    nodes, edges = builder.build_refined_network(large_data, min_frequency=2, min_weight=1)
    elapsed = time.time() - start

    # Should complete in reasonable time (< 5 seconds for 100 articles)
    assert elapsed < 5.0, f"Processing took too long: {elapsed:.2f}s"
    assert len(nodes) > 0


# ==================== FIXTURE FOR SAMPLE CSV ====================


@pytest.fixture
def sample_csv_file(tmp_path):
    """Create a temporary sample CSV file for testing"""
    csv_path = tmp_path / "sample_pubmed.csv"

    sample_df = pd.DataFrame(
        {
            "Manual Tags": [
                "Migraine; Depression; Anxiety",
                "Stress; Quality of Life",
                "Epilepsy; Comorbidity",
            ],
            "Abstract Note": [
                "Sample abstract about migraine and depression",
                "Sample abstract about stress",
                "Sample abstract about epilepsy",
            ],
            "Keywords": ["migraine, mental health", "stress, triggers", "comorbidity, epilepsy"],
        }
    )

    sample_df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    return csv_path


def test_load_pubmed_data_valid_file(sample_csv_file):
    """Test loading a valid CSV file"""
    builder = PubMedRefinedNetworkV2()
    df = builder.load_pubmed_data(str(sample_csv_file))

    assert df is not None
    assert len(df) == 3
    assert "Manual Tags" in df.columns


def test_load_pubmed_data_missing_file():
    """Test loading a non-existent file"""
    builder = PubMedRefinedNetworkV2()
    df = builder.load_pubmed_data("nonexistent_file.csv")

    assert df is None
