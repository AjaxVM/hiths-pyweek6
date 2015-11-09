# The Buglist #

Squash 'em if you can:
  * Better placement for capitols, preferably next to another friendly territory
  * Zooming needs to center on mouse cursor, or at least put things in the upper left corner with higher resolutions
  * Tile size should grow by default on higher resolutions
  * Do something to actually end the game when it is over
  * Map should be centered and not clumped in bottom right corner - this is due to the world renderer - it is only on the right when zoomed out - partly because every where else is water - this should probably be fixed - but not really a biggie right now.
  * More which we have forgotten.. =(
  * There is a problem with the music playback on different systems that requires different magic numbers to work :(
  * Mouse selecting of territories is off by one pixel since the fix for teh sprites being cut off - fix is: lib/world.py line:391 should be:
```
p = p[0] - x[0], p[1] - x[1] + self.tile_size[1]
```