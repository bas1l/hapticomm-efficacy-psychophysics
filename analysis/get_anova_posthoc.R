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

p_id = 0
for (f in files) {
  D = read.csv(str_c("data\\", f, ".csv", sep="", collapse=NULL), header=TRUE)
  condition[p_id,] <- (D[,2]-1)*3 + D[,3]
  cond_type[p_id,] <- type_str[D[,2]]
  cond_size[p_id,] <- size_str[D[,3]]
  
  answer[p_id,,] <-  t(D[,4:5])
  p_id = p_id + 1
}


cond_type = array(cond_type)
cond_size = array(cond_size)


# selection of the data
answer_type = array(answer[,, 2])


a2 <- aov(answer_type ~ cond_type * cond_size)
a2
summary(a2)
TukeyHSD(a2)




































