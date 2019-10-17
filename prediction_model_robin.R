if(!require(rstudioapi))install.packages("rstudioapi")
library(rstudioapi)
if(!require(forecast))install.packages("forecast")
library(forecast)
if(!require(lmtest))install.packages("lmtest")
library(lmtest)
library(tidyverse)
library(data.table)
library(lubridate)
library(Metrics)
library(RcppRoll)
setwd('\\Users\\20166843\\Documents\\Studie\\Data Challenge 3\\Files')

###############################################################
############################# NEW MODEL #######################
###############################################################

data_select <- function(file, pump_station_name=NA) {
  df <- fread(file) %>%
    mutate(datetime = ymd_hms(datetime))
  if (is.na(pump_station_name)){
    print(unique(df[,'pump_station']))
    NA
  }
  
  level <- df %>%
    filter(pump_station == pump_station_name,
           measurement_type=='level') %>%
    filter(!is.na(rainfall_volume)) %>%
    select(year, month, day, hour, mean_value) %>%
    rename(level = mean_value)
    
  df <- df %>%
    filter(pump_station == pump_station_name,
           measurement_type == 'flow') %>%
    filter(!is.na(rainfall_volume)) %>%
    left_join(level) %>%
    mutate(level = replace_na(level,mean(level,na.rm=TRUE)))
  #%>%
  #  mutate(level=level$mean_value)
  df
}

fit_model <- function(df, threshold) {
  df <- df %>%
    mutate(rainfall_delay = pmin(threshold, rainfall_volume + pmax(0, replace_na(lag(rainfall_volume),0) - threshold))) %>%
    mutate(weekday = wday(datetime),
           rainfall_delay_lag1 = replace_na(lag(rainfall_delay, 1), 0),
           rainfall_delay_lag2 = replace_na(lag(rainfall_delay, 2), 0)) %>%
    mutate(warm = ifelse(month >= 5 & month <= 10, 1, 0))
  
  stl_data <- df[,'mean_value'] %>%
    ts(frequency = 24) %>% 
    stlf(h=24)
  
  autoplot(stl_data)
  
  df$stl_fitted <- as.vector(fitted(stl_data))
  df$stl_residuals <- as.vector(residuals(stl_data))
  print(summary(stl_data))
  
  lm_data <- lm(mean_value ~ stl_fitted + rainfall_delay_lag2, df)
  df$lm_fitted <- pmax(as.vector(fitted(lm_data)),0)
  df$lm_residuals <- as.vector(residuals(lm_data))
  print(rmse(df$lm_fitted, df$mean_value))
  print(summary(lm_data))
  
  df
}

df <- data_select('combined_data_files/flow_level_and_rain.csv', 'helftheuvelweg')

df_model <- fit_model(df, 3000) 
  

# Select model
ggplot(df_model, aes(x=lm_residuals)) +
  geom_histogram(bins=50)


lm_residuals = roll_mean(df_model$lm_residuals, 12)
stl_residuals = roll_mean(df_model$stl_residuals, 12)

ggplot(data.frame(lm_residuals), aes(x=lm_residuals)) +
  geom_histogram(bins=50)
print(sqrt(mean(lm_residuals**2)))
hist(stl_residuals)

ggplot(df_model, aes(x=mean_value, y=lm_residuals, color=mean_value_sd)) +
  geom_point(alpha=0.05)

ggplot(df_model, aes(x=stl_residuals, y=lm_residuals, color=mean_value_sd)) +
  geom_point(alpha=0.05)

ggplot(df_model, aes(x=stl_residuals, y=rainfall_volume, color=mean_value_sd)) +
  geom_point(alpha=0.05)

mstl_data <- df[,'mean_value'] %>%
  ts(frequency = 24)%>% 
  mstl()

#autoplot(mstl_data) +
#  xlim(500,576)

ggplot(df_model, aes(x=mean_value, y=lm_fitted, color=rainfall_volume)) +
  geom_point(alpha=0.1)
