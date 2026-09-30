"""検査結果（Issue）の表現と整形。"""

from __future__ import annotations

from dataclasses import dataclass, asdict

SEVERITY_ORDER = {"error": 0, "warn": 1, "info": 2}
SEVERITY_LABEL = {"error": "エラー", "warn": "警告", "info": "参考"}


@dataclass
class Issue:
    rule: str
    severity: str  # error / warn / info
    message: str
    line: int | None = None
    excerpt: str = ""
    suggestion: str = ""

    def to_dict(self) -> dict:
        return {k: v for k, v in asdict(self).items() if v not in (None, "")}

    def format(self, path: str = "") -> str:
        loc = f"{path}:{self.line}" if path and self.line else (f"{self.line}行目" if self.line else path)
        head = f"[{SEVERITY_LABEL.get(self.severity, self.severity)}] {self.rule}"
        if loc:
            head += f" ({loc})"
        text = f"{head}: {self.message}"
        if self.excerpt:
            text += f"\n    該当: {self.excerpt}"
        if self.suggestion:
            text += f"\n    提案: {self.suggestion}"
        return text


def sort_issues(issues: list[Issue]) -> list[Issue]:
    return sorted(issues, key=lambda i: (SEVERITY_ORDER.get(i.severity, 9), i.line or 0, i.rule))


def count(issues: list[Issue]) -> dict:
    out = {"error": 0, "warn": 0, "info": 0}
    for i in issues:
        out[i.severity] = out.get(i.severity, 0) + 1
    return out


def format_issues(issues: list[Issue], path: str = "", limit: int | None = None,
                  min_severity: str = "info") -> str:
    threshold = SEVERITY_ORDER[min_severity]
    shown = [i for i in sort_issues(issues) if SEVERITY_ORDER.get(i.severity, 9) <= threshold]
    lines = [i.format(path) for i in (shown[:limit] if limit else shown)]
    if limit and len(shown) > limit:
        lines.append(f"…ほか {len(shown) - limit} 件")
    return "\n".join(lines)


def excerpt(text: str, width: int = 40) -> str:
    text = text.replace("\n", " ")
    return text if len(text) <= width else text[:width] + "…"
