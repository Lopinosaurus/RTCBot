# bot.py
# region Library
import os

import shutil
from PIL import Image
import discord
from discord.ext import tasks
from dotenv import load_dotenv
import json
import random
import time
#endregion

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()



# region Events and Loop Async Functions
@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')
    await client.change_presence(activity=discord.Game(name = "rhelp | rstart"))
    task_loop.start()


@tasks.loop(seconds=60)
async def task_loop(seconds=60):
    _time = time.asctime(time.localtime())
    _channel = client.get_channel(967395369296203786)

    #Checking new day at midnight
    if str(_time[11]) +  str(_time[12]) + str(_time[14]) + str(_time[15]) == "2354":
        # Avoiding recursive issues
        marketdb = open("market.json", "r+", encoding="utf-8")
        mdata = json.load(marketdb)
        marray = mdata["market"]
        # Taking random NFT in dir/
        nfn1 = random.randrange(len(marray) - 1)
        nfn2 = random.randrange(len(marray) - 1)
        nfn3 = random.randrange(len(marray) - 1)
        

        while nfn2 == nfn3 or nfn2 == nfn1 or nfn3 == nfn1 :
            nfn2 = random.randrange(len(marray) - 1)
            nfn3 = random.randrange(len(marray) - 1)

        # Setting the random NFT
        nft1 = "nft/" + marray[nfn1]
        nft2 = "nft/" + marray[nfn2]
        nft3 = "nft/" + marray[nfn3]

        marketdb.close()
        auctiondb = open("auction.json", "r+", encoding="utf-8")
        ahdata = json.load(auctiondb)
        aharray = ahdata["auction"]

        old_ah1 = aharray[0]
        old_ah2 = aharray[1]
        old_ah3 = aharray[2]
        aharray[0] = nft1
        aharray[1] = nft2
        aharray[2] = nft3

        auctiondb.seek(0)
        json.dump(ahdata, auctiondb, indent=4)
        auctiondb.truncate()
        
        auctiondb.close()

        market_embed = discord.Embed(title="NFT du jour à vendre : ", description="Marché NFT du " + time.asctime(time.localtime()), color=0xffef00)
        #Creating Market image
        images = [Image.open(x) for x in [nft1, nft2, nft3]]
        total_width = 0
        max_height = 0
        # Setting images dimensions

        for img in images:
            total_width += img.size[0]
            max_height = max(max_height, img.size[1])
        final_market = Image.new('RGB', (total_width, max_height))
        current_width = 0
        for img in images:
            final_market.paste(img, (current_width,0))
            current_width += img.size[0]
        
        final_market.save('market.png')

        nft1 = nft1.replace(".png", "")
        nft2 = nft2.replace(".png", "")
        nft3 = nft3.replace(".png", "")
        file = discord.File("market.png", filename="market.png")
        market_embed.add_field(name=nft1, value="Mise de départ : 1000 RTC <:rtc:967486256109994074> ")
        market_embed.add_field(name=nft2, value="Mise de départ : 1000 RTC <:rtc:967486256109994074> ")
        market_embed.add_field(name=nft3, value="Mise de départ : 1000 RTC <:rtc:967486256109994074> ")
        market_embed.set_image(url="attachment://market.png")
        await _channel.send(file = file, embed = market_embed)

        auctiondb = open("auction.json", "r+", encoding="utf-8")
        ahdata = json.load(auctiondb)
        aharray = ahdata["auction"]

        # Taking Buyers IDs
        id1 = aharray[3][1]
        id2 = aharray[4][1]
        id3 = aharray[5][1]
        m1 = aharray[3][0]
        m2 = aharray[4][0]
        m3 = aharray[5][0]

        

        # Resetting Auction House
        ahdata["auction"][3][0] = 1000
        ahdata["auction"][4][0] = 1000
        ahdata["auction"][5][0] = 1000
        ahdata["auction"][3][1] = 0
        ahdata["auction"][4][1] = 0
        ahdata["auction"][5][1] = 0
        ahdata["auction"][3][2] = "Personne"
        ahdata["auction"][4][2] = "Personne"
        ahdata["auction"][5][2] = "Personne"

        auctiondb.seek(0)
        json.dump(ahdata, auctiondb, indent=4)
        auctiondb.truncate()
        
        auctiondb.close()

        f = open("players.json", "r+", encoding="utf-8")
        fdata = json.load(f)
        farray = fdata['players']
        located_player = []
        index_target = 0
        # Finding targeted player in players json array
        for i in range (len(farray)):
            if id1 in farray[i]:
                located_player = farray[i]
                index_target = i
        # Player has been located

        fdata['players'][index_target][2] -= m1
        fdata['players'][index_target][3].append(old_ah1)
        shutil.move(old_ah1, "bought/" + old_ah1.replace("nft/", ""))

        for i in range (len(farray)):
            if id2 in farray[i]:
                located_player = farray[i]
                index_target = i

        fdata['players'][index_target][2] -= m2
        fdata['players'][index_target][3].append(old_ah2)
        shutil.move(old_ah2, "bought/" + old_ah2.replace("nft/", ""))

        for i in range (len(farray)):
            if id3 in farray[i]:
                located_player = farray[i]
                index_target = i

        fdata['players'][index_target][2] -= m3
        fdata['players'][index_target][3].append(old_ah3)
        shutil.move(old_ah3, "bought/" + old_ah3.replace("nft/", ""))

        f.seek(0)
        json.dump(fdata, f, indent=4)
        f.truncate()
        
        f.close()

        await _channel.send("Les transactions ont été faites ! Bravo à tous les entrepreneurs de la journée ! \n Voici Maintenant le nouveau market :")
        return


@client.event
# Ignore self messages
async def on_message(message):
    if message.author == client.user:
        return
#endregion


    #region HELP
    if message.content.lower().startswith("rhelp"):
        local_embed = discord.Embed(title='Help Menu', description="Liste des commandes disponibles (Version 1.2 du RTCBot)", color=0xffef00)
        local_embed.add_field(name="rstart", value="Ouvre un portefeuille de crypto-monnaie et débute votre aventure de sérial-entrepreneur.", inline=False)
        local_embed.add_field(name="rinv", value="Montre le contenu de votre portefeuille de digital marketeux", inline=False)
        local_embed.add_field(name="rdaily", value="Demande à Elon Musk de vous verser votre part quotidienne de crypto-monnaie", inline=False)
        local_embed.add_field(name="rnet", value="Montre le fameux marché noir de Feldup, où vous pouvez faire l'acquisition de mine(u)rs", inline=False)
        local_embed.add_field(name="rmine", value="Récolte les RTC minés par vos miners", inline=False)
        local_embed.add_field(name="rmarket", value="Montre le marché quotidien des NFT", inline=False)
        local_embed.add_field(name="En développement : ", value="ratio, rnft, rshow, rtrade", inline=False)
        local_embed.add_field(name="LE BOT EST EN DEV", value="Les commandes sont en constant changement, et de nouvelles sont en rajout", inline=False)
        
        await message.channel.send(embed = local_embed)
    #endregion


    #region START
    if message.content.lower().startswith("rstart") :
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
            new_player = [message.author.id, message.author.name, 0, [], "", 0, 0, 0, 0, 0]
            farray.append(new_player)
            f.seek(0)
            json.dump(fdata, f, indent=4)
            f.truncate()
            f.close()
        
        return
    #endregion


    #region Inventory
    if message.content.lower().startswith("rinv"):
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
    if message.content.lower().startswith('rdaily'):
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
    if message.content.lower().startswith("rnet"):
        local_embed = discord.Embed(title="DarkNet - Datacenters et miners", description = "Achetez des workers pour miner de la crypto et débuter votre empire financier  <:stonksup:967517993162649621>", color=0xffef00)
        local_embed.add_field(name="GeForce GTX 1060 : 20 RTC", value ="3 RTC/30min : rbuy1", inline=False)
        local_embed.add_field(name="GeForce GTX 1080ti : 35 RTC", value="7 RTC/30min : rbuy2", inline=False)
        local_embed.add_field(name="GeForce RTX 3080ti : 55 RTC", value="11 RTC/30min : rbuy3", inline=False)
        local_embed.add_field(name="Rigs de minage : 200 RTC", value = "50 RTC/30min : rbuy4", inline=False)
        local_embed.set_thumbnail(url="https://s3.us-east-2.amazonaws.com/nomics-api/static/images/currencies/STONK5.png")
        await message.channel.send(embed = local_embed)
    #endregion


    #region rbuy1
    if message.content.lower().startswith("rbuy1"):
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
    if message.content.lower().startswith('rbuy2'):
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
    if message.content.lower().startswith('rbuy3'):
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
    if message.content.lower().startswith('rbuy4'):
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
    if message.content.lower().startswith('rmine'):
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

        current_time = time.time()
        if located_player[9] - current_time <= - 1800:
            given_coins = located_player[5] * 3 + located_player[6] * 7 + located_player[7] * 11 + located_player[8] * 50
            fdata['players'][index_target][2] += given_coins
            await message.channel.send('{}'.format(message.author.mention) + ", votre minage vous fais gagner " + str(given_coins) + "RTC <:rtc:967486256109994074>")
            fdata['players'][index_target][9] = current_time
        else:
            await message.channel.send('{}'.format(message.author.mention) + ", vous avez vidé vos miners, attendez " + str(int((located_player[9] - current_time + 1800)// 60)) + " minutes que ceux-ci finissent de miner ! ")

        f.seek(0)
        json.dump(fdata, f, indent=4)
        f.truncate()
        f.close()
        return
    #endregion


    #region ALLOOOOOO
    if message.content.lower().startswith('rallo'):
        await message.channel.send("ALLOOOOOOO, JE SUIS DELIIIIIIIINK, LIIIIIIIIIIIIIIIINK")
        return
    #endregion


    #region News
    if message.content.lower().startswith('rnews'):
        local_embed= discord.Embed(title="Nouveautés du bot : Version 1.3 (Last Commit : 24/04/22 à 21h24)", description="By Lopinosaurus", color=0xffef00)
        local_embed.add_field(name="rmarket : " , value = "Quand qqn mise, son nom s'affiche sur le market et la mise du nft concerné est modif", inline=False)
        local_embed.add_field(name="rbid :" , value = "Permet de miser sur une nft si vous avez assez d'argent et que votre mise est plus grosse que l'actuelle", inline=False)
        local_embed.add_field(name="Évènement à minuit :", value="les vaincqueurs des enchères perdent l'argent misé, et gagnent les nft dans leur inventaire. Le nouveau market est affiché par le bot, les nft choisies sont tirées au sort", inline=False)

        await message.channel.send(embed = local_embed)
        return
    #endregion


    #region Market Command
    if message.content.lower().startswith('rmarket'):
        auctiondb = open ("auction.json" ,"r+", encoding="utf-8")
        ahdata = json.load(auctiondb)
        aharray = ahdata["auction"]
        nft1 = aharray[0].replace(".png", "")
        nft2 = aharray[1].replace(".png", "")
        nft3 = aharray[2].replace(".png", "")
        market_embed = discord.Embed(title="NFT du jour à vendre : ", description="Marché NFT du " + time.asctime(time.localtime()) + "\n Miser sur un NFT : rbid <numero du nft> <mise en RTC>", color=0xffef00)
        file = discord.File("market.png", filename="market.png")
        market_embed.add_field(name=nft1, value="Mise actuelle : " + str(aharray[3][0]) + " RTC <:rtc:967486256109994074> \n Miseur : " + str(aharray[3][2]))
        market_embed.add_field(name=nft2, value="Mise actuelle : " + str(aharray[4][0]) + " RTC <:rtrtc:967486256109994074> \n Miseur : " + aharray[4][2])
        market_embed.add_field(name=nft3, value="Mise actuelle : " + str(aharray[5][0]) + " RTC <:rtc:967486256109994074> \n Miseur : " + aharray[5][2])
        market_embed.set_image(url="attachment://market.png")
        await message.channel.send(file = file, embed = market_embed)
        return

    #endregion


    #region Bid Command
    if message.content.lower().startswith('rbid'):
        parsed_msg = message.content.split()
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

        if int(parsed_msg[2]) > located_player[2]:
            await message.channel.send('{}'.format(message.author.mention) + ", tu n'as pas assez de thunasse, revient plus tard jeune entrepreneur !")
            return
        f.close()

        auctiondb = open ("auction.json" , "r+", encoding="utf-8")
        ahdata = json.load(auctiondb)
        aharray = ahdata["auction"]
        


        if parsed_msg[1] == None or parsed_msg[2] == None:
            await message.channel.send('{}'.format(message.author.mention) + ", ta commande est invalide. Pour miser sur une NFT, fais rbid <numero de la nft> <nombre de RTC>")
            return
        
        if str(parsed_msg[1]) == "1":
            chosen_nft = 1
            if int(parsed_msg[2]) <= aharray[3][0]:
                await message.channel.send('{}'.format(message.author.mention) + ", ta mise est trop faible ! Mise actuelle pour ce NFT : " + str(aharray[3][0]) + " RTC <:rtc:967486256109994074>")
                return
            if int(parsed_msg[2]) > aharray[3][0]:
                aharray[3][0] = int(parsed_msg[2])
                aharray[3][1] = message.author.id
                aharray[3][2] = message.author.name

        if str(parsed_msg[1]) == "2":
            chosen_nft = 2
            if int(parsed_msg[2]) <= aharray[4][0]:
                await message.channel.send('{}'.format(message.author.mention) + ", ta mise est trop faible ! Mise actuelle pour ce NFT : " + str(aharray[4][0]) + " RTC <:rtc:967486256109994074>")
                return
            if int(parsed_msg[2]) > aharray[4][0]:
                aharray[4][0] = int(parsed_msg[2])
                aharray[4][1] = message.author.id
                aharray[4][2] = message.author.name

        if str(parsed_msg[1]) == "3":
            chosen_nft = 3
            if int(parsed_msg[2]) <= aharray[4][0]:
                await message.channel.send('{}'.format(message.author.mention) + ", ta mise est trop faible ! Mise actuelle pour ce NFT : " + str(aharray[5][0]) + " RTC <:rtc:967486256109994074>")
                return
            if int(parsed_msg[2]) > aharray[4][0]:
                aharray[5][0] = int(parsed_msg[2])
                aharray[5][1] = message.author.id
                aharray[5][2] = message.author.name
        
        auctiondb.seek(0)
        json.dump(ahdata, auctiondb, indent=4)
        auctiondb.truncate()
        auctiondb.close()

        await message.channel.send('{}'.format(message.author.mention) + ", a misé " + parsed_msg[2] + " RTC <:rtc:967486256109994074> pour la " + parsed_msg[1] + "ème NFT ! Qui ira concurrencer cet entrepreneur de GENIE ??")
        return



    #endregion

client.run(TOKEN)

# Todo : ratio command (give RTC to another member)
#      : rmarket (show nft market, refresh once a day, pick from market directory)
#      : rnft<number> (bid nft from market)
#      : rshow <name> (show your <name> nft)
#      : rtrade <@member> (trade nft with another member)
