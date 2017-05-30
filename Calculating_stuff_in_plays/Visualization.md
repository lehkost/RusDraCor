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

This graph shows how the distribution of number of segments (act/scenes) in plays from 1750 to 1950 for three different genres -- comedy, tragedy and drama.
------------------------------------------------------------------------------------------------------------------------------------------------------------

``` r
subset(data, Genre=='comedy' | Genre=='tragedy' | Genre=='drama') %>% ggplot(aes(Year_of_creation, Num_of_scenes)) +
  geom_point(aes(color=Genre), size=2) + stat_ellipse(geom = "polygon", alpha=0.1, aes(color=Genre, fill=Genre)) +
  scale_x_continuous(breaks=seq(1700, 1950, 50)) +
  labs(title='Number of scenes/acts in Russian drama depending on genre',
       y='Number of segments', x='Year of creation')
```

![](Visualization_files/figure-markdown_github/unnamed-chunk-3-1.png)

This graph shows how the number of characters in plays was changing from 1750 to 1950.
--------------------------------------------------------------------------------------

``` r
BG <- subset(data, Play == "Pushkin_-_Boris_Godunov")
GT <- subset(data, Play == "Gogol_Teatralnyi_razezd_posle_predstavlenija_novoi_komedii")
GT1 <- subset(data, Play == "Gogol'_-_Teatral'nyj_raz'ezd_posle_predstavlenija_novoj_komedii")
SG <- subset(data, Play == "Ostrovskij_Snegurochka")

data %>% ggplot(aes(Year_of_creation, Num_of_char)) +
  geom_smooth(method='lm', color='black') +
  geom_point() + scale_x_continuous(breaks=seq(1700, 1950, 50)) +
  geom_text(data=BG, label="Boris Godunov", vjust=1, size=3) +
  geom_text(data=GT, label="Teatralnyi razezd posle predstavlenija novoi komedii", vjust=1, size=3) +
  geom_text(data=GT1, label="Teatralnyi razezd posle predstavlenija novoi komedii", vjust=1, size=3) +
  geom_text(data=SG, label="Snegurochka", vjust=1, size=3) +
  labs(title='Number of characters in Russian drama',
       y='Number of characters', x='Year of creation')
```

![](Visualization_files/figure-markdown_github/unnamed-chunk-4-1.png)

However, this graph does not tell us much except the variaty of plays and absolute outliers. Maybe if we had around 300 plays we would see some stable development. As collecting the bigger corpus is work in progress, let's take a closer look at plays with more than 4 segments (act/scenes), exploring the distribution of number of characters for different groups of plays depending on the number of segments in these plays.

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

![](Visualization_files/figure-markdown_github/unnamed-chunk-5-1.png)

This graph shows how the number of characters in plays was changing from 1750 to 1950 for three different genres -- comedy, tragedy and drama.
----------------------------------------------------------------------------------------------------------------------------------------------

``` r
subset(data, Genre=='comedy' | Genre=='tragedy' | Genre=='drama') %>% ggplot(aes(Year_of_creation, Num_of_char)) +
  geom_point(aes(color=Genre), size=2) + stat_ellipse(geom = "polygon", alpha=0.1, aes(color=Genre, fill=Genre)) +
  scale_x_continuous(breaks=seq(1700, 1950, 50)) +
  labs(title='Number of characters in Russian drama',
       y='Number of characters', x='Year of creation')
```

![](Visualization_files/figure-markdown_github/unnamed-chunk-6-1.png)

Setting directories for CSV files to generate network graphs
------------------------------------------------------------

``` r
csv_list_ilibrary <- list.files('../TEI/current_CSV_files_extracted_from_TEI/ilibrary', full.names=T, pattern = "\\.csv$")

csv_list_wikisource <- list.files('../TEI/current_CSV_files_extracted_from_TEI/wikisource', full.names=T, pattern = "\\.csv$")

csv_list_test <- list.files('../Calculating_stuff_in_plays/test_csvs', full.names=T, pattern = "\\.csv$")
```

Making network visualization (ggplot) -- basic "easy" graphs
------------------------------------------------------------

    ## [1] "Bulgakov_Dni_Turbinyh"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-9-1.png)

    ## [1] "Chehov_Chaika"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-9-2.png)

    ## [1] "Chehov_Djadja_Vanja"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-9-3.png)

    ## [1] "Chehov_Ivanov"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-9-4.png)

    ## [1] "Chehov_Leshii"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-9-5.png)

    ## [1] "Chehov_Medved"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-9-6.png)

    ## [1] "Chehov_Na_bolshoi_doroge"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-9-7.png)

    ## [1] "Chehov_Noch_pered_sudom"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-9-8.png)

    ## [1] "Chehov_Predlozhenie"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-9-9.png)

    ## [1] "Chehov_Svadba"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-9-10.png)

    ## [1] "Chehov_Tatjana_Repina"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-9-11.png)

    ## [1] "Chehov_Tragik_ponevole"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-9-12.png)

    ## [1] "Chehov_Tri_sestry"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-9-13.png)

    ## [1] "Chehov_Vishnevyi_sad"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-9-14.png)

    ## [1] "Fonvizin_Brigadir"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-9-15.png)

    ## [1] "Fonvizin_Nedorosl"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-9-16.png)

    ## [1] "Gogol_Lakeiskaja"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-9-17.png)

    ## [1] "Gogol_Otryvok"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-9-18.png)

    ## [1] "Gogol_Revizor"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-9-19.png)

    ## [1] "Gogol_Teatralnyi_razezd_posle_predstavlenija_novoi_komedii"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-9-20.png)

    ## [1] "Gogol_Tjazhba"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-9-21.png)

    ## [1] "Gogol_Utro_delovogo_cheloveka"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-9-22.png)

    ## [1] "Gogol_Zhenitba"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-9-23.png)

    ## [1] "Gorkij_Egor_Bulychov_i_drugie"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-9-24.png)

    ## [1] "Gorkij_Na_dne"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-9-25.png)

    ## [1] "Majakovskij_Banja"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-9-26.png)

    ## [1] "Ostrovskij_Bednost_ne_porok"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-9-27.png)

    ## [1] "Ostrovskij_Bespridannitsa"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-9-28.png)

    ## [1] "Ostrovskij_Groza"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-9-29.png)

    ## [1] "Ostrovskij_Snegurochka"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-9-30.png)

    ## [1] "Ostrovskij_Svoi_ljudi_-_sochtemsja"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-9-31.png)

    ## [1] "Ostrovskij_Svoi_ljudi_—_sochtemsja"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-9-32.png)

    ## [1] "Ostrovskij_Volki_i_ovtsy"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-9-33.png)

    ## [1] "Pushkin_Kamenniy_gost"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-9-34.png)

    ## [1] "Pushkin_Pir_vo_vremja_chumy"
    ## [1] "empty graph"
    ## [1] "Pushkin_Rusalka"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-9-35.png)

    ## [1] "Pushkin_Skupoj_rytsar"
    ## [1] "empty graph"
    ## [1] "Pushkin_Stseny_iz_rytsarskih_vremen"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-9-36.png)

    ## [1] "Blok_-_Balaganchik"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-9-37.png)

    ## [1] "Blok_-_Korol_na_ploschadi"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-9-38.png)

    ## [1] "Blok_-_Neznakomka"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-9-39.png)

    ## [1] "Chehov_-_Jubilej"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-9-40.png)

    ## [1] "Chehov_-_Medved'"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-9-41.png)

    ## [1] "Chehov_-_Na_bol'shoj_doroge"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-9-42.png)

    ## [1] "Chehov_-_Predlozhenie"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-9-43.png)

    ## [1] "Chehov_-_Svad'ba"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-9-44.png)

    ## [1] "Chehov_-_Tat'jana_Repina"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-9-45.png)

    ## [1] "Gogol'_-_Teatral'nyj_raz'ezd_posle_predstavlenija_novoj_komedii"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-9-46.png)

    ## [1] "Gumilyov_-_Akteon"
    ## [1] "empty graph"
    ## [1] "Gumilyov_-_Ditja_Allaha"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-9-47.png)

    ## [1] "Gumilyov_-_Don-Zhuan_v_Egipte"
    ## [1] "empty graph"
    ## [1] "Gumilyov_-_Gondla"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-9-48.png)

    ## [1] "Krylov_-_Amerikantsy"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-9-49.png)

    ## [1] "Krylov_-_Podschipa_ili_Trumf"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-9-50.png)

    ## [1] "Krylov_-_Sonnyj_poroshok_ili_pohischennaja_krestjanka"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-9-51.png)

    ## [1] "Plavil'schikov_-_Sgovor_Kutejkina"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-9-52.png)

    ## [1] "Prutkov_-_Chereposlov_sirech_Frenolog"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-9-53.png)

    ## [1] "Prutkov_-_Spor_drevnih_grecheskih_filosofov_ob_izjaschnom"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-9-54.png)

    ## [1] "Pushkin_-_Boris_Godunov"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-9-55.png)

    ## [1] "Pushkin_-_Kamennyj_gost"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-9-56.png)

    ## [1] "Pushkin_-_Skupoj_rytsar"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-9-57.png)

    ## [1] "Sumarokov_-_Dimitrij_Samozvanets"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-9-58.png)

    ## [1] "Sumarokov_-_Horev"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-9-59.png)

    ## [1] "Sumarokov_-_Semira"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-9-60.png)

    ## [1] "Tolstoy_A_-_Blondy"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-9-61.png)

    ## [1] "Turgenev_-_Gde_tonko,_tam_i_rvetsja"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-9-62.png)

    ## [1] "Turgenev_-_Nahlebnik"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-9-63.png)

    ## [1] "Turgenev_-_Neostorozhnost'"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-9-64.png)

    ## [1] "Turgenev_-_Provintsialka"

    ## Saving 7 x 5 in image

![](Visualization_files/figure-markdown_github/unnamed-chunk-9-65.png)

Making network visualization (igraph) with characters clustering
----------------------------------------------------------------

    ## [1] "Bulgakov_Dni_Turbinyh"

    ## NULL

![](Visualization_files/figure-markdown_github/unnamed-chunk-10-1.png)

    ## [1] "Chehov_Chaika"

    ## NULL

![](Visualization_files/figure-markdown_github/unnamed-chunk-10-2.png)

    ## [1] "Chehov_Djadja_Vanja"

    ## NULL

![](Visualization_files/figure-markdown_github/unnamed-chunk-10-3.png)

    ## [1] "Chehov_Ivanov"

    ## NULL

![](Visualization_files/figure-markdown_github/unnamed-chunk-10-4.png)

    ## [1] "Chehov_Leshii"

    ## NULL

![](Visualization_files/figure-markdown_github/unnamed-chunk-10-5.png)

    ## [1] "Chehov_Medved"

    ## NULL

![](Visualization_files/figure-markdown_github/unnamed-chunk-10-6.png)

    ## [1] "Chehov_Na_bolshoi_doroge"

    ## NULL

![](Visualization_files/figure-markdown_github/unnamed-chunk-10-7.png)

    ## [1] "Chehov_Noch_pered_sudom"

    ## NULL

![](Visualization_files/figure-markdown_github/unnamed-chunk-10-8.png)

    ## [1] "Chehov_Predlozhenie"

    ## NULL

![](Visualization_files/figure-markdown_github/unnamed-chunk-10-9.png)

    ## [1] "Chehov_Svadba"

    ## NULL

![](Visualization_files/figure-markdown_github/unnamed-chunk-10-10.png)

    ## [1] "Chehov_Tatjana_Repina"

    ## NULL

![](Visualization_files/figure-markdown_github/unnamed-chunk-10-11.png)

    ## [1] "Chehov_Tragik_ponevole"

    ## NULL

![](Visualization_files/figure-markdown_github/unnamed-chunk-10-12.png)

    ## [1] "Chehov_Tri_sestry"

    ## NULL

![](Visualization_files/figure-markdown_github/unnamed-chunk-10-13.png)

    ## [1] "Chehov_Vishnevyi_sad"

    ## NULL

![](Visualization_files/figure-markdown_github/unnamed-chunk-10-14.png)

    ## [1] "Fonvizin_Brigadir"

    ## NULL

![](Visualization_files/figure-markdown_github/unnamed-chunk-10-15.png)

    ## [1] "Fonvizin_Nedorosl"

    ## NULL

![](Visualization_files/figure-markdown_github/unnamed-chunk-10-16.png)

    ## [1] "Gogol_Lakeiskaja"

    ## NULL

![](Visualization_files/figure-markdown_github/unnamed-chunk-10-17.png)

    ## [1] "Gogol_Otryvok"

    ## NULL

![](Visualization_files/figure-markdown_github/unnamed-chunk-10-18.png)

    ## [1] "Gogol_Revizor"

    ## NULL

![](Visualization_files/figure-markdown_github/unnamed-chunk-10-19.png)

    ## [1] "Gogol_Teatralnyi_razezd_posle_predstavlenija_novoi_komedii"

    ## NULL

![](Visualization_files/figure-markdown_github/unnamed-chunk-10-20.png)

    ## [1] "Gogol_Tjazhba"

    ## NULL

![](Visualization_files/figure-markdown_github/unnamed-chunk-10-21.png)

    ## [1] "Gogol_Utro_delovogo_cheloveka"

    ## NULL

![](Visualization_files/figure-markdown_github/unnamed-chunk-10-22.png)

    ## [1] "Gogol_Zhenitba"

    ## NULL

![](Visualization_files/figure-markdown_github/unnamed-chunk-10-23.png)

    ## [1] "Gorkij_Egor_Bulychov_i_drugie"

    ## NULL

![](Visualization_files/figure-markdown_github/unnamed-chunk-10-24.png)

    ## [1] "Gorkij_Na_dne"

    ## NULL

![](Visualization_files/figure-markdown_github/unnamed-chunk-10-25.png)

    ## [1] "Majakovskij_Banja"

    ## NULL

![](Visualization_files/figure-markdown_github/unnamed-chunk-10-26.png)

    ## [1] "Ostrovskij_Bednost_ne_porok"

    ## NULL

![](Visualization_files/figure-markdown_github/unnamed-chunk-10-27.png)

    ## [1] "Ostrovskij_Bespridannitsa"

    ## NULL

![](Visualization_files/figure-markdown_github/unnamed-chunk-10-28.png)

    ## [1] "Ostrovskij_Groza"

    ## NULL

![](Visualization_files/figure-markdown_github/unnamed-chunk-10-29.png)

    ## [1] "Ostrovskij_Snegurochka"

    ## NULL

![](Visualization_files/figure-markdown_github/unnamed-chunk-10-30.png)

    ## [1] "Ostrovskij_Svoi_ljudi_-_sochtemsja"

    ## NULL

![](Visualization_files/figure-markdown_github/unnamed-chunk-10-31.png)

    ## [1] "Ostrovskij_Svoi_ljudi_—_sochtemsja"

    ## NULL

![](Visualization_files/figure-markdown_github/unnamed-chunk-10-32.png)

    ## [1] "Ostrovskij_Volki_i_ovtsy"

    ## NULL

![](Visualization_files/figure-markdown_github/unnamed-chunk-10-33.png)

    ## [1] "Pushkin_Kamenniy_gost"

    ## NULL

![](Visualization_files/figure-markdown_github/unnamed-chunk-10-34.png)

    ## [1] "Pushkin_Pir_vo_vremja_chumy"
    ## [1] "empty graph"
    ## [1] "Pushkin_Rusalka"

    ## NULL

![](Visualization_files/figure-markdown_github/unnamed-chunk-10-35.png)

    ## [1] "Pushkin_Skupoj_rytsar"
    ## [1] "empty graph"
    ## [1] "Pushkin_Stseny_iz_rytsarskih_vremen"

    ## NULL

![](Visualization_files/figure-markdown_github/unnamed-chunk-10-36.png)

    ## [1] "Blok_-_Balaganchik"

    ## NULL

![](Visualization_files/figure-markdown_github/unnamed-chunk-10-37.png)

    ## [1] "Blok_-_Korol_na_ploschadi"

    ## NULL

![](Visualization_files/figure-markdown_github/unnamed-chunk-10-38.png)

    ## [1] "Blok_-_Neznakomka"

    ## NULL

![](Visualization_files/figure-markdown_github/unnamed-chunk-10-39.png)

    ## [1] "Chehov_-_Jubilej"

    ## NULL

![](Visualization_files/figure-markdown_github/unnamed-chunk-10-40.png)

    ## [1] "Chehov_-_Medved'"

    ## NULL

![](Visualization_files/figure-markdown_github/unnamed-chunk-10-41.png)

    ## [1] "Chehov_-_Na_bol'shoj_doroge"

    ## NULL

![](Visualization_files/figure-markdown_github/unnamed-chunk-10-42.png)

    ## [1] "Chehov_-_Predlozhenie"

    ## NULL

![](Visualization_files/figure-markdown_github/unnamed-chunk-10-43.png)

    ## [1] "Chehov_-_Svad'ba"

    ## NULL

![](Visualization_files/figure-markdown_github/unnamed-chunk-10-44.png)

    ## [1] "Chehov_-_Tat'jana_Repina"

    ## NULL

![](Visualization_files/figure-markdown_github/unnamed-chunk-10-45.png)

    ## [1] "Gogol'_-_Teatral'nyj_raz'ezd_posle_predstavlenija_novoj_komedii"

    ## NULL

![](Visualization_files/figure-markdown_github/unnamed-chunk-10-46.png)

    ## [1] "Gumilyov_-_Akteon"
    ## [1] "empty graph"
    ## [1] "Gumilyov_-_Ditja_Allaha"

    ## NULL

![](Visualization_files/figure-markdown_github/unnamed-chunk-10-47.png)

    ## [1] "Gumilyov_-_Don-Zhuan_v_Egipte"
    ## [1] "empty graph"
    ## [1] "Gumilyov_-_Gondla"

    ## NULL

![](Visualization_files/figure-markdown_github/unnamed-chunk-10-48.png)

    ## [1] "Krylov_-_Amerikantsy"

    ## NULL

![](Visualization_files/figure-markdown_github/unnamed-chunk-10-49.png)

    ## [1] "Krylov_-_Podschipa_ili_Trumf"

    ## NULL

![](Visualization_files/figure-markdown_github/unnamed-chunk-10-50.png)

    ## [1] "Krylov_-_Sonnyj_poroshok_ili_pohischennaja_krestjanka"

    ## NULL

![](Visualization_files/figure-markdown_github/unnamed-chunk-10-51.png)

    ## [1] "Plavil'schikov_-_Sgovor_Kutejkina"

    ## NULL

![](Visualization_files/figure-markdown_github/unnamed-chunk-10-52.png)

    ## [1] "Prutkov_-_Chereposlov_sirech_Frenolog"

    ## NULL

![](Visualization_files/figure-markdown_github/unnamed-chunk-10-53.png)

    ## [1] "Prutkov_-_Spor_drevnih_grecheskih_filosofov_ob_izjaschnom"

    ## NULL

![](Visualization_files/figure-markdown_github/unnamed-chunk-10-54.png)

    ## [1] "Pushkin_-_Boris_Godunov"

    ## NULL

![](Visualization_files/figure-markdown_github/unnamed-chunk-10-55.png)

    ## [1] "Pushkin_-_Kamennyj_gost"

    ## NULL

![](Visualization_files/figure-markdown_github/unnamed-chunk-10-56.png)

    ## [1] "Pushkin_-_Skupoj_rytsar"

    ## NULL

![](Visualization_files/figure-markdown_github/unnamed-chunk-10-57.png)

    ## [1] "Sumarokov_-_Dimitrij_Samozvanets"

    ## NULL

![](Visualization_files/figure-markdown_github/unnamed-chunk-10-58.png)

    ## [1] "Sumarokov_-_Horev"

    ## NULL

![](Visualization_files/figure-markdown_github/unnamed-chunk-10-59.png)

    ## [1] "Sumarokov_-_Semira"

    ## NULL

![](Visualization_files/figure-markdown_github/unnamed-chunk-10-60.png)

    ## [1] "Tolstoy_A_-_Blondy"

    ## NULL

![](Visualization_files/figure-markdown_github/unnamed-chunk-10-61.png)

    ## [1] "Turgenev_-_Gde_tonko,_tam_i_rvetsja"

    ## NULL

![](Visualization_files/figure-markdown_github/unnamed-chunk-10-62.png)

    ## [1] "Turgenev_-_Nahlebnik"

    ## NULL

![](Visualization_files/figure-markdown_github/unnamed-chunk-10-63.png)

    ## [1] "Turgenev_-_Neostorozhnost'"

    ## NULL

![](Visualization_files/figure-markdown_github/unnamed-chunk-10-64.png)

    ## [1] "Turgenev_-_Provintsialka"

    ## NULL

![](Visualization_files/figure-markdown_github/unnamed-chunk-10-65.png)

In progress:
------------

Calculating degree for every charecter and plotting vertex size by degree.
==========================================================================

Improving graph appearance.
===========================

Figuring out how to plot all the networks graphs on a single plot.
==================================================================

Introducing more detailed analysis for authors and genres differencies.
=======================================================================
