library("stringr")
library("emmeans")

# read.csv("data\\P01.csv")

files <- c('P01', 'P02', 'P03', 'P04', 'P05', 'P06', 'P07', 'P08', 'P09', 'P10')

condition <- array(NA, c(10, 54));
cond_type <- array(NA, c(10, 54));
cond_size <- array(NA, c(10, 54));
answer <- array(NA, c(10, 54, 2));
answer_sum <- array(NA, c(10, 3, 3, 2));



t_str = c("slide", "tap", "tap-and-hold")
s_str = c("2-4", "5-8", "9-12")

type_str <- array(t_str, c(3, 54));
size_str <- array(s_str, c(3, 54));

p_id = 1
for (f in files) {
  D = read.csv(str_c("data\\", f, ".csv", sep="", collapse=NULL), header=TRUE)
  condition[p_id,] <- (D[,2]-1)*3 + D[,3]
  cond_type[p_id,] <- type_str[D[,2]]
  cond_size[p_id,] <- size_str[D[,3]]
  
  answer[p_id,,] <-  t(D[,4:5])
  p_id = p_id + 1
}

# preprocessing
for (p_id in 1:10) {
  for (cond in 1:9) {
    idx <- which(condition[p_id,] %in% cond)
    t = cond_type[p_id, idx[1]]
    s = cond_size[p_id, idx[1]]
    answer_sum[p_id, t, s,] = colSums(answer[p_id, idx,], dims=1)
  }
}
#colnames(answer_sum) = c('slide24', 'slide58', 'slide912', 
##                         'tap24', 'tap58', 'tap912', 
#                         'tapnhold24', 'tapnhold58', 'tapnhold912')

colnames(answer_sum) = c('slide', 'tap', 'tapnhold')
rownames(answer_sum) = c('P01', 'P02', 'P03', 'P04', 'P05', 
                         'P06', 'P07', 'P08', 'P09', 'P10')

dimnames(answer_sum)[[1]] <- c('P01', 'P02', 'P03', 'P04', 'P05', 
                               'P06', 'P07', 'P08', 'P09', 'P10')
dimnames(answer_sum)[[2]] <- c('slide', 'tap', 'tap-and-hold')
dimnames(answer_sum)[[3]] <- c('2-4', '5-8', '9-12')


df = as.data.frame.table(answer_sum)
model = glm(Freq ~ Var2*Var3,
            family = binomial(link = "logit"),
            data = df,
            weights = df$Freq)

model = glm(Var2~Var1, weights = Freq, family = binomial(), data=d)
summary(model)












# selection of the data
cond_type = array(cond_type)
cond_size = array(cond_size)
answer_type = array(answer[,, 1])

lm.D9 <- lm(answer_type ~ cond_type*cond_size)
lm.D90 <- lm(answer_type ~ cond_type*cond_size - 1) # omitting intercept
a = anova(lm.D9)
summary(lm.D9)


a2 <- aov(answer_type ~ cond_type * cond_size)


pairs(a, simple = 'cond_type', adjust = 'holm', type = 'response', infer = TRUE)


glm.D93 <- glm(
  answer_type ~ cond_type*cond_size,
  family = binomial(link = "logit"),
)

summary(glm.D93)
AIC(glm.D93)

lr.anova = anova(glm.D93, test="Chisq")
lr.anova







































