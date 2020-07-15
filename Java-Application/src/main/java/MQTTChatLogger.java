import java.io.File;
import java.io.IOException;
import java.util.logging.Logger;
import java.util.logging.FileHandler;
import java.util.logging.SimpleFormatter;

public class MQTTChatLogger {

    private final static Logger logger = Logger.getLogger(Logger.GLOBAL_LOGGER_NAME);
    private static String pathToLog;

    private static boolean path = false;

    public static void setPathToLog(String pathToLogs) {
        MQTTChatLogger.pathToLog = pathToLogs;
    }

    public static void setHasPath(boolean hasPath) {
        MQTTChatLogger.path = hasPath;
    }

    public static void createLogFile(String pathToLog) {
        try {

            // Set path to log file
            setHasPath(true);
            setPathToLog(pathToLog);

            // Open file
            File logFile = new File(pathToLog);
            logFile.getParentFile().mkdirs();

            // Initialize file handler
            FileHandler fh = new FileHandler(pathToLog);
            logger.addHandler(fh);

            // Create formatter for logs
            SimpleFormatter formatter = new SimpleFormatter();
            fh.setFormatter(formatter);

            // Disable logging in console
            logger.setUseParentHandlers(false);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static void makeInfoLog(String log) {
        if (path) {
            logger.info(log);
        } else {
            System.out.println(log);
        }
    }

    public static void makeErrorLog(String log) {
        if (path) {
            logger.severe(log);
        } else {
            System.out.println(log);
        }
    }

}
