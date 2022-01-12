package commands.utilities;

import net.dv8tion.jda.api.EmbedBuilder;

import java.awt.*;

public class StyledEmbedBuilder extends EmbedBuilder {
    public StyledEmbedBuilder() {
        this.setColor(Color.RED);
    }
}
