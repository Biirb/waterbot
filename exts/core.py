import discord
import re
from typing import Optional
from .helpers.check import Checks
from .helpers.util import Converters
from discord.ext import commands


class Core(commands.Cog):
    '''Core commands
    '''

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    @Checks.is_dev()
    async def activity(self, ctx, *, text):
        '''Sets the bots status
        Set the bot's playing status
        activity <Status Text>
        Bot Owner only'''
        game = discord.Game(text)
        await ctx.bot.change_presence(status=discord.Status.online, activity=game)
        await ctx.send(':ok_hand: Done.')

    @commands.command(name='say')
    @commands.has_permissions(manage_messages=True)
    async def say(self, ctx, channel: Optional[discord.TextChannel],  *, text):
        '''Make the bot say something
        Self-explanatory. Note that ``channel`` is not a required argument, so you can just do ``.say text here`` to send the text in the current channel, or ``.say #testchannel something here`` to send it to #testchannel.
        say [channel] <text>
        Manage Messages'''
        await ctx.send(text)

    @commands.has_permissions(manage_messages=True)
    @commands.command()
    @Checks.is_dev()
    async def sayembed(self, ctx, body: str, title: str = None, channel: discord.TextChannel = None, footer: str = None,
                       color: str = discord.Embed.Empty):
        '''Make the bot say something
        Make the bot say something in embeds. \\nColor have to be a rgb integer number(155012074).
        sayembed <body> [title] [channel] [footer] [color]
        Manage Messages'''
        if channel is None:
            channel = ctx.channel
        if color is not discord.Embed.Empty:
            color = discord.Color.from_rgb(int(color[0] + color[1] + color[2]),
                                           int(color[3] + color[4] + color[5]),
                                           int(color[6] + color[7] + color[8]))
        embed = discord.Embed(title=title, description=body, color=color)
        if footer is not None:
            embed.set_footer(text=footer, icon_url=self.bot.user.avatar_url)
        await channel.send(embed=embed)

    @commands.command(alises=['invite'])
    async def info(self, ctx):
        '''Info command
        This command gives you an invite link to the support server, and also gives you a user to send hatemails to.
        info
        Send messages'''
        embed = discord.Embed(title='Waterbot Useful links', description=None)
        embed.add_field(name="Support server", value="[Here](https://discord.gg/ATCjdFA)")
        embed.add_field(name="Bot invite (admin)",
                        value="[Here](https://discordapp.com/api/oauth2/authorize?client_id=655262203309719552&permissions=8&scope=bot)")
        embed.add_field(name="Bot invite (normal)",
                        value="[Here](https://discordapp.com/api/oauth2/authorize?client_id=655262203309719552&permissions=2147483127&scope=bot)")
        embed.add_field(name="Guilds", value=f"{len(self.bot.guilds)}")
        embed.add_field(name="Feedback", value="DM <@397029587965575170> or email waterbotmail@protonmail.com")
        embed.add_field(name="Developers", value="**Waterbot is made by a bunch of hobby developers.\n"
                                                 "Here's a list of their names.**\n"
                                                 "Creator: lindsey#0001 (374047038926618624) \n"
                                                 "Developers:\n"
                                                 "```- Kenny_#2020    (397029587965575170) \n"
                                                 "- Dragonic#3535  (513603936033177620) \n"
                                                 "- appraiise#6117 (521656100924293141) ```", inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="help", aliases=['h'])
    async def help(self, ctx, command: str = None):
        '''Help command
        This command only include available extensions/cogs, and in-depth explanations of the specified command.
        help [command name]
        Send messages'''
        prefix = await ctx.bot.get_prefix(ctx.message)
        if command is None:
            embed = discord.Embed(title='Available commands', color=0x0fffbb)
            formlist = {}
            # Get commands
            for i in ctx.bot.commands:
                if i.cog_name not in formlist:
                    formlist[i.cog_name] = []
                formlist[i.cog_name].append(f'{prefix}{i.name}')

            # Add fields
            for i in formlist:
                temp = ""
                embed.add_field(name=f'{i} module', value=f'`{" ".join(formlist[i])}`', inline=False)

            await ctx.send(embed=embed)
        else:
            result = discord.utils.find(lambda a: a.name == command, ctx.bot.commands)
            if result is None:
                return await ctx.send(embed=discord.Embed(
                    description=f"No such command. ({command}) \n"
                                f"Use `.help` to list all available modules and use `.cmds <module name>` "
                                f"to check the available commands in that module.",
                    colour=0xff5555))
            else:
                doc = result.help.splitlines()
                embed = discord.Embed(title=f"Help for command `{command}`", colour=0xa12ba1,
                                      timestamp=ctx.message.created_at)
                embed.add_field(name="Short Description", value=doc[0], inline=False)
                embed.add_field(name="Usage", value=prefix + doc[2], inline=False)
                embed.add_field(name="Description", value=re.sub('\\\\n', '\n', doc[1]), inline=False)
                embed.add_field(name="Command Checks", value=doc[3], inline=False)
            await ctx.send(embed=embed)

    @commands.command(name="cmds")
    async def cmds(self, ctx, cogr=None):
        '''List commands available in an extension
        List all commands in an extension/category
        cmds <category name>
        Send messages'''
        # Grab the command list
        try:
            cogr = cogr.capitalize()
        except:
            pass
        cmds = {}
        excluded = [
            'reload'
        ]
        prefix = await ctx.bot.get_prefix(ctx.message)
        for i in ctx.bot.commands:
            if i.name not in excluded:
                # print(f"Loading command {i}")
                if i.cog_name not in cmds:
                    cmds[i.cog_name] = []
                    cmds[i.cog_name + '_des'] = i.cog.description
                cmds[i.cog_name].append(prefix + i.name)
        if cogr not in cmds:
            return await ctx.send(embed=discord.Embed(description=f"No such category({cogr}).", colour=0xff5555))
        else:
            await ctx.send("Loading", delete_after=5)
        out = "`"
        for i in cmds[cogr]:
            out += f"{i}\n"
        embed = discord.Embed(title=f"Commands in category `{cogr}`", colour=0xa12ba1)
        embed.add_field(name="Category description", value=f"`{cmds[cogr + '_des'].splitlines()[0]}`", inline=False)
        embed.add_field(name="Available commands", value=f"{out}`", inline=False)
        return await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Core(bot))
