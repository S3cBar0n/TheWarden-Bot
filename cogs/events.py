import asyncio
import csv
import discord
import datetime as dt
import pandas as pd
import os
from discord.ext import commands, tasks

try:
    df = pd.read_csv('filtered_words.csv')
    filtered_words = df["Words"]
    print(filtered_words)
except Exception as e:
    print(e)


class Events(commands.Cog):
    def __init__(self, client):
        self.client = client  # this allows us to access the client within our cog

    # ------------------- Events and Tasks -------------------
    # Loads bot, and lets us know when its ready
    @commands.Cog.listener()
    async def on_ready(self):
        self.ban_check.start()
        print("Logged in as " + self.client.user.name)
        print(self.client.user.id)
        print("----------------------")

    # When a known command fails, throws error
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await ctx.send(ctx.command.name + " didn't work! Give it another try.")
        print(error)

    # Event for monitoring command usage
    @commands.Cog.listener()
    async def on_command(self, ctx):
        print(ctx.command.name + " was invoked.")

    # Event for monitoring successful command usage
    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        print(ctx.command.name + " was invoked sucessfully.")

    @commands.Cog.listener()
    async def on_message(self, msg):
        for word in filtered_words:
            if word in msg.content and msg.author.id != 785550919327940668:
                await msg.delete()
                author = msg.author
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
                    if str(author.id) in infractions:
                        df = pd.read_csv('database.csv')
                        warnings = int(df.loc[df["User_ID"] == author.id, "Infractions"])
                        total_warnings = int(df.loc[df["User_ID"] == author.id, "Total_Infractions"])
                        if warnings > 0:
                            df.loc[df["User_ID"] == author.id, "Infractions"] += 1
                            df.to_csv("database.csv", index=False)
                            warnings = int(df.loc[df["User_ID"] == author.id, "Infractions"])
                            await author.send(
                                f'The word "{word}" is banned on our server... You have received an additional warning.. {warnings} total')
                        else:
                            df.loc[df["User_ID"] == author.id, "Infractions"] = 1
                            df.to_csv("database.csv", index=False)
                            await author.send(
                                f'The word "{word}" is banned on our server... Your infraction has been recorded..')

                        if total_warnings > 0:
                            df.loc[df["User_ID"] == author.id, "Total_Infractions"] += 1
                            df.to_csv("database.csv", index=False)
                        else:
                            df.loc[df["User_ID"] == author.id, "Infractions"] = 1
                            df.to_csv("database.csv", index=False)
                    else:
                        username = str(author)
                        user_id = str(author.id)
                        csv_writer.writerow([username, user_id])
                        csv_file.close()
                        df = pd.read_csv('database.csv')
                        df.loc[df["User_ID"] == author.id, "Infractions"] = 1
                        df.loc[df["User_ID"] == author.id, "Total_Infractions"] = 1
                        df.to_csv("database.csv", index=False)
                        await author.send(
                            f'The word "{word}" is banned on our server... Your infraction has been recorded..')
                except Exception as e:
                    print(e)

                try:
                    warnings = int(df.loc[df["User_ID"] == author.id, "Infractions"])
                    if int(warnings) >= 3:
                        print(warnings)
                        await msg.author.ban()
                        print(author)
                        await author.send(f'You have been banned for **3 day(s)**')
                        try:
                            df = pd.read_csv('database.csv')
                            df.loc[df["User_ID"] == author.id, "Tempban"] = dt.date.today()
                            df.to_csv("database.csv", index=False)

                        except Exception as e:
                            print(e)
                    else:
                        return
                except Exception as e:
                    print(e)
            else:
                continue

    @tasks.loop()
    async def ban_check(self):

        for guild in self.client.guilds:
            print("----------------------")
            print("Automatic Task is Running...")
            print(f"Checking {guild}'s ban list...")
            guild = await self.client.fetch_guild(guild_id=guild.id)

            await asyncio.sleep(30)

            df = pd.read_csv('database.csv')
            bandate = df["Tempban"]

            for date in bandate:
                if str(date) != "nan":
                    d1 = dt.datetime.strptime(str(date), "%Y-%m-%d")
                    d2 = dt.datetime.strptime(str(dt.date.today()), "%Y-%m-%d")
                    delta = (d2 - d1).days
                    if delta >= 3:
                        try:
                            print('------ Performing Unban ------')
                            user = int(df.loc[df["Tempban"] == date, "User_ID"])
                            df.loc[df["Tempban"] == date, "Infractions"] = 0
                            df.loc[df["Tempban"] == date, "Tempban"] = ''
                            df.to_csv("database.csv", index=False)
                            await guild.unban(discord.Object(id=user))
                            # Send message in a specific channel when the user has been unbanned
                            print(f'----- Unbanned {user} -----')
                        except Exception as e:
                            print(e)
                            continue
                else:
                    continue
            else:
                print("No Bans could be processed at this time")
                print('----------------------')
                continue


def setup(client):
    client.add_cog(Events(client))
