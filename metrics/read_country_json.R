read_country_json <- function(){
  filenames <- list.files(path = "website/plausible/country_data/",
                          pattern = "json", full.names = T)
  countries <- stringr::str_extract(filenames, "[A-Z]{2}.json")
  countries <- stringr::str_remove(countries, ".json")
    
  country_df <- 
  purrr::map(filenames,
         function(file) 
           jsonlite::read_json(file, simplifyVector = T) %>% 
           # we need to extract the results field
           .[["results"]]
         ) %>% 
    set_names(countries) %>% 
    bind_rows(.id="country_code")
  return(country_df)
}
