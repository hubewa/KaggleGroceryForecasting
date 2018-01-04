# general visualisation
library('ggplot2') # visualisation
library('scales') # visualisation
library('grid') # visualisation
library('gridExtra') # visualisation
library('RColorBrewer') # visualisation
library('corrplot') # visualisation

# general data manipulation
library('dplyr') # data manipulation
library('readr') # input/output
library('data.table') # data manipulation
library('tibble') # data wrangling
library('tidyr') # data wrangling
library('stringr') # string manipulation
library('forcats') # factor manipulation

# specific visualisation
library('ggfortify') # visualisation
library('ggrepel') # visualisation
library('treemapify') # visualisation
library('ggforce') # visualisation
library('ggridges') # visualization

# specific data manipulation
library('broom') # data wrangling
library('purrr') # string manipulation

# Date plus forecast
library('lubridate') # date and time
library('timeDate') # date and time


setwd("E:/KaggleComp/GrocerySalesForeCasting/data")

set.seed(1234)
#This reads data in
#train <- sample_frac(as_tibble(fread('train.csv')),0.1)
#train <- as_tibble(fread('20162017Datum.csv'))
train <- as_tibble(fread('itemsTrain.csv'))
test <- as_tibble(fread('test.csv'))
stores <- as_tibble(fread('stores.csv'))
items <- as_tibble(fread('items.csv'))
trans <- as_tibble(fread('transactions.csv'))
oil <- as_tibble(fread('oil.csv'))
holidays <- as_tibble(fread('holidays_events.csv'))



#look for dates with this feature
#train$date = as.POSIXct(train$date)
#newTrain = train[train$date >= as.POSIXct("2016-01-01"),]

#Now we create Validation data

#now we add new features. These features are from stores
train$city = stores$city[train$store_nbr]
train$state = stores$state[train$store_nbr]
train$type = stores$type[train$store_nbr]
train$cluster = stores$cluster[train$store_nbr]

#And these features are from families
#merge(items, train, by = "item_nbr") - NOTE DON'T DO THIS ON R. IT'S SLOW AS FUCK

train$class <- as.factor(train$class)
train$cluster <- as.factor(train$cluster)

trainExample <- train[train$item_nbr == 96995,]
trainExample <- trainExample[trainExample$store_nbr == 47,]

trainExample$date <- as.Date( trainExample$date)
trainExample$unit_sales <- as.integer(trainExample$unit_sales)
plot(trainExample$unit_sales ~ trainExample$date)
ggplot(data = trainExample, aes(date, unit_sales)) + geom_line() + geom_point()

#oil$date <- as.Date( oil$date)
#ggplot(data = oil, aes(date, dcoilwtico)) + geom_line() + geom_point()

#Now we create Validation data
sample <- sample.int(n = nrow(train), size = floor(.75*nrow(train)), replace = F)
newTrain <- train[sample,]
validate <- train[-sample,]

values <- tibble(validate$id, validate$unit_sales)
validate <- validate %>% select(-one_of("unit_sales"))

write_csv(newTrain, "newTrain.csv")
write_csv(values, "values.csv")
write_csv(validate, "validate.csv")

#initially, let's try a Linear model
#model <- lm(unit_sales ~ family, data = newTrain)

model.arima <- Arima(newTrain, order = c(0,0,2))

prediction1 <- predict(model, validate)

dataPrediction <- tibble(validate$id, prediction1)
write.csv(dataPrediction, "prediction1.csv")
