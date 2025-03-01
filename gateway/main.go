package main

import (
	"bytes"
	"encoding/json"
	"io/ioutil"
	"log"
	"net/http"
)

type NLPRequest struct {
	Text string `json:"text"`
}

type NLPResponse struct {
	Entities [][]string `json:"entities"`
}

func handler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Only POST requests allowed", http.StatusMethodNotAllowed)
		return
	}

	body, err := ioutil.ReadAll(r.Body)
	if err != nil {
		http.Error(w, "Invalid request", http.StatusBadRequest)
		return
	}

	resp, err := http.Post("http://localhost:8000/api/analyze/", "application/json", bytes.NewBuffer(body))
	if err != nil {
		http.Error(w, "Failed to reach NLP API", http.StatusInternalServerError)
		return
	}
	defer resp.Body.Close()

	var response NLPResponse
	err = json.NewDecoder(resp.Body).Decode(&response)
	if err != nil {
		http.Error(w, "Invalid response from NLP API", http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}

func main() {
	http.HandleFunc("/nlp", handler)
	log.Println("Gateway API running on :8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
