/*
* Author: Alfredo Mejia
* Date  : 10/21/20
* Class : CS 6350.002
* Descrp: This program will accept two command line arguments. The first command line argument will be the location
*         containing the tweets. The second command line argument would be the location of the output file. The program
*         first loads the data from the file specified. From the data it filters the out the rows that have null under
*         text. It then creates a pipeline with the following steps: removing stop words, tokenizing the text, term
*         hashing the words, and converting the sentiments (strings) to labels (numeric format). From this pipeline we
*         create a model with ParameterGridBuilder and do model testing with the cross validator class. The program then
*         creates a multiclassmetrics to get all the metrics from our model. These metrics are then outputted to an
*         output file specified in the second command line argument. This programs uses MLlib to get the necessary
*         classes. This programs follows the instructions detailed in the assignment 2 description.
 */

// Imports
import org.apache.spark.ml.Pipeline
import org.apache.spark.ml.classification.LogisticRegression
import org.apache.spark.ml.evaluation.MulticlassClassificationEvaluator
import org.apache.spark.ml.feature.{HashingTF, StopWordsRemover, StringIndexer, Tokenizer}
import org.apache.spark.ml.tuning.{CrossValidator, ParamGridBuilder}
import org.apache.spark.mllib.evaluation.MulticlassMetrics
import org.apache.spark.{SparkConf, SparkContext}
import org.apache.spark.sql.SparkSession

// tweets object
object tweets {

  /*
  * Funct: main
  * Input: Command line arguments | Array of Strings
  * Output: Nothing | Creates an output file
  * Descr: Implements the logistic regression to classify tweets via a pipeline and outputs the metrics to an output
  *        file.
   */
  def main(args: Array[String]): Unit = {
    // If number of arguments incorrect then exit
    if (args.length != 2) {
      println("Error. Invalid number of arguments.")
      System.exit(-1)
    }

    // Initialize Spark Context
    val conf = new SparkConf().setAppName("pageRank")
    val sc = new SparkContext(config = conf)

    // Create Spark Session
    val spark = SparkSession
      .builder()
      .appName("Assignment 2")
      .getOrCreate()

    // Import
    import spark.implicits._

    // Read the data and filter the tweets with null values
    val unfiltered_tweets = spark.read.option("header", "true").csv(args(0))
    val tweets_data = unfiltered_tweets.filter("text != 'null'")

    // Label conversion from string to numeric format
    val stringIndexer = new StringIndexer()
      .setInputCol("airline_sentiment")
      .setOutputCol("label")
    // Tokenize the text into words
    val tokenizer = new Tokenizer()
      .setInputCol("text")
      .setOutputCol("words")
    // Remove any stop words
    val stopWordsRemover = new StopWordsRemover()
      .setInputCol(tokenizer.getOutputCol)
      .setOutputCol("filtered_words")
    // Convert the words to term-frequency vector
    val hashingTF = new HashingTF()
      .setInputCol(tokenizer.getOutputCol)
      .setOutputCol("features")
    // Algorithm to use
    val lr = new LogisticRegression()

    // Create pipeline
    val pipeline = new Pipeline()
      .setStages(Array(stringIndexer, tokenizer, stopWordsRemover, hashingTF, lr))

    // Create parameter grid to evaluate different values at the same time
    val paramGrid = new ParamGridBuilder()
      .addGrid(hashingTF.numFeatures, Array(10, 100, 1000))
      .addGrid(lr.regParam, Array(0.1, 0.01, 0.001))
      .addGrid(lr.maxIter, Array(10, 50, 100))
      .build()

    // Create the cross validator to train and test the model
    val cv = new CrossValidator()
      .setEstimator(pipeline)
      .setEvaluator(new MulticlassClassificationEvaluator)
      .setEstimatorParamMaps(paramGrid)
      .setNumFolds(3)

    // Train and test the data
    val cvModel = cv.fit(tweets_data)
    val predictionDF = cvModel.transform(tweets_data)

    // Get the best parameters so it can be written to the file
    val bestParameters = cvModel.getEstimatorParamMaps.zip(cvModel.avgMetrics).maxBy((_._2))._1.toString()

    // Create a multiclassmetrics to be able to get the metrics
    val predictionAndLabels = predictionDF.select("prediction", "label").as[(Double, Double)].rdd
    val metrics = new MulticlassMetrics(predictionAndLabels)

    // Get the metrics and convert it to an RDD
    val metricsArray = writeMetrics(metrics, bestParameters)
    val metricsRDD = sc.parallelize(metricsArray)

    // Write the RDD to a file
    metricsRDD.saveAsTextFile(args(1))

  } // end of main

  /*
  * Funct: writeMetrics
  * Input: multiclassmetrics class & string containing the best parameters used
  * Output: Array of strings containing all the metrics as a string
  * Descr: Creates an array of string and appends all the metrics to you. It then returns the array to be converted to
  *        an RDD.
  */
  def writeMetrics(metrics: MulticlassMetrics, bestParameters: String): Array[String] = {

    // Convert metrics to string
    val accuracy = metrics.accuracy.toString
    val confusionMatrix = metrics.confusionMatrix.toString()
    val labels = metrics.labels

    // Create array and add the metrics
    var allMetrics = Array(
      "Best Parameters: \n" + bestParameters,
      "Overall Accuracy: " + accuracy,
      "Confusion Matrix: \n" + confusionMatrix
    )

    // Append more specific metrics based on label to the array
    labels.foreach { l =>
      allMetrics = allMetrics :+ s"Precision By Label $l: " + metrics.precision(l).toString
    }
    labels.foreach { l =>
      allMetrics = allMetrics :+ s"Recall By Label $l: " + metrics.recall(l).toString
    }
    labels.foreach { l =>
      allMetrics = allMetrics :+ s"False Positive Rate By Label $l: " + metrics.falsePositiveRate(l).toString
    }
    labels.foreach { l =>
      allMetrics = allMetrics :+ s"F1-Score By Label $l: " + metrics.fMeasure(l).toString
    }

    // Append more metrics to the array
    allMetrics = allMetrics :+ "Weighted Precision: " + metrics.weightedPrecision.toString
    allMetrics = allMetrics :+ "Weighted Recall: " + metrics.weightedRecall.toString
    allMetrics = allMetrics :+ "Weighted F1 Score: " + metrics.weightedFMeasure.toString
    allMetrics = allMetrics :+ "Weighted False Positive Rate: " + metrics.weightedFalsePositiveRate.toString

    // Return the array of strings (metrics)
    return allMetrics

  } // end writeMetrics
}
