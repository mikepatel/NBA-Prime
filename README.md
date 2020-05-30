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


### Preliminary ranking of MVP winners since 2000 by HITP Index values
(2012 season was shortened)
| Year | Name                  | HITP Index | Points | Rebounds | Assists | Wins | 
|------|-----------------------|------------|--------|----------|---------|------| 
| 2000 | Shaquille O'Neal      | 2.6595     | 29.7   | 13.6     | 3.8     | 67   | 
| 2017 | Russell Westbrook     | 2.5751     | 31.6   | 10.7     | 10.4    | 47   | 
| 2016 | Stephen Curry         | 2.4903     | 30.1   | 5.4      | 6.7     | 73   | 
| 2018 | James Harden          | 2.4715     | 30.4   | 5.4      | 8.8     | 65   | 
| 2010 | LeBron James          | 2.4356     | 29.7   | 7.3      | 8.6     | 61   | 
| 2019 | Giannis Antetokounmpo | 2.4344     | 27.7   | 12.5     | 5.9     | 60   | 
| 2009 | LeBron James          | 2.3973     | 28.4   | 7.6      | 7.2     | 66   | 
| 2013 | LeBron James          | 2.3504     | 26.8   | 8        | 7.3     | 66   | 
| 2004 | Kevin Garnett         | 2.1692     | 24.2   | 13.9     | 5       | 58   | 
| 2014 | Kevin Durant          | 2.1276     | 32     | 7.4      | 5.5     | 59   | 
| 2002 | Tim Duncan            | 1.9743     | 25.5   | 12.7     | 3.7     | 58   | 
| 2003 | Tim Duncan            | 1.9586     | 23.3   | 12.9     | 3.9     | 60   | 
| 2015 | Stephen Curry         | 1.906      | 23.8   | 4.3      | 7.7     | 67   | 
| 2007 | Dirk Nowitzki         | 1.8576     | 24.6   | 8.9      | 3.4     | 67   | 
| 2011 | Derrick Rose          | 1.7748     | 25     | 4.1      | 7.7     | 62   | 
| 2008 | Kobe Bryant           | 1.7131     | 28.3   | 6.3      | 5.4     | 57   | 
| 2005 | Steve Nash            | 1.5926     | 15.5   | 3.3      | 11.5    | 62   | 
| 2001 | Allen Iverson         | 1.5112     | 31.1   | 3.8      | 4.6     | 56   | 
| 2012 | LeBron James          | 1.4827     | 27.1   | 7.9      | 6.2     | 46   | 
| 2006 | Steve Nash            | 1.4577     | 18.8   | 4.2      | 10.5    | 54   | 


