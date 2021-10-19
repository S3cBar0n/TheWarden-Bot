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
    @commands.has_permissions(kick_members=True)
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
                        await ctx.send(f'You have received an additional warning.. {warnings} total')
                    else:
                        df.loc[df["User_ID"] == member.id, "Infractions"] = 1
                        df.to_csv("database.csv", index=False)
                        await ctx.send("Your infraction has been recorded..")

                    if total_warnings > 0:
                        df.loc[df["User_ID"] == member.id, "Total_Infractions"] += 1
                        df.to_csv("database.csv", index=False)
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
            await ctx.send("Silly, you cannot punish The Warden...")
            return

        try:
            warnings = int(df.loc[df["User_ID"] == member.id, "Infractions"])
            if int(warnings) >= 3:
                print(warnings)
                await ctx.guild.ban(member, delete_message_days=1)
                print(member)
                await ctx.send(f'{member} has been banned for **3 day(s)**')

                try:
                    df = pd.read_csv('database.csv')
                    df.loc[df["User_ID"] == member.id, "Tempban"] = dt.date.today()
                    df.to_csv("database.csv", index=False)

                except Exception as e:
                    print(e)

            else:
                return
                await ctx.send(f'Failed to ban {member}')
        except Exception as e:
            print(e)

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
                    await ctx.send(f'{member} has been forgiven..')
                else:
                    await ctx.send(f"{member} does not have any infractions to forgive.")
            else:
                await ctx.send(f"{member} does not have any infractions to forgive.")
                return
        except Exception as e:
            print(e)
            return

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')
        try:
            for ban_entry in banned_users:
                user = ban_entry.user

                if (user.name, user.discriminator) == (member_name, member_discriminator):
                    await ctx.guild.unban(user)
                    await ctx.send(f'{member} has been unbanned.')

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
                    await ctx.send(f"Can't find {member} to unban...")



        except Exception as e:
            print(e)
            await ctx.send(f'{member} is not on the banned list.')

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def banlist(self, ctx):
        bans = await ctx.guild.bans()
        pretty_list = ["• {0.id} ({0.name}#{0.discriminator})".format(entry.user) for entry in bans]
        await ctx.send("**Ban list:** \n{}".format("\n".join(pretty_list)))

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
        else:
            return

        embed = discord.Embed(title=member.name, description=member.mention, color=color)
        embed.add_field(name='ID', value=str(member.id), inline=False)
        embed.add_field(name='Troublemaker', value=troublemaker, inline=False)
        embed.add_field(name='Current Infractions', value=warnings, inline=False)
        embed.add_field(name='Lifetime Infractions', value=total_warnings, inline=False)
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author.name}")
        await ctx.send(embed=embed)
        
    @commands.command(aliases = ['purge']) # This is a very useful command, which can be used, when someone starts spamming a lot in the chat/channel.
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=100):
        await ctx.channel.purge(limit=amount)    
     


# This function allows us to connect this cog to our bot
def setup(client):
    client.add_cog(Commands(client))
