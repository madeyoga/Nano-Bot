package audio.manager;

import com.sedmelluq.discord.lavaplayer.player.AudioPlayerManager;
import com.sedmelluq.discord.lavaplayer.track.AudioTrack;
import net.dv8tion.jda.api.entities.Guild;
import net.dv8tion.jda.api.entities.Member;
import net.dv8tion.jda.api.events.interaction.GenericInteractionCreateEvent;

import java.util.Map;

public interface IGuildAudioManager {
    static void connectToAuthorVoiceChannel(Member author) {}
    static void play(Member author, GuildAudioState audioState, AudioTrack track) {}

    void loadAndPlay(final GenericInteractionCreateEvent event, String query);
    GuildAudioState getAudioState(Guild guild);
    boolean isGuildRegistered(Guild guild);
    Map<String, GuildAudioState> getAudioStates();
    AudioPlayerManager getPlayerManager();
    void removeAudioState(Guild guild);
}
