library(tidyverse)
li <- list.files(pattern = ".csv")
df <- lapply(li, read_csv) %>% bind_rows()

# date ranges
date_range <- str_extract(range(df$time),
            pattern="[0-9]{4}-[0-9]{2}-[0-9]{2}")

# we switch dates from "yyyy-mm-dd" to "Month Year"
text_date <- format(lubridate::parse_date_time(date_range,
                                               orders = c("Y-m-d")),
       "%B %Y")

subtitle_period <- paste("Period:", text_date[1], "—", text_date[2])

caption_twitter <- "Source @openneurosci analytics"
### colors

twitter_blue <- "#1DA1F2"
twitter_black <- "#14171A"
twitter_gray <- "#657786"


ggplot(df, aes(impressions))+
  geom_histogram(color=twitter_black, fill=twitter_blue) +
  scale_x_continuous(breaks = seq(0,11000, 2000),
                     labels = scales::label_number_si())+
  ggthemes::theme_clean()+
  labs(title = "Views per tweet",
       subtitle = subtitle_period,
       caption = glue::glue(caption_twitter),
       y="Tweets", x=""
  )

ggsave("views_per_tweet.png", width=6, height=4, units = "in")
  

ggplot(df, aes(1, `engagement rate`))+
  geom_violin(fill=twitter_gray)+
  stat_summary(fun=mean)+
  scale_y_continuous(labels = scales::label_percent())+
  scale_x_continuous(limits=c(0,2), name = "")+
  ggthemes::theme_clean()+
  theme(axis.title.x=element_blank(),
        axis.text.x=element_blank(),
        axis.ticks.x=element_blank(),
        axis.line.x = element_blank())+
  labs(title="Engagement Rate", subtitle = subtitle_period)
  
p <- ggplot(df, aes(1:nrow(df),
               cumsum(impressions)))+
  geom_line(color=twitter_black, lwd=1)+
  ggthemes::theme_clean() +
  theme(plot.background = element_rect(color=NA))+
  scale_y_continuous(labels=scales::label_number_si())+
  labs(title="Cumulative tweet views",
       subtitle = subtitle_period,
       caption = caption_twitter,
       x= "Tweets", y="")

# add twitter logo...  
#cowplot::ggdraw(p)+
#  cowplot::draw_image("https://help.twitter.com/content/dam/help-twitter/brand/logo.png",
#                      scale = 0.3, y = -0.15, x=+0.4, clip = FALSE)


p
ggsave("cum_views_tweet.png", width=6, height=4, units = "in")

