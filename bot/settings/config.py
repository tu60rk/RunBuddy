from logging import config as logging_config

from pydantic import BaseSettings, Field


class botSettings(BaseSettings):

    waitGetComment: int = Field(defaul=3600, env="waitGetComment")

    coreDayOfWeek:int = Field(defaul=0, env="coreDayOfWeek")
    coreHour:int = Field(defaul=12, env="coreHour")
    coreMinute:int = Field(defaul=0, env="coreMinute")

    activateComments:bool = Field(defaul=False, env="activateComments")
    commentDayOfWeek:int = Field(defaul=2, env="commentDayOfWeek")
    commentHour:int = Field(defaul=12, env="commentHour")
    commentMinute:int = Field(defaul=0, env="commentMinute")

    doubleCoreDayOfWeek:int = Field(defaul=4, env="doubleCoreDayOfWeek")
    doubleCoreHour:int = Field(defaul=12, env="doubleCoreHour")
    doubleCoreMinute:int = Field(defaul=0, env="doubleCoreMinute")

    ageRange:int = Field(defaul=10, env="ageRange")

    TELEGRAM_TOKEN:str
    NGINX_HOST:str
    IS_WEBHOOK:bool
    WEBAPP_HOST:str
    WEBAPP_PORT:int

    ADMINS:str

    isTest:bool = Field(defaul=False, env="isTest")

    path:str
    fileNameRegistered:str
    fileNameMeets:str

    class Config:
        case_sensitive = True
        env_file = ".bot.env"


class dbSettings(BaseSettings):

    DB:str
    DB_USER:str
    DB_PASS:str
    DB_PORT:int
    DB_HOST:str
    dsl_database: str = Field(
		None,
	)

    class Config:
        case_sensitive = True
        env_file = ".env"


class textBotSettings(BaseSettings):


    botStartText:str

    menuText:str
    exceptionText:str

    registrationTextFIO :str
    registrationTextFIOException :str

    registrationTextInputAge :str
    registrationTextInputAgeException :str
    registrationTextInputAgeException100 :str
    registrationTextInputAgeException18 :str

    registrationTextGender :str

    registrationTextCity :str
    registrationTextInputCity :str
    registrationTextInputCityException :str


    registrationTextRunLevel :str

    registrationTextInputLinkAccount :str

    registrationTextAdditionalPreQuestionText :str
    registrationTextAdditionalQuestionOne :str
    registrationTextAdditionalQuestionTwo :str
    registrationTextAdditionalQuestionThree :str
    registrationTextFinalText :str

    cities :str
    runLevels :str
    gender :str

    changeDataStart :str
    changeDataMenu :str
    changeDataQuestionAboutMeet :str

    dontFindPartner :str
    findPartner :str

    menuForAdmins:str
    menuForRegistered:str
    menuForUnRegistered:str

    class Config:
        case_sensitive = True
        env_file = ".text.bot.env"


botMainSettings = botSettings()
botTextSettings = textBotSettings()
botMainDbSettings = dbSettings()
botMainDbSettings.dsl_database = (
    f"postgres://{botMainDbSettings.DB_USER}:{botMainDbSettings.DB_PASS}@"
    f"{botMainDbSettings.DB_HOST}:{botMainDbSettings.DB_PORT}/{botMainDbSettings.DB}"
)
