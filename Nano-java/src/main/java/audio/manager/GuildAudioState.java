package audio.manager;

import audio.AudioPlayerSendHandler;
import audio.AudioTrackScheduler;
import com.sedmelluq.discord.lavaplayer.player.AudioPlayer;
import com.sedmelluq.discord.lavaplayer.player.AudioPlayerManager;

public class GuildAudioState {
    public final AudioPlayer player;
    public final AudioTrackScheduler scheduler;

    public GuildAudioState(AudioPlayerManager playerManager) {
        this.player = playerManager.createPlayer();
        this.scheduler = new AudioTrackScheduler(player);
        player.addListener(this.scheduler);
    }

    public AudioPlayerSendHandler getSendHandler() {
        return new AudioPlayerSendHandler(player);
    }
}
