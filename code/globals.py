import os
from datetime import timedelta
from dotenv   import load_dotenv

load_dotenv()

BOT_TOKEN         = os.getenv("BOT_TOKEN", "")

CHANNEL_USERNAMES = os.getenv("CHANNEL_USERNAMES", "").split(',')
ADMIN_ID          = int(os.getenv("ADMIN_ID", 1))

DB_PATH           = os.getenv("DB_PATH")
IMAGE_PATH        = os.getenv("IMAGE_PATH", "")
TEXT_PATH         = os.getenv("TEXT_PATH", "")
BACK_IMAGE        = os.getenv("BACKGROUND_IMG_PATH", "")
LOG_PATH          = os.getenv("LOG_PATH", "")
BOT_TEXT_PATH     = os.getenv("BOT_TEXT_PATH", "")

VERBS_COUNT       = int(os.getenv("VERBS_COUNT"))
VERBS_ON_PAGE     = int(os.getenv("VERB_ON_PAGE"))

TEXT_HEX          = int(os.getenv("VERB_TEXT_COLOR", "0xFFFFFF"), 16)
T_R, T_G, T_B     = ((TEXT_HEX >> 16) & 0xFF), ((TEXT_HEX >> 8) & 0xFF), (TEXT_HEX & 0xFF)
LAST_WORD_HEX     = int(os.getenv("VERB_TRANSLATION_COLOR", "0xFF0000"), 16)
LW_R, LW_G, LW_B  = ((LAST_WORD_HEX >> 16) & 0xFF), ((LAST_WORD_HEX >> 8) & 0xFF), (LAST_WORD_HEX & 0xFF)
FONT              = os.getenv("FONT", "arial.ttf")

CARTS_WIDTH                     = int(os.getenv("CARTS_WIDTH", 800))
CARTS_HEIGHT                    = int(os.getenv("CARTS_HEIGHT", 450))
CARTS_TEXT_SIZE                 = int(os.getenv("CARTS_TEXT_SIZE", 40))
CARTS_BACKGROUND_HEX            = int(os.getenv("CARTS_BACKGROUND_COLOR", "0x000000ff"), 16)
CB_R, CB_G, CB_B, C_ALPHA_CANAL = ((CARTS_BACKGROUND_HEX >> 24) & 0xFF),((CARTS_BACKGROUND_HEX>> 16) & 0xFF), ((CARTS_BACKGROUND_HEX >> 8) & 0xFF), (CARTS_BACKGROUND_HEX & 0xFF)

TABLE_WIDTH                     = int(os.getenv("TABLE_WIDTH", 1600))
TABLE_HEIGHT                    = int(os.getenv("TABLE_HEIGHT", 900))
TABLE_BACKGROUND_COLOR          = int(os.getenv("TABLE_BACKGROUND_COLOR", "0x000000ff"), 16)
TB_R, TB_G, TB_B, T_ALPHA_CANAL = ((TABLE_BACKGROUND_COLOR >> 24) & 0xFF), ((TABLE_BACKGROUND_COLOR >> 16) & 0xFF), ((TABLE_BACKGROUND_COLOR >> 8) & 0xFF), (TABLE_BACKGROUND_COLOR & 0xFF)
TABLE_HEADER_TEXT_COLOR         = int(os.getenv("TABLE_HEADER_TEXT_COLOR", "0xFF0000"), 16)
TH_R, TH_G, TH_B                = ((TABLE_HEADER_TEXT_COLOR >> 16) & 0xFF), ((TABLE_HEADER_TEXT_COLOR >> 8) & 0xFF), (TABLE_HEADER_TEXT_COLOR & 0xFF)
TABLE_HEADER_TEXT_SIZE          = int(os.getenv("TABLE_HEADER_TEXT_SIZE", 30))
TABLE_TEXT_SIZE                 = int(os.getenv("TABLE_TEXT_SIZE", 20))

ROW                             = int(os.getenv("VERB_ON_PAGE", 15))

IMAGES_CASH     = {}
LAST_MESSAGE    = {}
LOGS_BUFFER     = {}
VERBS_INDEXES   = {}
VERBS_WORK      = False