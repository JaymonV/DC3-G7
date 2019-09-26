setwd(dirname(rstudioapi::getActiveDocumentContext()$path))

if(!require(forecast))install.packages("forecast")
library(forecast)

if(!require(lmtest))install.packages("lmtest")
library(lmtest)

df <- read.csv('Export engelerschans flow.csv')

df[,'measurement_begin'] <- as.Date(df[,'measurement_begin'])

min_date = c(1975, 1)

df_ts <- ts(df[,'value'], 
          start=min(df[,'measurement_begin']))

df_ts2 <- df_ts - lag(df_ts, k=168)

df_pacf <- pacf(df_ts2, lag=48)

model <- arima(df_ts2, order=c(3,0,0), method="CSS",
               seasonal=list(order=c(0,1,1),period=168))

coeftest(model)