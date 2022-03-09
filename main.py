import discord
from python_aternos import Client
from discord.ext import commands
from discord import File
from discord.utils import get
import asyncio
import youtube_dl
import os
import datetime
from datetime import date
import random
import re
import time
import socket

### Le lien pour inviter le bot sur un serveur : https://discord.com/api/oauth2/authorize?client_id=793960522252156938&permissions=0&scope=bot


bot_prefix = '!'
client = commands.Bot(command_prefix=bot_prefix)


TOKEN = 'your token goes in here'

###Partie du code traitant des classes de jeu de rôle###

class player:
    def __init__(self,health,speed,agility,strenght,gold):
        self.health = health
        self.speed = speed
        self.agility = agility
        self.strenght = strenght
        self.balance = gold
        self.inventory = []
        #Les différentes stats du joueur, y compris l'inventaire et l'argent.



        #Fonction qui va ajouter un objet à l'inventaire du joueur
        def additem(self,item):
            self.inventory.append(item)
            print(f"Added {item} to {player}'s inventory.")


        #Fonction qui va retirer un objet de l'inventaire du joueur
        def removeitem(self,item):
            if item in self.inventory:
                self.inventory.remove(item)
                print(f"Removed {item} from {player}'s inventory.")
                #On retire l'objet de l'inventaire du joueur
            else:
                print(f"Unable to remove {item} from {player}'s inventory because it wasn't there.")
                #Au cas où l'objet n'existe pas dans l'inventaire du joueur, on le précise


        #Fonction qui interagit avec l'argent du joueur (retrait ou ajout)
        def amount(self,cash):
            self.balance = self.balance + cash
            #Après avoir modifié le compte en banque du joueur, on regarde si il/elle est dans le négatif ou pas
            if self.balance < cash:
                print(f"{player} is in debt of {self.balance}")
            else:
                print(f"{player} now has {self.balance}$")


        #Fonction qui vérifie si le joueur peut effectuer telle action
        def stat_check(self,target_stat,stat_level):
            if self.target_stat >= stat_level:
                #Si la compétence du joueur est assez élevée
                print(f"{player} won the stat check of {target_stat}.")
                #On renvoie un résultat positif (True)
                return True
            elif self.target_stat < stat_level:
                #Si la compétence du joueur n'est pas assez élevée
                print(f"{player} lost the stat check of {target_stat}")
                #On renvoie un résultat négatif (False)
                return False


        #Fonction qui va intéragir avec la vie du joueur (retirer ou ajouter des PV)
        def player_health(self,hp):
            self.health = self.health + hp
            if hp > 0:
                print(f"{player} was healed for {hp}")
                #Si la valeur 'hp' est positive, le joueur est soigné
            elif hp < 0:
                print(f"{player} took {hp} of damage")
                #Si la valeur 'hp' est négative, le joueur reçoit des dégâts


        #Fonction simple permettant d'avoir les stats du joueur facilement
        def show_player_data(self):
            player_data = (f"|{self.health}|{self.speed}|{self.agility}|{self.strenght}|{self.balance}|{self.inventory}|")
            return player_data



#Pour comprendre les commandes suivantes, jetez un coup d'oeuil à la classe 'player'
@client.command()
async def new_player(ctx,name,new_health,new_speed,new_agility,new_strenght,new_balance):
    name = player(new_health,new_speed,new_agility,new_strenght,new_balance)
    await ctx.send(f"Nouvelle feuille de joueur créée, ")

@client.command()
async def data(ctx,target_player):
    target_player_data = str(target_player.show_player_data())
    print(target_player_data)
    #await ctx.send(f"Voilà les infos du joueur {target_player} : {target_player.show_player_data()}")

@client.command()
async def inv(ctx,target_player,inv_action,target_item):
    inv_action = str(inv_action)
    if inv_action == 'add':
        target_player.additem(target_item)
        await ctx.send(f"Le joueur {target_player} a reçu l'objet {target_item} !")
    if inv_action == 'remove':
        target_player.removeitem(target_item)
        await ctx.send(f"L'objet {target_item} a été retiré au joueur {player}.")
    
@client.command()
async def balance(ctx,target_player,target_amount):
    target_player.amount(target_amount)
    if target_amount < 0:
        await ctx.send(f"Le joueur {target_player} a perdu {target_amount}$")
    if target_amount > 0:
        await ctx.send(f"Le joueur {target_player} a gagné {target_amount}$")
    if target_amount == 0:
        await ctx.send(f"Zéro n'est pas une valeur correcte pour ce genre d'action sur le joueur {target_player}.")

@client.command()
async def check_stats(ctx,target_player,check_stat,check_level):
    target_player.stat_check(check_stat,check_level)

@client.command()
async def health_action(ctx,target_player,amount):
    #Une valeur positive inflige des dégâts, tandis qu'une valeur négative soigne le joueur ciblé.
    if amount > 0:
        await ctx.send(f"Le joueur {target_player} a été soigné de {amount}HP")
    elif amount < 0:
        await ctx.send(f"Le joueur {target_player} a reçu {amount}HP de dégâts")

#Une commande expliquant les différentes commandes du système de roleplay
@client.command()
async def RPmenu(ctx):
    await ctx.send(f"Voici les différentes commandes à utiliser pour gérer une session de jeu :\n >>> new_player : crée un nouveau personnage, qui comprend les caractéristiques suivantes : \n le nom, les PVs, la vitesse, l'agilité, la force et l'argent du personnage. \n Les commandes suivantes prennent comme argument principal le nom du joueur cilbé.")
    await ctx.send(f" ->data : prend comme argument le nom du joueur. La commande va renvoyer les différentes statistiques du joueur.")
    await ctx.send(f" ->inv : prend comme arguments le joueur ciblé, l'action à effectuer (ajouter/retirer) et l'objet en question. Va retirer/ajouter un objet à l'inventaire du joueur")
    await ctx.send(f" ->balance : prend comme arguments le joueur ciblé, l'action bancaire à effectuer, et le montant de l'action. Va retirer/ajouter un montant d'argent.")
    await ctx.send(f" ->check_stat : prend comme argument le nom du joueur, la stat du joueur à vérifier et le niveau de la statistique à vérifier.")
    await ctx.send(f" ->health_action : prend comme argument le nom du joueur, et la quantité de HPs mise en jeu. Une valeur négative va faire des dégâts, tandis qu'une valeur positive va soigner.")

#Les commandes suivantes sont plus des 'gadgets' qui facilitent la vie.
@client.command()
async def Roll(ctx,faces:int):
    await ctx.send(f"Dé à {faces} faces >>> {random.randint(1,faces)}")
    #On lance un dé qui a un nombre de faces variable.

###Fin de la partie sur les classes de jeu de rôle###

#Token_file = 'token.txt'
#with open(Token_file, mode='r') as TokenSTR:
#    TOKEN = TokenSTR.read()
print(TOKEN)

date = date.today()
date = str(date)


log_name = f'{date}_logs.txt'
f =  open( log_name , 'w' )
f.write(f"Bot started at {datetime.datetime.now}.")

blacklisted = []

def pics_lookup():
    hostname = socket.gethostname()
    hostname1 = socket.gethostbyname(hostname)
    print(f"{hostname} <> {hostname1}")
    if hostname == 'Ultraportable-Lou':
        return
    pathway = r'C:\Users\Lou\Desktop\Python_Bot'
    pathway = pathway
    pic_amount = 0
    pics = []
    path = r'C:\Users\Lou\Desktop\Python_Bot'
    files = os.listdir(path)
    for f in files:
        if f.endswith(".png"):
            pics.append(f)
            pic_amount += 1
    print(f"Current image files in folder {path} : >>> {pics}")
#pics_lookup()

@client.command()
async def test(ctx):
    print(f"{ctx.message.author} ping'd the bot at {datetime.datetime.now()}")
    await ctx.send("Test")
    f.write(f">>> {ctx.message.author} ping'd the bot at {datetime.datetime.now()} \n")
    print("TEST")

@client.command()
async def play(ctx, url : str, canal):
    print(f"{ctx.message.author} requested {url} in channel {canal} at {datetime.datetime.now()}")
    f.write(f">>>{ctx.message.author} requested {url} in channel {canal} at {datetime.datetime.now} \n")
    if 'pornhub' in ctx.message.content:
        await ctx.send("Louis ! Pas de porno sur le bot !")
        return
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Attends que la musique se finisse ou utilise la commande 'stop'")
        return
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    await ctx.send("Je télécharge la musique, ça peut prendre du temps")
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir('./'):
        if file.endswith('mp3'):
            os.rename(file,'song.mp3')
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name=canal)
    await voiceChannel.connect()
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)    
    voice.play(discord.FFmpegPCMAudio("song.mp3"))
    

@client.command()
async def leave(ctx):
    print(f"{ctx.message.author} asked the bot to leave at {datetime.datetime.now()}")
    f.write(f">>>{ctx.message.author} asked the bot to leave at {datetime.datetime.now()}\n")
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("Le bot n'est pas en train de jouer de la musique")

@client.command()
async def pause(ctx):
    print(f"{ctx.message.author} asked the bot to pause the music at {datetime.datetime.now()}")
    f.write(f">>>{ctx.message.author} asked the bot to pause the music at {datetime.datetime.now()}\n")
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Il n'y a pas de musique en cours")

@client.command()
async def resume(ctx):
    print(f"{ctx.message.author} asked the bot to resume the music at {datetime.datetime.now()}")
    f.write(f">>>{ctx.message.author} asked the bot to resume the music at {datetime.datetime.now()}\n")
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        ctx.send("La musique n'est pas pausée")

@client.command()
async def stop(ctx):
    print(f"{ctx.message.author} asked the bot to stop the music at {datetime.datetime.now()}")
    f.write(f">>>{ctx.message.author} asked the bot to stop the music at {datetime.datetime.now()}\n")
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()

@client.command()
async def clock(ctx):
    print(f"{ctx.message.author} asked the bot for the time at {datetime.datetime.now()}")
    f.write(f">>>{ctx.message.author} asked the bot for the time at {datetime.datetime.now()}\n")
    time = datetime.datetime.now().replace(microsecond=0).isoformat()
    await ctx.send("Date et heure : {}".format(time))

@client.command()
async def coin(ctx):
    flip_coin = random.randint(0,1)
    if flip_coin == 1:
        print(f"{ctx.message.author} asked the bot to flip a coin at {datetime.datetime.now()}. It landed on tails")
        f.write(f">>>{ctx.message.author} asked the bot to flip a coin at {datetime.datetime.now()}. It landed on tails\n")
        await ctx.send("Pile !")
    elif flip_coin == 0:
        print(f"{ctx.message.author} asked the bot to flip a coin at {datetime.datetime.now()}. It landed on heads")
        f.write(f">>>{ctx.message.author} asked the bot to flip a coin at {datetime.datetime.now()}. It landed on heads\n")
        await ctx.send("Face !")

@client.command()
async def jukebox(ctx):
    print(f"{ctx.message.author} read the instructions for the Jukebox at {datetime.datetime.now()}")
    f.write(f">>>{ctx.message.author} read the instructions for the Jukebox at {datetime.datetime.now()}\n")
    await ctx.send("Voici les différentes commandes pour la musique, à utiliser avec le préfixe {} : \n >>>  >>> play : on donne une URL de vidéo youtube et le nom d'un canal vocal, et le bot jouera de la musique. \n >>> leave : fait sortir le bot du canal vocal où il se trouve. \n >>> pause : met la musique en pause. \n >>> resume : reprend la musique en cours. \n >>> stop : arrête de jouer de la musique.".format(bot_prefix))

@client.command()
async def menu(ctx):
    print(f"{ctx.message.author} read the instructions for the bot at {datetime.datetime.now()}")
    f.write(f">>>{ctx.message.author} read the instructions for the bot at {datetime.datetime.now()}\n")
    await ctx.send(f"Voici les différentes commandes, à utiliser avec le préfixe de commande {bot_prefix} : \n >>>  >>> menu : montre ce message. \n >>> time : donne l'heure. \n >>> coin : fait un pile ou face. \n >>> jukebox : montre les commandes du Jukebox. \n >>> math : permet de faire des calculs mathématiques (il faut que tous les caractères soient attachés) \n >>> ping : va simplement 'pinger' l'utilisateur désigné. \n >>> invite : permet d'inviter un autre utilisateur (donner l'identifiant correctement). Peut être accompagné d'un message supplémentaire (mettre un '/' pour ne pas ajouter de message) \n >>> shodId : Permet de voir les infos Discord d'une personne. \n mute et unmute >>> permet de rendre mute/révoquer le mutisme d'un utilisateur. Admin uniquement. \n >>> secret : vous donne le lien pour inviter le bot à votre serveur. Requiert un code. \n >>> sendLink : envoie le lien du bot à un utilisateur, comme la commande 'secret'. Requiert aussi un code \n >>> activity : change l'activité du bot.")

@client.command()
async def embed(ctx,message_title:str,message:str):
    embed = discord.Embed(title=message_title, description=message) #,color=Hex code
    #embed.add_field(name="Name", value="you can make as much as fields you like to")
    await ctx.message.delete()
    await ctx.send(embed=embed)

@client.command()
async def math(ctx,compute:str):
    await ctx.send("Brr, je calcule -")
    global previous
    equation = compute
    previous = eval(equation)
    result = round(previous,3)
    await ctx.send(f"Voici le résultat : {result} !")
    f.write(f">>>{ctx.message.author} asked the bot to compute {compute} at {datetime.datetime.now()}\n")
    print(f"At {datetime.datetime.now()}, user {ctx.message.author} asked the bot to calculate {compute}")

@client.command()
async def ping(ctx,user:discord.Member):
    back_ping = '{}'.format(user.mention)
    await ctx.message.delete()
    await ctx.send(back_ping)

@client.command(description="On rend l'utilisateur muet, avec raison bien sûr")
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
    embed = discord.Embed(title="Mute", description=f"{member.mention} va être... plus silencieux à l'avenir ", colour=discord.Colour.light_gray())
    embed.add_field(name="reason:", value=reason, inline=False)
    await ctx.send(embed=embed)
    await member.add_roles(mutedRole, reason=reason)
    await member.send(f" Bon bah chut {guild.name} parce que {reason}")
    print(f"{ctx.message.author} muted {member} at {datetime.datetime.now} for the following reason : {reason}")
    f.write(f">>>{ctx.message.author} muted {member} at {datetime.datetime.now()} for the following reason : {reason}\n")

@client.command(description="Unmutes a specified user.")
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
    mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

    await member.remove_roles(mutedRole)
    await member.send(f" Maintenant, tu peux parler !: - {ctx.guild.name}")
    embed = discord.Embed(title="Unmute", description=f" Tu as retrouvé ta voix, -{member.mention}",colour=discord.Colour.light_gray())
    await ctx.send(embed=embed)
    print(f"{ctx.message.author} unmuted {member} at {datetime.datetime.now()}")

@client.command()
async def secret(ctx, code:str):
    await ctx.message.delete()
    if code == 'ErisIsGoodBot69':
        await ctx.message.author.send("Voici le lien pour inviter le bot sur ton propre serveur. Attention : Lou reste le dev du bot, et le bot est, par extension, sa propriété, donc, si des gens sur votre serveur l'utilisent mal, ils seront blacklistés. Vous, je vous fait confiance. \n le lien : >>> |https://discord.com/api/oauth2/authorize?client_id=793960522252156938&permissions=0&scope=bot|")
        print("At ",datetime.datetime.now(),", user ",ctx.message.author," accessed the inviting link, and gave the right code.")
        f.write(f">>>{ctx.message.author} accessed the invite link at {datetime.datetime.now()}\n")
    elif code != 'ErisIsGoodBot69':
        await ctx.send("Hey, c'est pas le bon code !")
        print("At ",datetime.datetime.now(),", user ",ctx.message.author," tried to access the inviting link, but gave the wrong code.")
        f.write(f">>>{ctx.message.author} requested the invite link but gave the wrong code at {datetime.datetime.now()}\n")

@client.command()
async def showId(ctx,member:str):
    await ctx.send("Ton ID est {}".format(ctx.message.author.id))
    await ctx.send("Ton nom est {}".format(ctx.message.author.mention))
    print(f"{ctx.message.author} asked the bot for {member}'s ID at {datetime.datetime.now()}")

@client.command()
@commands.is_owner()
async def blacklist(ctx,member:discord.Member,reason,code:str):
    if code == 'blacklist24':
        if member == "@Shadow_Lou#1847":
            print(f"{datetime.datetime.now()}, {ctx.message.author}, tried to blacklist you")
            ctx.send(f"Bien essayé, mais non. C'était prévu que quelqu'un essaie d'utiliser cette commande à mauvais escient. Mais non. Maintentant, utilise le bot |correctement|, sinon ça va mal se passer, {ctx.message.author}")
            return
        blacklist_message_list = ("L'utilisateur ",member," a été blacklisté (embargo total de l'utilisation du bot) pour la raison suivante : ",reason)
        blacklist_message = str(blacklist_message_list)
        await ctx.send(blacklist_message)
        blacklist_addon = member
        blacklisted.append(blacklist_addon)
        print(f"At {datetime.datetime.now()}, user {member} was blacklisted by {ctx.message.author} for the following reason : {reason}")
        f.write(f">>>{ctx.message.author} blacklisted {member} for the following reason : {reason} at {datetime.datetime.now()}\n")

@client.command()
async def sendLink(ctx,code:str,member:discord.Member):
    await ctx.message.delete()
    if code == 'ErisIsGoodBot69':
        await member.send("Voici le lien pour inviter le bot sur ton propre serveur. Attention : Lou reste le dev du bot, et le bot est, par extension, sa propriété, donc, si des gens sur votre serveur l'utilisent mal, ils seront blacklistés. Vous, je vous fait confiance. \n le lien : >>> |https://discord.com/api/oauth2/authorize?client_id=793960522252156938&permissions=0&scope=bot|")
        print(f"At {datetime.datetime.now()}, user {ctx.message.author} send the invite link to {member}")
    else:
        await ctx.send("C'est pas le bon code, alors je sais pas qui t'essaie de faire profiter, mais non.")
        print(f"At {datetime.datetime.now()}, user {ctx.message.author} tried to send the invite link to {member}, but entered the wrong code.")

@client.command()
async def invite(ctx,member:discord.Member,reason:str):
    await ctx.send(f"J'envoie le lien à {member}")
    await member.send("Hello, je suis Eris, bot du discord de Lou. Voici le lien pour rejoindre le serveur : \n >>> |║| https://discord.gg/4cqg4wrWh7 [] À vous de rejoindre ! [] |║|")
    f.write(f">>>{ctx.message.author} sent the invite link to {member} at {datetime.datetime.now()} with the additionnal message : {reason}\n")
    if reason != '/':
        await member.send(f"Petit message en plus : {reason}")
    else:
        return

@client.command()
async def memberShow(ctx,member:discord.Member):
    await ctx.send(f"Tu est {member}")

@client.event
async def on_new_member(member):
    print(f"At {datetime.datetime.now()}, new user {member} joined the server")
    welcome_message = (f"Hello, {member}, bienvenue sur le serveur ! \n Je suis Eris, un bot polyvalent, qui est là pour t'aider :)\n Si tu souhaites en savoir plus sur mes fonctionnalités, tape {bot_prefix}menu. \n J'espère que tu appréciera ce serveur !")
    await member.send(welcome_message)
    channel = client.get_channel("général")
    await channel.send(welcome_message) 

@client.command()
async def portfolio(ctx):
    directory = r"C:\Users\louma\Desktop\Python_Bot\images"
    file_name = random.choice(os.listdir(directory))
    print(f"At {datetime.datetime.now()}, user {ctx.message.author} asked a random image.")
    with open(f'{directory}\\{file_name}', 'rb') as f:
        await ctx.send(file=File(f, 'new_filename.png'))

@client.command()
async def reactions(ctx,reaction,user):
    message = await ctx.send("Test")
    emoji = '\N{THUMBS UP SIGN}'
    await message.add_reaction(emoji)

@client.command()
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send(f"Eris se déconnecte. Sayonara !")
    print(f"At {datetime.datetime.now()}, user {ctx.message.author} asked the bot to log out.")
    f.write(f">>>{ctx.message.author} asked the bot to logout at {datetime.datetime.now()}\n")
    await exit()

@client.command()
async def raffle(ctx,*choices:str):
    await ctx.send(f"Voilà l'option choisie au hasard : {random.choice(choices)}")
    print(f"At {datetime.datetime.now()}, user {ctx.message.author} asked the bot to pick a random choices from these : {choices}")
    f.write(f">>>{ctx.message.author} asked the bot to do a raffle with all of the choices : {choices} at {datetime.datetime.now()}\n")

@client.command()
async def file_download(ctx,file:str):
    await ctx.send(f"Voici l'archive ZIP relative au programme {file}")
    if file == "camera":
        await ctx.send(file=discord.File(r"C:\Users\Lou\Desktop\Camera_system\Python_security_camera\Security_camera_UNZIP_ME.7z"))
        print(f"{ctx.message.author} downloaded the file {file} ")
    if file == "":
        await ctx.message.send("Veuillez entrer un nom de projet valide.")
    if file == "character_sheet_exe":
        await ctx.send(file=discord.File(r"C:\Users\Lou\Desktop\Envoi_de_fichiers\broadcast\character_sheet_maker_exe.zip"))
        print(f"{ctx.message.author} downloaded the file {file} ")
    if file == "character_sheet":
        await ctx.send(file=discord.File(r"C:\Users\Lou\Desktop\Envoi_de_fichiers\broadcast\character_sheet_maker.zip"))
        print(f"{ctx.message.author} downloaded the file {file} ")

@client.command()
async def file_list(ctx):
    await ctx.send("Voici la liste des programmes actuellement disponibles : \n []Caméra : tourne sur un ordinateur avec une webcam et va vous envoyer un message en cas d'intrusion. Nom : 'camera' \n [] Créateur de fiche de personnage : permet de créer une fiche de personnage pour un jeu de rôle. Noms : character_sheet_exe > version .exe (exécutable) | character_sheet > version .py (programme python, nécessite python 3.x)")

@client.command()
@commands.is_owner()
async def echo(ctx,say:str):
    if say != "":
        await ctx.message.delete()
        await ctx.send(say)

class Server():
    """A class to interact with my minecraft server,\n
    hosted on ```aternos.org```. There are currently two available\n
    functions : """
    def __init__(self):
        self.aternos = Client("TheDarkWolfer","Aternosconfig")
        self.atservers = self.aternos.servers
        self.myserv = self.atservers[0]
        self.state = False
    def toggle(self):
        """Turns on/off the server (here ```LastLife```) swiftly."""
        if self.state == False:
            self.myserv.start()
            self.state = True
        elif self.state == True:
            self.myserv.stop()
            self.state = False
    def check(self):
        """Checks wether the server is currently on or off. Based on a 
        True/False statement, it'll return ```en ligne``` if the server is online, and ```hors-ligne``` if not."""
        if self.state == True:
            return ("en ligne")
        else :
            return ("hors-ligne")

#Lastlife = Server()

@client.command()
async def aternos(ctx):#,arg:str
    await ctx.send(f"- Command not yet implemented -")
    return
    if arg == "ip":
        await ctx.send(f"Voilà l'IP, {ctx.message.author} ! -|ip|-")
    elif arg == "toggle":
        Lastlife.toggle()
    elif arg == "state":
        await ctx.send(f"Le serveur est {Lastlife.check()}")

@client.event
async def on_ready():
    activity = discord.Game(name=f"Fait son baroud d'honneur",type=1)
    await client.change_presence(status=discord.Status.online,activity=activity)
    print(f"Current command prefix > {bot_prefix}")
    print(f"Voici les différentes commandes, à utiliser avec le préfixe de commande {bot_prefix} : \n >>>  >>> menu : montre ce message. \n >>> time : donne l'heure. \n >>> coin : fait un pile ou face. \n >>> jukebox : montre les commandes du Jukebox. \n >>> math : permet de faire des calculs mathématiques (il faut que tous les caractères soient attachés) \n >>> ping : va simplement 'pinger' l'utilisateur désigné. \n >>> invite : permet d'inviter un autre utilisateur (donner l'identifiant correctement). Peut être accompagné d'un message supplémentaire (mettre un '/' pour ne pas ajouter de message) \n >>> shodId : Permet de voir les infos Discord d'une personne. \n mute et unmute >>> permet de rendre mute/révoquer le mutisme d'un utilisateur. Admin uniquement. \n >>> secret : vous donne le lien pour inviter le bot à votre serveur. Requiert un code. \n >>> sendLink : envoie le lien du bot à un utilisateur, comme la commande 'secret'. Requiert aussi un code \n >>> activity : change l'activité du bot.")
    print(f"\nEris logged in at {(datetime.datetime.now().replace(microsecond=0).isoformat())}")
    f.write(f">>>Eris logged in at {datetime.datetime.now()}\n")

try:
    client.run(TOKEN)
except ConnectionError:
    print("Error : can't connect to the servers. Try restarting your router, checking your network connection or pray ")
