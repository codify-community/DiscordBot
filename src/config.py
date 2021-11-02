import toml


class CodifyBotConfig:
    def __init__(self, token, telegramToken, discordWebhookUrl, telegramChannelId, OffTopicChannelId):
        self.token = token
        self.telegramToken = telegramToken
        self.discordWebhookUrl = discordWebhookUrl
        self.telegramChannelId = telegramChannelId
        self.OffTopicChannelId = OffTopicChannelId


def config() -> CodifyBotConfig:
    """
    Returns the configuration object.
    """
    __cfg = __parse_config()
    return CodifyBotConfig(__cfg["discord"]["token"], __cfg["telegram"]["token"], __cfg["discord"]["webhook"], __cfg["ids"]["telegramChatId"], __cfg["ids"]["OffTopicChatId"])


def __parse_config() -> dict:
    """
    Loads the configuration file.
    """
    with open("config.toml") as f:
        return toml.load(f)
