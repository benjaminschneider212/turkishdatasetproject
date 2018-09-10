#Data file for Turkish MP dataset

#import libraries
library(readr)
library(haven)
library(dplyr)
library(ggplot2)

#read in datasets
TurkMP <- read_csv("~/Desktop/Pythonproject/pdfminer.six-20170720/TurkMP.csv")

#Data work, this creates numbers that I use in Table 2
glimpse(TurkMP)
kurdishmp<-TurkMP%>%
  filter(Kurdish==1)%>%
  arrange(Region,Parliament)%>%
  select(Region,Parliament,Year)


#Data found here was used for Table 1 of the poster
summary(TurkMP)


    