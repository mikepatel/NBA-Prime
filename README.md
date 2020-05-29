# NBA-Prime
## Overview
* Building a data-driven model to find an NBA player's "prime"
* To create the ultimate system for power ranking the NBA's greatest players (e.g. Why is player X the 27th best player of all time, and player Y the 28th? What separates the two?)
* Sponsored by and providing model results and insights for the [Hard in the Paint NBA Podcast](https://soundcloud.com/engineers-play "Hard in the Paint NBA Podcast")
<a href="https://soundcloud.com/engineers-play">
  <img src="https://i1.sndcdn.com/avatars-000446326572-ycrzp2-t500x500.jpg" alt="Hard in the Paint NBA Podcast Logo" width="300"/>
</a>

## Data
* Using a variety of statistical metrics provided by Basketball Reference and NBA Stats
* Created and calculated a custom statistic called **M_VALUE** to measure an NBA player's prime

## Instructions
```
$ python model.py
```

## Results
* Visualization Coming Soon!
* Preliminary results can be found in [Results](https://github.com/mikepatel/NBA-Prime/tree/master/Results)

LeBron James Career Stats
![LBJ Raw Stats](https://github.com/mikepatel/NBA-Prime/blob/master/Results/LeBron%20James/LeBron%20James_Plots_Raw.png)


What is LeBron James' Prime? Check the table below to find out!

|Season |Age|Team|Points|Rebounds|Assists|FT%  |eFG% |PER |TS%  |M_VALUE|
|-------|---|----|------|--------|-------|-----|-----|----|-----|-------|
|2011-12|27 |MIA |27.1  |7.9     |6.2    |0.771|0.554|30.7|0.605|0.4707 |
|2012-13|28 |MIA |26.8  |8.0     |7.3    |0.753|0.603|31.6|0.64 |0.5467 |
|2013-14|29 |MIA |27.1  |6.9     |6.3    |0.75 |0.61 |29.3|0.649|0.4727 |


### Preliminary ranking of MVP winners since 2000
(2012 season was shortened)
| Year | Name                  | HITP Index | 
|------|-----------------------|------------| 
| 2016 | Stephen Curry         | 115.2      | 
| 2000 | Shaquille O'Neal      | 114.1      | 
| 2018 | James Harden          | 109.6      | 
| 2009 | LeBron James          | 109.2      | 
| 2013 | LeBron James          | 108.1      | 
| 2010 | LeBron James          | 106.6      | 
| 2019 | Giannis Antetokounmpo | 106.1      | 
| 2007 | Dirk Nowitzki         | 103.9      | 
| 2014 | Kevin Durant          | 103.9      | 
| 2015 | Stephen Curry         | 102.8      | 
| 2004 | Kevin Garnett         | 101.1      | 
| 2003 | Tim Duncan            | 100.1      | 
| 2002 | Tim Duncan            | 99.9       | 
| 2017 | Russell Westbrook     | 99.7       | 
| 2011 | Derrick Rose          | 98.8       | 
| 2008 | Kobe Bryant           | 97         | 
| 2001 | Allen Iverson         | 95.5       | 
| 2005 | Steve Nash            | 92.3       | 
| 2006 | Steve Nash            | 87.5       | 
| 2012 | LeBron James          | 87.2       | 
