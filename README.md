Steam Market CLI
================

Some sort of commandline interface for the [Steam Marketplace](http://steamcommunity.com/market/)

Example
-------
<pre>
>>> python market.py -s "Portal 2"
&lt;Portal 2 Set: total_price=1.47, foil_price=8.00, 5levels=7.35&gt;

>>> python market.py -s "Sid Meier's Civilization V"
&lt;Sid Meier's Civilization V Set: total_price=0.76, foil_price=2.96, 5levels=3.80&gt;
</pre>

`-s` should match the exact name that is used on the marketplace. It'll append "Trading Card" to do the search, and discard any that don't match the game name exactly.
