from uuid import uuid4

from senpai_bot.instance import SingleInstance


def test_only_one_instance_can_own_the_application_lock():
    name = f"Senpai_Bot.test.{uuid4()}"
    first = SingleInstance(name)
    second = SingleInstance(name)
    third = SingleInstance(name)
    try:
        assert first.acquire() is True
        assert second.acquire() is False
        first.close()
        assert third.acquire() is True
    finally:
        first.close()
        second.close()
        third.close()
