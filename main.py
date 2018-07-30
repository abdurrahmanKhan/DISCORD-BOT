import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
from itertools import cycle5
import json
import os


players={}                          #-------
queues={}                           #       |
def check_queue(id):                #       |
    if queues[id]!=[]:              #       |------- This piece of code will be used for making queues to add next song in your BOT's playlist
        player= queues[id].pop(0)   #       |
        players[id]=player          #       |
        player.start()              #       |
                                    #-------

bot = commands.Bot(command_prefix='#') # This is how you will denote your BOT.


os.chdir(r'F:\progs\Discord BOT')      #this will we your directory in which your JSON file with user's experience will be stored


bot.remove_command('help')    #to remove the preliminary help.


#Just a check that your's BOT is working fine,
#this prints on console
#---------------------------------------------

@bot.event
async def on_ready():
    print("Ready when you are")
    print("I am running on " + bot.user.name)
    print("with the ID:" + bot.user.id)



#This chunk of code tells the BOT what you want to say,
#basically it just echo's what you say to it
#------------------------------------------------------
    
@bot.command()
async def echo(*args):
    output=''
    for word in args:
        output+= word
        output+= ''
    await bot.say(output)
            



#BOT pings you!!
#just for fun, GO ahead!! try it...
#-----------------------------------
    
@bot.command(pass_context=True)
async def ping(ctx):
    await bot.say(":ping_pong: ping!! xSSS")
    print("user has pinged")



#to get the info of any user or of anyone who is in your own server
#------------------------------------------------------------------
    
@bot.command(pass_context=True)
async def info(ctx, user: discord.Member):
   embed= discord.Embed(title="{}'s info".format(user.name), description = "Here's what I could find.", color=0x00ff00)
   embed.add_field(name="Name", value=user.name, inline=True)
   embed.add_field(name="ID", value=user.id, inline=True)
   embed.add_field(name="Status", value=user.status, inline=True)
   embed.add_field(name="Highest Role", value=user.top_role)
   embed.add_field(name="Joined", value=user.joined_at)
   embed.set_thumbnail(url=user.avatar_url)
   await bot.say(embed=embed)
   

#to get the information about the server
#---------------------------------------
   
@bot.command(pass_context=True)
async def serverinfo(ctx):
    embed= discord.Embed(name="{}'s info".format(ctx.message.server.name), description="Here's what I could find.", color=0x00ff00)
    embed.set_author(name="Mr.Robot of ServBots")
    embed.add_field(name="Name", value=ctx.message.server.name, inline=True)
    embed.add_field(name="ID", value=ctx.message.server.id, inline=True)
    embed.add_field(name="Roles", value=len(ctx.message.server.roles), inline=True)
    embed.add_field(name="Members", value=len(ctx.message.server.members))
    embed.set_thumbnail(url=ctx.message.server.icon_url)
    await bot.say(embed=embed)



#This chunk of code is to show the status of your BOT or say to give it a task.
#-----------------------------------------------------------------------------

status=['CS:GO', 'PALADINS', 'DOTA 2', 'PUBG']
async def change_status():
    await bot.wait_until_ready()
    msgs= cycle(status)                             
                                       #also refer to last second line of the code, which is used to create a task
    while not bot.is_closed:           #--------------------------------------------------------------------------
        current_status=next(msgs)
        await bot.change_presence(game=discord.Game(name=current_status))
        await asyncio.sleep(5)


    




    
#Your BOT can even kick to whom you specify him to do so, consider your plus the members ROLE first.
#---------------------------------------------------------------------------------------------------
        
@bot.command(pass_context=True)
@commands.has_role("Friends")                        #if you wanna specify to whom you give permission to do so.
async def kick(ctx, user: discord.Member):           #----------------------------------------------------------
    await bot.say(":boot: Seeya, {}, Ya loser!".format(user.name))
    await bot.kick(user)


#This piece of code shows you how to use EMBEDS, i.e. for eg. what you wanna display in CHAT.
#--------------------------------------------------------------------------------------------
    
@bot.command(pass_context=True)
async def embed(ctx):
    embed= discord.Embed(title="Lets see how does it work", description="My name is Mr.Robot", color=0x00ff00)
    embed.set_footer(text="this is footer")
    embed.set_author(name="Mr.Robot of ServBots")
    embed.add_field(name="Field", value='value you wanna give', inline=True)
    await bot.say(embed=embed)


#If you want your BOT to be PRIVATE.
#-----------------------------------
    
@bot.command(pass_context=True)
async def private(ctx):
    author = ctx.message.author
    embed= discord.Embed(title="PRIVATE MESSAGE!!", color=0x00ff00)
    embed.add_field(name='Wanna be private??', value='What do you wanna know?', inline=False)
    await bot.send_message(author, embed=embed)
    


#If you want to delete messages in chat queue.
#---------------------------------------------
    
@bot.command(pass_context=True)
async def clear(ctx,amount=100):
    channel= ctx.message.channel
    messages=[]
    async for message in bot.logs_from(channel, limit= int(amount)):
        messages.append(message)
    await bot.delete_messages(messages)
    await bot.say("Messages deleted")


#
@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.server.roles, name='Example Role')
    await bot.add_roles(member, role)


#TO add or remove reaction.
#--------------------------
    
@bot.event
async def on_reaction_add(reaction, user):
    channel=reaction.message.channel
    await bot.send_message(channel,'{} has added {} to the message: {}'.format(user.name, reaction.emoji, reaction.message.content))


@bot.event
async def on_reaction_remove(reaction, user):
    channel=reaction.message.channel
    await bot.send_message(channel,'{} has removed {} to the message: {}'.format(user.name, reaction.emoji, reaction.message.content))




#this chunk of code gives your BOT the ability to play music for you and other members.
#-------------------------------------------------------------------------------------
     #for music your BOT must be into voice channel of your server.
     #-------------------------------------------------------------
    
@bot.command(pass_context=True)    
async def join(ctx):            #this function is used to join your BOT to voice channel.                    
    channel= ctx.message.author.voice.voice_channel   
    await bot.join_voice_channel(channel)


@bot.command(pass_context=True)
async def leave(ctx):           #to exit your BOT from voice channel you need to call this function               
    server= ctx.message.server
    voice_bot= bot.voice_bot_in(server)
    await voice_bot.disconnect()

@bot.command(pass_context=True)
async def play(ctx, url):        # to play music you must call this function, (REMINDER: your BOT should be in voice channel)
        server = ctx.message.server
        voice_client = bot.voice_client_in(server)
        player = voice_client.create_ffmpeg_player('F:\Music\Automatic.mp3', after= lambda: check_queue(server.id))
        players[server.id] = player
        player.start()
        await bot.say('Playing your awesome music!')

@bot.command(pass_context=True)
async def pause(ctx):           # calling this function will PAUSE your music.
    id= ctx.message.server.id
    players[id].pause()

@bot.command(pass_context=True)
async def stop(ctx):           # calling this function will STOP your music.
    id= ctx.message.server.id
    players[id].stop()

@bot.command(pass_context=True)
async def resume(ctx):         # calling this function will RESUME your music.
    id= ctx.message.server.id
    players[id].resume()


#tis will add more songs to the play queue so that your BOT continuously plays music.
#------------------------------------------------------------------------------------
    
@bot.command(pass_context=True)
async def queue(ctx, url):
    server=ctx.message.server
    voice_client=bot.voice_client_in(server)
    player= voice_client.create_ffmpeg_player('F:\Music\Arms.mp3',after= lambda: check_queue(server.id))


# this prepares a leveling system for users just enhancing their experience while typing in particular CHAT channel.
#-------------------------------------------------------------------------------------------------------------------


@bot.event
async def on_member_join(member):   #this opens a JSON file to write the user's experience 
    with open('users.json', 'r') as f:    
        users= json.load(f)

    await update_data(users, member)

    with open('users.json','w') as f:
        json.dump(users,f)
    
@bot.event
async def on_message(message):
    with open('users.json', 'r') as f:
        users= json.load(f)

    await update_data(users, message.author)
    await add_experience(users, message.author, 5)
    await level_up(users, message.author, message.channel)

    with open('users.json','w') as f:
        json.dump(users,f)

async def update_data(users, user):      #this updates the experience of user in the prepared JSON file
    if not user.id in users:
        users[user.id]={}
        users[user.id]['experience']=0
        users[user.id]['level'] = 1

async def add_experience(users, user, exp):   #adds the total experience
    users[user.id]['experience']+= exp


async def level_up(users, user, channel):     #to level up the user when he instantly stats typing  and show the LEVEl when he abrubts writing in a channel/
    experience= users[user.id]['experience']
    lvl_start= users[user.id]['level']
    lvl_end= int(experience **(1/4))

    if lvl_start < lvl_end:
        await client.send_message(channel,'{} has leveled up to level{}'.format(user.mention,lvl_end))
        users[user.id]['level']= lvl_end


bot.add_listener(on_ready)                    #when BOT is ready as well as the user,
bot.add_listener(my_message, 'on_message')     # the experience and the level increases when the user starts typing


bot.loop.create_task(change_status())        # to create a task that will be assigned to your BOT

bot.run("ENTER YOUR BOT's TOKEN for YOUR BOT TO BE ONLINE AND START WORKING WITH YOUR BOT")
