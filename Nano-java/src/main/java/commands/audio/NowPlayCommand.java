package commands.audio;

import audio.manager.GuildAudioManager;
import audio.manager.GuildAudioState;
import audio.manager.IGuildAudioManager;
import com.jagrosh.jdautilities.command.SlashCommand;
import com.sedmelluq.discord.lavaplayer.track.AudioTrack;
import net.dv8tion.jda.api.events.interaction.SlashCommandEvent;

public class NowPlayCommand extends SlashCommand {
    private final IGuildAudioManager audioManager;

    public NowPlayCommand(GuildAudioManager audioManager, Category category) {
        this.audioManager = audioManager;
        this.name = "now_playing";
        this.help = "Shows current playing audio";
        this.guildOnly = true;
        this.category = category;
    }

    @Override
    protected void execute(SlashCommandEvent event) {
        event.deferReply().queue();

        if (event.getGuild().getSelfMember().getVoiceState().getChannel() == null) {
            event.getHook().editOriginal(":x: Not playing anything").queue();
            return;
        }

        GuildAudioState audioState = audioManager.getAudioState(event.getGuild());

        AudioTrack playingTrack = audioState.player.getPlayingTrack();
        if (playingTrack == null) {
            event.getHook().editOriginal(":x: Not playing anything").queue();
            return;
        }

        String songName = playingTrack.getInfo().title;
        event.getHook().editOriginal(":musical_note: Now playing: " + songName).queue();
    }
}
