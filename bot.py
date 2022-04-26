# bot.py
# region Library
import os

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
    if str(_time[11]) +  str(_time[12]) + str(_time[14]) + str(_time[15]) == "0000":
        auctiondb = open("auction.json", "r+", encoding="utf-8")
        ahdata = json.load(auctiondb)
        aharray = ahdata["auction"]

        nft1_sold = False
        nft2_sold = False
        nft3_sold = False

        # FIRST NFT GIFT AND REMOVING MONEY
        if not aharray[3][1] == -1:
            f = open("players.json", "r+", encoding="utf-8")
            fdata = json.load(f)
            farray = fdata['players']
            index_target = -1

            for i in range (len(farray)):
                if aharray[3][1] in farray[i]:
                    index_target = i
            
            if fdata['players'][index_target][2] >= aharray[3][0]:
                fdata['players'][index_target][3].append(aharray[0].replace(".png", ""))
                fdata['players'][index_target][2] -= aharray[3][0]
                nft1_sold = True
            else:
                await _channel.send(fdata['players'][index_target][1] + " n'avait pas assez d'argent au moment de la vente, elle est donc annulée !" )

            f.seek(0)
            json.dump(fdata, f, indent=4)
            f.truncate()
            f.close()


        # SECOND NFT GIFT AND REMOVING MONEY
        if not aharray[4][1] == -1:
            f = open("players.json", "r+", encoding="utf-8")
            fdata = json.load(f)
            farray = fdata['players']
            index_target = -1

            for i in range (len(farray)):
                if aharray[4][1] in farray[i]:
                    index_target = i

            if fdata['players'][index_target][2] >= aharray[4][0]:
                fdata['players'][index_target][3].append(aharray[1].replace(".png", ""))
                fdata['players'][index_target][2] -= aharray[4][0]
                nft2_sold = True
            else:
                await _channel.send(fdata['players'][index_target][1] + " n'avait pas assez d'argent au moment de la vente, elle est donc annulée !" )

            f.seek(0)
            json.dump(fdata, f, indent=4)
            f.truncate()
            f.close()
            
        

        # THIRD NFT GIFT AND REMOVING MONEY
        if not aharray[5][1] == -1:
            f = open("players.json", "r+", encoding="utf-8")
            fdata = json.load(f)
            farray = fdata['players']
            index_target = -1

            for i in range (len(farray)):
                if aharray[5][1] in farray[i]:
                    index_target = i

            if fdata['players'][index_target][2] >= aharray[5][0]:
                fdata['players'][index_target][3].append(aharray[2].replace(".png", ""))
                fdata['players'][index_target][2] -= aharray[5][0]
                nft3_sold = True
            else:
                await _channel.send(fdata['players'][index_target][1] + " n'avait pas assez d'argent au moment de la vente, elle est donc annulée !" )

            f.seek(0)
            json.dump(fdata, f, indent=4)
            f.truncate()
            f.close()
            
        
        nft1 = aharray[0].replace("nft/", "")
        nft2 = aharray[1].replace("nft/", "")
        nft3 = aharray[2].replace("nft/", "")

        auctiondb.close()


        # DELETING FROM DATABASE THE NFTs
        marketdb = open("market.json" , "r+", encoding="utf-8")
        marketdata = json.load(marketdb)
        
        if nft1_sold :
            marketdata["market"].remove(nft1)
        if nft2_sold:
            marketdata["market"].remove(nft2)
        if nft3_sold:
            marketdata["market"].remove(nft3)

        marketdb.seek(0)
        json.dump(marketdata, marketdb, indent=4)
        marketdb.truncate()
        marketdb.close()

        # RESETING AND CREATING NEW AH
        auctiondb = open("auction.json", "r+", encoding="utf-8")
        ahdata = json.load(auctiondb)
        aharray = ahdata["auction"]

        ahdata["auction"][3][0] = 1000
        ahdata["auction"][3][1] = -1
        ahdata["auction"][3][2] = "Personne"
        ahdata["auction"][4][0] = 1000
        ahdata["auction"][4][1] = -1
        ahdata["auction"][4][2] = "Personne"
        ahdata["auction"][5][0] = 1000
        ahdata["auction"][5][1] = -1
        ahdata["auction"][5][2] = "Personne"
        
        
        auctiondb.seek(0)
        json.dump(ahdata, auctiondb, indent=4)
        auctiondb.truncate()
        auctiondb.close()
        
        
        # Creating new market
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
        await _channel.send("Les transactions ont été faites ! Bravo à tous les entrepreneurs de la journée ! \n Voici Maintenant le nouveau market :")
        await _channel.send(file = file, embed = market_embed)

        return


@client.event
# Ignore self messages
async def on_message(message):
    if message.author == client.user:
        return
#endregion


    #region HELP
    if message.content.lower().startswith("rhelp"):
        local_embed = discord.Embed(title='Help Menu', description="Liste des commandes disponibles (Version 1.8 du RTCBot)", color=0xffef00)
        local_embed.add_field(name="rstart", value="Ouvre un portefeuille de crypto-monnaie et débute votre aventure de sérial-entrepreneur.", inline=False)
        local_embed.add_field(name="rinv", value="Montre le contenu de votre portefeuille de digital marketeux", inline=False)
        local_embed.add_field(name="rdaily", value="Demande à Elon Musk de vous verser votre part quotidienne de crypto-monnaie", inline=False)
        local_embed.add_field(name="rnet", value="Montre le fameux marché noir de Feldup, où vous pouvez faire l'acquisition de mine(u)rs", inline=False)
        local_embed.add_field(name="rmine", value="Récolte les RTC minés par vos miners", inline=False)
        local_embed.add_field(name="rmarket", value="Montre le marché quotidien des NFT", inline=False)
        local_embed.add_field(name="rbid <num du nft> <mise en rtc>", value="Pose une enchère sur le NFT choisi et montre votre supériorité. Si vous êtes le miseur en tête à 00h; vous emportez le NFT.", inline=False)
        local_embed.add_field(name="ratio <@membre> <prix en rtc>", value="Transfert direct entre compte via un ratio amical (ou pas)", inline=False)
        local_embed.add_field(name="rnft <nom du nft>", value="Montre le NFT demandé et son bg de propriétaire", inline=False)
        local_embed.add_field(name="rlist", value="Liste tous les NFT présents sur ce discord d'entrepreneurs de génie du web", inline=False)
        local_embed.add_field(name="En développement : ", value="rtrade", inline=False)
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
        local_embed.add_field(name="GeForce GTX 1060 : 20 RTC", value ="3 RTC/30min : rbuy1 <nombre de miners>", inline=False)
        local_embed.add_field(name="GeForce GTX 1080ti : 35 RTC", value="7 RTC/30min : rbuy2 <nombre de miners>", inline=False)
        local_embed.add_field(name="GeForce RTX 3080ti : 55 RTC", value="11 RTC/30min : rbuy3 <nombre de miners>", inline=False)
        local_embed.add_field(name="Rigs de minage : 200 RTC", value = "50 RTC/30min : rbuy4 <nombre de miners>", inline=False)
        local_embed.set_thumbnail(url="https://s3.us-east-2.amazonaws.com/nomics-api/static/images/currencies/STONK5.png")
        await message.channel.send(embed = local_embed)
    #endregion


    #region rbuy1
    if message.content.lower().startswith("rbuy1"):
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
        
        try:
            parsed_msg[1] = int(parsed_msg[1])
            price = parsed_msg[1] * 20
            if price == 0:
                await message.channel.send('{}'.format(message.author.mention + ", tu ne peux pas acheter 0 miner cher entrepreneur !"))
                return
        except:
            await message.channel.send('{}'.format(message.author.mention + ", nombre de miners invalide !"))
            return

        if located_player[2] < price:
            await message.channel.send('{}'.format(message.author.mention) + ", vous n'avez pas assez d'argent, demandez à ceux qui aident les gens dans le besoin.")
            return
        
        fdata['players'][index_target][2] -= price
        fdata['players'][index_target][5] += parsed_msg[1]

        f.seek(0)
        json.dump(fdata, f, indent=4)
        f.truncate()
        f.close()

        await message.channel.send('{}'.format(message.author.mention) + ", vous avez acheté " + str(parsed_msg[1]) + " GeForce GTX 1060 !")
        return

    #endregion

    
    #region rbuy2
    if message.content.lower().startswith('rbuy2'):
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
        
        try:
            parsed_msg[1] = int(parsed_msg[1])
            price = parsed_msg[1] * 35
            if price == 0:
                await message.channel.send('{}'.format(message.author.mention + ", tu ne peux pas acheter 0 miner cher entrepreneur !"))
                return
        except:
            await message.channel.send('{}'.format(message.author.mention + ", nombre de miners invalide !"))
            return

        if located_player[2] < price:
            await message.channel.send('{}'.format(message.author.mention) + ", vous n'avez pas assez d'argent, demandez à ceux qui aident les gens dans le besoin.")
            return
        
        fdata['players'][index_target][2] -= price
        fdata['players'][index_target][6] += parsed_msg[1]

        f.seek(0)
        json.dump(fdata, f, indent=4)
        f.truncate()
        f.close()

        await message.channel.send('{}'.format(message.author.mention) + ", vous avez acheté " + str(parsed_msg[1]) + " GeForce GTX 1080ti !")
        return
    #endregion


    #region rbuy3
    if message.content.lower().startswith('rbuy3'):
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
        

        try:
            parsed_msg[1] = int(parsed_msg[1])
            price = parsed_msg[1] * 55
            if price == 0:
                await message.channel.send('{}'.format(message.author.mention + ", tu ne peux pas acheter 0 miner cher entrepreneur !"))
                return
        except:
            await message.channel.send('{}'.format(message.author.mention + ", nombre de miners invalide !"))
            return

        if located_player[2] < 55:
            await message.channel.send('{}'.format(message.author.mention) + ", vous n'avez pas assez d'argent, demandez à ceux qui aident les gens dans le besoin.")
            return
        
        fdata['players'][index_target][2] -= price
        fdata['players'][index_target][7] += parsed_msg[1]

        f.seek(0)
        json.dump(fdata, f, indent=4)
        f.truncate()
        f.close()

        await message.channel.send('{}'.format(message.author.mention) + ", vous avez acheté " + str(parsed_msg[1]) + " GeForce RTX 3080ti !")
        return
    #endregion

    
    #region rbuy4
    if message.content.lower().startswith('rbuy4'):
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
        
        try:
            parsed_msg[1] = int(parsed_msg[1])
            price = parsed_msg[1] * 200
            if price == 0:
                await message.channel.send('{}'.format(message.author.mention + ", tu ne peux pas acheter 0 miner cher entrepreneur !"))
                return
        except:
            await message.channel.send('{}'.format(message.author.mention + ", nombre de miners invalide !"))
            return        

        if located_player[2] < price:
            await message.channel.send('{}'.format(message.author.mention) + ", vous n'avez pas assez d'argent, demandez à ceux qui aident les gens dans le besoin.")
            return
        
        fdata['players'][index_target][2] -= price
        fdata['players'][index_target][8] += parsed_msg[1]

        f.seek(0)
        json.dump(fdata, f, indent=4)
        f.truncate()
        f.close()

        await message.channel.send('{}'.format(message.author.mention) + ", vous avez acheté " + str(parsed_msg[1]) + " rigs de minage !")
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
        local_embed= discord.Embed(title="Nouveautés du bot : Version 1.8 (Last Commit : 26/04/22 à 18h39)", description="By Lopinosaurus", color=0xffef00)
        local_embed.add_field(name="rmarket : " , value = "Quand qqn mise, son nom s'affiche sur le market et la mise du nft concerné est modif", inline=False)
        local_embed.add_field(name="rbid <num du nft> <mise en rtc> :" , value = "Permet de miser sur une nft si vous avez assez d'argent et que votre mise est plus grosse que l'actuelle", inline=False)
        local_embed.add_field(name="rbuy<num> <nombre> :" , value = "Vous devez maintenant spécifier combien de miners vous achetez", inline=False)
        local_embed.add_field(name="ratio <@membre> <prix en rtc>", value="Donne directement du RTC à la personne pinged", inline=False)
        local_embed.add_field(name="rnft <nom du nft>:" , value = "Permet de voir le NFT noté", inline=False)
        local_embed.add_field(name="rlist :" , value = "Liste l'ensemble des NFT implémentés par série de sortie", inline=False)
        local_embed.add_field(name="Évènement à minuit :", value="Les vainqueurs des enchères perdent l'argent misé, et gagnent les nft dans leur inventaire. Le nouveau market est affiché par le bot, les nft choisies sont tirées au sort", inline=False)

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
        possible_bids = [1,2,3]
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
        


        if int(parsed_msg[1]) not in possible_bids or parsed_msg[2] == None:
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
            if int(parsed_msg[2]) <= aharray[5][0]:
                await message.channel.send('{}'.format(message.author.mention) + ", ta mise est trop faible ! Mise actuelle pour ce NFT : " + str(aharray[5][0]) + " RTC <:rtc:967486256109994074>")
                return
            if int(parsed_msg[2]) > aharray[5][0]:
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


    #region Ratio
    if message.content.lower().startswith('ratio'):
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
        
        try:
            parsed_msg[2] = int(parsed_msg[2])
        except:
            await message.channel.send('{}'.format(message.author.mention + ", ton ratio est invalide ! Commande : ratio @membre <nombre rtc>"))

        if len(parsed_msg) < 3:
            await message.channel.send('{}'.format(message.author.mention + ", ton ratio est invalide ! Commande : ratio @membre <nombre rtc>"))
            return

        if parsed_msg[2] < 0:
            await message.channel.send('{}'.format(message.author.mention + ", tu ne peux pas voler l'argent des autres (t'es con ou quoi ?) !"))
            return

        if parsed_msg[2] > fdata['players'][index_target][2]:
            await message.channel.send('{}'.format(message.author.mention) + ", tu ne peux pas ratio plus de RTC que ce que tu as dans ton wallet, connard.")
            return
        
        # Finding ratioed id
        pinged_id = int(parsed_msg[1][1:][:len(parsed_msg[1])-2].replace("@","").replace("!",""))

        was_old_ratioed = False
        index_target_ratioed = 0
        
        for i in range (len(farray)):
            if pinged_id in farray[i]:
                index_target_ratioed = i
                was_old_ratioed = True

        # Ratioed player has been located
        if not was_old_ratioed:
            await message.channel.send('{}'.format(message.author.mention) + ", votre cible pour le ratio n'est pas inscrite sur RTCBot ! Pour ouvrir un compte de digital marketeux, elle doit faire rstart !")
            return
        
        fdata['players'][index_target][2] -= parsed_msg[2]
        fdata['players'][index_target_ratioed][2] += parsed_msg[2]

        await message.channel.send('{}'.format(message.author.mention + ", ton ratio s'est déroulé avec succès. Cry."))

        f.seek(0)
        json.dump(fdata, f, indent=4)
        f.truncate()
        f.close()
        
    #endregion


    #region NFT Viewer
    if message.content.lower().startswith('rnft'):
        parsed_msg = message.content.split()
        if len(parsed_msg) < 2:
            await message.channel.send('{}'.format(message.author.mention, ", tu dois spécifier quelle NFT tu veux voir ! Commande : rnft <nom du nft>"))
            return
        
        try:
            if "nft/" in parsed_msg[1]:
                await message.channel.send("Je ne peux pas trouver le fichier si tu spécifies nft/ ! ")
                return

            if ".png" in parsed_msg[1]:
                local_file = discord.File("nft/" + parsed_msg[1], filename=parsed_msg[1])
                filename = "nft/" + parsed_msg[1]
            else:
                local_file = discord.File("nft/" + parsed_msg[1] + ".png", filename=parsed_msg[1]+ ".png")
                filename = "nft/" + parsed_msg[1] + ".png"
        except:
            await message.channel.send('{}'.format(message.author.mention + ", le NFT spécifié n'existe pas ! (Fichier non existant)"))
            return
        

        f = open("players.json", "r+", encoding="utf-8")
        fdata = json.load(f)
        farray = fdata['players']

        nft_owner = "Personne"

        for i in range(len(farray)):
            if parsed_msg[1].replace(".png", "") in farray[i][3]:
                nft_owner = farray[i][1]
        
        local_embed = discord.Embed(title="NFT : " + parsed_msg[1].replace(".png", ""), description="Appartient à : " + nft_owner, color=0xffef00)
        local_embed.set_image(url="attachment://" + filename.replace("nft/", ""))
        await message.channel.send(file=local_file, embed=local_embed)

    #endregion


    #region NFT Lister
    if message.content.lower().startswith('rlist'):
        nft_db = open("nft_db.json", "r", encoding="utf-8")
        nft_data = json.load(nft_db)
        nft_array = nft_data["nft_db"]

        local_embed = discord.Embed(title="Liste des NFT actuellement implémentées : ", color=0xffef00)
        for nft_name in nft_array:
            local_embed.add_field(name = "Série 1 :", value=nft_name.replace(".png", ""))
        
        nft_db.close()
        await message.channel.send(embed = local_embed)
    #endregion

    

client.run(TOKEN)

# Todo : ratio command (give RTC to another member)
#      : rmarket (show nft market, refresh once a day, pick from market directory)
#      : rnft<number> (bid nft from market)
#      : rshow <name> (show your <name> nft)
#      : rtrade <@member> (trade nft with another member)
