# amos
just a bot
i should try to add this:

`
autoroles, muteroles = {}

class Roles(Enum):
    AUTOROLE = "autorole"
    MUTE = "mute"

async def reload_configs():
    with open("/nice/autorole.json", "r") as f:
        autoroles = json.load(f)
    with open("/nice/mute.json", "r") as f:
        muteroles = json.load(f)
        
async def set_role(type, guild_id, role_name):
    with open(f"/nice/{type(Roles.AUTOROLE.value)}.json", "r") as f:
        roles = json.load(f)

        roles[str(guild_id)] = role_name

    with open(f"/nice/{type(Roles.AUTOROLE.value)}.json", "w") as f:
        json.dump(roles, f, indent=4)
`
