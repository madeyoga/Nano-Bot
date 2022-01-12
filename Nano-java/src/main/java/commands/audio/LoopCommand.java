package commands.audio;

import audio.manager.GuildAudioState;
import audio.manager.IGuildAudioManager;
import com.jagrosh.jdautilities.command.SlashCommand;
import commands.utilities.EventValidator;
import net.dv8tion.jda.api.events.interaction.SlashCommandEvent;

public class LoopCommand extends SlashCommand {
    private final IGuildAudioManager audioManager;

    public LoopCommand(IGuildAudioManager audioManager, Category category) {
        this.audioManager = audioManager;
        this.name = "loop";
        this.help = "Put current audio track to the last entry of the queue after finished playing";
        this.category = category;
    }

    @Override
    protected void execute(SlashCommandEvent event) {
        event.deferReply().queue();
        if (!EventValidator.isValidAuthorVoice(event)) {
            event.getHook().setEphemeral(true).editOriginal(":x: You are not connected to any voice channel").queue();
            return;
        }

        if (!audioManager.isGuildRegistered(event.getGuild())) {
            event.getHook().setEphemeral(true).editOriginal(":x: Not playing anything").queue();
            return;
        }

        GuildAudioState state = audioManager.getAudioState(event.getGuild());
        state.scheduler.setRepeatMode(!state.scheduler.isRepeatMode());
        if (state.scheduler.isRepeatMode()) {
            event.getHook().editOriginal(":repeat:").queue();
        }
        else {
            event.getHook().editOriginal(":arrow_right_hook:").queue();
        }
    }
}
