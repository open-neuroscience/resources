#' this script will take the csv files from plausible folder and collapse them by year
#' 
library(dplyr)
collapse_country_data <- function(year){
  stopifnot(dplyr::between(year, 2020, lubridate::year(lubridate::today())))
  csv_files <- list.files(path = "website/plausible/country_data/", 
                          pattern = as.character(year),
                          full.names = T)
  date_country <- fs::path_ext_remove(basename(csv_files))
  year_folder <- file.path("website/plausible/", as.character(year))
  fs::dir_create(year_folder)
  message("Reading data, this might take a while...")
  df <- purrr:::map(csv_files, vroom::vroom, col_types = readr::cols()) %>% 
    purrr::set_names(date_country) %>% 
    bind_rows(.id = "date_country") %>% 
    tidyr::separate(col = "date_country", into=c("date", "country"), sep = "_")
  message("Saving data")
  fn <- file.path(year_folder, glue::glue("{year}_country_data.Rdata"))
  save(df, file = fn)
  
} 
