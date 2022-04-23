# bot.py
# Libaries
import os

import discord
from dotenv import load_dotenv
import json
import random
import time

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

# On ready
@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')
    await client.change_presence(activity=discord.Game(name = "rhelp | rstart"))

@client.event
# Ignore self messages
async def on_message(message):
    if message.author == client.user:
        return

    #region HELP
    if message.content.startswith("rhelp"):
        local_embed = discord.Embed(title='Help Menu', description="Liste des commandes disponibles (Version 1.1 du RTCBot)", color=0xffef00)
        local_embed.add_field(name="rstart", value="Ouvre un portefeuille de crypto-monnaie et débute votre aventure de sérial-entrepreneur.", inline=False)
        local_embed.add_field(name="rinv", value="Montre le contenu de votre portefeuille de digital marketeux", inline=False)
        local_embed.add_field(name="rdaily", value="Demande à Elon Musk de vous verser votre part quotidienne de crypto-monnaie", inline=False)
        local_embed.add_field(name="rnet", value="Montre le fameux marché noir de Feldup, où vous pouvez faire l'acquisition de mine(u)rs", inline=False)
        local_embed.add_field(name="rmine", value="Récolte les RTC minés par vos miners", inline=False)
        local_embed.add_field(name="LE BOT EST EN DEV", value="Les commandes sont en constant changement, et de nouvelles sont en rajout", inline=False)
        
        await message.channel.send(embed = local_embed)
    #endregion


    #region START
    if message.content.startswith("rstart") :
        f = open('players.json', 'r+', encoding='utf-8')
        fdata = json.load(f)
        farray = fdata['players']
        was_old = False
        # Finding player in players json array
        for ply in farray:
            if ply[0] == message.author.id :  # author.id
                await message.channel.send('{}'.format(message.author.mention) + ", tu as déjà créé ton portefeuille de digital marketeux !")
                was_old = True
                break
        
        if not was_old:
            await message.channel.send('{}'.format(message.author.mention) + ", ton compte de serial entrepreneur vient d'être mis en ligne pour faire trembler le CAC40 !")
            new_player = [message.author.id, message.author.name, 0, [], "", 0, 0, 0, 0, ""]
            farray.append(new_player)
            f.seek(0)
            json.dump(fdata, f, indent=4)
            f.truncate()
            f.close()
        
        return
    #endregion


    #region Inventory
    if message.content.startswith("rinv"):
        f = open('players.json', 'r+', encoding='utf-8')
        fdata = json.load(f)
        farray = fdata['players']
        local_embed = discord.Embed(title='Inventaire de ' + message.author.name, description="RTCs et NFTs", color=0xffef00)
        located_player = []
        was_old = False
        r1c = 0
        r2c = 0
        r3c = 0
        r4c = 0
        for player_data in farray:
            if message.author.id in player_data:
                located_player = player_data
                was_old = True
            
        if not was_old:
            await message.channel.send('{}'.format(message.author.mention) + ", créez un compte RTC pour faire bouger la blockchain ! --> rstart")
            return

        for i in range (1, len(located_player)):
                if i == 2:
                    local_embed.add_field(name="RatioCoins de " + message.author.name, value = str(located_player[i]) + " RTC <:rtc:967486256109994074>", inline=False)

                if i == 3:
                    for j in range (len(located_player[i])):
                        local_embed.add_field(name = "NFT :", value = located_player[i][j], inline=False)
                
                if i == 5:
                    r1c = located_player[i]
                
                if i == 6:
                    r2c = located_player[i]
                
                if i == 7:
                    r3c = located_player[i]
                
                if i == 8:
                    r4c = located_player[i]

        local_embed.add_field(name="GeForce GTX 1060 : ", value = r1c, inline=False)
        local_embed.add_field(name="GeForce GTX 1080ti :", value = r2c, inline=False)
        local_embed.add_field(name="GeForce RTX 3080ti : ", value = r3c, inline=False)
        local_embed.add_field(name="Rigs de minage : ", value = r4c, inline=False)

        await message.channel.send(embed = local_embed)
        f.close()
    #endregion


    #region Daily
    if message.content.startswith('rdaily'):
        f = open("players.json", "r+", encoding="utf-8")
        fdata2 = json.load(f)
        farray = fdata2['players']
        located_player = []
        index_target = 0
        was_old = False
        # Finding targeted player in players json array
        for i in range (len(farray)):
            if message.author.id in farray[i]:
                located_player = farray[i]
                index_target = i
                was_old = True
        # Player has been located
        if not was_old:
            await message.channel.send('{}'.format(message.author.mention) + ", créez un compte RTC pour faire bouger la blockchain ! --> rstart")
            return
        date = time.asctime(time.localtime())
        current_day = date[0] + date[1] + date [2]
        if located_player[4] != current_day:
            given_coins = random.randrange(5, 20)
            fdata2['players'][index_target][2] += given_coins
            await message.channel.send('{}'.format(message.author.mention) + ", votre bonus quotidien vous donne " + str(given_coins) + "RTC <:rtc:967486256109994074>")
            fdata2['players'][index_target][4] = current_day
        else:
            await message.channel.send('{}'.format(message.author.mention) + ", vous avez déjà réclamé votre bonus quotidien, revenez plus tard grand RIM.")

        f.seek(0)
        json.dump(fdata2, f, indent=4)
        f.truncate()
        f.close()
        return
    #endregion


    #region DarkNet
    if message.content.startswith("rnet"):
        local_embed = discord.Embed(title="DarkNet - Datacenters et miners", description = "Achetez des workers pour miner de la crypto et débuter votre empire financier  <:stonksup:967517993162649621>", color=0xffef00)
        local_embed.add_field(name="GeForce GTX 1060 : 20 RTC", value ="45 RTC/jour : rbuy1", inline=False)
        local_embed.add_field(name="GeForce GTX 1080ti : 35 RTC", value="100 RTC/jour : rbuy2", inline=False)
        local_embed.add_field(name="GeForce RTX 3080ti : 55 RTC", value="130 RTC/jour : rbuy3", inline=False)
        local_embed.add_field(name="Rigs de minage : 200 RTC", value = "510 RTC/jour : rbuy4", inline=False)
        local_embed.set_thumbnail(url="https://s3.us-east-2.amazonaws.com/nomics-api/static/images/currencies/STONK5.png")
        await message.channel.send(embed = local_embed)
    #endregion


    #region rbuy1
    if message.content.startswith("rbuy1"):
        f = open("players.json", "r+", encoding="utf-8")
        fdata = json.load(f)
        farray = fdata['players']
        located_player = []
        index_target = 0
        was_old = False
        # Finding targeted player in players json array
        for i in range (len(farray)):
            if message.author.id in farray[i]:
                located_player = farray[i]
                index_target = i
                was_old = True
        # Player has been located
        if not was_old:
            await message.channel.send('{}'.format(message.author.mention) + ", créez un compte RTC pour faire bouger la blockchain ! --> rstart")
            return
        
        if located_player[2] < 20:
            await message.channel.send('{}'.format(message.author.mention) + ", vous n'avez pas assez d'argent, demandez à ceux qui aident les gens dans le besoin.")
            return
        
        fdata['players'][index_target][2] -= 20
        fdata['players'][index_target][5] += 1

        f.seek(0)
        json.dump(fdata, f, indent=4)
        f.truncate()
        f.close()

        await message.channel.send('{}'.format(message.author.mention) + ", vous avez acheté une GeForce GTX 1060 !")
        return

    #endregion

    
    #region rbuy2
    if message.content.startswith('rbuy2'):
        f = open("players.json", "r+", encoding="utf-8")
        fdata = json.load(f)
        farray = fdata['players']
        located_player = []
        index_target = 0
        was_old = False
        # Finding targeted player in players json array
        for i in range (len(farray)):
            if message.author.id in farray[i]:
                located_player = farray[i]
                index_target = i
                was_old = True
        # Player has been located
        if not was_old:
            await message.channel.send('{}'.format(message.author.mention) + ", créez un compte RTC pour faire bouger la blockchain ! --> rstart")
            return
        
        if located_player[2] < 35:
            await message.channel.send('{}'.format(message.author.mention) + ", vous n'avez pas assez d'argent, demandez à ceux qui aident les gens dans le besoin.")
            return
        
        fdata['players'][index_target][2] -= 35
        fdata['players'][index_target][6] += 1

        f.seek(0)
        json.dump(fdata, f, indent=4)
        f.truncate()
        f.close()

        await message.channel.send('{}'.format(message.author.mention) + ", vous avez acheté une GeForce GTX 1080ti !")
        return
    #endregion


    #region rbuy3
    if message.content.startswith('rbuy3'):
        f = open("players.json", "r+", encoding="utf-8")
        fdata = json.load(f)
        farray = fdata['players']
        located_player = []
        index_target = 0
        was_old = False
        # Finding targeted player in players json array
        for i in range (len(farray)):
            if message.author.id in farray[i]:
                located_player = farray[i]
                index_target = i
                was_old = True
        # Player has been located
        if not was_old:
            await message.channel.send('{}'.format(message.author.mention) + ", créez un compte RTC pour faire bouger la blockchain ! --> rstart")
            return
        
        if located_player[2] < 55:
            await message.channel.send('{}'.format(message.author.mention) + ", vous n'avez pas assez d'argent, demandez à ceux qui aident les gens dans le besoin.")
            return
        
        fdata['players'][index_target][2] -= 55
        fdata['players'][index_target][7] += 1

        f.seek(0)
        json.dump(fdata, f, indent=4)
        f.truncate()
        f.close()

        await message.channel.send('{}'.format(message.author.mention) + ", vous avez acheté une GeForce RTX 3080ti !")
        return
    #endregion

    
    #region rbuy4
    if message.content.startswith('rbuy4'):
        f = open("players.json", "r+", encoding="utf-8")
        fdata = json.load(f)
        farray = fdata['players']
        located_player = []
        index_target = 0
        was_old = False
        # Finding targeted player in players json array
        for i in range (len(farray)):
            if message.author.id in farray[i]:
                located_player = farray[i]
                index_target = i
                was_old = True
        # Player has been located
        if not was_old:
            await message.channel.send('{}'.format(message.author.mention) + ", créez un compte RTC pour faire bouger la blockchain ! --> rstart")
            return
        
        if located_player[2] < 200:
            await message.channel.send('{}'.format(message.author.mention) + ", vous n'avez pas assez d'argent, demandez à ceux qui aident les gens dans le besoin.")
            return
        
        fdata['players'][index_target][2] -= 200
        fdata['players'][index_target][8] += 1

        f.seek(0)
        json.dump(fdata, f, indent=4)
        f.truncate()
        f.close()

        await message.channel.send('{}'.format(message.author.mention) + ", vous avez acheté un rigs de minage !")
        return
    #endregion


    #region Mining Command
    if message.content.startswith('rmine'):
        f = open("players.json", "r+", encoding="utf-8")
        fdata = json.load(f)
        farray = fdata['players']
        located_player = []
        index_target = 0
        was_old = False
        # Finding targeted player in players json array
        for i in range (len(farray)):
            if message.author.id in farray[i]:
                located_player = farray[i]
                index_target = i
                was_old = True
        # Player has been located
        if not was_old:
            await message.channel.send('{}'.format(message.author.mention) + ", créez un compte RTC pour faire bouger la blockchain ! --> rstart")
            return
        
        if located_player[5] + located_player[6] + located_player[7] + located_player[8] == 0:
            await message.channel.send('{}'.format(message.author.mention) + ", vous n'avez aucun miner ! Minage abandonné...")
            return

        date = time.asctime(time.localtime())
        current_day = date[0] + date[1] + date [2]
        if located_player[9] != current_day:
            given_coins = located_player[5] * 45 + located_player[6] * 100 + located_player[7] * 130 + located_player[8] * 510
            fdata['players'][index_target][2] += given_coins
            await message.channel.send('{}'.format(message.author.mention) + ", votre minage vous fais gagner " + str(given_coins) + "RTC <:rtc:967486256109994074>")
            fdata['players'][index_target][9] = current_day
        else:
            await message.channel.send('{}'.format(message.author.mention) + ", vous avez vidé vos miners, attendez jusqu'à demain que ceux-ci finisse de miner ! ")

        f.seek(0)
        json.dump(fdata, f, indent=4)
        f.truncate()
        f.close()
        return
    #endregion


client.run(TOKEN)