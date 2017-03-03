package main

import (
  "fmt"
  "net/http"
  "io"
  "io/ioutil"
  "os"
  "encoding/json"
)

const NODE_NEXT = "http://6857coin.csail.mit.edu:8080/next"
const NODE_ADD  = "http://6857coin.csail.mit.edu:8080/add"
const BLOCK_CONTENT = "Andrew Xia, Emily Mu, Akaki"

type Next_info struct{
  Parentid string
  Root string
  Difficulty int
  Timestamp int
  Nonce int
  Version int
}
type Block struct{
  version string
  root string // hash
  parentid string
  timestamp int
  difficulty int
}

func main() {
  fmt.Printf("Hello, world.\n")

  // resp, err := http.Get(NODE_NEXT)
  // fmt.Println("resp",resp.Body)  
  // io.Copy(os.Stdout, resp.Body)
  // if err != nil{
  //   fmt.Println("error")
  // }

  // hu := Next_info{}
  hu :=get_next()
  fmt.Println("hu",hu)

  // req, err := http.NewRequest("POST", NODE_ADD, nil)

  // new block

  // var jsonStr = []byte(`{"title":"Buy cheese and bread for breakfast."}`)
  // req, err := http.NewRequest("POST", url, bytes.NewBuffer(jsonStr))
  // req.Header.Set("X-Custom-Header", "myvalue")
  // req.Header.Set("Content-Type", "application/json")

  // x := make_block(block, block)
  // fmt.Println(x)

  // jsonValue, _ := json.Marshal(block)
  // resp, err := http.Post(NODE_ADD, "application/json", bytes.NewBuffer(jsonValue))

  // for {

  // }
}


func get_next() Next_info {
  resp, err := http.Get(NODE_NEXT)
  fmt.Println("get next")
  body, err := ioutil.ReadAll(resp.Body)
    // if err != nil {
  io.Copy(os.Stdout, resp.Body)
  var data Next_info //interface{} // TopTracks
  err = json.Unmarshal(body, &data)
  if err != nil {
      panic(err.Error())
  }
  fmt.Printf("Results: %v\n", data)
  // out.parentid = data.parentid


  return data
}

func make_block(next_info map[string]string, contents string) map[string]string{
  fmt.Println("yay")
  block := make(map[string]string) 
  block["version"] = next_info["version"]
  // block["root"] = hash_to_hex(contents)
  block["parentid"] = next_info["parentid"]
  block["timestamp"] = "time" // in some format
  block["difficulty"] = next_info["difficulty"]
  return block
} 

// func
