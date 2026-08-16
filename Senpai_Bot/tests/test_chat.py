from pathlib import Path

from senpai_bot.chat import ChatSession
from senpai_bot.contract import ContractStore


ROOT = Path(__file__).parents[1]


def test_system_message_is_persona_first_and_bounded():
    session = ChatSession(ContractStore(ROOT))
    messages = session.build_messages("Explain a Python for loop")
    assert messages[0]["role"] == "system"
    assert "Address the learner as Daddy" in messages[0]["content"]
    assert len(messages[0]["content"]) < 50_000


def test_history_is_bounded():
    session = ChatSession(ContractStore(ROOT), max_history_messages=4)
    for number in range(5):
        session.record(str(number), str(number))
    assert len(session.history) == 4
