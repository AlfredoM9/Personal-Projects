name := "Assignment 2"

version := "0.1"

scalaVersion := "2.11.8"

val sparkVersion = "2.2.1"

libraryDependencies ++= Seq(
  "org.apache.spark" %% "spark-core" % sparkVersion,
  "org.apache.spark" %% "spark-sql" % sparkVersion,
  "org.apache.spark" %% "spark-mllib" % sparkVersion,
//  "org.apache.spark" %% "graphx" % sparkVersion,
  "org.apache.spark" %% "spark-sql-kafka-0-10" % sparkVersion,
  "org.apache.spark" %% "spark-streaming-kafka-0-10" % sparkVersion,
  "org.apache.spark" %% "spark-core" % sparkVersion,
  "org.apache.spark" %% "spark-streaming" % sparkVersion,
  "org.scala-lang" % "scala-library" % "2.11.12",
  "com.typesafe" % "config" % "1.3.4",
  "org.apache.kafka" %% "kafka" % "2.1.0",
  "org.twitter4j" % "twitter4j-core" % "3.0.3",
  "org.twitter4j" % "twitter4j-stream" % "3.0.3",
  "org.apache.bahir" %% "spark-streaming-twitter" % "2.3.2-SNAPSHOT",
  "com.typesafe" % "config" % "1.3.4"
)