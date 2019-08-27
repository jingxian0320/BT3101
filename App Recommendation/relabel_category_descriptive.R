### For external Data, Get a list of all category for references ###
### Tang Jiahui ###
### A0119415J ###

# To get a list of all app categories of external data
# as a reference to overall category relabelling

labels <- read.csv("label_categories.csv")
app_id <- read.csv("app_labels.csv")
apple <- read.csv("a0119415.csv")
category <- apple[,3]
all <- labels[,2]
summary(category)
summary(all)

relabels <- read.csv("relabel_categories.csv")
re_category <- relabels$new_category
summary(re_category)
