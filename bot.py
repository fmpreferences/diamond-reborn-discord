from discord.ext import commands
import json
import datetime

# a chat application to retrieve all of a certain author's msgs, organized by
# date (the msg objs returned by the method has both date and msg cntent)
# can be generalized through the application itself but when I wrote I only
# sought my msgs
bot = commands.Bot(command_prefix="d+")


@bot.command()
async def retrieve(
        ctx,
        tz: int = 0,
        limit=4294967294,
        *AUTHOR_IDS):  # receives desired author id through actual chat
    # put your timezone
    limit += 1
    AUTHOR_IDS = map(int, AUTHOR_IDS)
    print(ctx, tz, limit, AUTHOR_IDS)
    msgs = await ctx.channel.history(limit=4294967295).flatten()
    filtered_msgs = [
        m for m in msgs if m.author.id in AUTHOR_IDS
    ]
    print(filtered_msgs)
    filtered_msgs = list(
        reversed(filtered_msgs)
    )  # reversed is faster than the oldest first kwarg in channel.history()
    msg_json = {}
    for filtered_msg in filtered_msgs:
        creation = filtered_msg.created_at + datetime.timedelta(hours=tz)
        dateasstr = f"{creation:%d/%m/%Y}"  # %d, %m 2 digits %Y 4 digits
        if dateasstr not in msg_json:  # check if there first to avoid keyerror
            msg_json[dateasstr] = [filtered_msg.content]
        else:
            msg_json[dateasstr].append(filtered_msg.content)
    with open(f'mymsgs{ctx.guild.name}{ctx.channel.name}.txt', 'w') as stuff:
        json.dump(msg_json, stuff, indent=4)
    await ctx.send(f'success\n{len(filtered_msgs)} messages')


with open('token.txt') as token:
    token = token.readlines()[0]

bot.run(token)
