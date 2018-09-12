# Change Log
All notable changes to this project will be documented in this file.

## Update 12/09/2018
- TURNED OFF FOR A WHILE COMMANDS :
  - PIXIV
  - FGO GAME
- Added new mini game FGO Mini (roll simulator)
  - roll1
    usage: `n>roll1`   -> roll 1 times, requires 3 SaintQuartz 
  - roll10
    usage: `n>roll10`  -> roll 10 times, requires 30 SaintQuartz to roll
  - my_room
    usage: `n>my_room` -> to check master's profile or spirit origin list<br>
  
  Master's experience would increase every time you sent a message on server wherever nano is in it<br>
  leveling system is not fixed yet.
  
  and that being said, you can play anywhere as long as nano is in the server.
  
  your profile(level/spirit_origin) is also the same wherever you play.
  
  Upcoming game updates:
  - daily -> to get free Saint_Quartz
  - rich embed
  
- Added new [reddit](https://reddit.com) commands
  - fgo
    usage: `n>fgo`
  - fgoart
    usage: `n>fgoart` -> fgo's fan art
  - anime
    usage: `n>anime` 
  - scathach
    usage: `n>scathach`
  - animeme
    usage: `n>animeme`
  - dank
    usage: `n>dank`
  - [moescape](https://reddit.com/r/moescape)
    usage: `n>moescape`
  - aniwallp
    usage: `n>aniwallp`
  - tsun
    usage: `n>tsun`
  - waifu
    usage: `n>waifu` -> picks random waifu

## Update 15/08/2018
- Added new [reddit](https://reddit.com) commands
  - [memes](https://reddit.com/r/memes)<br>
    Usage: `n>memes`
  - [rwtf](https://reddit.com/r/wtf)<br>
    Usage: `n>rwtf`
  
## Update 14/08/2018
- Fixes Bug on command `volume`, error after change `music_prefix`
- Added new [Pixiv](https://www.pixiv.net) commands
  - pxv <br>
    search illustrations from pixiv <br>
    usage: `n>pxv anime`<br>
    search `anime` from pixiv, response would be a link
  - pxv_user
  
    search Pixiv's users. 
    
    will response max 7 users. choose 1 user by typing the user's entry number to get the users detail.
    
    usage: `n>pxv_user chrome`<br>
    search pixiv's users named 'chrome'<br>
    [example](https://raw.githubusercontent.com/MadeYoga/San/master/img/pxv_user.PNG)
    
  - illust
    
    usage: `n>illust`
    
  - manga
  
    usage: `n>manga`
  
  - novel
  
    usage: `n>novel`

## Update 13/08/2018
- pick many entries at once<br>
  - ex. `n>play 1 2 4 3`, to pick entry number 1, 2, 4 and 3
  - ex. `n>p 3 4 6 1`, to pick entry number 3, 4, 6, and 1
- `p` and `play` now support auto play from a keyword
  - ex. `n>p the hoopers` or `n>play the hoopers`, will automatically search, load, and play 
  
## Update 11/08/2018
- New moderations commands
  - `add_role` and `rm_role`
    
    example usage: `n>add_role @role3 @user1 @user2 @role1`<br>
      adds role1 and role3 to user1 and user2, it takes `min` 1 mentioned `role` and 1 mentioned `user`
      
    example usage: `n>rm_role @role3 @user1 @user2 @role1`<br>
      removes role1, and role3 from user1 and user2, it takes `min` 1 mentioned `role` and 1 mentioned `user`
      
  - `c_category`, `c_text`, and `c_voice`
  
    example usage: `n>c_category new_category`<br>
    creates a new `category` named new_category
    
    example usage: `n>c_text new_text`<br>
    creates a new `text channel` named new_text
    
    example usage: `n>c_voice new_voice`<br>
    creates a new `voice channel` named new_voice
  
  - `ban`
  
    example usage: `n>ban @user1`
  
  - `kick`
  
    example usage: `n>kick @user1`
    
  - `mute`and `unmute` 
  
    example usage: `n>mute @user1` , `n>unmute @user1`
