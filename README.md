# Nano-bot-rewrite
[![Discord Badge](https://discordapp.com/api/guilds/458296099049046018/embed.png)](https://discord.gg/Y8sB4ay)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/madeyoga/Nano-Bot/issues)
[![CodeFactor](https://www.codefactor.io/repository/github/madeyoga/nano-bot/badge)](https://www.codefactor.io/repository/github/madeyoga/nano-bot)

Feel free to invite & test [Nano-Rewrite](https://discordapp.com/oauth2/authorize?client_id=458298539517411328&scope=bot&permissions=1567734903). 

I would really appreciate some feedback/ideas/suggestions/contributions, contact me via discord group chat (@tag me)/DM (invite me @ SomeLikeItHot#8195) or join nano-bot support server, or you can also contact me via email.

Thanks!

## Profile
Nano-bot is designed for image sharing & music.
- Deployed on Heroku cloud platform (Free).
- Prefix: `n>`. To have Nano-Bot to response to your command, you need to use the prefix before the command name.

## Image Command: Names
`dank` `anime` `animeme` `waifu` `tsun` `aniwallp` `moescape` `rwtf` `fgo` `fgoart` `scathach` `raikou` `saber` `abby` 

### Image Commands: Usage
To use the commands, you have to add prefix `n>` before the command name. 

For example, image command `rwtf` 'd be `n>rwtf`

### Image Commands: Search Image From Reddit
Command: `reddit`

Aliases: `reddit` `r/` `reddit_search`

Argument: Keywords

Usage:
```bash
n>reddit <keywords>
```

## Music Commands
### play
Aliases: `p` `search` `s` 
Argument: keywords

`play` command accept `keyword` argument

Example: Search & select & play song.
```bash
Made Y
  n>play naruto opening

Nano-Bot
  Song list
  1. .........
  2. .........
  3. .........
  
Made Y
  1
```
Reply the entry number to select which song to play. for example: `1`

### volume
Aliases: -
Argument: number

`volume` command accept number as the argument

Example: Change volume to 15%.
```bash
n>volume 15
```

- queue 
Aliases: `q` 
Argument: -

Shows current queue state

### skip
Aliases: -

Argument: -

Skips current playing song

### stop 
Aliases: -

Argument: -

Stops `current playing` song & leaves voice channel

### now_playing 
Aliases: `now_play` `nowplay` `np` 

Argument: -

Check now play song data.

### pause
Aliases: - 

Argument: -

Pause current playing song.

### resume 
Aliases: -

Argument: -

Resume paused song

### repeat 
Aliases: `loop` 

Argument: -

Put ended song to the last queue entry

### shuffle
Aliases: -

Argument: -

Shuffles current queue state
