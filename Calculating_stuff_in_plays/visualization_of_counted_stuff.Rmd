---
title: "vizualization_of_counted_stuff"
output: html_document
---
```{r results='hide', warning=FALSE, message=FALSE}
library(tidyverse)
```

```{r}
data = read.csv('/Users/IrinaPavlova/Desktop/Uni/Бакалавриат/2015-2016/Programming/github desktop/RusDraCor/Calculating_stuff_in_plays/num_of_stuff_in_plays.csv')
```
```{r, echo=FALSE}
plot(data$Year_of_creation, data$Num_of_char)
abline(lm(data$Num_of_char~data$Year_of_creation))
```
