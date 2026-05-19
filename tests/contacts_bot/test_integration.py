import builtins

from src.scripts.contacts_bot import COMMAND_MESSAGES, main


def test_main_prints_replies_and_goodbye(monkeypatch, capsys, valid_phone_generator):
    lines = iter(
        [
            "hello",
            f"add Pat {valid_phone_generator()}",
            f"add Pat {valid_phone_generator()}",
            "exit",
        ]
    )

    monkeypatch.setattr(builtins, "input", lambda: next(lines))
    main()
    out = capsys.readouterr().out
    assert COMMAND_MESSAGES["HELLO"] in out
    assert COMMAND_MESSAGES["CONTACT_ADDED"] in out
    assert COMMAND_MESSAGES["GOOD_BYE"] in out
