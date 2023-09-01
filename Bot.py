import requests
import json
import os
import discord
import asyncio
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()




bot = commands.Bot(command_prefix="-", intents=discord.Intents.all()) #declare the bot variable used for discord.py


importpeopleids = [1058768145722134528] #DONT EDIT UNLESS YOU KNOW WHAT YOUR DOING

#check if the user declaring the command is one of the people in the importpeopleids array
def botowners(ctx):
    return ctx.author.id in importpeopleids

#get this stuff form the .env file
apikey = os.getenv('apikey')
token = os.getenv('token')
idlist = os.getenv('idlist')
bottoken = os.getenv('bottoken')
webhook = os.getenv('webhook')




#wait for when the bot is ready
@bot.listen('on_ready')
async def on_ready():

    print(f'bot online- {bot.user} - {bot.user.id}')
    for s in bot.guilds:
      print(f'{s} - {s.id}') #print each guild and the guild id of the bot it is in
      

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


#send a discord webhook to the webhook used in the .env file with the message parsed in
def sendlog(msg):
    json = {
        "content": msg,
        "embeds": None,
        "attachments": []
    }
    requests.post(webhook, json=json)





#gets the username from an api
def getusername(userid):
  r = requests.get(f'https://api.newstargeted.com/roblox/users/v2/user.php?userId={userid}')
  response = r.json()
  plrusername = response["username"]
  print(plrusername)


#gets the userid from username from an api
def getuserid(username):
    r = requests.get(f'https://api.newstargeted.com/roblox/users/v2/user.php?username={username}')
    response = r.json()
    plruserid = response['userId']



@bot.command()
#@commands.has_role()
async def ban(ctx, user,*, reason=None): #if the reason is not specified do this so it doesnt error out
    if user.isnumeric(): #check if the user argument is a number
      opuser = getusername(user) #if so then get their username
      print('User id')
      jbziscool = 'd' #i forgor what this varibale was for
    else: #if its not (i know i should use elif statements incase of errors yea yea i know) then get the userid
        user = getuserid(user)

    url = "https://api.trello.com/1/cards"

    headers = {
      "Accept": "application/json" #declare the type as application/json
    }

    query = { #this will be the query that is send in the request
      'idList': idlist,
      'key': apikey,
      'token': token
    }

    responsee = requests.request(
      "POST", #post rquest
      url, # to the url
      headers=headers, #with these headers
      params=query
    )

    a = responsee.json() #get the https or http response as a json
    this = a['shortLink'] # get "shortlink" from the json response


    url = f"https://api.trello.com/1/cards/{this}" #get the shortlink thing (sorry i am so tired rn)
    query = {'key': apikey, 'token': token}
    payload = {'name': user}
    response = requests.request("PUT", url, params=query, data=payload) # send a put request

    try:
      plrusernamefunc = getusername(user)
      await ctx.send(f'```\nBANNED ({ctx.author}): {plrusernamefunc} unban key: {this}```')
    except:
      await ctx.send(f'\nBANNED ({ctx.author}): {user} - use key `{this}` to unban')

    sendlog(f'Banned id: `{user}` with key `{this}`')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Exploiters get banned - jbziscool"))
    await ctx.message.add_reaction('\N{WHITE HEAVY CHECK MARK}') #react with checkmakr





@bot.command()
#@commands.has_role(1061432140333596683)
async def unban(ctx, trelloident,*, reason=None):

  url = f"https://api.trello.com/1/cards/{trelloident}"

  query = {
    'key': apikey,
    'token': token
  }

  response = requests.request(
    "DELETE",
    url,
    params=query
  )
  await ctx.message.add_reaction('\N{WHITE HEAVY CHECK MARK}')



#this is a command to execute python code with a command
@bot.command(aliases=['e', 'evaluate'])
@commands.check(botowners)
async def eval(ctx, *, code):
    """Evaluates customized code"""
    language_specifiers = ["python", "py", "javascript", "js", "html", "css", "php", "md", "markdown", "go", "golang", "c", "c++", "cpp", "c#", "cs", "csharp", "java", "ruby", "rb", "coffee-script", "coffeescript", "coffee", "bash", "shell", "sh", "json", "http", "pascal", "perl", "rust", "sql", "swift", "vim", "xml", "yaml"]
    loops = 0
    while code.startswith("`"):
        code = "".join(list(code)[1:])
        loops += 1
        if loops == 3:
            loops = 0
            break
    for language_specifier in language_specifiers:
        if code.startswith(language_specifier):
            code = code.lstrip(language_specifier)
    try:
        while code.endswith("`"):
            code = "".join(list(code)[0:-1])
            loops += 1
            if loops == 3:
                break
        code = "\n".join(f"    {i}" for i in code.splitlines())
        code = f"async def eval_expr():\n{code}"
        def send(text):
            bot.loop.create_task(ctx.send(text))
        env = {
            "bot": bot,
            "client": bot,
            "ctx": ctx,
            "print": send,
            "_author": ctx.author,
            "_message": ctx.message,
            "_channel": ctx.channel,
            "_guild": ctx.guild,
            "_me": ctx.me
        }
        env.update(globals())
        exec(code, env)
        eval_expr = env["eval_expr"]
        result = await eval_expr()
        await ctx.message.add_reaction("\N{WHITE HEAVY CHECK MARK}")
        if result:
            await ctx.send(result)
    except Exception as learntofuckingcode:
        await ctx.message.add_reaction("\N{WARNING SIGN}")
        await ctx.send(f'**Error**```py\n{learntofuckingcode}```')



bot.run(bottoken) #start the bot
