Drama Analysis
================
Ira Pavlova
May 2017

This project is devoted to studying the evolution of Russian drama. The study is based on the Russian Drama Corpus which now contains 49 Russian plays encoded in TEI. The creation time of plays ranges from 1747 to 1925.
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

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
library(tools)
library(gridExtra)

data = read.csv('calculations.csv', stringsAsFactors=FALSE)
data = data.frame(data)
data[data=="empty weights"] <- 0
data[, 5:6] <- sapply(data[, 5:6], as.numeric)
data
```

This graph shows how the distribution of number of segments (act/scenes) in plays from 1750 to 1950.
----------------------------------------------------------------------------------------------------

``` r
data %>% ggplot(aes(Year_of_creation, Num_of_scenes)) +
  geom_point(size=0.2) +geom_text(aes(label=Play),hjust=0, vjust=0, size=1.5) +
  scale_x_continuous(breaks=seq(1700, 1950, 50)) +
  labs(title='Number of scenes/acts in Russian drama',
       y='Number of segments', x='Year of creation')
```

![](Visualization_files/figure-markdown_github/unnamed-chunk-2-1.png)

This graph shows how the number of characters in plays was changing from 1750 to 1950. The observations are the mean number of characters in plays of a particular year.
------------------------------------------------------------------------------------------------------------------------------------------------------------------------

``` r
char_data <- aggregate(data[, 4], list(Year_of_creation=data$Year_of_creation), mean)
BG <- subset(char_data, Year_of_creation == "1825")

char_data %>% ggplot(aes(Year_of_creation, x)) +
  geom_point() +
  geom_line() + scale_x_continuous(breaks=seq(1700, 1950, 50)) +
  geom_text(data=BG, label="Boris Godunov", vjust=1) +
  labs(title='Number of characters in Russian drama',
       y='Number of characters', x='Year of creation')
```

![](Visualization_files/figure-markdown_github/unnamed-chunk-3-1.png) \# However, this graph does not show us much except the variaty of plays and absolute outliers. Maybe if we had around 300 plays we would see some stable development. As collecting the bigger corpus is work in progress, let's take a closer look at plays with more than 4 segments (act/scenes), exploring the distribution of number of characters for different groups of plays depending on the number of segments in these plays.

This graph shows how the number of characters in plays was changing from 1750 to 1950 for the plays with 4/10/20/30 or more segments.
-------------------------------------------------------------------------------------------------------------------------------------

``` r
char_data_4 <- subset(data, Num_of_scenes >= 4)

char_data_4 <- ggplot(char_data_4, aes(Year_of_creation, Num_of_char, label=Play)) +
  geom_point(size=0.2) + scale_x_continuous(breaks=seq(1700, 1950, 50)) +
  geom_text(aes(label=Play),hjust=0, vjust=0, size=1.5) +
  labs(title='in plays of 4 and more segments',
       y='Number of characters', x='Year of creation')

char_data_10 <- subset(data, Num_of_scenes >= 10)

char_data_10 <- ggplot(char_data_10, aes(Year_of_creation, Num_of_char, label=Play)) +
  geom_point(size=0.2) + scale_x_continuous(breaks=seq(1700, 1950, 50)) +
  geom_text(aes(label=Play),hjust=0, vjust=0, size=1.5) +
  labs(title='in plays of 10 and more segments',
       y='Number of characters', x='Year of creation')

char_data_20 <- subset(data, Num_of_scenes >= 20)

char_data_20 <- ggplot(char_data_20, aes(Year_of_creation, Num_of_char, label=Play)) +
  geom_point(size=0.2) + scale_x_continuous(breaks=seq(1700, 1950, 50)) +
  geom_text(aes(label=Play),hjust=0, vjust=0, size=1.5) +
  labs(title='in plays of 20 and more segments',
       y='Number of characters', x='Year of creation')

char_data_30 <- subset(data, Num_of_scenes >= 30)

char_data_30 <- ggplot(char_data_30, aes(Year_of_creation, Num_of_char, label=Play)) +
  geom_point(size=0.2) + scale_x_continuous(breaks=seq(1700, 1950, 50)) +
  geom_text(aes(label=Play),hjust=0, vjust=0, size=1.5) +
  labs(title='in plays of 30 and more segments',
       y='Number of characters', x='Year of creation')

grid.arrange(char_data_4,
              char_data_10,
              char_data_20,
              char_data_30,
              nrow=2, ncol=2,
             top="Number of charaters in Russian drama")
```

![](Visualization_files/figure-markdown_github/unnamed-chunk-4-1.png)

This graph shows how the maximum degree of a character in plays was changing from 1750 to 1950. The observations are the mean number of max degree in plays of a particular year.
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

``` r
degree_data <- aggregate(data[, 6], list(Year_of_creation=data$Year_of_creation), mean)
BG <- subset(degree_data, Year_of_creation == "1825")

degree_data %>% ggplot(aes(Year_of_creation, x)) +
  geom_point() +
  geom_line() + scale_x_continuous(breaks=seq(1700, 1950, 50)) +
  geom_text(data=BG, label="Boris Godunov") +
  labs(title='Max character degree in Russian drama',
       y='Max degree', x='Year of creation')
```

    ## Warning: Removed 1 rows containing missing values (geom_point).

![](Visualization_files/figure-markdown_github/unnamed-chunk-5-1.png)

Setting directories for CSV files to generate network graphs
------------------------------------------------------------

``` r
csv_list_ilibrary <- list.files('../TEI/current_CSV_files_extracted_from_TEI/ilibrary', full.names=T, pattern = "\\.csv$")

csv_list_wikisource <- list.files('../TEI/current_CSV_files_extracted_from_TEI/wikisource', full.names=T, pattern = "\\.csv$")
```

Making network visualization (ggplot)
-------------------------------------

``` r
make_ggplot_graphs <- function(input){
  
            output <- file_path_sans_ext(basename(file.path(input)))
            print(output)
            play <- read.csv(input, sep = ";")
            num_of_rows <- nrow(play)
            if(num_of_rows != 0)
            {
            play <- play[, c(1, 3, 4)]
            play
            
            ggplot(data = play, aes(from_id=Source, to_id=Target)) +
              geom_net(layout.alg ="kamadakawai", 
              size = 2, labelon = TRUE, vjust = -0.6, ecolour = "grey60",
              directed =FALSE, fontsize = 3, ealpha = 0.5) +
              labs(title=output)
            
            print(ggplot(data = play, aes(from_id=Source, to_id=Target)) +
              geom_net(layout.alg ="kamadakawai", 
              size = 2, labelon = TRUE, vjust = -0.6, ecolour = "grey60",
              directed =FALSE, fontsize = 3, ealpha = 0.5) +
              labs(title=output))

            ggsave(paste(output,".png"),
                   path= '../Calculating_stuff_in_plays/network_graphs/ggplot')
            
  } else {print('empty graph')}}

par(mfrow = c(7, 10)) 
for(file in csv_list_ilibrary) make_ggplot_graphs(file)
```

    ## [1] "Bulgakov_Dni_Turbinyh"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-8-1.png)

    ## [1] "Chehov_Chaika"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-8-2.png)

    ## [1] "Chehov_Djadja_Vanja"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-8-3.png)

    ## [1] "Chehov_Ivanov"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-8-4.png)

    ## [1] "Chehov_Leshii"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-8-5.png)

    ## [1] "Chehov_Medved"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-8-6.png)

    ## [1] "Chehov_Na_bolshoi_doroge"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-8-7.png)

    ## [1] "Chehov_Noch_pered_sudom"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-8-8.png)

    ## [1] "Chehov_Predlozhenie"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-8-9.png)

    ## [1] "Chehov_Svadba"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-8-10.png)

    ## [1] "Chehov_Tatjana_Repina"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-8-11.png)

    ## [1] "Chehov_Tragik_ponevole"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-8-12.png)

    ## [1] "Chehov_Tri_sestry"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-8-13.png)

    ## [1] "Chehov_Vishnevyi_sad"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-8-14.png)

    ## [1] "Fonvizin_Brigadir"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-8-15.png)

    ## [1] "Fonvizin_Nedorosl"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-8-16.png)

    ## [1] "Gogol_Lakeiskaja"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-8-17.png)

    ## [1] "Gogol_Otryvok"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-8-18.png)

    ## [1] "Gogol_Revizor"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-8-19.png)

    ## [1] "Gogol_Teatralnyi_razezd_posle_predstavlenija_novoi_komedii"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-8-20.png)

    ## [1] "Gogol_Tjazhba"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-8-21.png)

    ## [1] "Gogol_Utro_delovogo_cheloveka"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-8-22.png)

    ## [1] "Gogol_Zhenitba"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-8-23.png)

    ## [1] "Gorkij_Egor_Bulychov_i_drugie"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-8-24.png)

    ## [1] "Gorkij_Na_dne"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-8-25.png)

    ## [1] "Majakovskij_Banja"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-8-26.png)

    ## [1] "Ostrovskij_Bednost_ne_porok"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-8-27.png)

    ## [1] "Ostrovskij_Bespridannitsa"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-8-28.png)

    ## [1] "Ostrovskij_Groza"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-8-29.png)

    ## [1] "Ostrovskij_Snegurochka"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-8-30.png)

    ## [1] "Ostrovskij_Svoi_ljudi_-_sochtemsja"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-8-31.png)

    ## [1] "Ostrovskij_Svoi_ljudi_—_sochtemsja"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-8-32.png)

    ## [1] "Ostrovskij_Volki_i_ovtsy"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-8-33.png)

    ## [1] "Pushkin_Kamenniy_gost"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-8-34.png)

    ## [1] "Pushkin_Pir_vo_vremja_chumy"
    ## [1] "empty graph"
    ## [1] "Pushkin_Rusalka"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-8-35.png)

    ## [1] "Pushkin_Skupoj_rytsar"
    ## [1] "empty graph"
    ## [1] "Pushkin_Stseny_iz_rytsarskih_vremen"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-8-36.png)

``` r
for(file in csv_list_wikisource) make_ggplot_graphs(file)
```

    ## [1] "Blok_-_Balaganchik"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-8-37.png)

    ## [1] "Blok_-_Korol_na_ploschadi"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-8-38.png)

    ## [1] "Blok_-_Neznakomka"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-8-39.png)

    ## [1] "Chehov_-_Jubilej"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-8-40.png)

    ## [1] "Chehov_-_Medved'"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-8-41.png)

    ## [1] "Chehov_-_Na_bol'shoj_doroge"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-8-42.png)

    ## [1] "Chehov_-_Predlozhenie"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-8-43.png)

    ## [1] "Chehov_-_Svad'ba"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-8-44.png)

    ## [1] "Chehov_-_Tat'jana_Repina"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-8-45.png)

    ## [1] "Gogol'_-_Teatral'nyj_raz'ezd_posle_predstavlenija_novoj_komedii"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-8-46.png)

    ## [1] "Gumilyov_-_Akteon"
    ## [1] "empty graph"
    ## [1] "Gumilyov_-_Ditja_Allaha"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-8-47.png)

    ## [1] "Gumilyov_-_Don-Zhuan_v_Egipte"
    ## [1] "empty graph"
    ## [1] "Gumilyov_-_Gondla"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-8-48.png)

    ## [1] "Krylov_-_Amerikantsy"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-8-49.png)

    ## [1] "Krylov_-_Podschipa_ili_Trumf"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-8-50.png)

    ## [1] "Krylov_-_Sonnyj_poroshok_ili_pohischennaja_krestjanka"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-8-51.png)

    ## [1] "Plavil'schikov_-_Sgovor_Kutejkina"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-8-52.png)

    ## [1] "Prutkov_-_Chereposlov_sirech_Frenolog"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-8-53.png)

    ## [1] "Prutkov_-_Spor_drevnih_grecheskih_filosofov_ob_izjaschnom"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-8-54.png)

    ## [1] "Pushkin_-_Boris_Godunov"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-8-55.png)

    ## [1] "Pushkin_-_Kamennyj_gost"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-8-56.png)

    ## [1] "Pushkin_-_Skupoj_rytsar"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-8-57.png)

    ## [1] "Sumarokov_-_Dimitrij_Samozvanets"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-8-58.png)

    ## [1] "Sumarokov_-_Horev"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-8-59.png)

    ## [1] "Sumarokov_-_Semira"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-8-60.png)

    ## [1] "Tolstoy_A_-_Blondy"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-8-61.png)

    ## [1] "Turgenev_-_Gde_tonko,_tam_i_rvetsja"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-8-62.png)

    ## [1] "Turgenev_-_Nahlebnik"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-8-63.png)

    ## [1] "Turgenev_-_Neostorozhnost'"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-8-64.png)

    ## [1] "Turgenev_-_Provintsialka"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-8-65.png)

Making network visualization (igraph)
-------------------------------------

``` r
make_igraph_graphs <- function(input)
  {
            output <- file_path_sans_ext(basename(file.path(input)))
            print(output)
            play <- read.csv(input, sep = ";")
            num_of_rows <- nrow(play)
            if(num_of_rows != 0)
            {
              play <- play[, c(1, 3, 4)]
            play
net <- graph_from_data_frame(d=play, directed=F)
E(net)$weight <- play$Weight
# net <- network(play, directed=FALSE)

clust <- cluster_optimal(net)
modularity(clust)
membership(clust)

net

E(net)$weight > 1

# prettyColors <- c("turquoise4", "azure4", "olivedrab","deeppink4")
# communityColors <- prettyColors[membership(clust)]

layout = layout.fruchterman.reingold(net)

layout=layout.kamada.kawai(net, kkconst=50)

# vertex.label= ifelse(V(net)$name %in% c('Drugoj'),V(net)$name, NA)

filename= paste('../Calculating_stuff_in_plays/network_graphs/igraph/', output, '.png', sep='')

png(filename, width=3.25,height=3.25, units='in', res=600)

plot(net,
     vertex.size=3,
     edge.arrow.size=.6,
     vertex.label=V(net)$name,
     edge.width=E(net)$weight*0.5,
     layout=layout.graphopt,
     vertex.label.color = "black",
     vertex.label.cex = 0.5,
     vertex.color = membership(clust),
     vertex.label.dist=0.5,
     )
     
dev.off() }
            else {print('empty graph')
}}

for(file in csv_list_ilibrary) make_igraph_graphs(file)
```

    ## [1] "Bulgakov_Dni_Turbinyh"

    ## [1] "Chehov_Chaika"

    ## [1] "Chehov_Djadja_Vanja"

    ## [1] "Chehov_Ivanov"

    ## [1] "Chehov_Leshii"

    ## [1] "Chehov_Medved"

    ## [1] "Chehov_Na_bolshoi_doroge"

    ## [1] "Chehov_Noch_pered_sudom"

    ## [1] "Chehov_Predlozhenie"

    ## [1] "Chehov_Svadba"

    ## [1] "Chehov_Tatjana_Repina"

    ## [1] "Chehov_Tragik_ponevole"

    ## [1] "Chehov_Tri_sestry"

    ## [1] "Chehov_Vishnevyi_sad"

    ## [1] "Fonvizin_Brigadir"

    ## [1] "Fonvizin_Nedorosl"

    ## [1] "Gogol_Lakeiskaja"

    ## [1] "Gogol_Otryvok"

    ## [1] "Gogol_Revizor"

    ## [1] "Gogol_Teatralnyi_razezd_posle_predstavlenija_novoi_komedii"

    ## [1] "Gogol_Tjazhba"

    ## [1] "Gogol_Utro_delovogo_cheloveka"

    ## [1] "Gogol_Zhenitba"

    ## [1] "Gorkij_Egor_Bulychov_i_drugie"

    ## [1] "Gorkij_Na_dne"

    ## [1] "Majakovskij_Banja"

    ## [1] "Ostrovskij_Bednost_ne_porok"

    ## [1] "Ostrovskij_Bespridannitsa"

    ## [1] "Ostrovskij_Groza"

    ## [1] "Ostrovskij_Snegurochka"

    ## [1] "Ostrovskij_Svoi_ljudi_-_sochtemsja"

    ## [1] "Ostrovskij_Svoi_ljudi_—_sochtemsja"

    ## [1] "Ostrovskij_Volki_i_ovtsy"

    ## [1] "Pushkin_Kamenniy_gost"

    ## [1] "Pushkin_Pir_vo_vremja_chumy"
    ## [1] "empty graph"
    ## [1] "Pushkin_Rusalka"

    ## [1] "Pushkin_Skupoj_rytsar"
    ## [1] "empty graph"
    ## [1] "Pushkin_Stseny_iz_rytsarskih_vremen"

``` r
for(file in csv_list_wikisource) make_igraph_graphs(file)
```

    ## [1] "Blok_-_Balaganchik"

    ## [1] "Blok_-_Korol_na_ploschadi"

    ## [1] "Blok_-_Neznakomka"

    ## [1] "Chehov_-_Jubilej"

    ## [1] "Chehov_-_Medved'"

    ## [1] "Chehov_-_Na_bol'shoj_doroge"

    ## [1] "Chehov_-_Predlozhenie"

    ## [1] "Chehov_-_Svad'ba"

    ## [1] "Chehov_-_Tat'jana_Repina"

    ## [1] "Gogol'_-_Teatral'nyj_raz'ezd_posle_predstavlenija_novoj_komedii"

    ## [1] "Gumilyov_-_Akteon"
    ## [1] "empty graph"
    ## [1] "Gumilyov_-_Ditja_Allaha"

    ## [1] "Gumilyov_-_Don-Zhuan_v_Egipte"
    ## [1] "empty graph"
    ## [1] "Gumilyov_-_Gondla"

    ## [1] "Krylov_-_Amerikantsy"

    ## [1] "Krylov_-_Podschipa_ili_Trumf"

    ## [1] "Krylov_-_Sonnyj_poroshok_ili_pohischennaja_krestjanka"

    ## [1] "Plavil'schikov_-_Sgovor_Kutejkina"

    ## [1] "Prutkov_-_Chereposlov_sirech_Frenolog"

    ## [1] "Prutkov_-_Spor_drevnih_grecheskih_filosofov_ob_izjaschnom"

    ## [1] "Pushkin_-_Boris_Godunov"

    ## [1] "Pushkin_-_Kamennyj_gost"

    ## [1] "Pushkin_-_Skupoj_rytsar"

    ## [1] "Sumarokov_-_Dimitrij_Samozvanets"

    ## [1] "Sumarokov_-_Horev"

    ## [1] "Sumarokov_-_Semira"

    ## [1] "Tolstoy_A_-_Blondy"

    ## [1] "Turgenev_-_Gde_tonko,_tam_i_rvetsja"

    ## [1] "Turgenev_-_Nahlebnik"

    ## [1] "Turgenev_-_Neostorozhnost'"

    ## [1] "Turgenev_-_Provintsialka"
