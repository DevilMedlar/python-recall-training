from pathlib import Path

from senpai_bot.contract import ContractStore


ROOT = Path(__file__).parents[1]


def test_loads_all_contract_files_verbatim():
    store = ContractStore(ROOT)
    assert set(store.documents) == {"README.md", "SECURITY.md", "rules.md"}
    for name, text in store.documents.items():
        assert text == (ROOT / name).read_text(encoding="utf-8")


def test_retrieval_prioritizes_matching_heading():
    store = ContractStore(ROOT)
    context = store.relevant_context("How should you verify a Python package before installing it?")
    assert "SECURITY.md" in context
    assert "package" in context.lower()
    assert len(context) <= 18_000


def test_persona_core_is_bounded_and_present():
    store = ContractStore(ROOT)
    assert "Tutor persona" in store.persona_core
    assert len(store.persona_core) < 25_000
