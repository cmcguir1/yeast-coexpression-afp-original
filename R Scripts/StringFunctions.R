find <- function(needle,haystack) {
  return(gregexpr(needle,haystack)[[1]][1])
}

rfind <- function(needle,haystack) {
  lst <- gregexpr(needle,haystack)[[1]]
  return(lst[length(lst)])
}