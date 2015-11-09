**CLASSIC MODE:**

Map is a grid of square shaped tiles.
Each territory is a group of tiles, kinda  like the hex tiles grouped together in dice wars.
Territories must containt at least 5 squares, and 7 if there are the extra units.
When you control a territory, if there is a supply center and/or fort, they show up on one of the sub-tiles.
Each unit-type in your army on that tile gets a sub-tile space, and a "xN" display for the the number of that type of unit.

Armies are groups of units that occupy players territories. They can be any size as long as you have enough supply centers.

Supply centers are located on some territories. They set the maximum number of troops you can own, and also create new units at the rate of
> (max troop amount) / (total territories  / player territories)
> Max troop count is number of supply centers **the number of troops each center supports.**

Forts are defensive buildings that you can instruct your armies to build instead of moving, it might take a turn? or cost troops...

Palaces are the ultimate defensive building and also serve as a supply center.
When you capture an enemy palace, it remains a  palace and you get the benefit of it as if you had another palace.

Their are 3-6 kinds of units, each has an advantage against another kind of unit, or against supply centers/forts.
3 is simpler, but not quite as fun me thinks...
Kinda cute fantasy like setting (this can change to fit the theme)

Units:
Spearman - beats Horseman
Archer - beats Spearman
Horseman - beats Archer
Catapult - gets a bonus against any unit when attacking a fortress or palace
Rats (this is dependant on a fantasy theme) - ok against all, gets a bonus against supply centers.

When you attack, you can select the number and types of units to send.
Your troops then assault the enemy tile you chose.
The number of casualties for both sides is determined by the types/numbers of units each side has, whether their is a fort, etc.
Even if you lose the enemy will take casualties, and if you win you will as well.

You can transfer units from one tile to another at the rate of 1 unit of each type from any one tile per turn.

Obviously there needs to be some places where we can change the idea to fit the theme.
So I was thinking units, locations (space, desert, it really is only about the images, the game won't make use of different terrains ;) ),
> buildings, etc. can all be changed around a bit.
Also, the game will feature cut-scenes, which should allow us to fit in more of the theme.
We could also allow Mercs that you can buy with a currency that reflects the theme, which you would get from supply centers and stuff.
We may even want to make it so that all units are bought, supply centers simply give you a certain amount of currency each turn.
The only problem with that is that it is less simple, and is kinda Battle for Wesnoth-y, IMO.


**ULTIMATE MODE:**
This MODE may be to in-depth to make for Pyweek.

This MODE is the same as CLASSIC MODE, except it adds more game-play and slows the game up to focus more on strategy.

Battle Plans, each army has a certain number of strategy cards, which allows you to use special strategies.
This is useful because then even significantly smaller armies can over-power stronger armies, if they pick a good strategy that beats the others strategy.

When you defeat another army, you take control of the Battle Strategies that the army had at its disposal.
Besides the most basic battle card, you can only use each card once, before it is destroyed.
But you may have several of the same type of card with one army for multiple uses.

When you have control of a battle plan for 5-10? turns, your palace will automatically generate a new one that you can give to one of your armies.

Armies may now have a new unit attached to them, a general.
With a general a army has two new basic battle plans that never are used up - one attack one defense one.
Some unique battle plans also require a general to be able to use.

You can transfer battle cards to another unit, by moving a small part of your army with it like you would normally move an army,
> except that it takes the battle plan with it.

You can also now cooperate with other players more.
When you attack an enemy territory, you select your army as before, except now, before selecting the enemy, you can also select other players territories, this will send them a prompt allowing them to "loan" you some troops to attack an adjacent enemy.
Units then either die or are returned to the other player.

With this mode we could change around the generals and battle plans to fit the theme.



**NON-SPECIFIC MODE stuff:**

The game can start like dice wars, with everyone in random positions, with one palace each, or with an "already dominant player", where everyone starts out with their own little connected territories, except one player starts with 1/3 or 1/2 of the territories already under their control.
The dominant player can also be a Rebel, so it will attack everyone roughly equally, and defend weaker players.
We could also allow so that everyone starts with their own little territories, but except there is no dominant player.

If you move all units from a territory, a Rebel will arise and take control.

Game will be multiplayer, with a lounge and in-game chat.

We will use OpenGL for the graphics. But the map will be 2d (we are just using the hardware accelaration here ;) )
The units/buildings/cards? will be 3d meshes that are rendered to the 2d grid.
Map grid can be rotated, zoomed, etc.

Game will be highly GUI intensive ;)