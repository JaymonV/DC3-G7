if(!require(rstudioapi))install.packages("rstudioapi")
library(rstudioapi)
if(!require(forecast))install.packages("forecast")
library(forecast)
if(!require(lmtest))install.packages("lmtest")
library(lmtest)

setwd(dirname(rstudioapi::getActiveDocumentContext()$path))

###############################################################
############################# NEW MODEL #######################
###############################################################

df <- read.csv('flow_level_and_rain.csv')

unique(df[,'pump_station'])

# Select model
df <- df[df[,'pump_station'] == 'helftheuvelweg',]

df[is.na(df[,'rainfall_volume']),'rainfall_volume'] <- 0
rainfall <- df[,'rainfall_volume']
flow_value <- df[,'mean_value']

df[,'datetime'] <- as.Date(df[,'datetime'])

df_ts <- ts(df[,'mean_value'], 
            start=min(df[,'datetime']))

lags <- rep(0, 171)
lags[167:171] <- NA
lags[24] <- NA

length(lags)

model <- Arima(df_ts, order=c(169, 0, 0), xreg=rainfall, method='CSS', fixed=lags)

coeftest(model)

df_aacf <- pacf(df_ts, lag=169)