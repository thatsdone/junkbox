/**
 * mpmt1.scala: A Scala version of mpmt1
 *
 * STATUS:
 *  Under development
 * License:
 *   Apache License, Version 2.0
 * History:
 *   2022/01/01 v0.1 Initial version.
 * Author:
 *   Masanori Itoh <masanori.itoh@gmail.com>
 * TODO:
 *   * Write multi process version?
 */

//break requires scala 2.8 or later.
//import scala.util.control.Breaks._

object mpmt1 {
  def main(args: Array[String]) = {
    var num_context = 4
    var duration = 30
    var mode = "t"

    //Parse options.
    //NOTE(thatsdone): Avoided to use getopt pacakge for now.
    for (i <- 0 until args.length) {
      if (args(i) == "-n") {
        if (args(i + 1).startsWith("-")) {
          println("-n requires a value")
          sys.exit()
        }
        num_context = args(i + 1).toInt

      } else if (args(i) == "-d") {
        if (args(i + 1).startsWith("-")) {
          println("-d requires a value")
          sys.exit()
        }
        duration = args(i + 1).toInt
      } else if (args(i) == "-m") {
        //ignore at the moment
        if (args(i + 1).startsWith("-")) {
          println("-m requires a value")
          sys.exit()
        }
        //mode = args(i + 1)
        println("Currently -m option is ignored.")
      } else {
        //ignore at the moment
      }
    }

    printf("num_context: %d duration %d (s) mode: %s\n",
           num_context, duration, mode)

    val threads = {
      for (i <- 0 until num_context)
        yield new Thread(new BusyWorker(num_context, duration))
    }
    threads.foreach({
      t => t.start()
      println("Thread started: " + t)
    })
    threads.foreach({
      t => t.join()
      println("Thread completed: " + t)
    })
  }
}

class BusyWorker(num_context: Int, duration: Int) extends Runnable {

  def run() = {
    var ts_save = System.currentTimeMillis()
    var ts = ts_save
    //duration is in seconds. max is in milli-seconds
    val max = duration * 1000

    //Don't use Scala3 syntax for now.
    while ({
      ts = System.currentTimeMillis()
      (ts - ts_save) <= max
    }) ()
    //BTW, Scala does not have 'break'
    println("Expired! " + (ts - ts_save))
  }
}
