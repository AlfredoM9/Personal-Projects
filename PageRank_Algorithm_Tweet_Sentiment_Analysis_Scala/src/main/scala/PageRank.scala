/*
* Author: Alfredo Mejia
* Date  : 10/21/20
* Class : CS 6350.002
* Descrp: This program will accept three command line arguments. One for the location of the csv file containing the
*         the necessary data, the maxmium number of iterations to run, and the location of the output file: in that
*         order. The program will initialize the spark context and read from the file indicated. From the file it will
*         process the data and get all the edges of a vertex. From this the page rank algorithm will be implemented
*         with the initial page rank for each node to be 10, the alpha rate to be 0.15, and the number of iterations
*         indicated by the command line argument. Finally, the program will create an output file as indicated by the
*         argument containing the airport code and its page rank sorted by the page rank in a descending order. This
*         programs follows the instructions detailed in the assignment 2 description.
 */

// Imports
import org.apache.spark.{SparkConf, SparkContext}


// PageRank object
object PageRank {

  /*
  * Funct: main
  * Input: Command line arguments | Array of Strings
  * Output: Nothing | Creates an output file
  * Descr: Implements the page rank algorithm and creates an output file with the results
   */
  def main(args: Array[String]): Unit = {
    // If number of arguments incorrect then exit
    if (args.length != 3) {
      println("Error. Invalid number of arguments.")
      System.exit(-1)
    }

    // Initialize Spark Context
    val conf = new SparkConf().setAppName("pageRank")
    val sc = new SparkContext(config = conf)

    // Read in file
    val dataWithHead = sc.textFile(args(0))

    // Get rid of header
    val header = dataWithHead.first()
    val dataWOHead = dataWithHead.filter { row => row != header }

    // Tokenize the data
    val dataProcessed = dataWOHead.map(row => row.dropRight(1).replace("\"", "").split(','))
    val data = dataProcessed.map(row => (row(0), row(1)))

    // Aggregate all destinations to a particular origin
    val edges = data.reduceByKey((x, y) => x + " " + y)
    val edgesProcessed = edges.map(row => (row._1, row._2.split(' ')))

    // Add a default page rank value to each origin
    var pageRank = edgesProcessed.map(row => (row._1, (10.0, row._2)))

    // Initialize variables for page rank algorithm
    val alpha_val = 0.15
    val num_nodes = pageRank.count()


    // For each iteration
    for (x <- 0 to args(1).toInt) {
      // Divide the page rank of the origin with all its destination nodes
      val pageRank_map = pageRank.map(row =>
        for (dest <- row._2._2) yield {
          (dest, row._2._1 / row._2._2.length)
        }
      )

      // Flatten the arrays
      val pageRankFlatMap = pageRank_map.flatMap(row =>
        for (x <- row) yield {
          x
        }
      )

      // Aggregate all the sums of each node
      val ranks = pageRankFlatMap.reduceByKey((x, y) => x + y)

      // Add the other parameters of page rank
      val new_pageRank = ranks.map(row => (row._1, (alpha_val * (1 / num_nodes)) + (1 - alpha_val) * row._2))

      // Update the data with the new page rank for next iteration
      pageRank = new_pageRank.join(pageRank).map(row => (row._1, (row._2._1, row._2._2._2)))
    }

    // Map the data to only have the airport and page rank
    val pageRanker = pageRank.map(row => (row._1, row._2._1))

    // Sort by descending order
    val outputPageRanker = pageRanker.sortBy(row => row._2, ascending=false)

    // Create the output file and write the contents of the output page ranker into it
    outputPageRanker.saveAsTextFile(args(2))

  } // End of main

}