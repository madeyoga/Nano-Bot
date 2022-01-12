import audio.manager.GuildAudioManager;
import com.jagrosh.jdautilities.command.Command;
import com.jagrosh.jdautilities.command.CommandClient;
import com.jagrosh.jdautilities.command.CommandClientBuilder;
import commands.audio.*;
import commands.awaiter.SearchCommandResponseWaiter;
import commands.info.AvatarCommand;
import commands.info.HelpCommand;
import commands.info.PingCommand;
import net.dv8tion.jda.api.JDA;
import net.dv8tion.jda.api.JDABuilder;
import net.dv8tion.jda.api.entities.Activity;
import net.dv8tion.jda.api.requests.GatewayIntent;
import net.dv8tion.jda.api.utils.ChunkingFilter;
import net.dv8tion.jda.api.utils.MemberCachePolicy;
import net.dv8tion.jda.api.utils.cache.CacheFlag;

import javax.security.auth.login.LoginException;

public class Main {
    public static void main(String[] args) throws LoginException {
        String botToken = System.getenv("NR_TOKEN");

        JDABuilder jdaBuilder = JDABuilder.createDefault(botToken);
        configureMemoryUsage(jdaBuilder);

        Command.Category audioCategory = new Command.Category("Audio Commands");
        Command.Category infoCategory = new Command.Category("Info Commands");

        GuildAudioManager audioManager = new GuildAudioManager();

        SearchCommandResponseWaiter searchWaiter = new SearchCommandResponseWaiter(audioManager);

        CommandClientBuilder clientBuilder = setupClientBuilderBasicInfo(new CommandClientBuilder());
        clientBuilder.forceGuildOnly("791580705892466689");
        clientBuilder.addSlashCommand(new JoinCommand(audioCategory));
        clientBuilder.addSlashCommand(new LoopCommand(audioManager, audioCategory));
        clientBuilder.addSlashCommand(new StopCommand(audioManager, audioCategory));
        clientBuilder.addSlashCommand(new PlayCommand(audioManager, audioCategory));
        clientBuilder.addSlashCommand(new NowPlayCommand(audioManager, audioCategory));
        clientBuilder.addSlashCommand(new ShowQueueCommand(audioManager, audioCategory));
        clientBuilder.addSlashCommand(new ShuffleQueueCommand(audioManager, audioCategory));
        clientBuilder.addSlashCommand(new YoutubeSearchCommand(audioManager, audioCategory, searchWaiter));

        HelpCommand helpCommand = new HelpCommand(infoCategory);
        clientBuilder.addSlashCommand(helpCommand);
        clientBuilder.addSlashCommand(new AvatarCommand(infoCategory));
        clientBuilder.addSlashCommand(new PingCommand(infoCategory));

        clientBuilder.setActivity(Activity.playing("Loading..."));

        CommandClient commandClient = clientBuilder.build();

        helpCommand.addCommands(commandClient.getSlashCommands());

        jdaBuilder.addEventListeners(commandClient);
        jdaBuilder.addEventListeners(searchWaiter);

        JDA jda = jdaBuilder.build();

        helpCommand.buildEmbed(jda);
    }

    public static CommandClientBuilder setupClientBuilderBasicInfo(CommandClientBuilder builder) {
        builder.setOwnerId("213866895806300161");
        builder.setPrefix("n>");

        return builder;
    }

    private static void configureMemoryUsage(JDABuilder builder) {
        // Disable cache for member activities (streaming/games/spotify)
        builder.disableCache(CacheFlag.ACTIVITY);
        builder.disableCache(CacheFlag.CLIENT_STATUS);
        builder.disableCache(CacheFlag.MEMBER_OVERRIDES);
        builder.disableCache(CacheFlag.EMOTE);

        // Only cache members who are either in a voice channel or owner of the guild
        builder.setMemberCachePolicy(MemberCachePolicy.VOICE.or(MemberCachePolicy.OWNER));

        // Disable member chunking on startup
        builder.setChunkingFilter(ChunkingFilter.NONE);

        // Disable presence updates and typing events and more Guild Events
        builder.disableIntents(GatewayIntent.GUILD_PRESENCES, GatewayIntent.GUILD_MESSAGE_TYPING,
                GatewayIntent.GUILD_MEMBERS, GatewayIntent.GUILD_BANS,
                GatewayIntent.GUILD_INVITES, GatewayIntent.GUILD_EMOJIS,
                GatewayIntent.GUILD_MESSAGES, GatewayIntent.DIRECT_MESSAGES);

        builder.disableIntents(GatewayIntent.DIRECT_MESSAGE_REACTIONS, GatewayIntent.DIRECT_MESSAGE_TYPING,
                GatewayIntent.DIRECT_MESSAGE_REACTIONS);

        // Consider guilds with more than 50 members as "large".
        // Large guilds will only provide online members in their setup and thus reduce bandwidth if chunking is disabled.
        builder.setLargeThreshold(50);
    }
}
