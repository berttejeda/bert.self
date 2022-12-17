package main

import (
  "fmt"
  "github.com/akamensky/argparse"
  "os"
)

func main() {
  // Create new parser object
  parser := argparse.NewParser("hell", "Says hello to specified name")
  // Create string flag
  s := parser.String("n", "name", &argparse.Options{Required: true, Help: "Name to greet"})
  // Parse input
  err := parser.Parse(os.Args)
  if err != nil {
    // In case of error print error and print usage
    // This can also be done by passing -h or --help flags
    fmt.Print(parser.Usage(err))
  }
  // Finally print the collected string
  fmt.Println(*s)
}  
