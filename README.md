### **The Warden - Discord.Py Moderation Bot:**

For every individual message that contains words on the banned words list you get 1 infraction, moderators can also manually give warnings with **>warn** Username

Once a user gets 3 infractions they are automatically banned for 3 days time and then unbanned after that time. 

The **>user** command displays the users current stats, containing their name, pfp, discord ID, if they are a troublemaker (you are a trouble maker if you have any current infractions, you can become a permanent trouble maker by reaching 15+ infractions), current and lifetime infractions.
The **>user** command also will display as green for 0 infractions, yellow for 1, red for 2, and dark red for 3 (however this is only for testing).

Once a user is unbanned, or pardoned with the **>pardon** command, their current infractions are reset back to 0. 

You can manually ban with **>ban** (THE BAN COMMAND IS FOR A PERM BAN) and unban with **>unban**

You can access the current banlist for the server with **>banlist**


You will need to create your own filtered_words.csv in the working directory for it to properly monitor for banned words.


#### **Future Features:**
- Auto invite after unban
- Adding a manual tempban command
- Add some more advanced functionality for users who are set as troublemakers
- Work out any bugs we find during use
- Convert our current csv "database" to a SQL based DB