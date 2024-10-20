# Welcome to LeetCode Civilization

Here in LeetCode Civilization no-one chooses to code for the hard, it's better to be safe and code for the easy rather than risk it all for the hard.

Practice your LeetCode skills by ascending the ranks in LeetCode Civilization. Complete questions to rank up and become the LeetCode Champion.

## Getting Started
Start by using `/link`

Input your LeetCode username, found in your profile. Then continue the linking process. Next put the code generated in your profile summary for the bot to see.

Finish this process by using `/verify`

Congratulations! You have joined LeetCode Civilization, you are now ready to get tickets and rank up!

## Tickets
Tickets are the currency in LeetCode Civilization. You can gain tickets in a few ways:
- Completing new questions on LeetCode and then using the `/sync` command to update your completed questions
- Completing the LeetCode daily question by using the `/daily` command after solving the question (you can use `\sync` on this question if you haven't already solved it to double dip on points!)
- Competing in LeetCode battles, this will be explained more later!

## Rank up
To rank up in LeetCode Civilization you must complete a rank up trial. If you pass the trial you rank up. The trial is a timed LeetCode problem. You have 25 minutes to complete the trial. The difficulty of the problem depends on the rank you currently possess:
- Noob --> Pro: Easy
- Pro --> Master: Medium
- Master --> Champion: Hard
- Master --> Master: Medium/Hard

Once you reach the Master rank, completing the rank up challenge gives you elo points. Rise to the top of the Master rank to claim the title of LeetCode God.

## Battles
An important part of LeetCode Civilization are LeetCode battles. At any time you can challenge someone else to a LeetCode battle. The aggressor decides the difficulty of the problem. If the person challenged chooses to accept the battle, both parties are given the same random question of the chosen difficulty and whoever solves it first wins the battle.

LeetCode battles are started with the `/battle <user> <difficulty>` command. A prompt will show up for the challenged person to accept. The first person to solve the question within the 60 minute time limit and use the `/submit` command wins the battle. If the battle times out, then no-one wins and nothing happens.

The consequences for winning or losing a LeetCode battle can vary. If a Noob is involved in the battle, then nothing happens at all. This can be considered as just practice. 

Otherwise, if both parties are the same level, then whoever wins the battle rises a rank and whoever loses drops a rank. 

If the parties are of unbalanced rank, the loser still drops a rank but if the winner is of higher rank, then they gain tickets instead of rising a rank. If the lower ranked player wins, they still rise a rank.

If one of the parties is Champion rank, then they gain LP for battle wins.

If both parties agree to call off the battle, one of the parties can use the `/cancel` command to end the battle.

## Profile
You can use the `/profile` command to check your stats. It features how many tickets you have, how many problems you have solved, and your win/loss record for non-Noob battles.

## Leaderboard
You can use the `/leaderboard` command to check the top 10 ranking leaderboard. The leaderboard is sorted by elo in the Champion tier, and by tickets in lower tiers.