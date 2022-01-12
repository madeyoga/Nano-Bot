package commands.audio;

import audio.manager.GuildAudioManager;
import audio.manager.GuildAudioState;
import audio.manager.IGuildAudioManager;
import com.jagrosh.jdautilities.command.SlashCommand;
import com.sedmelluq.discord.lavaplayer.track.AudioTrack;
import net.dv8tion.jda.api.events.interaction.SlashCommandEvent;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class ShuffleQueueCommand extends SlashCommand {
    private final IGuildAudioManager audioManager;

    public ShuffleQueueCommand(GuildAudioManager audioManager, Category category) {
        this.audioManager = audioManager;
        this.name = "shuffle";
        this.help = "Shuffles current queue";
        this.category = category;
    }

    @Override
    protected void execute(SlashCommandEvent event) {
        event.deferReply().queue();
        if (event.getGuild().getSelfMember().getVoiceState().getChannel() == null) {
            event.getHook().editOriginal("I'm not in a voice channel").queue();
            return;
        }
        if (event.getMember().getVoiceState().getChannel() == null) {
            event.getHook().editOriginal("You're not in a voice channel").queue();
            return;
        }
        GuildAudioState audioState = audioManager.getAudioState(event.getGuild());
        if (audioState.scheduler.getQueue().size() > 1)
            shuffleQueue(audioState);
        event.getHook().editOriginal(":white_check_mark: Queue shuffled").queue();
    }

    private void shuffleQueue(GuildAudioState audioState) {
        List<AudioTrack> tracks = new ArrayList<>(audioState.scheduler.getQueue());
        Collections.shuffle(tracks);

        audioState.scheduler.getQueue().clear();
        audioState.scheduler.getQueue().addAll(tracks);
    }
}
