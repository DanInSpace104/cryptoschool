# cryptoschool
This repository contains homework and Labs for DistributedLab course.

## Testing
You need to install pytest lib to run tests. `python3 -m pip install pytest`
To run tests: `pytest`

# Baby blockchain implementation - Project Sansara
## Overview
Anonymous reputation / karma system similar to that on habr.com. Anonymity of all authors ensure honest voting without influence of author name and personal grudges. It allows open discussion of difficult social topics or non-popuar opinions, which is especially actual with modern cancelling culture. Anonymity benefits its readers in countries where you can be arrested for simple "like" on wrong post in social media. Also the system protects from spamming votes with bot accounts and some other methods of vote cheating. 
If articles itself stored in blockchain (optional), the system prevents its content from being damaged, removed or censured. 

## Rules of how it works
*Note: All numbers intended to be an example and should be balanced on integration process.*

- Each article is account in similar way as UTXO in Bitcoin. Article receive positive and negative amount of karma from votes of readers. 
- If amount of karma is positive, author of the article can vote for other articles that he likes or dislikes. Amount of available vote is calculated as articleKarma/10. It can not be stored/saved for later and it resets every day. 
- Karma received today will be taken into account of vote amount only on the next day. 
- Karma slowly decomposes at the rate of 0.1 point per day. It ensures that active authors have more influence than lucky ones from past. 
- There is also can be some additional rules to prevent vote cheating and self-pumping. For example your vote for article can not be validated if resulting amount karma you send there from all time is more than your current max voting amount. (If Bob has 30 karma, every day he receives 3 vote points. If yesterday he voted with 1 point, today he can not send more than 2 points on the same article, and tomorrow he will not be able to send it at all).
- Nodes (validators) can receive karma for validating votes (transactions) and connecting new blocks to the chain.

## Users
Authors that want to have open place for ideas and hones reviews. Readers that want to distinct good content from bad and to better spend their time.

## Restrictions 
The system requires several accounts to be included in genesis block. It can work great as new system on existing platform where owners can set initial amount of karma based on previous stats and then system will self-sustain. But if it is new platform, some measures to create alive accounts with vote power must be made. For example open period, where every article will receive karma points immediately until required user count is achieved. 
