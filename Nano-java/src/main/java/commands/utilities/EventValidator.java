package commands.utilities;

import audio.manager.GuildAudioManager;
import net.dv8tion.jda.api.entities.VoiceChannel;
import net.dv8tion.jda.api.events.interaction.SlashCommandEvent;
import net.dv8tion.jda.api.events.message.MessageReceivedEvent;

public class EventValidator {
    public static boolean isValidAuthorVoice(SlashCommandEvent event) {
        VoiceChannel authorVoiceChannel = event.getMember().getVoiceState().getChannel();
        return authorVoiceChannel != null;
    }

    public static boolean isValidAuthorVoice(MessageReceivedEvent event) {
        VoiceChannel authorVoiceChannel = event.getMember().getVoiceState().getChannel();
        return authorVoiceChannel != null;
    }

    /**
     * return true if self member & author are in voice channel and Guild should be registered in audio manager.
     * @param event SlashCommandEvent
     * @param audioManager implementation of IGuildAudioManager
     * @return boolean
     */
    public static boolean isVoiceStatesValid(SlashCommandEvent event, GuildAudioManager audioManager) {
        if (event.getGuild().getSelfMember().getVoiceState().getChannel() == null) return false;
        if (event.getMember().getVoiceState().getChannel() == null) return false;
        return audioManager.getAudioStates().containsKey(event.getGuild().getId());
    }

    /**
     * return true if self member & author are in voice channel and Guild should be registered in audio manager.
     * @param event SlashCommandEvent
     * @param audioManager implementation of IGuildAudioManager
     * @return boolean
     */
    public static boolean isVoiceStatesValid(MessageReceivedEvent event, GuildAudioManager audioManager) {
        if (event.getGuild().getSelfMember().getVoiceState().getChannel() == null) return false;
        if (event.getMember().getVoiceState().getChannel() == null) return false;
        return audioManager.getAudioStates().containsKey(event.getGuild().getId());
    }
}
