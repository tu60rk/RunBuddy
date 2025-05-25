from pydantic import Field
from pydantic_settings import BaseSettings


class botSettings(BaseSettings):

    waitGetComment: int = Field(defaul=3600, env="waitGetComment")

    coreDayOfWeek: int = Field(defaul=0, env="coreDayOfWeek")
    coreHour: int = Field(defaul=12, env="coreHour")
    coreMinute: int = Field(defaul=0, env="coreMinute")

    # activateComments:bool = Field(defaul=False, env="activateComments")
    commentDayOfWeek: int = Field(defaul=2, env="commentDayOfWeek")
    commentHour: int = Field(defaul=12, env="commentHour")
    commentMinute: int = Field(defaul=0, env="commentMinute")

    doubleCoreDayOfWeek: int = Field(defaul=4, env="doubleCoreDayOfWeek")
    doubleCoreHour: int = Field(defaul=12, env="doubleCoreHour")
    doubleCoreMinute: int = Field(defaul=0, env="doubleCoreMinute")

    dontAnswerDayOfWeek: int
    dontAnswerHour: int
    dontAnswerMinute: int

    backupHour: int
    backupMinute: int
    documentBackUp: str

    ageRange: int = Field(defaul=10, env="ageRange")

    TELEGRAM_TOKEN: str
    # PAYMENTS_TOKEN: str
    NGINX_HOST: str
    IS_WEBHOOK: bool
    WEBAPP_HOST: str
    WEBAPP_PORT: int
    REDIS_DSN: str
    OPENAI_API_KEY: str
    OPENAPI_URL: str

    ADMINS: str

    isTest: bool = Field(defaul=False, env="isTest")

    path: str
    fileNameRegistered: str
    fileNameMeets: str
    fileNameComments: str

    throttlingChatGptTimeLimit: int
    throttlingChatGptCountLimit: int

    # nats
    # NATS_SERVERS: str
    # NATS_NOTIFIED_CONSUMER_SUBJECT: str
    # NATS_NOTIFIED_CONSUMER_STREAM: str
    # NATS_NOTIFIED_CONSUMER_DURABLE_NAME: str

    class Config:
        case_sensitive = True
        env_file = ".bot.env"


class dbSettings(BaseSettings):

    DB: str
    DB_USER: str
    DB_PASS: str
    DB_PORT: int
    DB_HOST: str
    dsl_database: str = Field(
        "1",
    )

    class Config:
        case_sensitive = True
        env_file = ".env"


class textBotSettings(BaseSettings):

    botStartText: str

    menuText: str
    menuSuccess: str
    menuException: str
    exceptionText: str
    buttonReturn: str

    registrationDontHaveData: str
    registrationTextFIO: str
    registrationTextFIOException: str

    stayComment: str
    stayCommentExeption: str
    stayCommentFinish: str

    registrationTextInputAge: str
    registrationTextInputAgeException: str
    registrationTextInputAgeException100: str
    registrationTextInputAgeException18: str

    registrationTextGender: str

    registrationTextCity: str
    registrationTextInputCity: str
    registrationTextInputCityException: str

    registrationTextRunLevel: str

    registrationTextInputLinkAccount: str

    registrationTextAdditionalPreQuestionText: str
    registrationTextAdditionalQuestionOne: str
    registrationTextAdditionalQuestionTwo: str
    registrationTextAdditionalQuestionThree: str
    registrationTextFinalText: str

    cities: str
    runLevels: str
    gender: str

    changeDataStart: str
    changeDataMenu: str
    changeDataQuestionAboutMeet: str

    dontFindPartner: str
    findPartner: str

    menuForAdmins: str
    menuForRegistered: str
    menuForUnRegistered: str
    menuForComment: str
    commentTextInputException255: str

    startShortComment: str
    positiveAnswerOfShortComment: str
    # negativeAnswerOfShortComment: str
    # notAnswerShortComment: str

    usersDontMeet: str

    chatGptStart: str
    limitOfCountRequest: str

    class Config:
        case_sensitive = True
        env_file = ".text.bot.env"


botMainSettings = botSettings()
botTextSettings = textBotSettings()
botMainDbSettings = dbSettings()
# botMainDbSettings.dsl_database = (
# f"postgres://{botMainDbSettings.DB_USER}:{botMainDbSettings.DB_PASS}@"
# f"{botMainDbSettings.DB_HOST}:{botMainDbSettings.DB_PORT}/{botMainDbSettings.DB}"
# )

botMainDbSettings.dsl_database = (
    f"postgresql+psycopg://{botMainDbSettings.DB_USER}:{botMainDbSettings.DB_PASS}@"
    f"{botMainDbSettings.DB_HOST}:{botMainDbSettings.DB_PORT}/{botMainDbSettings.DB}"
)
