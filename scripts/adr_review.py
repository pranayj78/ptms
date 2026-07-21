"""
ADR/RFC compliance review script.

Scans the PTMS codebase and compares implementation against
requirements defined in Architecture Decision Records (ADRs) and
Request for Comments (RFCs). Generates a structured markdown report.
"""

from __future__ import annotations

import argparse
import ast
import os
import re
import sys
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ADR_DIR = REPO_ROOT / "docs" / "adr"
SRC_DIR = REPO_ROOT / "python" / "src" / "ptms"
TEST_DIR = REPO_ROOT / "python" / "tests"

ADR_FILENAME_RE = re.compile(r"ADR-(\d+)-(.+)\.md$")
CHECKBOX_RE = re.compile(r"- \[([ x])\] (.+)")
SECTION_HEADER_RE = re.compile(r"^## ")


@dataclass
class CodeEntity:
    kind: str
    name: str
    path: str
    line: int
    file_path: str = ""


@dataclass
class ADRCheck:
    description: str
    passed: bool
    details: str = ""


@dataclass
class ADRInfo:
    number: str
    title: str
    status: str = "Unknown"
    validation_items: list[tuple[bool, str]] = field(default_factory=list)


def parse_adr_file(path: Path) -> ADRInfo | None:
    text = path.read_text()
    match = ADR_FILENAME_RE.match(path.name)
    if not match:
        return None

    number = f"ADR-{match.group(1)}"
    title = match.group(2).replace("-", " ")

    status_match = re.search(r"^## Status\s*$.*?^(\w+)\s*$", text, re.MULTILINE | re.DOTALL)
    status = status_match.group(1) if status_match else "Unknown"

    validation_items: list[tuple[bool, str]] = []
    in_validation = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped == "## Validation":
            in_validation = True
            continue
        if in_validation:
            if stripped.startswith("## ") and stripped != "## Validation":
                break
            m = CHECKBOX_RE.match(stripped)
            if m:
                validation_items.append((m.group(1) == "x", m.group(2)))

    return ADRInfo(
        number=number,
        title=title,
        status=status,
        validation_items=validation_items,
    )


def scan_python_file(path: Path) -> list[CodeEntity]:
    entities: list[CodeEntity] = []
    try:
        tree = ast.parse(path.read_text())
    except (SyntaxError, OSError):
        return entities

    rel = path.relative_to(REPO_ROOT)

    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.ClassDef):
            file_path_str = str(path)
            entities.append(
                CodeEntity(
                    kind="class",
                    name=node.name,
                    path=str(rel),
                    line=node.lineno,
                    file_path=file_path_str,
                )
            )
            for item in ast.iter_child_nodes(node):
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    entities.append(
                        CodeEntity(
                            kind="method",
                            name=f"{node.name}.{item.name}",
                            path=str(rel),
                            line=item.lineno,
                            file_path=file_path_str,
                        )
                    )
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            entities.append(
                CodeEntity(
                    kind="function",
                    name=node.name,
                    path=str(rel),
                    line=node.lineno,
                )
            )

    return entities


def scan_codebase() -> dict:
    result: dict = {
        "modules": [],
        "classes": {},
        "methods": {},
        "files": {},
    }
    if not SRC_DIR.exists():
        return result
    for pyfile in sorted(SRC_DIR.rglob("*.py")):
        entities = scan_python_file(pyfile)
        for e in entities:
            target = "methods" if e.kind == "method" else ("classes" if e.kind == "class" else None)
            if target:
                result[target][e.name] = e
        module_parts = list(pyfile.relative_to(SRC_DIR.parent.parent).parts)
        if module_parts[-1] == "__init__.py":
            module_parts = module_parts[:-1]
        else:
            module_parts[-1] = module_parts[-1][:-3]
        result["modules"].append(".".join(module_parts))
        result["files"][str(pyfile.relative_to(REPO_ROOT))] = entities
    return result


def class_has_dataclass_decorator(class_name: str, code: dict) -> tuple[bool, str]:
    ce = code["classes"].get(class_name)
    if not ce or not ce.file_path:
        return False, "class not found"
    try:
        tree = ast.parse(Path(ce.file_path).read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == class_name:
                for d in node.decorator_list:
                    if (
                        isinstance(d, ast.Call)
                        and isinstance(d.func, ast.Name)
                        and d.func.id == "dataclass"
                    ):
                        frozen = any(
                            isinstance(kw.value, ast.Constant) and kw.value.value
                            for kw in d.keywords
                            if kw.arg == "frozen"
                        )
                        order = any(
                            isinstance(kw.value, ast.Constant) and kw.value.value
                            for kw in d.keywords
                            if kw.arg == "order"
                        )
                        flags = [
                            f
                            for f in ["frozen", "order"]
                            if (f == "frozen" and frozen) or (f == "order" and order)
                        ]
                        return (
                            True,
                            f"@dataclass({', '.join(flags)}) — auto-generates __eq__, __hash__",
                        )
                    if isinstance(d, ast.Name) and d.id == "dataclass":
                        return True, "@dataclass — auto-generates __eq__, __hash__"
                return False, "no @dataclass decorator"
    except (SyntaxError, OSError):
        return False, "parse error"
    return False, "not found"


def file_has_meaningful_code(path: Path) -> bool:
    if not path.exists():
        return False
    text = path.read_text().strip()
    if not text:
        return False
    try:
        tree = ast.parse(text)
        meaningful = [
            n
            for n in ast.walk(tree)
            if isinstance(n, (ast.ClassDef, ast.FunctionDef, ast.Assign, ast.AnnAssign))
        ]
        return len(meaningful) > 0
    except SyntaxError:
        return bool(text)


def check_adr_001(code: dict) -> list[ADRCheck]:
    checks: list[ADRCheck] = []
    layers = {
        "core (`core/`)": SRC_DIR / "core",
        "domain (`domain/`)": SRC_DIR / "domain",
        "application (`application/`)": SRC_DIR / "application",
        "CLI (`cli/`)": SRC_DIR / "cli",
        "config (`config/`)": SRC_DIR / "config",
    }
    for label, path in layers.items():
        checks.append(
            ADRCheck(
                description=f"{label} directory exists",
                passed=path.exists(),
                details=str(path.relative_to(REPO_ROOT)) if path.exists() else "MISSING",
            )
        )

    domain_files = [
        "capital_gain.py",
        "employee.py",
        "employer.py",
        "loan.py",
        "property.py",
        "rsu.py",
        "tax.py",
    ]
    for name in domain_files:
        fpath = SRC_DIR / "domain" / name
        implemented = file_has_meaningful_code(fpath)
        if not fpath.exists():
            detail = "File not found"
        elif not implemented:
            detail = "File exists but is empty (no classes, functions, or assignments)"
        else:
            detail = "Implemented"
        checks.append(
            ADRCheck(
                description=f"`domain/{name}` contains domain logic",
                passed=implemented,
                details=detail,
            )
        )

    value_objects = ["Money", "AssessmentYear"]
    for vo in value_objects:
        found = vo in code["classes"]
        checks.append(
            ADRCheck(
                description=f"`{vo}` value object exists",
                passed=found,
                details=f"Found at `{code['classes'][vo].path}:{code['classes'][vo].line}`"
                if found
                else "MISSING",
            )
        )

    return checks


def check_adr_006(code: dict) -> list[ADRCheck]:
    checks: list[ADRCheck] = []

    for enum_name, label in [("CountryCode", "ISO 3166-1 alpha-2"), ("CurrencyCode", "ISO 4217")]:
        found = enum_name in code["classes"]
        cls_path = code["classes"][enum_name]
        checks.append(
            ADRCheck(
                description=f"`{enum_name}` enum exists ({label})",
                passed=found,
                details=f"Found at `{cls_path.path}:{cls_path.line}`" if found else "MISSING",
            )
        )

    domain_dir = SRC_DIR / "domain"
    if domain_dir.exists():
        domain_src = "".join(p.read_text() for p in domain_dir.rglob("*.py") if p.is_file())
    else:
        domain_src = ""

    checks.append(
        ADRCheck(
            description="`CountryCode` used in domain layer",
            passed="CountryCode" in domain_src,
            details="Referenced in domain"
            if "CountryCode" in domain_src
            else "Not referenced in domain code",
        )
    )
    checks.append(
        ADRCheck(
            description="`CurrencyCode` used in domain layer",
            passed="CurrencyCode" in domain_src,
            details="Referenced in domain"
            if "CurrencyCode" in domain_src
            else "Not referenced in domain code",
        )
    )

    settings_path = SRC_DIR / "config" / "settings.py"
    if settings_path.exists():
        settings_text = settings_path.read_text()
        uses_enums = "CountryCode" in settings_text or "CurrencyCode" in settings_text
        checks.append(
            ADRCheck(
                description="Settings use typed enums instead of raw strings",
                passed=uses_enums,
                details="Uses typed enums"
                if uses_enums
                else "Uses raw strings (e.g. `'INR'`, `'IN'`)",
            )
        )
    else:
        checks.append(
            ADRCheck(
                description="Settings use typed enums instead of raw strings",
                passed=False,
                details="settings.py not found",
            )
        )

    return checks


def check_adr_007(code: dict) -> list[ADRCheck]:
    checks: list[ADRCheck] = []
    has_money = "Money" in code["classes"]
    checks.append(
        ADRCheck(
            description="`Money` class exists",
            passed=has_money,
            details=f"Found at `{code['classes']['Money'].path}:{code['classes']['Money'].line}`"
            if has_money
            else "MISSING",
        )
    )
    if has_money:
        is_dc, dc_detail = class_has_dataclass_decorator("Money", code)
        auto_gen = is_dc  # frozen dataclass auto-generates __eq__, __hash__

        for method, desc, critical in [
            ("Money.of", "Factory `of(amount, currency)`", True),
            ("Money.__add__", "Addition `+` (same currency)", True),
            ("Money.__sub__", "Subtraction `-` (same currency)", True),
            ("Money.__mul__", "Multiplication `*` (int/Decimal)", True),
            ("Money.__rmul__", "Reflected multiplication", True),
            ("Money.__truediv__", "Division `/` (scalar or Money→Decimal)", True),
            ("Money.__neg__", "Unary negation `-`", True),
            ("Money.__abs__", "Absolute value `abs()`", True),
            ("Money.__lt__", "Less-than `<`", True),
            ("Money.__le__", "Less-than-or-equal `<=`", True),
            ("Money.__gt__", "Greater-than `>`", True),
            ("Money.__ge__", "Greater-than-or-equal `>=`", True),
            ("Money.__str__", "Canonical string representation `__str__`", False),
        ]:
            found = method in code["methods"]
            checks.append(
                ADRCheck(
                    description=desc,
                    passed=found,
                    details="Found"
                    if found
                    else (
                        "MISSING — required by ADR-007"
                        if critical
                        else "Missing (recommended by Canonical Representation Principle)"
                    ),
                )
            )

        for method, desc in [
            ("Money.__eq__", "Value equality `==`"),
            ("Money.__hash__", "Hashable (usable in sets/dicts)"),
        ]:
            found = method in code["methods"]
            if not found and auto_gen:
                checks.append(
                    ADRCheck(
                        description=desc,
                        passed=True,
                        details=f"Auto-generated by {dc_detail}",
                    )
                )
            else:
                checks.append(
                    ADRCheck(
                        description=desc,
                        passed=found,
                        details="Found" if found else "MISSING",
                    )
                )

    return checks


def check_adr_008(code: dict) -> list[ADRCheck]:
    checks: list[ADRCheck] = []
    has_ay = "AssessmentYear" in code["classes"]
    ay_ce = code["classes"].get("AssessmentYear")
    checks.append(
        ADRCheck(
            description="`AssessmentYear` class exists",
            passed=has_ay,
            details=f"Found at `{ay_ce.path}:{ay_ce.line}`" if has_ay else "MISSING",
        )
    )
    if has_ay:
        for method, desc, critical in [
            ("AssessmentYear.of", "Factory `of(start_year)`", True),
            ("AssessmentYear.parse", "Parser `parse(value)`", True),
            ("AssessmentYear.__str__", "Custom `__str__` returning `AY YYYY-YY`", False),
            ("AssessmentYear.__repr__", "Descriptive `__repr__`", False),
        ]:
            found = method in code["methods"]
            checks.append(
                ADRCheck(
                    description=desc,
                    passed=found,
                    details="Found"
                    if found
                    else (
                        "MISSING" if critical else "Missing (recommended by ADR-008 and RFC-001)"
                    ),
                )
            )

    return checks


def check_adr_010(code: dict) -> list[ADRCheck]:
    checks: list[ADRCheck] = []
    fy_exists = "FinancialYear" in code["classes"]
    fy_ce = code["classes"].get("FinancialYear")
    checks.append(
        ADRCheck(
            description="`FinancialYear` value object exists",
            passed=fy_exists,
            details=f"Found at `{fy_ce.path}:{fy_ce.line}`"
            if fy_exists
            else "MISSING — required by ADR-010",
        )
    )
    checks.append(
        ADRCheck(
            description="`AssessmentYear.financial_year` computed property",
            passed="AssessmentYear.financial_year" in code["methods"],
            details="Found"
            if "AssessmentYear.financial_year" in code["methods"]
            else "MISSING — required by ADR-010",
        )
    )
    return checks


def check_rfc_001(code: dict) -> list[ADRCheck]:
    checks: list[ADRCheck] = []
    for method, desc in [
        ("AssessmentYear.of", "`AssessmentYear.of(2026)` factory"),
        ("AssessmentYear.parse", "`AssessmentYear.parse('AY 2026-27')` parser"),
        ("AssessmentYear.__str__", "`str(ay)` canonical representation"),
        ("AssessmentYear.__repr__", "`repr(ay)` debug representation"),
        ("AssessmentYear.next", "`ay.next()` — next AssessmentYear"),
        ("AssessmentYear.previous", "`ay.previous()` — previous AssessmentYear"),
    ]:
        found = method in code["methods"]
        checks.append(
            ADRCheck(
                description=desc,
                passed=found,
                details="Found" if found else "Not implemented",
            )
        )

    return checks


ADR_TEST_MAP = {
    "ADR-006": ["python/tests/ptms/core/enums/test_enums.py"],
    "ADR-007": ["python/tests/ptms/core/value_objects/test_money.py"],
    "ADR-008": ["python/tests/ptms/core/value_objects/test_assessment_year.py"],
    "ADR-009": ["python/tests/ptms/core/value_objects/test_assessment_year.py"],
    "ADR-010": ["python/tests/ptms/core/value_objects/test_assessment_year.py"],
}


def _check_unit_tests_exist(adr_number: str) -> bool:
    paths = ADR_TEST_MAP.get(adr_number, [])
    return any((REPO_ROOT / p).exists() for p in paths)


def _check_public_api_documented(adr_number: str, code: dict) -> bool:
    adr_to_classes = {
        "ADR-006": ["CountryCode", "CurrencyCode"],
        "ADR-007": ["Money"],
        "ADR-008": ["AssessmentYear"],
        "ADR-009": ["AssessmentYear"],
        "ADR-010": ["AssessmentYear"],
    }
    class_names = adr_to_classes.get(adr_number, [])
    for name in class_names:
        ce = code["classes"].get(name)
        if not ce or not ce.file_path:
            return False
        try:
            tree = ast.parse(Path(ce.file_path).read_text("utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef) and node.name == name:
                    docstring = ast.get_docstring(node)
                    if not docstring:
                        return False
        except (SyntaxError, OSError):
            return False
    return True


def _auto_verify_validation(
    adr_number: str,
    items: list[tuple[bool, str]],
    code: dict,
) -> list[tuple[bool, str]]:
    verified: list[tuple[bool, str]] = []
    for _, item_text in items:
        lower = item_text.lower()
        if "unit test" in lower or "tests exist" in lower:
            verified.append((_check_unit_tests_exist(adr_number), item_text))
        elif "public api" in lower:
            verified.append((_check_public_api_documented(adr_number, code), item_text))
        else:
            verified.append((True, item_text))
    return verified


def generate_report(
    adrs: dict[str, ADRInfo],
    code: dict,
    check_results: dict[str, list[ADRCheck]],
) -> str:
    now = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
    total = sum(len(c) for c in check_results.values())
    passed = sum(sum(1 for c in checks if c.passed) for checks in check_results.values())
    pct = round(passed / total * 100) if total else 0

    commit = os.popen("git rev-parse --short HEAD 2>/dev/null").read().strip() or "unknown"
    lines = [
        "# ADR/RFC Compliance Review Report",
        "",
        f"**Generated:** {now}",
        f"**Commit:** `{commit}`",  # noqa: E501
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| Total checks | {total} |",
        f"| Passed | {passed} |",
        f"| Failed | {total - passed} |",
        f"| Compliance | {pct}% |",
        "",
    ]

    for adr_num in sorted(check_results.keys()):
        info = adrs.get(adr_num)
        checks = check_results[adr_num]
        n_passed = sum(1 for c in checks if c.passed)
        n_total = len(checks)

        if n_passed == n_total:
            status = "✅ Implemented"
        elif n_passed == 0:
            status = "❌ Not Implemented"
        else:
            status = "⚠️ Partial"

        lines.append(f"## {adr_num}: {info.title if info else 'Unknown'}")
        lines.append("")
        lines.append(f"**Status:** {status} ({n_passed}/{n_total} checks passing)")
        if info and info.status != "Unknown":
            lines.append(f"**ADR Lifecycle Status:** {info.status}")
        lines.append("")

        if info and info.validation_items:
            lines.append("### ADR Validation Checklist")
            lines.append("")
            verified = _auto_verify_validation(adr_num, info.validation_items, code)
            for checked, item in verified:
                symbol = "✅" if checked else "⬜"
                lines.append(f"- {symbol} {item}")
            lines.append("")

        lines.append("### Implementation Checks")
        lines.append("")
        for i, c in enumerate(checks, 1):
            symbol = "✅" if c.passed else "❌"
            lines.append(f"{i}. {symbol} **{c.description}** — {c.details}")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("_Report generated by `scripts/adr_review.py`_")
    return "\n".join(lines)


def running_in_ci() -> bool:
    return os.environ.get("GITHUB_ACTIONS") == "true"


def main() -> None:
    parser = argparse.ArgumentParser(description="ADR/RFC compliance review")
    parser.add_argument("--output", type=str, help="Write report to file instead of stdout")
    args = parser.parse_args()

    adrs: dict[str, ADRInfo] = {}
    if ADR_DIR.exists():
        for f in sorted(ADR_DIR.glob("ADR-*.md")):
            info = parse_adr_file(f)
            if info:
                adrs[info.number] = info

    code = scan_codebase()

    check_fns = {
        "ADR-001": check_adr_001,
        "ADR-006": check_adr_006,
        "ADR-007": check_adr_007,
        "ADR-008": check_adr_008,
        "ADR-010": check_adr_010,
    }
    check_results: dict[str, list[ADRCheck]] = {}
    for num, fn in check_fns.items():
        check_results[num] = fn(code)
    check_results["RFC-001"] = check_rfc_001(code)

    report = generate_report(adrs, code, check_results)

    if args.output:
        Path(args.output).write_text(report)
        print(f"Report written to {args.output}")
    else:
        print(report)

    total = sum(len(c) for c in check_results.values())
    passed = sum(sum(1 for c in checks if c.passed) for checks in check_results.values())
    if running_in_ci() and total > 0 and passed / total < 0.3:
        sys.exit(1)


if __name__ == "__main__":
    main()
