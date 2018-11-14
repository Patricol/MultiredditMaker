# MultiredditMaker

## Features
* Creates a set of combo multireddits using all subscribed subreddits.
  * Each created multireddit has a maximum of 100 subreddits.
    * This makes it easier to view all subscribed subreddits; by visiting each combo multireddit instead of having to figure out which aren't being shown on the front page and visiting each one of those individually.
  * Subreddits are sorted between combo multireddits by their number of subscribers.
    * That helps to keep smaller subreddits from being drowned out; especially when viewing categories like top.
  * Rerunning the script updates the combo multireddits; adding any newly subscribed subreddits, and re-sorting by number of subscribers.

## Instructions
* Add your credentials by following the instructions in creds_example.py.
* Depends on [praw](https://pypi.org/project/praw/); install using pip.
* Run using python 3.