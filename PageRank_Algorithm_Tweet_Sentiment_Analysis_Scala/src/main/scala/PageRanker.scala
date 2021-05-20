import org.apache.spark.sql.catalyst.dsl.expressions.{DslExpression, StringToAttributeConversionHelper}
import org.apache.spark.sql.types.{IntegerType, StringType, StructField, StructType}
import org.apache.spark.sql.{Row, SparkSession}
import org.apache.spark.sql.{Encoder, Encoders}
import org.apache.spark.sql.functions.{collect_set, concat_ws, lit}


object PageRanker {
  def main(args: Array[String]): Unit = {

    if (args.length != 3) {
      println("Error. Invalid number of arguments.")
      System.exit(-1)
    }

    println(args(0))

    val spark = SparkSession.builder
      .master("local[*]")
      .appName("Assignment 2")
      .getOrCreate()

    val unfiltered_tripData = spark.read.option("header", "true").csv(args(0))
    val tripData = unfiltered_tripData.drop("_c2")

    val vertices = tripData.select("ORIGIN").distinct()
      .withColumnRenamed("ORIGIN", "vertices").union(tripData.select("DEST").distinct()
      .withColumnRenamed("DEST", "vertices")).distinct()


    val test = Seq(
      Row("n1","n2"),
      Row("n1","n4"),
      Row("n2","n3"),
      Row("n2","n5"),
      Row("n3","n4"),
      Row("n4","n5"),
      Row("n5","n1"),
      Row("n5","n3"),
      Row("n5","n2")
    )
    val someSchema = List (
      StructField("orig", StringType, true),
      StructField("dest", StringType, true)
    )
    val testDF = spark.createDataFrame(spark.sparkContext.parallelize(test),
      StructType(someSchema))

    testDF.filter("dest == 'n2'").show()

    val n1 = testDF.select("orig").distinct()
      .withColumnRenamed("orig", "vertices")

    val n2 = testDF.select("dest").distinct()
      .withColumnRenamed("dest", "vertices")

    val v1 = testDF.select("orig").distinct()
      .withColumnRenamed("orig", "vertices").union(testDF.select("dest").distinct()
      .withColumnRenamed("dest", "vertices")).distinct()

    val v2 = v1.withColumn("value", lit(1))

    // testDF.map(row => )

  }
}
