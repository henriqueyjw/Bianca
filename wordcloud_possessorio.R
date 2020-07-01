library(wordcloud)
library(readr)

setwd("E:/bianca/possessorio/")
freq = read_csv("frequencia_autor.csv")
freq = read_csv("frequencia_reu.csv")
set.seed(1234)
png("wordcloud.jpeg", width= 4,height=3, units='in', res=300)
wordcloud(words = freq$Term, freq = freq$Frequency, min.freq = 2,
          max.words=200, random.order=FALSE, rot.per=0.15, 
          colors=brewer.pal(8, "Dark2"))
dev.off()

