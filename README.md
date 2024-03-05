# hsbot-backend

## Introduction

The hsbot-backend is a docker-based application for [Gufu-hsbot](https://github.com/SolaMeow/hsbot-Gufu), it provides the information services and information filt.

It contains 3 component:

### crawl

Python based information crawl program, it can get the information from hearthstone leaderboard, d0nkey.top, and hsreplay.net.

### db

This part contains the information get from crawl, but with carefully design: The tables of db have not been detireminted yet.

### trans

This part contains the infomation get function, and it is the most simple component of the three. It can receive the information, with being called by front-end, and using SQL like commands to call db and get the result, and finally return the information to the front-end.
