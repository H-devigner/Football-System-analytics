from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql.window import Window

class SeasonAnalyticsProcessor:
    def __init__(self):
        self.spark = SparkSession.builder \
            .appName("FootballSeasonAnalytics") \
            .config("spark.sql.warehouse.dir", "/user/hive/warehouse") \
            .config("spark.sql.streaming.checkpointLocation", "/tmp/checkpoint") \
            .enableHiveSupport() \
            .getOrCreate()

    def process_season_statistics(self, season):
        # Read historical match data
        matches_df = self.spark.read \
            .format("jdbc") \
            .option("url", "jdbc:mysql://localhost:3306/football_analytics") \
            .option("driver", "com.mysql.cj.jdbc.Driver") \
            .option("dbtable", "historical_matches") \
            .option("user", "your_username") \
            .option("password", "your_password") \
            .load() \
            .where(col("season") == season)

        # Calculate team performance metrics
        team_performances = matches_df \
            .groupBy("team_id", "team_name") \
            .agg(
            count("*").alias("matches_played"),
            sum(when(col("result") == "WIN", 3)
                .when(col("result") == "DRAW", 1)
                .otherwise(0)).alias("points"),
            sum(when(col("result") == "WIN", 1).otherwise(0)).alias("wins"),
            sum(when(col("result") == "DRAW", 1).otherwise(0)).alias("draws"),
            sum(when(col("result") == "LOSS", 1).otherwise(0)).alias("losses"),
            sum("goals_for").alias("goals_scored"),
            sum("goals_against").alias("goals_conceded"),
            avg("possession").alias("avg_possession"),
            avg("shots_on_target").alias("avg_shots_on_target")
        )

        # Calculate form over time
        window_spec = Window.partitionBy("team_id").orderBy("match_date").rowsBetween(-4, 0)
        form_df = matches_df \
            .withColumn("last_5_form",
                        collect_list("result").over(window_spec)) \
            .withColumn("form_points",
                        sum(when(col("result") == "WIN", 3)
                            .when(col("result") == "DRAW", 1)
                            .otherwise(0)).over(window_spec))

        # Save processed data
        team_performances.write \
            .mode("overwrite") \
            .saveAsTable("season_team_performances")

        form_df.write \
            .mode("overwrite") \
            .saveAsTable("season_team_form")

    def calculate_advanced_metrics(self, season):
        """Calculate advanced season metrics"""
        # Read base statistics
        stats_df = self.spark.table("season_team_performances")

        # Expected Goals (xG) analysis
        xg_df = stats_df \
            .withColumn("xG_per_shot",
                        col("goals_scored") / col("shots_on_target")) \
            .withColumn("xG_performance",
                        col("goals_scored") - col("expected_goals"))

        # Team playing style analysis
        style_df = self.spark.read.table("match_statistics") \
            .groupBy("team_id") \
            .agg(
            avg("pass_accuracy").alias("avg_pass_accuracy"),
            avg("tackles").alias("avg_tackles"),
            avg("possession").alias("avg_possession")
        ) \
            .withColumn("playing_style",
                        when(col("avg_possession") > 55, "Possession based")
                        .when(col("avg_tackles") > 20, "Defensive")
                        .otherwise("Balanced"))

        # Save advanced metrics
        xg_df.write.mode("overwrite").saveAsTable("season_advanced_metrics")
        style_df.write.mode("overwrite").saveAsTable("season_team_styles")

if __name__ == "__main__":
    processor = SeasonAnalyticsProcessor()
    processor.process_season_statistics("2023")
    processor.calculate_advanced_metrics("2023")