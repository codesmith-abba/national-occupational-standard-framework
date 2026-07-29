#!/usr/bin/env python3

import argparse
import sys

from validator.engine import ValidationEngine
from validator.loader import JSONLoader
from validator.report import ConsoleReport

from validator.rules.structure import StructureRule
from validator.rules.trade import TradeRule
from validator.rules.level import LevelRule
from validator.rules.unit_code import UnitCodeRule
from validator.rules.learning_outcomes import LearningOutcomesRule
from validator.rules.performance_criteria import PerformanceCriteriaRule
from validator.rules.duplicates import DuplicatesRule
from validator.rules.empty_descriptions import EmptyDescriptionsRule


def build_engine() -> ValidationEngine:
    engine = ValidationEngine()

    engine.register(StructureRule())
    engine.register(TradeRule())
    engine.register(LevelRule())
    engine.register(UnitCodeRule())
    engine.register(LearningOutcomesRule())
    engine.register(PerformanceCriteriaRule())
    engine.register(DuplicatesRule())
    engine.register(EmptyDescriptionsRule())

    return engine


def main() -> int:

    parser = argparse.ArgumentParser(
        description="Validate extracted NOS JSON files."
    )

    parser.add_argument(
        "path",
        help="JSON file or directory to validate.",
    )

    args = parser.parse_args()

    loader = JSONLoader()
    engine = build_engine()
    report = ConsoleReport()

    total_files = 0
    total_errors = 0
    total_warnings = 0

    for path, data in loader.load(args.path):

        total_files += 1

        result = engine.validate(str(path), data)

        total_errors += len(result.errors)
        total_warnings += len(result.warnings)

        print(report.render(result))
        print()

    print("=" * 60)
    print("Validation Summary")
    print("=" * 60)
    print(f"Files     : {total_files}")
    print(f"Errors    : {total_errors}")
    print(f"Warnings  : {total_warnings}")

    return 1 if total_errors else 0


if __name__ == "__main__":
    sys.exit(main())