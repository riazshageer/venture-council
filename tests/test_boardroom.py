from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class BoardroomTests(unittest.TestCase):
    def test_repository_validation(self) -> None:
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/validate_boardroom.py")],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_context_budgets(self) -> None:
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/audit_context_budget.py"), "--json"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        audit = json.loads(result.stdout)
        self.assertLessEqual(audit["direct_words"], 475)
        self.assertLessEqual(audit["consult_bootstrap_words"], 725)

    def test_packages_are_self_contained(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            tmp_path = Path(temporary)
            for provider, manifest in (
                ("codex", ".codex-plugin/plugin.json"),
                ("claude", ".claude-plugin/plugin.json"),
            ):
                with self.subTest(provider=provider):
                    target = tmp_path / provider
                    subprocess.run(
                        [
                            sys.executable,
                            str(ROOT / "scripts/package_boardroom.py"),
                            provider,
                            str(target),
                        ],
                        cwd=ROOT,
                        check=True,
                    )
                    data = json.loads((target / manifest).read_text(encoding="utf-8"))
                    self.assertEqual(data["name"], "boardroom")
                    self.assertTrue((target / "core/council/index.md").exists())
                    self.assertTrue((target / "skills/boardroom/SKILL.md").exists())
                    if provider == "claude":
                        self.assertTrue((target / "agents/boardroom-critic.md").exists())

    def test_foundational_reframing_capability_is_active_and_complete(self) -> None:
        playbook = ROOT / "core/playbooks/business/foundational-reframing.md"
        content = playbook.read_text(encoding="utf-8")
        _, frontmatter, body = content.split("---", 2)

        self.assertIn("owner: business-strategist", frontmatter)
        self.assertIn("status: active", frontmatter)
        for heading in (
            "## Activation signals",
            "## Method",
            "## Required output",
            "## Calibration example",
            "## Boundaries",
        ):
            self.assertIn(heading, body)
        self.assertIn("conventional baseline", body.lower())
        self.assertIn("at least two", body.lower())
        self.assertIn("independent `critic`", body)
        self.assertTrue((ROOT / "core/templates/foundational-reframe.md").is_file())
        self.assertTrue((ROOT / "examples/foundational-reframing.md").is_file())

        playbook_index = (ROOT / "core/playbooks/index.md").read_text(encoding="utf-8")
        team_lead = (ROOT / "skills/boardroom/SKILL.md").read_text(encoding="utf-8")
        quality_gates = (ROOT / "core/protocols/quality-gates.md").read_text(encoding="utf-8")
        self.assertIn("business-foundational-reframing", playbook_index)
        self.assertIn("screen for conflicting unit/system economics", team_lead.lower())
        self.assertIn("the do-not-reframe case may win", quality_gates.lower())

    def test_global_install_separates_runtime_knowledge_and_repository(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            boardroom_home = root / "global-boardroom"
            codex_home = root / "codex"
            client_repo = root / "client-repository"
            client_repo.mkdir()
            env = os.environ.copy()
            env["BOARDROOM_HOME"] = str(boardroom_home)
            env["CODEX_HOME"] = str(codex_home)
            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts/install_global.py"),
                    "--provider",
                    "codex",
                    "--skip-prereq-check",
                ],
                cwd=client_repo,
                env=env,
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertTrue((boardroom_home / "core/council/index.md").is_file())
            self.assertTrue((boardroom_home / "app/skills/boardroom/SKILL.md").is_file())
            budget = subprocess.run(
                [
                    sys.executable,
                    str(boardroom_home / "app/scripts/audit_context_budget.py"),
                    "--core",
                    str(boardroom_home / "core"),
                    "--json",
                ],
                cwd=client_repo,
                env=env,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(budget.returncode, 0, budget.stdout + budget.stderr)
            installed_skill = codex_home / "skills/boardroom"
            self.assertTrue(installed_skill.is_dir())
            if os.name != "nt":
                self.assertTrue(installed_skill.is_symlink())
            self.assertFalse((client_repo / "core").exists())

            employee = boardroom_home / "core/council/employees/team-lead.md"
            learned_marker = "\n<!-- globally learned marker -->\n"
            employee.write_text(employee.read_text(encoding="utf-8") + learned_marker, encoding="utf-8")
            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts/install_global.py"),
                    "--provider",
                    "codex",
                    "--skip-prereq-check",
                ],
                cwd=client_repo,
                env=env,
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertIn("globally learned marker", employee.read_text(encoding="utf-8"))

            subprocess.run(
                [
                    sys.executable,
                    str(boardroom_home / "app/scripts/record_knowledge_change.py"),
                    "employee",
                    "team-lead",
                    "1.0.1",
                    "Test global learning",
                ],
                cwd=client_repo,
                env=env,
                check=True,
                capture_output=True,
                text=True,
            )
            audit = boardroom_home / "audit/knowledge-changes.jsonl"
            self.assertIn("team-lead", audit.read_text(encoding="utf-8"))

            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts/uninstall_global.py"),
                    "--provider",
                    "codex",
                ],
                cwd=client_repo,
                env=env,
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertFalse(installed_skill.exists())
            self.assertTrue((boardroom_home / "core/council/index.md").is_file())

            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts/uninstall_global.py"),
                    "--provider",
                    "codex",
                    "--purge",
                    "--yes",
                ],
                cwd=client_repo,
                env=env,
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertFalse(boardroom_home.exists())


if __name__ == "__main__":
    unittest.main()
