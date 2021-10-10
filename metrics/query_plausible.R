#' This function queries plausible
#' It saves data in the plausible directory

query_plausible <- function(){
  # plausible data 
  visitors_url <- "https://plausible.io/open-neuroscience.com/visitors.csv?period=custom&date={lubridate::today()}&from={from}&to={to}"
  
  # the actual info is buried here in a modal...to get the data by country we have to parse each country...
  codes <- countrycode::codelist$iso3c
  codes <- codes[complete.cases(codes)]
  # total views will have no filters
  no_filters <- "&filters={}"
  # create the filters using the country codes
  options(useFancyQuotes = FALSE)
  country_filters <- paste0("&filters={",
                            dQuote("country"),":",
                            dQuote(codes),
                            "}")

  dates_df <- tibble::tibble(
    from = seq(from = lubridate::floor_date(lubridate::ymd("2020-06-01"),
                                            "1 month"),
               to = lubridate::floor_date(
                 lubridate::add_with_rollback(lubridate::today(),
                                              months(-1)),
                 "1 month"),
               by = "1 month"),
    to = lubridate::add_with_rollback(from, months(1)))
  
  # we can use glue tidyeval to eval the thing inside {} on this mutate call
  query_df <- dplyr::mutate(dates_df,
                            url = glue::glue(visitors_url),
                            # we then paste the no filter
                            url = paste0(url, no_filters),
                            # we create filenames
                            # we should be working from "metrics folder"
                            fn = file.path(getwd(),
                                           "website",
                                           "plausible",
                                           paste0(from, "_visitors.csv"))
  )
  
  
  # total visitors data ----
  # we wrap the thing with file.exists to only query what's needed
  purrr::map2(query_df$url,
              query_df$fn,
              function(url, fn){
                if (file.exists(fn) == FALSE){
                  download.file(url, fn)
                  Sys.sleep(0.5)
                }
              })
  
  # country data ----
  if (dir.exists(file.path(getwd(), "website", "plausible", "country_data")) == FALSE){
    dir.create(file.path(getwd(), "website", "plausible", "country_data"))
  }
  
  country_df1 <- tidyr::expand_grid(dates_df,
                                    tibble::tibble(
                                      country_filters,
                                               codes))

  country_df2 <- dplyr::mutate(dates_df,
                               url = glue::glue(visitors_url))
  
  country_df <- dplyr::left_join(country_df1, country_df2, by=c("from", "to"))
  country_df <- dplyr::mutate(country_df,
                              url = paste0(url, country_filters),
                              fn = file.path(getwd(),
                                             "website",
                                             "plausible",
                                             "country_data",
                                             paste0(from, "_", codes, ".csv")))
  
  purrr::map2(country_df$url,
              country_df$fn,
              function(url, fn){
                if (file.exists(fn) == FALSE) {
                  # method = "curl" was failing....
                  download.file(url, fn, method = "wget")
                  #print(fn)
                  #print(url)
                  Sys.sleep(0.5)
                }
                }
              )
  
}

if (interactive()){
  message("Not calling query_plausible() because interactive session.\nYou can call it from the console")
} else {
  query_plausible()  
}
