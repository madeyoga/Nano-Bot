package commands.info;

import com.jagrosh.jdautilities.command.SlashCommand;
import net.dv8tion.jda.api.EmbedBuilder;
import net.dv8tion.jda.api.JDA;
import net.dv8tion.jda.api.entities.User;
import net.dv8tion.jda.api.events.interaction.SlashCommandEvent;
import net.dv8tion.jda.api.interactions.components.Button;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.awt.*;
import java.util.*;
import java.util.List;

public class HelpCommand extends SlashCommand {
    private final Logger logger;
    private final EmbedBuilder builder;
    private final Map<String, String> commandMap;

    public HelpCommand(Category category) {
        this.logger = LoggerFactory.getLogger(HelpCommand.class);

        this.name = "help";
        this.help = "Get command list";

        this.builder = new EmbedBuilder();
        this.category = category;

        this.commandMap = new HashMap<>();
    }

    @Override
    protected void execute(SlashCommandEvent event) {
        event.replyEmbeds(this.builder.build())
                .addActionRow(
                        Button.link("https://discord.com/api/oauth2/authorize?client_id=458298539517411328&permissions=8&scope=applications.commands%20bot", "Invite Nano"),
                        Button.link("https://discord.gg/Y8sB4ay", "Support Server"),
                        Button.link("https://top.gg/bot/458298539517411328/vote", "Vote"))
                .queue();
    }

    public void addCommands(List<SlashCommand> commandList) {
        for (SlashCommand command : commandList) {
            if (command.getCategory() == null) {
                this.logger.warn("Skipping " + command.getName() + " command. Command does not have category set");
                continue;
            }
            String categoryName = command.getCategory().getName();

            String currentSubtitleState = "";

            if (!commandMap.containsKey(categoryName)) {
                commandMap.put(categoryName, currentSubtitleState);
            }
            else {
                currentSubtitleState = commandMap.get(categoryName);
            }

            String commandName = "`" + command.getName() + "` ";

            currentSubtitleState += commandName;

            commandMap.put(categoryName, currentSubtitleState);
        }

        commandMap.replaceAll((k, v) -> v.trim());
    }

    public void buildEmbed(JDA jda) {
        for (String key : commandMap.keySet()) {
            this.builder.addField(key, commandMap.get(key), false);
        }

        User self = jda.getSelfUser();
        this.builder.setAuthor("Nano Help", "https://github.com/madeyoga/Nano-Bot", self.getAvatarUrl());
        this.builder.setFooter("Thanks for using Nano", self.getAvatarUrl());

        this.builder.setColor(Color.RED);

        this.commandMap.clear();
    }
}
