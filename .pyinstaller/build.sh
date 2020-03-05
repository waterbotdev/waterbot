pyinstaller -i .pyinstaller/icon.ico --add-data guildconfig.json:. --add-data config.json:. --log-level DEBUG bot.py --add-data exts:exts -y
