package commands.utilities;

public class TimeFormatter {
    /**
     *
     * @param durationMillis
     * @return String formatted duration
     */
    public static String getDurationFormat(long durationMillis){
        int seconds = (int) durationMillis / 1000;
        String format = "";
        if (seconds > 3600) {
            format = String.format("%d:%02d:%02d", seconds / 3600, (seconds % 3600) / 60, (seconds % 60));
        }
        else {
            format = String.format("%02d:%02d", (seconds % 3600) / 60, (seconds % 60));
        }
        return format;
    }

    /**
     *
     * @param durationMillis
     * @return Formatted Minute
     */
    public static String getMinuteFormat(long durationMillis){
        String durationMinute = String.valueOf((int)(durationMillis/1000)/60);
        String durationSecond = String.valueOf((int)(durationMillis/1000)%60);
        if (durationMinute.length() == 1) durationMinute = "0" + durationMinute;
        if (durationSecond.length() == 1) durationSecond = "0" + durationSecond;
        return durationMinute + ":" + durationSecond;
    }
}
