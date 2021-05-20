/*
*  Name: Alfredo Mejia
*  Assg: Assignment 3 Part 1
*  Date: 11/9/20
*  Desc: The program will continously read from Twitter about a topic. These Twitter feeds will be analyzed for their
*        sentiment, and then analyzed using ElasticSearch. To exchange data between these two, you will use Kafka as a
*        broker.
 */


// Imports
package org.apache.spark.examples.streaming.twitter
package com.harpribot.corenlp_scala
import org.apache.log4j.{Level, Logger}
import org.apache.spark.streaming.{Seconds, StreamingContext}
import org.apache.spark.streaming.twitter._
import org.apache.spark.streaming
import org.apache.spark.SparkConf
import java.io.File
import java.nio.charset.Charset
import java.util.Properties
import com.google.common.io.Files
import edu.stanford.nlp.coref.CorefCoreAnnotations
import edu.stanford.nlp.ling.CoreAnnotations
import edu.stanford.nlp.neural.rnn.RNNCoreAnnotations
import edu.stanford.nlp.pipeline.{Annotation, StanfordCoreNLP}
import edu.stanford.nlp.sentiment.SentimentCoreAnnotations
import edu.stanford.nlp.sentiment.SentimentCoreAnnotations.SentimentAnnotatedTree
import edu.stanford.nlp.util.CoreMap
import scala.collection.JavaConverters._
import akka.Done
import akka.stream.alpakka.elasticsearch.IncomingMessage
import akka.stream.alpakka.elasticsearch.scaladsl.ElasticsearchSink
import akka.stream.alpakka.slick.javadsl.SlickSession
import akka.stream.alpakka.slick.scaladsl.Slick
import org.apache.http.HttpHost
import org.elasticsearch.client.RestClient
import playground.elastic.ElasticsearchMock
import playground.{ActorSystemAvailable, ElasticSearchEmbedded}
import spray.json.DefaultJsonProtocol._
import spray.json.JsonFormat
import scala.concurrent.Future
import scala.concurrent.duration._

// Object
object TweetAnalysis {
  // Main function
  def main(args: Array[String]): Unit = {
    // Check if args pass is correct
    if (args.length < 4) {
      System.err.println("Usage: TwitterPopularTags <consumer key> <consumer secret> " +
        "<access token> <access token secret>")
      System.exit(1)
    }

    // Set logging level if log4j not configured (override by adding log4j.properties to classpath)
    if (!Logger.getRootLogger.getAllAppenders.hasMoreElements) {
      Logger.getRootLogger.setLevel(Level.WARN)
    }

    // Get keys
    val Array(consumerKey, consumerSecret, accessToken, accessTokenSecret) = args.take(4)

    // Set the system properties so that Twitter4j library used by twitter stream
    // can use them to generate OAuth credentials
    System.setProperty("twitter4j.oauth.consumerKey", consumerKey)
    System.setProperty("twitter4j.oauth.consumerSecret", consumerSecret)
    System.setProperty("twitter4j.oauth.accessToken", accessToken)
    System.setProperty("twitter4j.oauth.accessTokenSecret", accessTokenSecret)

    val sparkConf = new SparkConf().setAppName("TwitterAnalysis")

    // check Spark configuration for master URL, set it to local if not configured
    if (!sparkConf.contains("spark.master")) {
      sparkConf.setMaster("local[2]")
    }

    // Get data
    val ssc = new StreamingContext(sparkConf, Seconds(2))
    val stream = TwitterUtils.createStream(ssc, None, filters)
    val tweets = stream.flatMap(status => status.getText.split(" "))

    ssc.start()
    ssc.awaitTermination()

    // Get sentiment
    val sentiment = getSentiment(tweets)

    // Visualize Sentiment
    visualData(sentiment)
  }

  // Gets sentiments of the tweets
  def getSentiment(value: Any): List[Any] = {
    val props: Properties = new Properties()
    props.put("annotators", "tokenize, ssplit, parse, sentiment")

    val pipeline: StanfordCoreNLP = new StanfordCoreNLP(props)

    // create blank annotator
    val document1: Annotation = new Annotation(text1)
    val document2: Annotation = new Annotation(text2)

    // run all Annotators
    pipeline.annotate(document1)
    pipeline.annotate(document2)


    val sentences1: List[CoreMap] = document1.get(classOf[CoreAnnotations.SentencesAnnotation]).asScala.toList
    val sentences2: List[CoreMap] = document2.get(classOf[CoreAnnotations.SentencesAnnotation]).asScala.toList

    // Check if positive sentiment sentence is truly positive
    sentences1
      .map(sentence => (sentence, sentence.get(classOf[SentimentAnnotatedTree])))
      .map { case (sentence, tree) => (sentence.toString, determineSentiment(RNNCoreAnnotations.getPredictedClass(tree))) }
      .foreach(println)

    // Check if the negative sentiment sentence is truly negative
    sentences2
      .map(sentence => (sentence, sentence.get(classOf[SentimentAnnotatedTree])))
      .map { case (sentence, tree) => (sentence.toString, determineSentiment(RNNCoreAnnotations.getPredictedClass(tree))) }
      .foreach(println)

    return sentences1 + sentences2
  }

  // Helps determine the sentiment of the tweet
  def determineSentiment(sentiment: Int): String = sentiment match {
    case x if x == 0 || x == 1 => "Negative"
    case 2 => "Neutral"
    case x if x == 3 || x == 4 => "Positive"
  }

  // Visulaizes the data
  def visualData(sentiment: List[Any]): Unit = {
    implicit val session = SlickSession.forConfig("slick-h2-mem")

    implicit val client = RestClient.builder(new HttpHost("localhost", 9201)).build()
    implicit val format: JsonFormat[Tweet] = jsonFormat4(Tweet)

    val done: Future[Done] =
      Slick
        .source(TableQuery[Tweets].result)
        .map {
          case (id, tweet) => Tweet(id, tweet)
        }
        .map(tweet => IncomingMessage(Option(tweet.id).map(_.toString), tweet))
        .runWith(ElasticsearchSink.create[Tweet]("id", "tweet"))

    done.onComplete {
      case _ =>
        session.close()
        client.close()
        runner.close()
        runner.clean()
    }
  }
}
