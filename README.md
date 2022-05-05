<div id="top"></div>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://zupimages.net/viewer.php?id=22/17/4sqm.png">
    <img src="https://zupimages.net/up/22/17/4sqm.png" alt="" /></a>

  <h3 align="center">RatioCoin Discord Bot</h3>

  <p align="center">
    A simple Karuta-like Discord game bot. 
    <br />
    <a href="https://github.com/othneildrew/Best-README-Template/issues">Report Bug</a>
    ·
    <a href="https://github.com/othneildrew/Best-README-Template/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#gameplay-and-commands">Gameplay And Commands</a>
      <li><a href="#built-with">Built With</a>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>




## Gameplay And Commands

RTCBot (for RatioCoins Bot) is mostly inspired by Karuta and other "Card Dropping" game bots. The gameplay is simple : you can nine every 30 minutes a fictive currency ("RatioCoin"), to buy some miners to mine faster and more coins (like a tycoon gameplay). When you have enough coins, you can bid on NFTs at the market, which rotate every days. The best bidder on a NFT wins it at midnight, and can trade it with his friend. If you want to add more NFTs, simply add them in `nft/` directory (be sure to have the same dimension for every pictures).

Here are all the commands supported by RTCBot :
- **rstart** : creates you an account on the bot
- **rinv** : shows your inventory
- **rdaily** : claims your daily award (between 20 and 45 RTC per day)
- **rnet** : shows the miners you can buy
- **rmine** : claims the RTC your miners have mined. Cooldown of 30minutes.
- **rmarket** : shows the day's NFT market
- **rbid [nft number] [bid in RTC]** : bid on the NFT you chose
- **ratio @member [amount in RTC]** : direct transaction to an other member
- **rnft [nft name]** : shows the nft you typed
- **rlist** : list all the available NFTs
- **(indev) rtrade @member [nft name]** : allow you to trade your NFT with an other member

When you have rigs miners, you have 1 of 4 chances to loose between 15% and 40% of them (to avoid exponential benefits with rigs). Every day at midnight, the market reset and NFTs are given to bidders if they have enough RTC at the time.
  
<p align="right">(<a href="#top">back to top</a>)</p>



### Built With

This bot is coded in Python, using JSON databases and Discord.py library. Here are all the compenents and languages used to develop RTCBot :

* [Python](https://www.python.org/)
* [JSON](https://www.json.org/json-en.html)
* [Dotenv](https://www.dotenv.org/)
* [Discord.py](https://discordpy.readthedocs.io/en/stable/)
* [PIL Library](https://pillow.readthedocs.io/en/stable/)

<p align="right">(<a href="#top">back to top</a>)</p>


### Prerequisites

All libraries installation :
* Dotenv
  ```sh
  pip install python-dotenv
  ```
* Discord.py
  ```sh
  pip install discord.py
  ```
* PIL
  ```sh
  pip install pillow
  ```



### Setting up the Bot

1. Clone the repo.
   ```sh
   git clone git@github.com:Lopinosaurus/RTCBot.git
   ```
   
2. Create `nft/` directory, and put all of your custom pictures in it. It is highly recommended to put all your images in the same dimensions.
   
3. Enter your bot's token in `.env` file.
 
4. Change the channel id by the wanted one on line 32 of `bot.py` file.

5. Everything is set up ! You can modify what you want in the json for a custom start.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Documentation :

### Functions : 

#### @task.loop async function :

Every minute, this function is checking if it's midnight, so the bot can update the market and do the transactions. 
If current time is 00h00, the bot create the transaction, give the NFT to the concerned players, and build the image of the new market using PIL library. It also reset the auction house.

#### on_message(message):

- rstart command : start a new player array in `players.json`. Initialize all player attribute with default values (0RTC. 0NFT, rdaily possible).
- rnet command : display miner shop. It is basically an embed constructor.
- rbuy<miner> <amount> : Open `players.json`, localize the player operate. Close the file when operation is done.
- rinv : Open `players.json`, localize the player, and display the value in an embed.
- rdaily : Open `players.json`, localize the player, verify if he did not run the command today (time.asctime value)
- rmine : Open `players.json`, localize the player, find the amount of miners. Add the RTC depending of miners possessed by player. If he has miner rigs, he has 1/4 chance to loose between 15% and 40% of them.
- rmarket : Display the market in an embed, by opening and reading `auction.json`.
- rbid <nft number> <bid in RTC> : Open `players.json`, localize the player, verify if he has enough money. Then open `auction.json` and refresh the data.
- rnft <nft name> : open `nft_db.json` and search for the nft in args.
- rlist : open `nft_db.json`, display all files in an embed.
  

<p align="right">(<a href="#top">back to top</a>)</p>






<!-- CONTRIBUTING -->
## Contributing

If you want to add something or modify the bot, please follow this :

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Discord : Lopinosaurus#0404 - [@Lopinosaurus](https://twitter.com/Lopinosaurus)

<p align="right">(<a href="#top">back to top</a>)</p>



