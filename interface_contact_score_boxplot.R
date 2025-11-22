library(ggplot2)
library(svglite)
library(extrafont)
library(forcats)
font_import(pattern = "Arial")
loadfonts(device = "win")
library(gridExtra)
library(dplyr)

data_frame <- "C:/Users/selcuk.1/OneDrive - The Ohio State University/Desktop/dimer project/boxplot_data_II.csv"
md_data <- read.csv(data_frame)

# set order first on original labels
md_data$Mutation <- factor(md_data$Mutation,
                           levels = c("WT_II", "V34A_II", "S41A_II",
                                      "V34A_S41A_II", "F49A_II"))

label_mapping <- c("WT_II" = "WT",
                   "V34A_II" = "V34A",
                   "S41A_II" = "S41A",
                   "V34A_S41A_II" = "V34A-S41A",
                   "F49A_II" = "F49A")

md_data$Mutation <- recode(md_data$Mutation, !!!label_mapping)

# refactor to keep the same order but with new labels
md_data$Mutation <- factor(md_data$Mutation,
                           levels = c("WT", "V34A", "S41A", "V34A-S41A", "F49A"))

# Perform ANOVA
anova_result <- aov(Contact.Score ~ Mutation, data = md_data)

# Display the summary of the ANOVA result
summary(anova_result)

# If the ANOVA result is significant, you can perform a post-hoc test to identify which groups are different
if(summary(anova_result)[[1]][["Pr(>F)"]][1] < 0.05) {
  # Post-hoc test (Tukey's HSD)
  tukey_result <- TukeyHSD(anova_result)
  print(tukey_result)
}




p <- ggplot(md_data, aes(x = Mutation, y = Contact.Score, colour = Mutation)) +
  geom_boxplot(
    alpha = 0.5,
    outlier.shape = NA,
    fill = NA,
    lwd = 0.8,
    fatten = 1
  ) +
  geom_point(
    position = position_jitter(width = 0.15, height = 0),
    alpha = 0.5,
    size = 3
  ) +
  scale_color_manual(values = c("#78A1BB","#BFA89E","#C33C54","#033860","#E2B6CF")) +
  ylab("Interface Contact Score") +
  theme(
    text = element_text(size = 18, family = "Arial"),
    panel.grid.major = element_blank(),
    panel.grid.minor = element_blank(),
    panel.background = element_blank(),
    axis.line.y = element_line(colour = "black"),
    axis.title.x = element_blank(),
    axis.ticks.x = element_blank(),
    axis.text.y = element_text(size = 20, colour = "black"),
    axis.text.x = element_text(size = 20, colour = "black"),
    legend.position = "none"
  )

print(p)

ggsave(
  "C:/Users/selcuk.1/OneDrive - The Ohio State University/Desktop/dimer project/MD_boxplot.svg",
  plot = p, width = 9, height = 6
)
