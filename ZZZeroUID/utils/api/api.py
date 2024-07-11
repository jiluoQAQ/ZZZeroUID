from gsuid_core.utils.api.mys.api import NEW_URL, OLD_URL, OLD_URL_OS

# BASE_URL
ZZZ_API = f"{NEW_URL}/event/game_record_zzz/api/zzz"
ZZZ_OS_API = "https://sg-act-nap-api.hoyolab.com/event/game_record_zzz/api/zzz"

ZZZ_INDEX_API = "/index"
ZZZ_NOTE_API = "/note"
ZZZ_BUDDY_INFO_API = "/buddy/info"
ZZZ_AVATAR_BASIC_API = "/avatar/basic"
ZZZ_AVATAR_INFO_API = "/avatar/info"
ZZZ_CHALLENGE_API = "/challenge"

ZZZ_BIND_API = f"{OLD_URL}/binding/api"
ZZZ_BIND_OS_API = f"{OLD_URL_OS}/binding/api"
ZZZ_GAME_INFO_API = "/getUserGameRolesByCookie?game_biz=nap_cn"


# Resource
ZZZ_RES = "https://act-webstatic.mihoyo.com/game_record/zzz"
ZZZ_SQUARE_AVATAR = f"{ZZZ_RES}/role_square_avatar"
ZZZ_SQUARE_BANGBOO = f"{ZZZ_RES}/bangboo_rectangle_avatar"

PUBLIC_API = "https://public-operation-nap.mihoyo.com"
PUBILC_GACHA_LOG_API = f"{PUBLIC_API}/common/gacha_record/api"
ZZZ_GET_GACHA_LOG_API = f"{PUBILC_GACHA_LOG_API}/getGachaLog"
