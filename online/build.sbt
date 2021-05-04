name := "online"

version := "0.1"

scalaVersion := "2.12.4"

val akkaHttpVersion = "10.2.4"
val akkaVersion    = "2.6.14"

libraryDependencies ++= Seq(
  "com.typesafe.akka" %% "akka-http"            % akkaHttpVersion,
  "com.typesafe.akka" %% "akka-actor-typed"     % akkaVersion,
  "com.typesafe.akka" %% "akka-stream"          % akkaVersion,
  "com.typesafe.akka" %% "akka-http-jackson"    % akkaHttpVersion,
  "ch.qos.logback"    % "logback-classic"       % "1.2.3",
//
//  "com.typesafe.akka" %% "akka-testkit"                 % akkaVersion     % Test,
//  "com.typesafe.akka" %% "akka-http-testkit"            % akkaHttpVersion % Test,
//  "com.typesafe.akka" %% "akka-actor-testkit-typed"     % akkaVersion     % Test,
//  "junit"              % "junit"                        % "4.12"          % Test,
//  "com.novocode"       % "junit-interface"              % "0.10"          % Test
)



