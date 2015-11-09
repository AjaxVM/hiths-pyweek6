# Core #

## Overview ##
Name = ???

Game map is an isometric or tile grid that is divided into regions - like dicewars (gamedesign.jp/flash/dice/dice.html), except not hex-tiles.

Objects will be 3d renders at an isometric angle - regardless of tile-type.

GUI will be the PygLibs GUI module - http://pymike93.googlepages.com/RoeBroesGUI.zip - current host only - moving to main pyglibs distro next release.

Network play with a lobby + AI.

## Specifics ##
### Units ###
There are two types of units - captains and soldiers.
Soldiers are the basic fighting unit, you can only have as many soldiers in a territory as there are open spaces for them to be in.
Captains are special units that boost your armies fighting potential by adding more Formation Tomes/Cards/NeedABetterName ;)

Units can be moved between territories each turn, but only one territory a turn for each unit.

### Formations ###
There are a certain number of formations in the game - each are stronger/worse than other formations.
Armies that do not have a captain with them can only use a small number of basic ones.
Armies with captains may use all the basic formations plus any special ones the captain knows.
Special formations are cards generated at random times by your capitol that you can teach to your captains, but are only usable once. Once a captain has learned a formation they remember it until they die.
When a captain is killed there is a 33% chance that the victorious army - if it has captain - will learn some or all of the formation known by the defeated captain.

### Buildings ###
There are two kinds of buildings in the game.
The palace/capitol is located on your starting territory, and will generate new troops, captains and formations for you. It also gives your troops extra defense against an enemy invasion.
If you lose your capitol you do not get a new one, and the conqueror keeps your palace as a secondary one for themselves.

Cities function like palaces - except they don't generate new formations or captains, and their troop production and defense bonus is decreased.

### Battles ###
When a battle occurs in this game, both sides pick a formation to imploy.
The attacking team gets a random attack in the range of:
> `(troops - 1 + captain?) to ((troops - 1 + captain?) * num) + or - the advantage/disadvantage of this card against the defenders card`.
Num should be somewhere between 5 or 10 - we can use this to balance the game.

The defending team then gets a random defense value in the range of:
> `(troops - 1 + captain?) to ((troops - 1 + captain?) * num) + whatever defense is active on the defenders territory`.

Unlike dicewars - when a battle is fought - both sides suffer casualties, not just the losing side.
Also, not every battle ends in a territory change, as not necessarily will the aggressor destroy every unit of an enemies in one round.


## Variations for themes ##
### Jig ###
The Jig formation is a special formation that is created at the beginning of the game by each team  it is unique for each team.
These card cannot be captured by enemies, but are generated less often than other formations.
When creating a Jig, the player specifies where to place troops etc. and the game will automatically determine hog good it is against enemy formations using some method.
Where two regular formations may end in a tie, ie neither has an advantage - the jig will always have the advantage in such a case, unless the other card is also a Jig.

### Robots ###
Well, all units are robots ;)
Other interesting things could also be done, but that is the gist of it.
Maybe robot buildings? ie - you can move your capitol around :)

### Shuffle ###
In this mode - each team only gets a certain number of cards, which are randomly given to each player after being shuffled up :)
Also, every few turns all cards are regathered again, shuffled, and redistributed.

### Mashed ###
Add me.

### Formation ###
This one is already implemented - I guess if we don't do formation we can cut captains and formations altogether - but we'll have to see.


## Possible Additions ##
### Building ###
Forts are a defense enhancing building that an army can build at a cost of no movement for 2 turns on a territory that has neither a city nor capitol. They give as much defense as a city.