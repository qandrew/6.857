package main

import (
  "fmt"
  "net/http"
  "io"
  "io/ioutil"
  "os"
  "encoding/json"
  "encoding/hex"
  "github.com/lhecker/argon2"
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
  Version int
  Root string // hash
  Parentid string
  Timestamp int
  Difficulty int
}

func main() {
  fmt.Printf("Hello, world.\n")

  // resp, err := http.Get(NODE_NEXT)
  // fmt.Println("resp",resp.Body)  
  // io.Copy(os.Stdout, resp.Body)
  // if err != nil{
  //   fmt.Println("error")
  // }

  next :=get_next()
  block := make_block(next,BLOCK_CONTENT)
  fmt.Println("solving block")
  fmt.Println(block)
  // solve_block(&block)
  cfg := argon2.DefaultConfig()

  // var cfg Config
  // cfg.HashLength = 32
  // cfg.SaltLength = 8
  // cfg.TimeCost = 3
  // cfg.MemoryCost = 4096 // 1 << 12
  // cfg.Parallelism = 1
  // cfg.Mode = Mode(C.Argon2_id) // argon2.low_level.Type.D
  // cfg.Version = Version19


  var password = []byte("a")
  fmt.Printf("Hash:        %s\n", password)

  raw, err := cfg.Hash(password, []byte("somesalt"))
  if err != nil {
    fmt.Printf("Error during hashing: %s\n", err.Error())
    os.Exit(1)
  }

  // The Raw struct contains 3 members:
  //   - A reference to the Config which created it
  //   - The Hash
  //   - And the Salt
  // It also has a method to turn it into a encoded string.
  fmt.Printf("Hash:        %s\n", hex.EncodeToString(raw.Hash))


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
  return data
}

func make_block(next_info Next_info, contents string) Block{
  fmt.Println("yay")
  var block Block
  block.Version = next_info.Version
  // block["root"] = hash_to_hex(contents)
  block.Parentid = next_info.Parentid
  // block["timestamp"] = "time" // in some format
  block.Difficulty = next_info.Difficulty
  return block
} 

// func solve_block(*block Block) {

// }

// func
