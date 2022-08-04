# In blending problems, two or more raw materials are to be blended into one or more 
# finished goods, satisfying one or more quality requirements on the finished goods.
# In this example, the Chess Snackfoods Co. markets four brands of mixed nuts. 
# Each brand contains a specified ration of peanuts and cashews. 
# Chess has contracts with suppliers to receive 750 pounds of peanuts/day and 250 
# pounds of cashews/day. The problem is to determine the number of pounds of each brand
# to produce each day to maximize total revenue without exceeding the available supply
# of nuts.

# max p'x
# st Fx <= b
# x >= 0

# p - price that each brand sells for
# F - formula matrix F_ij number of nut_i needed in brand_j
# b - supply of each type of nut
# x - amount of each brand to produce

# Output: print out

# [1] "=============================================="
#    Brand Peanut_Count Cashews_Count  Produce
# 1   Pawn    721.15385      48.07692 769.2308
# 2 Knight      0.00000       0.00000   0.0000
# 3 Bishop      0.00000       0.00000   0.0000
# 4   King     28.84615     201.92308 230.7692
# [1] "=============================================="
# Total Peanuts :  750
# Total Cashews :  250
# Total Produced: 1000

# To run have the LINGO demo server running localy.
# Then run the command:
# Rscript path\to\Samples\chess.R

# The API root is set to root='http://localhost:8000' by defualt in main function.
# To install httr type in install.packages("httr") to an R console 




library(httr)
library(jsonlite)
library(glue)
# NUTS, BRANDS, SUPPLY, PRICE, FORMULA, PRODUCE
model <- function(root, NUTS, BRANDS, SUPPLY, PRICE, FORMULA, PRODUCE) {
    body = list(
        LINGO_script="chess.lng"
    )
    res <- POST(url = glue("{root}/model/"), body = body)
    model_id <- content(res)$model_id


    foo = list(list(
                pointer_pos= 1,
                model_id= model_id,
                pointer_name= "NUT",
                pointer_type= "SET",
                pointer_data= c(NUTS)
                ),
                list(
                pointer_pos= 2,
                model_id= model_id,
                pointer_name= "BRANDS",
                pointer_type= "SET",
                pointer_data= c(BRANDS)
                ),
            list(
                pointer_pos= 3,
                model_id= model_id,
                pointer_name= "SUPPLY",
                pointer_type= "PARAM",
                pointer_data= c(SUPPLY)
                ),
            list(
                pointer_pos= 4,
                model_id= model_id,
                pointer_name= "PRICE",
                pointer_type= "PARAM",
                pointer_data= c(PRICE)
                ),
            list(
                pointer_pos= 5,
                model_id= model_id,
                pointer_name= "FORMULA",
                pointer_type= "PARAM",
                pointer_data= c(FORMULA)
                ),
            list(
                pointer_pos= 6,
                model_id= model_id,
                pointer_name= "PRODUCE",
                pointer_type= "VAR",
                pointer_data= c(PRODUCE)
                ),
            list(
                pointer_pos= 7,
                model_id= model_id,
                pointer_name= "STATUS",
                pointer_type= "VAR",
                pointer_data= I(-1)
                )
    )
    res <- POST(url = glue("{root}/pointer/"), body = toJSON(foo, auto_unbox=TRUE), add_headers('Content-Type' = "application/json"))
    res <- PUT(url = glue("{root}/solve/{model_id}/"))
    res <- GET(url = glue("{root}/model_pointer/{model_id}/"))


    STATUS <- as.numeric(unlist(content(res)$pointers[[7]]$pointer_data))
    PRODUCE <- as.numeric(unlist(content(res)$pointers[[6]]$pointer_data))
    ERROR_MESSAGE <- content(res)$errorMessage


    return(list(
                STATUS=STATUS,
                ERROR_MESSAGE=ERROR_MESSAGE,
                PRODUCE=PRODUCE
                )
            )
}


root    <- "http://localhost:8000"
NUTS    <- c("Peanut","Cashew") 
nNUTS   <- length(NUTS)
BRANDS  <- c("Pawn","Knight","Bishop","King")
nBRANDS <- length(BRANDS)
SUPPLY  <- c(750,250)
PRICE   <- c(2,3,4,5)
FORMULA <- matrix(c(15,10, 6, 2,
                     1, 6,10,14), nrow=nBRANDS,ncol=nNUTS)
PRODUCE <- c(0,0,0,0)

returnData <- model(root, NUTS, BRANDS, SUPPLY, PRICE, FORMULA, PRODUCE)

if(returnData$ERROR_MESSAGE == "NONE") {
    Peanuts <- (FORMULA[,1]*returnData$PRODUCE)/16
    Cashews <- (FORMULA[,2]*returnData$PRODUCE)/16
    DT = data.frame(
        Brand = BRANDS,
        Peanut_Count = Peanuts,
        Cashews_Count = Cashews,
        Produce = returnData$PRODUCE
    )
    totalPeanuts  <- sum(DT$Peanut_Count)
    totalCashew   <- sum(DT$Cashews_Count)
    totalProduced <- sum(DT$Produce)
    print("==============================================")
    print(DT)
    print("==============================================")
    print(glue("Total Peanuts :  {totalPeanuts}"))
    print(glue("Total Cashews :  {totalCashew}"))
    print(glue("Total Produced: {totalProduced}"))
}