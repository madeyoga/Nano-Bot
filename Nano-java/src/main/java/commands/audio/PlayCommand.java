package commands.audio;

import audio.manager.GuildAudioManager;
import audio.manager.IGuildAudioManager;
import com.jagrosh.jdautilities.command.SlashCommand;
import net.dv8tion.jda.api.events.interaction.SlashCommandEvent;
import net.dv8tion.jda.api.interactions.commands.OptionMapping;
import net.dv8tion.jda.api.interactions.commands.OptionType;
import net.dv8tion.jda.api.interactions.commands.build.OptionData;

import java.util.Collections;

public class PlayCommand extends SlashCommand {
    private final IGuildAudioManager audioManager;

    public PlayCommand(GuildAudioManager audioManager, Category category) {
        this.audioManager = audioManager;
        this.name = "play";
        this.help = "Play or queue an audio track";
        this.options = Collections.singletonList(
            new OptionData(OptionType.STRING, "query", "Query can be an URL or keywords").setRequired(true)
        );
        this.guildOnly = true;
        this.category = category;
    }

    @Override
    protected void execute(SlashCommandEvent event) {
        if (event.getMember().getVoiceState() == null) return;

        event.deferReply().queue();

        OptionMapping queryOption = event.getOption("query");
        if (queryOption == null) {
            event.getHook().editOriginal(":x: | Could not execute play command. Query option was null").queue();
            return;
        }

        audioManager.loadAndPlay(event, queryOption.getAsString());
    }
}
