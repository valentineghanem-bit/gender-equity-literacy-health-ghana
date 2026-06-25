# Spatial cross-check (R / spdep) — independent confirmation of the Python centroid-KNN Moran's I.
# Reads the 261-district master, builds k-nearest-neighbour spatial weights from district
# centroids, and tests Global Moran's I for female illiteracy and poverty incidence.
suppressMessages({ library(spdep) })

dm <- read.csv("data/processed/district_master_261.csv")
coords <- as.matrix(dm[, c("lon", "lat")])

# k = 6 nearest neighbours, row-standardised (matches the Python pipeline)
knn <- knearneigh(coords, k = 6)
nb  <- knn2nb(knn)
lw  <- nb2listw(nb, style = "W")

for (v in c("illiteracy_rate", "poverty_incidence")) {
  mt <- moran.test(dm[[v]], lw, zero.policy = TRUE)
  cat(sprintf("Global Moran's I  %-18s I = %.3f   p = %.4g\n",
              v, mt$estimate[["Moran I statistic"]], mt$p.value))
}
