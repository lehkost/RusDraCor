Drama Analysis
================
Ira Pavlova
08.05.2017

### This project is devoted to studying the evolution of Russian drama. The study is based on the Russian Drama Corpus which now contains 49 Russian plays encoded in TEI. The creation time of plays ranges from 1747 to 1925.

``` r
library(tidyverse)
library(plotly)
library(plotrix)
library(network)
library(sna)
library(GGally)
library(geomnet)
library(ggnetwork)
library(igraph)


setwd('/Users/IrinaPavlova/Desktop/Uni/Бакалавриат/2015-2016/Programming/github desktop/RusDraCor/Calculating_stuff_in_plays')
data = read.csv('calculations.csv', stringsAsFactors=FALSE)
data = data.frame(data)
data[data=="empty weights"] <- 0
data[, 5:6] <- sapply(data[, 5:6], as.numeric)
data
```

### This graph shows how the number of characters in plays was changing from 1750 to 1950. The observations are the mean number of characters in plays of a particular year.

``` r
char_data <- aggregate(data[, 4], list(Year_of_creation=data$Year_of_creation), mean)
BG <- subset(char_data, Year_of_creation == "1825")

char_data %>% ggplot(aes(Year_of_creation, x)) +
  geom_point() +
  geom_line() + scale_x_continuous(breaks=seq(1700, 1950, 50)) +
  geom_text(data=BG, label="Boris Godunov", vjust=1) +
  labs(title='Number of characters in Russian drama',
       x='Number of characters', y='Year of creation')
```

![](Visualization_files/figure-markdown_github/unnamed-chunk-2-1.png)

### This graph shows how the number of scenes/acts in plays was changing from 1750 to 1950. The observations are the mean number of scenes/acts in plays of a particular year.

``` r
scenes_data <- aggregate(data[, 3], list(Year_of_creation=data$Year_of_creation), mean)

scenes_data %>% ggplot(aes(Year_of_creation, x)) +
  geom_point() +
  geom_line() + scale_x_continuous(breaks=seq(1700, 1950, 50)) +
  labs(title='Number of scenes/acts in Russian drama',
       x='Number of scenes/acts', y='Year of creation')
```

![](Visualization_files/figure-markdown_github/unnamed-chunk-3-1.png)

### This graph shows how the maximum degree of a character in plays was changing from 1750 to 1950. The observations are the mean number of max degree in plays of a particular year.

``` r
degree_data <- aggregate(data[, 6], list(Year_of_creation=data$Year_of_creation), mean)
BG <- subset(degree_data, Year_of_creation == "1825")

degree_data %>% ggplot(aes(Year_of_creation, x)) +
  geom_point() +
  geom_line() + scale_x_continuous(breaks=seq(1700, 1950, 50)) +
  geom_text(data=BG, label="Boris Godunov") +
  labs(title='Max character degree in Russian drama',
       x='Max degree', y='Year of creation')
```

![](Visualization_files/figure-markdown_github/unnamed-chunk-4-1.png)

### Making network visualization

``` r
boris_godunov <- read.csv('ready_CSV/Pushkin_-_Boris_Godunov.csv', sep = ";")
boris_godunov <- boris_godunov[, c(1, 3, 4)]
head(boris_godunov)
```

    ##           Source        Target weight
    ## 1         Bojare    Malchishka      1
    ## 2        Plennik   Samozvanets      1
    ## 3     Malchishki          Odin      1
    ## 4 Muzhiknaamvone       Pushkin      1
    ## 5       Grigorij Pervyjpristav      1
    ## 6        Nischij  Odiniznaroda      1

``` r
net <- graph_from_data_frame(d=boris_godunov, directed=F)
class(net)
```

    ## [1] "igraph"

``` r
E(net)$weight = boris_godunov$weight
E(net)
```

    ## + 385/385 edges (vertex names):
    ##  [1] Bojare        --Malchishka       Plennik       --Samozvanets     
    ##  [3] Malchishki    --Odin             Muzhiknaamvone--Pushkin         
    ##  [5] Grigorij      --Pervyjpristav    Nischij       --Odiniznaroda    
    ##  [7] Schelkalov    --Tretij           Ljah          --Vse             
    ##  [9] Kurbskij      --Pushkin          Feodor        --Tretij          
    ## [11] Boris         --Knjazvorotynskij Malchishki    --Drugoj          
    ## [13] Poet          --Vse              Samozvanets   --Vse             
    ## [15] Staruha       --Tretij           Jurodivyj     --Tretij          
    ## [17] Jurodivyj     --Chetvertyj       Semengodunov  --Tsar            
    ## [19] Gavrilapushkin--Vse              Poet          --Gavrilapushkin  
    ## + ... omitted several edges

``` r
plot(net, edge.arrow.size=.4,vertex.label=NA)
```

![](Visualization_files/figure-markdown_github/unnamed-chunk-5-1.png)

``` r
# net = network(boris_godunov, directed=FALSE)
# ggplot(data = boris_godunov, aes(from_id=Source, to_id=Target)) + geom_net(layout.alg = "kamadakawai", 
           # size = 2, labelon = TRUE, vjust = -0.6, ecolour = "grey60",
           # directed =FALSE, fontsize = 3, ealpha = 0.5)
```
