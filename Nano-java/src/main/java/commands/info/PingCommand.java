package commands.info;

import com.jagrosh.jdautilities.command.SlashCommand;
import net.dv8tion.jda.api.events.interaction.SlashCommandEvent;

import java.time.temporal.ChronoUnit;

public class PingCommand extends SlashCommand {
    public PingCommand(Category category) {
        this.name = "ping";
        this.help = "Check Nano's latency";
        this.category = category;
    }

    @Override
    protected void execute(SlashCommandEvent event) {
        event.deferReply().queue();
        long latency = System.currentTimeMillis() - event.getTimeCreated().toInstant().toEpochMilli();
        event.getHook().editOriginal(":hourglass_flowing_sand: " + latency + "ms.").queue();
    }
}
