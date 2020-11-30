# Nano-bot-rewrite
[![Discord Badge](https://discordapp.com/api/guilds/458296099049046018/embed.png)](https://discord.gg/Y8sB4ay)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/madeyoga/Nano-Bot/issues)
[![CodeFactor](https://www.codefactor.io/repository/github/madeyoga/nano-bot/badge)](https://www.codefactor.io/repository/github/madeyoga/nano-bot)

<a href="https://top.gg/bot/458298539517411328">
    <img src="https://top.gg/api/widget/458298539517411328.svg" alt="Nano" />
</a>

## Profile
Nano-bot is designed for image sharing & music.
- Deployed on Heroku cloud platform (Free).
- Prefix: `n>`. To have Nano-Bot to response to your command, you need to use the prefix before the command name.

## Update v2.2.0 (2020/11/30)
- Added custom prefix
- Added new help command
- Reimplement music commands

### Custom Prefix
You can now set a custom prefix using `set_prefix` command

Example usage
```
n>set_prefix n!
```

### New Help Command (new)
- Added detail

To check the command list use `n>help` without any arguments. For command description and usage, provide command name as the argument.

Example usage
```python
# To show list of command name
n>help

# To get command description & usage
n>help <command-name>
n>help play
n>help search
n>help now_play
```

### New Music
Music has been reimplemented! Following Rythm bot user experience. Here are the new command names. 

`join` `leave` `play` `search` `now_play` `queue` `repeat` `pause` `resume` `shuffle` `skip`

You can also check their description and usage with the new help command. 
```
n>help play
```

## Image Command: Names
`dank` `anime` `animeme` `waifu` `tsun` `aniwallp` `moescape` `rwtf` `fgo` `fgoart` `scathach` `raikou` `saber` `abby` 

### Image Commands: Usage
To use the commands, you have to add prefix `n>` before the command name. 

For example, image command `rwtf` 'd be `n>rwtf`

### Image Commands: Search Image From Reddit
- Command: `reddit`

- Aliases: `reddit` `r/` `reddit_search`

- Argument: Keywords

- Usage:
```bash
n>reddit <keywords>
```
