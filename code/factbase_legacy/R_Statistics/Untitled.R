# 📦 加载必要包
library(dplyr)
library(tidyr)
library(purrr)
library(car)       # for leveneTest
library(FSA)       # for dunnTest
library(stats)

# ==== 路径设置 ====
base_path <- "C:/Users/numinose/Desktop/Trump in factbase/Trump Speech Study/txt_short_sampled/All_Statistics"
files <- list.files(base_path, pattern = "Dimensions_.*\\.csv$", full.names = TRUE)

# ==== 合并 Dimensions 数据 ====
extract_session <- function(filename) {
  if (grepl("First", filename)) return("First Session")
  if (grepl("Second", filename)) return("Second Session")
  if (grepl("Third", filename)) return("Third Session")
  return("Unknown")
}

read_and_clean <- function(file) {
  df <- read.csv(file)
  df <- head(df, -1)  # 删除总体均值行
  df$Session <- extract_session(file)
  return(df)
}

all_dims <- map_dfr(files, read_and_clean)
value_cols <- all_dims %>% select(where(is.numeric)) %>% colnames()

analyze_variable <- function(varname, alpha = 0.05) {
  df <- all_dims %>% select(all_of(varname), Session) %>% drop_na()
  colnames(df)[1] <- "Value"
  
  # ⬅️ Shapiro-Wilk 正态性检验
  shapiro_results <- df %>%
    group_by(Session) %>%
    summarise(p = tryCatch(shapiro.test(Value)$p.value, error = function(e) NA_real_)) %>%
    pull(p)
  
  shapiro_min <- min(shapiro_results, na.rm = TRUE)
  shapiro_pass <- all(shapiro_results > alpha, na.rm = TRUE)
  shapiro_note <- if (shapiro_pass) "All p > 0.05" else "At least one p < 0.05"
  
  # ⬅️ Levene’s Test
  levene_result <- tryCatch(leveneTest(Value ~ Session, data = df), error = function(e) NULL)
  levene_p <- if (!is.null(levene_result)) levene_result$`Pr(>F)`[1] else NA
  levene_pass <- !is.na(levene_p) && levene_p > alpha
  levene_note <- paste0("p = ", round(levene_p, 3))
  
  # 决策路径
  if (shapiro_pass && levene_pass) {
    test_used <- "ANOVA"
    test_reason <- "Normality + Variance OK"
    model <- aov(Value ~ Session, data = df)
    p_val <- summary(model)[[1]][["Pr(>F)"]][1]
    overall_sig <- ifelse(p_val < alpha, "Yes", "No")
    posthoc_method <- ifelse(p_val < alpha, "Tukey HSD", "")
    
    if (p_val < alpha) {
      tukey <- TukeyHSD(model)$Session
      results <- as.data.frame(tukey)
      results$Comparison <- rownames(results)
      results <- results %>%
        mutate(
          Variable = varname,
          TestUsed = test_used,
          Shapiro_Results = shapiro_note,
          Levene_Results = levene_note,
          TestDecisionReason = test_reason,
          OverallSig = overall_sig,
          PostHocMethod = posthoc_method,
          Shapiro_Min_P = shapiro_min,
          Levene_P = levene_p,
          P_Value = round(`p adj`, 4),
          Significant = ifelse(`p adj` < alpha, "Yes", "No"),
          Interpretation = paste(TestUsed, "used;", shapiro_note, ";", levene_note, ";",
                                 ifelse(`p adj` < alpha, "significant difference found", "no significant difference"))
        ) %>%
        select(Variable, TestUsed, Shapiro_Results, Levene_Results, TestDecisionReason, OverallSig,
               PostHocMethod, Comparison, Shapiro_Min_P, Levene_P, P_Value, Significant, Interpretation)
    } else {
      results <- tibble(
        Variable = varname,
        TestUsed = test_used,
        Shapiro_Results = shapiro_note,
        Levene_Results = levene_note,
        TestDecisionReason = test_reason,
        OverallSig = overall_sig,
        PostHocMethod = "",
        Comparison = "",
        Shapiro_Min_P = shapiro_min,
        Levene_P = levene_p,
        P_Value = p_val,
        Significant = "No",
        Interpretation = paste(test_used, "used;", shapiro_note, ";", levene_note, "; no significant difference")
      )
    }
    
  } else {
    test_used <- "Kruskal"
    test_reason <- if (!shapiro_pass) "Normality failed" else "Variance not equal"
    kw <- kruskal.test(Value ~ Session, data = df)
    p_val <- kw$p.value
    overall_sig <- ifelse(p_val < alpha, "Yes", "No")
    posthoc_method <- ifelse(p_val < alpha, "Dunn", "")
    
    if (p_val < alpha) {
      dunn <- dunnTest(Value ~ Session, data = df, method = "bonferroni")
      results <- dunn$res %>%
        mutate(
          Variable = varname,
          TestUsed = test_used,
          Shapiro_Results = shapiro_note,
          Levene_Results = levene_note,
          TestDecisionReason = test_reason,
          OverallSig = overall_sig,
          PostHocMethod = posthoc_method,
          Shapiro_Min_P = shapiro_min,
          Levene_P = levene_p,
          P_Value = round(P.adj, 4),
          Significant = ifelse(P.adj < alpha, "Yes", "No"),
          Interpretation = paste(test_used, "used;", shapiro_note, ";", levene_note, ";",
                                 ifelse(P.adj < alpha, "significant difference found", "no significant difference"))
        ) %>%
        select(Variable, TestUsed, Shapiro_Results, Levene_Results, TestDecisionReason, OverallSig,
               PostHocMethod, Comparison, Shapiro_Min_P, Levene_P, P_Value, Significant, Interpretation)
    } else {
      results <- tibble(
        Variable = varname,
        TestUsed = test_used,
        Shapiro_Results = shapiro_note,
        Levene_Results = levene_note,
        TestDecisionReason = test_reason,
        OverallSig = overall_sig,
        PostHocMethod = "",
        Comparison = "",
        Shapiro_Min_P = shapiro_min,
        Levene_P = levene_p,
        P_Value = p_val,
        Significant = "No",
        Interpretation = paste(test_used, "used;", shapiro_note, ";", levene_note, "; no significant difference")
      )
    }
  }
  
  return(results)
}

# 批量执行
all_results <- map_dfr(value_cols, analyze_variable)

# 输出路径
output_path <- "C:/Users/numinose/Desktop/dimensions_analysis_detailed.csv"
write.csv(all_results, output_path, row.names = FALSE)

# 查看部分结果
print(head(all_results, 5))

