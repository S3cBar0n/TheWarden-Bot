import os
import csv
import pandas as pd
import discord
import datetime as dt
from discord.ext import commands

try:
    if os.path.isfile('database.csv'):
        csv_file = open('database.csv', 'a', encoding='utf-8-sig', newline='')
        csv_writer = csv.writer(csv_file)
        csv_file.close()
    # If the file does not exist, creates it
    else:
        csv_file = open('database.csv', 'w', encoding='utf-8-sig', newline='')
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Username', 'User_ID', 'Infractions', 'Muted', 'Tempban', 'Ban', 'Total_Infractions'])
        csv_file.close()
except Exception as e:
    print(e)
    exit()


# This references the client we created within our bot.py and passes it into the cog
class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client  # this allows us to access the client within our cog

    @commands.command()
    @commands.has_permissions(manage_channels=True) # Permissions required for executing the command
    async def warn(self, ctx, *, member: discord.Member):
        # This is to check to see if the user is trying to Warn the bot, and fails if so
        print(dt.date.today())
        if member.id != 785550919327940668:
            try:
                if os.path.isfile('database.csv'):
                    csv_file = open('database.csv', 'a', encoding='utf-8-sig', newline='')
                    csv_writer = csv.writer(csv_file)
                # If the file does not exist, creates it
                else:
                    csv_file = open('database.csv', 'w', encoding='utf-8-sig', newline='')
                    csv_writer = csv.writer(csv_file)
                    csv_writer.writerow(
                        ['Username', 'User_ID', 'Infractions', 'Muted', 'Tempban', 'Ban', 'Total_Infractions'])
            except Exception as e:
                print(e)
                exit()
            try:
                infractions = []
                with open('database.csv', encoding='utf-8-sig', newline='') as file:
                    for row in csv.reader(file):
                        infractions.append(row[1])
                if str(member.id) in infractions:
                    df = pd.read_csv('database.csv')
                    warnings = int(df.loc[df["User_ID"] == member.id, "Infractions"])
                    total_warnings = int(df.loc[df["User_ID"] == member.id, "Total_Infractions"])
                    if warnings > 0:
                        df.loc[df["User_ID"] == member.id, "Infractions"] += 1
                        df.to_csv("database.csv", index=False)
                        warnings = int(df.loc[df["User_ID"] == member.id, "Infractions"])
                        em = discord.Embed(title="Additional Warning", description=f'You have received an additional warning.. {warnings} total')
                    else:
                        df.loc[df["User_ID"] == member.id, "Infractions"] = 1
                        df.to_csv("database.csv", index=False)
                        em = discord.Embed(title="Infraction recorded", description="Your infraction has been recorded..")
                    await ctx.send(embed=em)
                    if total_warnings > 0:
                        df.loc[df["User_ID"] == member.id, "Total_Infractions"] += 1
                    else:
                        df.loc[df["User_ID"] == member.id, "Infractions"] = 1
                    df.to_csv("database.csv", index=False)
                else:
                    username = member
                    user_id = member.id
                    csv_writer.writerow([username, user_id])
                    csv_file.close()
                    df = pd.read_csv('database.csv')
                    df.loc[df["User_ID"] == member.id, "Infractions"] = 1
                    df.loc[df["User_ID"] == member.id, "Total_Infractions"] = 1
                    df.to_csv("database.csv", index=False)
                    await ctx.send("Your infraction has been recorded..")

            except Exception as e:
                print(e)
                return
        else:
            em = discord.Embed(title="Cannot punish Warden", description="Silly, you cannot punish The Warden...")
            await ctx.send(embed=em)
            return

        try:
            warnings = int(df.loc[df["User_ID"] == member.id, "Infractions"])
            if int(warnings) >= 3:
                print(warnings)
                await ctx.guild.ban(member, delete_message_days=1)
                print(member)
                em = discord.Embed(title="Member Banned", description=f'{member} has been banned for **3 day(s)**')
                await ctx.send(embed=em)

                try:
                    df = pd.read_csv('database.csv')
                    df.loc[df["User_ID"] == member.id, "Tempban"] = dt.date.today()
                    df.to_csv("database.csv", index=False)

                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)
            
    @warn.error
    async def warn_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):  # Runs when the ctx.author doesn't have the permission to execute the command.
            em = discord.Embed(title="Error", description=f"You don't have the `Manage Chanels` permission to use this command.{ctx.author.mention}", colour=ctx.author.colour)
            await ctx.send(embed=em) # Sends the embed message

    @commands.command(aliases=['pardon'])
    @commands.has_permissions(kick_members=True)
    async def forgive(self, ctx, *, member: discord.Member):
        try:
            infractions = []
            with open('database.csv', encoding='utf-8-sig', newline='') as file:
                for row in csv.reader(file):
                    infractions.append(row[1])
            if str(member.id) in infractions:
                df = pd.read_csv('database.csv')
                warnings = int(df.loc[df["User_ID"] == member.id, "Infractions"])
                if warnings > 0:
                    df.loc[df["User_ID"] == member.id, "Infractions"] = 0
                    df.to_csv("database.csv", index=False)
                    em = discord.Embed(title="Forgiven", description=f'{member} has been forgiven..')
                else:
                    em = discord.Embed(title="No Interactions", description=f"{member} does not have any infractions to forgive.")
                await ctx.send(embed=em)
            else:
                em = discord.Embed(title="No Infractions", description=f"{member} does not have any infractions to forgive.")
                await ctx.send(embed=em)
                return
        except Exception as e:
            print(e)
            return
        
    @forgive.error
    async def forgive_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            em = discord.Embed(title="Error", description=f"You don't have the `Kick Members` permission to use this command.{ctx.author.mention}", colour=ctx.author.colour)
            await ctx.send(embed=em)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')
        try:
            for ban_entry in banned_users:
                user = ban_entry.user

                if (user.name, user.discriminator) == (member_name, member_discriminator):
                    await ctx.guild.unban(user)
                    em = discord.Embed(title="Unbanned Member", description=f'{member} has been unbanned.')
                    await ctx.send(embed=em)

                    print(member)

                    df = pd.read_csv('database.csv')
                    bannedlist = df["Username"]
                    print(bannedlist)

                    for ban in bannedlist:
                        if ban == member:
                            print(ban)
                            print(member)
                            df.loc[df["Username"] == ban, "Infractions"] = 0
                            df.loc[df["Username"] == ban, "Tempban"] = ''
                            df.to_csv("database.csv", index=False)
                else:
                    em = discord.Embed(title="No Member Found", description=f"Can't find {member} to unban...")
                    await ctx.send(embed=em)



        except Exception as e:
            print(e)
            em = discord.Embed(title="No Member Found", description=f'{member} is not on the banned list.')
            await ctx.send(embed=em)
            
    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            em = discord.Embed(title="Error", description=f"You don't have the `Ban Members` permission to use this command.{ctx.author.mention}", colour=ctx.author.colour)
            await ctx.send(embed=em)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def banlist(self, ctx):
        bans = await ctx.guild.bans()
        pretty_list = ["• {0.id} ({0.name}#{0.discriminator})".format(entry.user) for entry in bans]
        await ctx.send("**Ban list:** \n{}".format("\n".join(pretty_list)))
        
    @banlist.error
    async def banlist_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            em = discord.Embed(title="Error", description=f"You don't have the `Kick Members` permission to use this command.{ctx.author.mention}", colour=ctx.author.colour)
            await ctx.send(embed=em)

    @commands.command(aliases=["user", "info"])
    @commands.has_permissions(kick_members=True)
    async def whois(self, ctx, *, member: discord.Member):
        infractions = []
        with open('database.csv', encoding='utf-8-sig', newline='') as file:
            for row in csv.reader(file):
                infractions.append(row[1])
        df = pd.read_csv('database.csv')

        try:
            warnings = int(df.loc[df["User_ID"] == member.id, "Infractions"])
        except Exception as e:
            print(e)
            warnings = 0

        try:
            total_warnings = int(df.loc[df["User_ID"] == member.id, "Total_Infractions"])
        except Exception as e:
            print(e)
            total_warnings = 0

        if warnings >= 3:
            troublemaker = True
            color = discord.Colour.dark_red()
        elif warnings >= 2:
            troublemaker = True
            color = discord.Colour.red()
        elif warnings >= 1:
            troublemaker = True
            color = discord.Colour.gold()
        else:
            troublemaker = False
            color = discord.Colour.green()

        if total_warnings >= 15:
            troublemaker = True

        embed = discord.Embed(title=member.name, description=member.mention, color=color)
        embed.add_field(name='ID', value=str(member.id), inline=False)
        embed.add_field(name='Troublemaker', value=troublemaker, inline=False)
        embed.add_field(name='Current Infractions', value=warnings, inline=False)
        embed.add_field(name='Lifetime Infractions', value=total_warnings, inline=False)
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author.name}")
        await ctx.send(embed=embed)
        
    @whois.error
    async def whois_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            em = discord.Embed(title="Error", description=f"You don't have the `Kick Members` permission to use this command.{ctx.author.mention}", colour=ctx.author.colour)
            await ctx.send(embed=em)
        
    @commands.command(aliases = ['purge']) # This is a very useful command, which can be used, when someone starts spamming a lot in the chat/channel.
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=100):
        await ctx.channel.purge(limit=amount)    
        
    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            em = discord.Embed(title="Error", description=f"You don't have the `Manage Messages` permission to use this command.{ctx.author.mention}", colour=ctx.author.colour)
            await ctx.send(embed=em)
                                   
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, seconds: int):
        await ctx.channel.edit(slowmode_delay=seconds)
        em = discord.Embed(title="Slowmode Set -", description=f"Set the slowmode to {seconds} seconds in {ctx.channel.mention}", colour= discord.Color.random())
        await ctx.channel.send(embed=em)

    @slowmode.error
    async def slowmode_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            em = discord.Embed(title="Error", description=f"You don't have the `Manage Channels` permission to use this command.{ctx.author.mention}", colour=ctx.author.colour)
            await ctx.send(embed=em)

    @commands.command(aliases=["remove_slowmode", "removeslowmode"])
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def removedelay(self, ctx):  
        if ctx.channel.slowmode_delay != 0:
            await ctx.channel.edit(slowmode_delay=0)
            em = discord.Embed(title="Slowmode removed -", description=f"Removed the slowmode of {ctx.channel.mention}!", colour=discord.Color.random())
        else:
            em = discord.Embed(title="No Slowmode detected", description=f"No slowmode detected in the channel {ctx.channel.mention}", colour=discord.Color.random())
        await ctx.channel.send(embed=em)

    @removedelay.error
    async def removedelay_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            em = discord.Embed(title="Error", description=f"You don't have the `Manage Channels` permission to use this command.{ctx.author.mention}", colour=ctx.author.colour)
            await ctx.send(embed=em)
     

# This function allows us to connect this cog to our bot
def setup(client):
    client.add_cog(Commands(client))
