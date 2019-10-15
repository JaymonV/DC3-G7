if(!require(rstudioapi))install.packages("rstudioapi")
library(rstudioapi)
if(!require(forecast))install.packages("forecast")
library(forecast)
if(!require(lmtest))install.packages("lmtest")
library(lmtest)
library(ggplot2)
setwd(dirname(rstudioapi::getActiveDocumentContext()$path))

###############################################################
############################# NEW MODEL #######################
###############################################################

timeslot = 48

df <- read.csv('flow_level_and_rain.csv')

unique(df[,'pump_station'])

# Select model
df <- df[df['pump_station'] == 'helftheuvelweg' & df['measurement_type'] == 'flow',]

df[is.na(df[,'rainfall_volume']),'rainfall_volume'] <- 0
rainfall <- df[,'rainfall_volume']
flow_value <- df[,'mean_value']

df[,'datetime'] <- as.Date(df[,'datetime'])

df_ts <- ts(df[,'mean_value'], 
            start=min(df[,'datetime']))
df_ts_train <- window(df_ts, end=(31930-timeslot))
df_ts_test <- window(df_ts, start=(31931-timeslot))
rainfall_train <- c(0, rainfall[1:(14398-timeslot)])
rainfall_test <- rainfall[(14399-timeslot):14398]

lags <- rep(0, 175)
lags[167:175] <- NA
lags[24] <- NA

length(lags)

length(df_ts_train)
length(rainfall_train)

model <- Arima(df_ts_train, order=c(169, 1, 1), xreg=rainfall_train, method='CSS')

df_forecast <- forecast(model, df_ts_test, xreg=rainfall_test)
summary(df_forecast)

coeftest(model)

df[,'mean_value'] %>%
  ts(frequency = 24)%>% 
  stlf() %>% 
  autoplot() +
  xlim(595, 605)

df[,'mean_value'] %>%
  ts(frequency = 24)%>% 
  mstl() %>% 
  autoplot() +
  xlim(595, 605)

rain_df <- as.data.frame(list(rain=rainfall_test, Time=(31931-timeslot):31930))

acf(diff(df_ts,1))
df_aacf <- pacf(df_ts, lag=169)
autoplot(df_forecast) +
  xlim(32000-168, 31930)
plot(df_forecast)
