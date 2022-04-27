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
    <li><a href="#getting-started">Modify The Source Code</a>
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



## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* npm
  ```sh
  npm install npm@latest -g
  ```

### Installation

_Below is an example of how you can instruct your audience on installing and setting up your app. This template doesn't rely on any external dependencies or services._

1. Get a free API Key at [https://example.com](https://example.com)
2. Clone the repo
   ```sh
   git clone https://github.com/your_username_/Project-Name.git
   ```
3. Install NPM packages
   ```sh
   npm install
   ```
4. Enter your API in `config.js`
   ```js
   const API_KEY = 'ENTER YOUR API';
   ```

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [x] Add Changelog
- [x] Add back to top links
- [ ] Add Additional Templates w/ Examples
- [ ] Add "components" document to easily copy & paste sections of the readme
- [ ] Multi-language Support
    - [ ] Chinese
    - [ ] Spanish

See the [open issues](https://github.com/othneildrew/Best-README-Template/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Your Name - [@your_twitter](https://twitter.com/your_username) - email@example.com

Project Link: [https://github.com/your_username/repo_name](https://github.com/your_username/repo_name)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

Use this space to list resources you find helpful and would like to give credit to. I've included a few of my favorites to kick things off!

* [Choose an Open Source License](https://choosealicense.com)
* [GitHub Emoji Cheat Sheet](https://www.webpagefx.com/tools/emoji-cheat-sheet)
* [Malven's Flexbox Cheatsheet](https://flexbox.malven.co/)
* [Malven's Grid Cheatsheet](https://grid.malven.co/)
* [Img Shields](https://shields.io)
* [GitHub Pages](https://pages.github.com)
* [Font Awesome](https://fontawesome.com)
* [React Icons](https://react-icons.github.io/react-icons/search)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/screenshot.png
