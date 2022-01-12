package commands.info;

import com.jagrosh.jdautilities.command.SlashCommand;
import net.dv8tion.jda.api.entities.User;
import net.dv8tion.jda.api.events.interaction.SlashCommandEvent;
import net.dv8tion.jda.api.interactions.commands.OptionMapping;
import net.dv8tion.jda.api.interactions.commands.OptionType;
import net.dv8tion.jda.api.interactions.commands.build.OptionData;

import java.util.Collections;


public class AvatarCommand extends SlashCommand {

    public AvatarCommand(Category category) {
        this.name = "avatar";
        this.help = "Shows mentioned user's avatar";
        this.options = Collections.singletonList(
                new OptionData(OptionType.USER, "mention", "Mention the user").setRequired(true)
        );
        this.category = category;
    }

    @Override
    protected void execute(SlashCommandEvent event) {
        event.deferReply().queue();
        OptionMapping option = event.getOption("mention");

        if (option == null) {
            event.getHook().editOriginal(":x: | Could not execute play command. Query option was null").queue();
            return;
        }

        User user = option.getAsUser();
        String url = user.getAvatarUrl();
        if (url == null) {
            event.getHook().editOriginal(user.getName() + " has not set an avatar ").queue();
            return;
        }
        event.getHook().editOriginal(user.getAvatarUrl()).queue();
    }
}
