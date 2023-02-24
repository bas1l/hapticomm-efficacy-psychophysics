library("stringr")
library("emmeans")
library("rstatix")
library("ggplot2")
library("tidyverse") 
library("agricolae") 

## INITIALISE VARIABLES
files <- c('P01', 'P02', 'P03', 'P04', 'P05', 'P06', 'P07', 'P08', 'P09', 'P10')
n_participant = length(files)
n_type = 3
n_size = 3
n_rep = 6
n_obs = n_type * n_size * n_rep  # number of observations per participant

condition <- array(NA, c(n_participant, n_obs));
cond_type <- array(NA, c(n_participant, n_obs));
cond_size <- array(NA, c(n_participant, n_obs));

answer_type <- array(NA, c(n_participant, n_obs));
answer_size <- array(NA, c(n_participant, n_obs));
answer_sum <- array(NA, c(n_participant, n_type, n_size));
answer_sum_c <- array(n_rep, c(n_participant, n_type, n_size));


## LOAD DATA
p_id = 0
for (f in files) {
  D = read.csv(str_c("data\\", f, ".csv", sep="", collapse=NULL), header=TRUE)
  
  condition[p_id,] <- (D[,2]-1)*3 + D[,3]
  cond_type[p_id,] <- D[,2]
  cond_size[p_id,] <- D[,3]
  
  answer_type[p_id,] <-  t(D[,4])
  answer_size[p_id,] <-  t(D[,5])
  p_id = p_id + 1
}


# SELECT WHICH ANSWER TO PROCESS
answer_selection = 0  # 1 = type, 0= size
if (answer_selection) {
  answer = answer_type
} else {
  answer = answer_size
}


# PREPROCESS DATA FOR THE ANOVA
# for each condition, sum the correct value to get n_correct for each cond*participant
for (p_id in 1:10) {
  for (cond in 1:9) {
    idx <- which(condition[p_id,] %in% cond)  # extract index of the condition
    t = cond_type[p_id, idx[1]]  # get type of the condition (1,2,3)
    s = cond_size[p_id, idx[1]]  # get size of the condition (1,2,3)
    answer_sum[p_id, t, s] = sum(answer[p_id, idx])
  }
}
dimnames(answer_sum)[[1]] <- c('P01', 'P02', 'P03', 'P04', 'P05', 
                               'P06', 'P07', 'P08', 'P09', 'P10')
dimnames(answer_sum)[[2]] <- c('slide', 'tap', 'tap-and-hold')
dimnames(answer_sum)[[3]] <- c('2-4', '5-8', '9-12')
answer_sum = answer_sum[,c(3,2,1),] # fits with previous graph

df = as.data.frame.table(answer_sum/6)
names(df) <- c("participant", "type", "size", "answer")
df_weight = as.data.frame.table(answer_sum_c)



## ANALYSING THE DATA
# Testing for sphericity and normality
anova_test(data=df, dv=answer, wid=participant, within=c(type,size))
df %>% group_by(type, size) %>% shapiro_test(answer)

# logit transform into anova 2-way rm
res.model = glm(answer ~ type*size,
            family = binomial(link = "logit"),
            data = df,
            weights = df_weight$Freq)
summary(res.model)
AIC(res.model)

res.df = anova(df, test="Chisq")
res.anova = anova(res.model, test="Chisq")
summary(res.anova)


emm <- emmeans(res.model, ~ type + size, type='response')  # confidence interval
pairs(emm, simple = 'type', adjust = 'holm', type = 'response', infer = TRUE)


## display the results
answer_selection = 1
if (answer_selection){  # meaning it's type answer
  p <- emm %>% as_tibble() %>%  ggplot(aes(x=type, y=prob, fill=size))
  col = "Blues"
} else {
  p <- emm %>% as_tibble() %>%  ggplot(aes(x=size, y=prob, fill=type))
  col = "Greens"
}

p <- p + geom_bar(stat="identity", color="black", linewidth=1.0, position=position_dodge()) +
    geom_errorbar(aes(ymin=asymp.LCL, ymax=asymp.UCL), linewidth=1.5, width=.2, position=position_dodge(.9)) + 
    theme_minimal()
p + scale_fill_brewer(palette=col)

# + theme(
#  plot.title = element_text(color="red", size=14, face="bold.italic"),
#  axis.title.x = element_text(color="blue", size=14, face="bold"),
#  axis.title.y = element_text(color="#993333", size=14, face="bold")
#)


#p + scale_fill_manual(values=c('#999999','#E69F00', '#82D45F'))















