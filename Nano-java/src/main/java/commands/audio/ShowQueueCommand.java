package commands.audio;

import audio.manager.GuildAudioState;
import audio.manager.IGuildAudioManager;
import com.jagrosh.jdautilities.command.SlashCommand;
import com.sedmelluq.discord.lavaplayer.track.AudioTrack;
import commands.utilities.StyledEmbedBuilder;
import net.dv8tion.jda.api.EmbedBuilder;
import net.dv8tion.jda.api.events.interaction.SlashCommandEvent;

public class ShowQueueCommand extends SlashCommand {
    private final IGuildAudioManager audioManager;

    public ShowQueueCommand(IGuildAudioManager audioManager, Category category) {
        this.audioManager = audioManager;
        this.name = "queue";
        this.help = "Shows current playing queue";
        this.guildOnly = true;
        this.category = category;
    }

    @Override
    protected void execute(SlashCommandEvent event) {
        if (!audioManager.isGuildRegistered(event.getGuild())) {
            event.reply(":x: Could not execute show_queue command: Queue is empty").queue();
            return;
        }
        event.deferReply(true).queue();

        GuildAudioState state = audioManager.getAudioState(event.getGuild());
        if (state.scheduler.getQueue().isEmpty()) {
            event.getHook()
                 .editOriginal("Queue is currently empty, add audio track to queue using /play or /ytsearch")
                 .queue();
            return;
        }
        StyledEmbedBuilder embedBuilder = new StyledEmbedBuilder();
        embedBuilder.setAuthor(event.getGuild().getName() + "'s queue", event.getGuild().getIconUrl(),
                event.getUser().getAvatarUrl());
        StringBuilder stringBuilder = new StringBuilder();
        int index = 1;
        for (AudioTrack track : state.scheduler.getQueue()) {
            stringBuilder.append(index)
                    .append(". [**")
                    .append(track.getInfo().title)
                    .append("**](")
                    .append(track.getInfo().uri)
                    .append(")\n");
            index += 1;

            if (index == 5) {
                break;
            }
        }
        embedBuilder.addField("Top 5 entries in queue", stringBuilder.toString(), false);
        embedBuilder.setFooter("Thank you for using " + event.getJDA().getSelfUser().getName(),
                event.getJDA().getSelfUser().getAvatarUrl());
        event.getHook().editOriginal("").setEmbeds(embedBuilder.build()).queue();
    }
}
