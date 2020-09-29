


# Website analysis  -------------------------------------------------------

library(tidyverse)
library(sf)
library(rnaturalearth)

country_data <- read_csv("2020_march_sep_website_visits_country.csv")
# clean the column
country_data <- country_data %>% 
  separate(Visitors, into=c("views", "percent"), sep=" ") %>% 
  mutate(views= as.numeric(views),
         percent = parse_number(percent))


world <- ne_countries(scale = 'small', returnclass = 'sf')

world_robinson <- st_transform(world, crs = '+proj=robin +lon_0=0 +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m +no_defs')

# exclude antartica
world_robinson <- world_robinson %>% 
  filter(!str_detect(name, "Antarctica"))

filter(country_data, Country %in% world$name_long == FALSE) %>% 
  pull(Country)
# some of the countries are not on the world dataset 
# [1] "Hong Kong"                 "Korea"                    
# [3] "Singapore"                 "Viet Nam"                 
# [5] "Macao"                     "Iran, Islamic Republic Of"

country_data <- 
  mutate(country_data,
         name_long = case_when(
           Country == "Korea" ~ "South Korea",
           Country == "Iran, Islamic Republic Of" ~ "Iran",
           Country == "Viet Nam" ~ "Vietnam",
           # if nothing matches, keep the country
           TRUE ~ Country
         ))


ggplot() +
  geom_sf(data = world_robinson) +
  geom_sf(data = left_join(world_robinson, country_data),
          aes(fill=log10(views)),
          color="black",
          size=0.5, na.rm = TRUE)+
  labs(title = "Website visits",
       subtitle = "Period: May 2020 — Sep 2020") +
  ggthemes::theme_clean() +
  scale_fill_gradient(low="white", high="#F7490C",
                      na.value = "white") +
  # theme nothing
  theme(axis.line=element_blank(),
        axis.text.x=element_blank(),
        axis.text.y=element_blank(),
        axis.ticks=element_blank(),
        axis.title.x=element_blank(),
        axis.title.y=element_blank(),
        legend.position="bottom",
        legend.box.background = element_rect(colour = NA),
        legend.background = element_rect(colour = NA),
        legend.title = element_text(face="plain"),
        panel.background=element_blank(),
        panel.border=element_blank(),
        panel.grid.major=element_blank(),
        panel.grid.minor=element_blank(),
        plot.background=element_blank(),
        text = element_text(family="sans"))

ggsave("world_map.png", width=6, height=4, units = "in")


# Text analysis -----------------------------------------------------------
# adjust this to the place on the local machine with the website folder
post_paths <- list.dirs("/home/matias/Projects/academic-kickstart/content/en/post/")
posts <- sapply(post_paths, function(tt) list.files(tt, pattern = ".md", full.names = T))

post_list <- lapply(posts, read_lines)

txt <- unlist(post_list)

library(tidytext)

tidy_txt %>% 
  unnest_tokens(x) %>%
  count(book, word, sort = TRUE)


words <- tibble(line = 1:length(txt), text = txt) %>% 
  unnest_tokens(word, text)
# remove common words
data(stop_words)

# We need to add words that are common for us
our_stop_words <- tibble(word=c("title",
                                "categories", "admin", 
                                "http", "generated", "automatically", "author",
                                "https", "0", "1", "2","3","4","5","6","7","8","9",
                                "www.youtube.com",
                                "post", "layout", "nbsp", "div",
                                "chagas", "andina", "andré", "maia", "matias",
                                "01","02","03","04","05","06","07","08","09",
                                "2021","2020", "2019", "authors","tags","date"), lexicon="OPENNEURO")

tidy_words <- words %>%
  anti_join(bind_rows(stop_words, our_stop_words))

tidy_words %>%
  count(word, sort=TRUE) %>% 
  filter(n > 30) %>%
  mutate(word = reorder(word, n)) %>%
  ggplot(aes(word, n)) +
  geom_col() +
  xlab(NULL) +
  coord_flip()+
  labs(title="Most Common terms used in posts")

library(ggwordcloud)
tidy_words %>%
  count(word, sort=TRUE) %>% 
  filter(n > 30) %>%
  mutate(word = reorder(word, n))%>%
  ggplot() + 
  geom_text_wordcloud_area(aes(label = word, size = n)) +
  scale_size_area(max_size = 15)

tidy_txt <- tidy(txt)
tidy_txt %>% 
  filter(str_detect(x, "categories:")) %>% 
  mutate(x=str_remove(string = x, "categories: \\["),
         x=str_remove(string = x, "\\]"),
         x=str_remove_all(x, "\\'")) %>% 
  mutate(x = strsplit(x, ",")) %>% 
  unnest(x) %>% 
  mutate(x=gsub(pattern="^ ", replacement = "", x=x)) %>% 
  count(x, sort = TRUE) -> categories

categories %>% 
  ggplot(aes(fct_reorder(x, n), n)) +
  geom_col()+
  coord_flip()
