/*
* Name: Alfredo Mejia
* Date: 11/9/20
* Assg: Assignment 3 Part 2
* Desc: In this program a GraphX graph will be constructed using Google's plus social network file. It will first load
*       data to an dataframe and it will then create a GraphFrame from it. Then it will perform a set of queries
*       specified in the assignment description. It will then output the results into a file. The program will take two
*       arguments, one for the input file and the other for the output file.
*
 */

// Imports
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions.desc
import org.apache.spark.{SparkConf, SparkContext}
import org.graphframes.GraphFrame

// Object
object SocialNetworks {
  // Main Function
  def main(args: Array[String]): Unit = {

    // Check the number of arguments. If invalid then exit
    if (args.length != 2){
      println("Error. Invalid number of arguments.")
      System.exit(-1)
    }

    // Create spark context
    val conf = new SparkConf().setAppName("Assignment3")
    val sc = new SparkContext(conf)

    // Read the file and get the unique ids
    val input = sc.textFile(args(0))
    val ids = input.flatMap(line => line.split("""\W+"""))
    val unique_vertices = ids.map(id => (id, 1)).reduceByKey((count1, count2) => count1 + count2)
    val vertices = unique_vertices.map( pair => pair._1)

    // Create the spark session
    val spark = SparkSession.builder
      .appName("Assignment3")
      .getOrCreate()

    import spark.implicits._

    // Create the dataframe for the edges
    val edges = spark.read.csv(args(0))

    // Create the GraphFrame
    val graph = GraphFrame(vertices.toDF(), edges)

    // Part A
    // Retrieve the top 5 nodes with the highest out degree along with the count of each node
    val outDeg = graph.outDegrees
    val outDegOutput = outDeg.select("id", "outDegree").orderBy(desc("outDegree")).show(5, false)

    // Part B
    // Retrieve the top 5 nodes with the highest in degree along with the count of each node
    val inDeg = graph.inDegrees
    val inDegOutput = inDeg.select("id", "outDegree").orderBy(desc("inDegree")).show(5, false)

    // Part C
    // Calculate PageRank for each of the nodes and output the top 5 nodes with the highest PageRank values
    val pageRank = graph.pageRank.resetProbability(0.15).tol(0.01).run()
    val pageRankOutput = pageRank.vertices.select("id", "pagerank").orderBy(desc("pagerank")).show(5)

    // Part D
    // Find the top 5 components with the largest number of nodes.
    val component = graph.connectedComponents.run()
    val componentOutput = component.select("id", "component").orderBy(desc("component")).show(5)

    // Part E
    // output the top 5 vertices with the largest triangle count
    val triangle = graph.triangleCount.run()
    val triangleOutput = triangle.select("id", "count").orderBy(desc("count")).show(5)

    // Add outputs to a single array
    val output = Array(outDegOutput.toString, inDegOutput.toString, pageRankOutput.toString, componentOutput.toString,
                       triangleOutput.toString)

    // Convert to RDD
    val outputRDD = sc.parallelize(output)

    // Write to File
    outputRDD.saveAsTextFile(args(1))
  }
}
