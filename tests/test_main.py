"""Tests for option6.__main__."""
from unittest.mock import Mock, patch

import pytest
from discord.ext.commands import Bot

from option6 import __version__
from option6.__main__ import main


def test_main_version(capsys):
    """Test basic argument parsing."""
    with pytest.raises(SystemExit) as e:
        main(("--version",))
    assert e.value.code == 0
    stdout, _ = capsys.readouterr()
    assert __version__ in stdout


def test_main(tmp_path):
    """Test main parses keys.json and creates and runs the bot."""
    # set up key file
    key_file = tmp_path / "keys.json"
    key_file.write_text('{"channel_id": 1, "discord": 2}')

    # mock make_bot to return mocked Bot
    mock_bot = Mock(Bot)
    mock_make_bot = Mock()
    mock_make_bot.return_value = mock_bot
    with patch("option6.__main__.make_bot", mock_make_bot):
        # run main and assert functions were correctly called
        main((str(key_file),))
        mock_make_bot.assert_called_with(1)
        mock_bot.run.assert_called_with(2)
