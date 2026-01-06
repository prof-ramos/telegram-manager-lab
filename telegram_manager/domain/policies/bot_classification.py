OFFICIAL_BOTS = {
    "botfather",
    "spambot",
    "telegramsupport",
    "notifications",
    "groupanonymousbot",
}


def is_official_bot(username: str) -> bool:
    if not username:
        return False
    return username.strip().lower() in OFFICIAL_BOTS
