package commands.audio;

import audio.manager.GuildAudioManager;
import audio.manager.GuildAudioState;
import com.jagrosh.jdautilities.command.SlashCommand;
import commands.utilities.EventValidator;
import net.dv8tion.jda.api.entities.Guild;
import net.dv8tion.jda.api.entities.VoiceChannel;
import net.dv8tion.jda.api.events.interaction.SlashCommandEvent;

public class StopCommand extends SlashCommand {

    private final GuildAudioManager audioManager;

    public StopCommand(GuildAudioManager audioManager, Category category){
        this.audioManager = audioManager;
        this.name = "stop";
        this.help = "Stop playing audio and leave voice channel";
        this.guildOnly = true;
        this.category = category;
    }

    @Override
    protected void execute(SlashCommandEvent event) {
        if (!EventValidator.isValidAuthorVoice(event)) return;
        VoiceChannel selfVoiceChannel = event.getGuild().getSelfMember().getVoiceState().getChannel();
        if (selfVoiceChannel == null) {
            event.reply(":x: | I'm currently not in a voice channel").queue();
            return;
        }

        event.deferReply().queue();

        stopAndLeaveVoice(event.getGuild());

        event.getHook().sendMessage(":mega: Finished playing current queue.").queue();
    }

    private void stopAndLeaveVoice(Guild guild) {
        guild.getAudioManager().closeAudioConnection();
        GuildAudioState audioState = audioManager.getAudioState(guild);
        audioState.player.destroy();
        audioState.scheduler.getQueue().clear();
        audioManager.removeAudioState(guild);
    }
}
