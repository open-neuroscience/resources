get_credentials <- function(path){
  stopifnot(file.exists(path))
  credentials <- jsonlite::read_json(path)
  return(credentials)
}

query_plausible <- function(credentials, from, to, country_code, verbose=T){
  site_id <- credentials$site_id
  token <- credentials$token
  period <- glue::glue("&period=custom&date={from},{to}")
  metrics <- "&metrics=visitors"
  # after the metrics use ISO 3166-1 alpha-2 code of the visitor country
  filters <- glue::glue("&filters=visit:country%3D%3D{country_code}")
  
  # query has {site_id}{period}{metrics}{filters} kinda logic
  # mind the shQuote, the path has & onto it, so it will get terminated on command line without shQuotes
  query_type <- "https://plausible.io/api/v1/stats/timeseries?site_id="
  query <- glue::glue("{query_type}{site_id}{period}{metrics}{filters}")
  query <- shQuote(query, type="cmd") 
  auth <- shQuote(glue::glue('Authorization: Bearer {token}'), type="cmd")
  
  # build country destfile
  filename <- glue::glue("{from}_{country_code}.json")
  # expected to be working from metrics folder
  dest_file <- file.path(getwd(), "website/plausible/country_data/", filename)
  # build curl query
  final_query <- glue::glue("curl {query} -H {auth} > {dest_file}")
  if (verbose){
    message("Query API")
    cat(final_query)
  }

  system(final_query)
  
}

# This will create all months for the current year
library(tidyverse)
year_start <- lubridate::floor_date(Sys.Date(), "year")
month_start <- c(year_start, lubridate::add_with_rollback(year_start, months(1:11)))
# add one month
month_end <- month_start + months(1)
# remove one day
month_end <- lubridate::add_with_rollback(month_end, lubridate::days(-1))

countries <- countrycode::codelist$iso2c
countries <- countries[complete.cases(countries)]

# construct the data to query up to this date
data_to_query <-
tibble::tibble(month_start, month_end) %>% 
  filter(month_start < lubridate::floor_date(Sys.Date(), "month")) %>% 
  expand_grid(country_code = countries)


# API limits to 1000 queries per hour
# queries larger than that will probably fail...
if (nrow(data_to_query) > 1000) {
  message("Your data is too large, split!")
} else{
  purrr::pmap(data_to_query, 
              function(month_start, month_end, country_code) 
                query_plausible(credentials, from=month_start, to=month_end, 
                                country_code = country_code))
}



