"""Unit tests for subgroup assigners on brset_mlcp metadata (no images)."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.subgroups import (
    SUBGROUP_ASSIGNERS,
    assign_age_subgroup,
    assign_education_subgroup,
    assign_insurance_subgroup,
    assign_sex_subgroup,
)


BRSET_CSV = ROOT / ".reference" / "brset_mlcp" / "data" / "train_brset_nooverlap.csv"
MBRSET_CSV = ROOT / ".reference" / "brset_mlcp" / "data" / "test_mbrset_nooverlap.csv"


@pytest.fixture
def brset_df():
    assert BRSET_CSV.exists(), f"Missing {BRSET_CSV}"
    return pd.read_csv(BRSET_CSV)


@pytest.fixture
def mbrset_df():
    assert MBRSET_CSV.exists(), f"Missing {MBRSET_CSV}"
    return pd.read_csv(MBRSET_CSV)


def test_censored_age_is_old():
    assert assign_age_subgroup(">= 90", use_median=60.0) == "old"


def test_brset_age_assignments(brset_df):
    ages = brset_df["patient_age"].dropna()
    median = float(ages.median())
    groups = ages.map(lambda a: assign_age_subgroup(a, use_median=median))
    assert set(groups.unique()) <= {"young", "old", "unknown"}
    assert len(groups) == len(ages)
    young = (ages < median).sum()
    assert (groups == "young").sum() == young


def test_brset_sex_assignments(brset_df):
    groups = brset_df["patient_sex"].map(assign_sex_subgroup)
    assert set(groups.unique()) <= {"male", "female", "unknown"}
    assert groups.isin(["male", "female"]).mean() > 0.95


def test_mbrset_has_demographic_columns(mbrset_df):
    for col in ("age", "sex"):
        assert col in mbrset_df.columns
        assert mbrset_df[col].notna().sum() > 0


def test_mbrset_education_insurance_if_present(mbrset_df):
    for col in ("educational_level", "insurance"):
        assert col in mbrset_df.columns
        assigner = SUBGROUP_ASSIGNERS[col]
        groups = mbrset_df[col].dropna().map(lambda v: assigner(v))
        assert set(groups.unique()) <= {"literate", "illiterate", "insured", "uninsured", "unknown"}


def test_education_code_1_is_illiterate():
    # PhysioNet mBRSET codebook: 1 = Illiterate, 2-7 = higher schooling.
    assert assign_education_subgroup(1) == "illiterate"
    assert assign_education_subgroup(1.0) == "illiterate"
    assert assign_education_subgroup(2) == "literate"
    assert assign_education_subgroup(7) == "literate"
    assert assign_education_subgroup(float("nan")) == "unknown"


def test_insurance_codes():
    assert assign_insurance_subgroup(0) == "uninsured"
    assert assign_insurance_subgroup(1) == "insured"
    assert assign_insurance_subgroup(float("nan")) == "unknown"


def test_no_all_unknown_sex(brset_df):
    groups = brset_df["patient_sex"].map(assign_sex_subgroup)
    assert (groups == "unknown").mean() < 0.01
