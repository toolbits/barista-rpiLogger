package main
​
import (
	"bytes"
	"encoding/binary"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"math/rand"
	"net"
	"net/http"
	"os"
	"path"
	"strings"
	"time"
​
	"github.com/go-martini/martini"
)
​
const queueDir = "/var/lib/barista/queue"
​
func main() {
	rand.Seed(time.Now().UnixNano())
	go ping()
	go queue()
	listen()
}
​
func queue() {
	for {
		dir := queueDir
		list, err := ioutil.ReadDir(dir)
		if err != nil {
			log.Fatal(err)
		}
		for _, f := range list {
			if !f.IsDir() && strings.HasSuffix(f.Name(), ".json") {
				fpath := path.Join(dir, f.Name())
				b, err := ioutil.ReadFile(fpath)
				if err == nil {
					params := map[string]interface{}{}
					err := json.Unmarshal(b, &params)
					if err == nil {
						log.Print(params)
						resp, err := http.Post("http://vps.artsat.jp:51966/post/params.json", "application/json", bytes.NewReader(b))
						log.Print(resp, err)
					}
				}
				os.Remove(fpath)
			}
		}
		time.Sleep(5 * time.Second)
	}
}
​
func ping() {
	addr, err := net.ResolveUDPAddr("udp", "255.255.255.255:1900")
	if err != nil {
		log.Fatal(err)
	}
	c, err := net.DialUDP("udp", nil, addr)
	for {
		b := []byte("COFFEE-rasp")
		s := make([]byte, 4)
		binary.LittleEndian.PutUint32(s, rand.Uint32())
		c.Write(append(b, s...))
		time.Sleep(5 * time.Second)
	}
}
​
func listen() {
	m := martini.Classic()
	sensors := map[string]interface{}{}
​
	m.Post("/sensor", func(req *http.Request) string {
		params := map[string]interface{}{}
		d := json.NewDecoder(req.Body)
		err := d.Decode(&params)
		if err == nil {
			for k, v := range params {
				sensors[k] = v
			}
			log.Print(sensors)
		} else {
			log.Print(err)
		}
		return "ok"
	})
​
	m.Post("/params", func(req *http.Request) string {
		params := map[string]interface{}{}
		d := json.NewDecoder(req.Body)
		err := d.Decode(&params)
		if err == nil {
			b, err := hex.DecodeString(params["idhex"].(string))
			if err == nil {
				id := binary.LittleEndian.Uint64(b)
				delete(params, "idhex")
				params["id"] = fmt.Sprintf("%v", id)
				params["created"] = time.Now()
				for k, v := range sensors {
					params[k] = v
				}
				j, err := json.Marshal(params)
				if err == nil {
					name := queueDir + "/" + fmt.Sprintf("%v", id) + ".json"
					ioutil.WriteFile(name, j, 0666)
				} else {
					log.Print(err)
				}
			} else {
				log.Print(err)
			}
		} else {
			log.Print(err)
		}
		return "ok"
	})
	m.RunOnAddr(":51966")
}
