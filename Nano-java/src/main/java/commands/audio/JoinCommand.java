package commands.audio;

import audio.manager.GuildAudioManager;
import com.jagrosh.jdautilities.command.SlashCommand;
import net.dv8tion.jda.api.entities.Member;
import net.dv8tion.jda.api.events.interaction.SlashCommandEvent;

public class JoinCommand extends SlashCommand {

    public JoinCommand(Category category){
        this.name = "join";
        this.help = "Join author's voice channel";
        this.guildOnly = true;
        this.category = category;
    }

    @Override
    protected void execute(SlashCommandEvent event) {
        event.deferReply().queue();
        Member author = event.getMember();
        if (author.getVoiceState().getChannel() == null) {
            event.getHook().sendMessage(":x: | You are not in a voice channel").queue();
            return;
        }
        GuildAudioManager.connectToAuthorVoiceChannel(author);
        event.getHook().sendMessage("Joined **" + author.getVoiceState().getChannel().getName() + "**").queue();
    }
}
