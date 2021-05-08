# NBA-Prime
## Overview
* Building a data-driven model to find an NBA player's "prime"
* To create the ultimate system for power ranking the NBA's greatest players (e.g. Why is player X the 27th best player of all time, and player Y the 28th? What separates the two?)
* Check out the full articles on [Medium-NBA Primes](https://michaelpatel.medium.com/discovering-nba-players-primes-8bd91895757d) and [Medium-MVP's]()
* Sponsored by and providing model results and insights for the [Hard in the Paint NBA Podcast](https://soundcloud.com/engineers-play "Hard in the Paint NBA Podcast")
<a href="https://soundcloud.com/engineers-play">
  <img src="https://i1.sndcdn.com/avatars-000446326572-ycrzp2-t500x500.jpg" alt="Hard in the Paint NBA Podcast Logo" width="300"/>
</a>

## Data
* Using a variety of statistical metrics provided by Basketball Reference and NBA Stats
* Created and calculated a custom statistic called **M_VALUE** to measure an NBA player's prime

## Results
### LeBron James
LeBron James Career Stats
![LBJ Raw Stats](https://github.com/mikepatel/NBA-Prime/blob/master/Primes/results/LeBron%20James/LeBron%20James_plots.png)


What is LeBron James' Prime? Check the table below to find out!

|Season |Age|Team|Points|Rebounds|Assists|FT%  |eFG% |PER |TS%  |M_VALUE|
|-------|---|----|------|--------|-------|-----|-----|----|-----|-------|
|2011-12|27 |MIA |27.1  |7.9     |6.2    |0.771|0.554|30.7|0.605|0.4707 |
|2012-13|28 |MIA |26.8  |8.0     |7.3    |0.753|0.603|31.6|0.64 |0.5467 |
|2013-14|29 |MIA |27.1  |6.9     |6.3    |0.75 |0.61 |29.3|0.649|0.4727 |


### Preliminary ranking of MVP winners since 2000 by HITP
(2012 season was shortened)\
![](https://github.com/mikepatel/NBA-Prime/blob/master/MVP/results/racing_bar_mvp.gif)
![](https://github.com/mikepatel/NBA-Prime/blob/master/MVP/results/bar_mvp.png)
![](https://github.com/mikepatel/NBA-Prime/blob/master/MVP/results/sorted_bar_mvp.png)

| Year | Name                  | Points | Rebounds | Assists | HITP   | 
|------|-----------------------|--------|----------|---------|--------| 
| 2016 | Stephen Curry         | 30.1   | 5.4      | 6.7     | 3.4904 | 
| 2009 | LeBron James          | 28.4   | 7.6      | 7.2     | 3.3874 | 
| 2013 | LeBron James          | 26.8   | 8        | 7.3     | 3.3405 | 
| 2020 | Giannis Antetokounmpo | 29.5   | 13.6     | 5.6     | 3.2035 | 
| 2018 | James Harden          | 30.4   | 5.4      | 8.8     | 2.9601 | 
| 2019 | Giannis Antetokounmpo | 27.7   | 12.5     | 5.9     | 2.916  | 
| 2000 | Shaquille O'Neal      | 29.7   | 13.6     | 3.8     | 2.9009 | 
| 2014 | Kevin Durant          | 32     | 7.4      | 5.5     | 2.8576 | 
| 2011 | Derrick Rose          | 25     | 4.1      | 7.7     | 2.759  | 
| 2010 | LeBron James          | 29.7   | 7.3      | 8.6     | 2.6684 | 
| 2007 | Dirk Nowitzki         | 24.6   | 8.9      | 3.4     | 2.599  | 
| 2001 | Allen Iverson         | 31.1   | 3.8      | 4.6     | 2.4869 | 
| 2015 | Stephen Curry         | 23.8   | 4.3      | 7.7     | 2.3975 | 
| 2012 | LeBron James          | 27.1   | 7.9      | 6.2     | 2.3731 | 
| 2017 | Russell Westbrook     | 31.6   | 10.7     | 10.4    | 2.2881 | 
| 2002 | Tim Duncan            | 25.5   | 12.7     | 3.7     | 2.203  | 
| 2003 | Tim Duncan            | 23.3   | 12.9     | 3.9     | 2.1901 | 
| 2004 | Kevin Garnett         | 24.2   | 13.9     | 5       | 2.1479 | 
| 2008 | Kobe Bryant           | 28.3   | 6.3      | 5.4     | 0.6903 | 
| 2005 | Steve Nash            | 15.5   | 3.3      | 11.5    | 0.5769 | 
| 2006 | Steve Nash            | 18.8   | 4.2      | 10.5    | 0.4307 | 

