package main

import (
	"net/http"
	"log"
	"io/ioutil"
	"crypto/sha1"
	"encoding/base64"
	"html/template"
	"encoding/json"
)



type handler struct {
	*Config
	H func(*Config, http.ResponseWriter, *http.Request) (int, error)
}

func (h handler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	if status, err := h.H(h.Config, w, r); err != nil {
		log.Println(err)
		switch status {
		case http.StatusNotFound:
			http.Error(w, http.StatusText(http.StatusNotFound), http.StatusNotFound)
		case http.StatusUnauthorized:
			http.Error(w, http.StatusText(http.StatusUnauthorized), http.StatusUnauthorized)
		case http.StatusInternalServerError:
			http.Error(w, http.StatusText(http.StatusInternalServerError), http.StatusInternalServerError)
		default:
			http.Error(w, http.StatusText(http.StatusInternalServerError), http.StatusInternalServerError)
		}
	}
}

func handlerIndex(conf *Config, w http.ResponseWriter, r *http.Request) (int, error) {
	type OutputData struct {
		DocId string
		HtmlString template.HTML
		TopicId string
		TopicTitle string
		TopicCriteria string
		TopicError string
		CompletionCode string
		ErrorMessage string
	}

	type TopicDetail struct {
		TopicId string `json:"topicId"`
		Title string `json:"title"`
		Description string `json:"description"`
		Criteria string `json:"criteria"`
	}

	outData := OutputData{}

	// fetch the requested document id from the url
	outData.DocId = r.URL.Query().Get("doc")

	// fetch html string
	byteContent, err := ioutil.ReadFile(conf.PoolFileLocation + outData.DocId)
	if err != nil {
		outData.ErrorMessage = "Oops... page not found!" + conf.PoolFileLocation + outData.DocId
	}

	outData.HtmlString = template.HTML(byteContent)

	// generate Completion Code
	hasher := sha1.New()
	hasher.Write([]byte(outData.DocId + conf.Salt))
	outData.CompletionCode = base64.URLEncoding.EncodeToString(hasher.Sum(nil))

	// fetch the requested document id from the url
	outData.TopicId = r.URL.Query().Get("topicId")

	// if TopicId found from the URL, load topics detail from json file
	var topics []TopicDetail
	if outData.TopicId != "" {
		fTopic, err := ioutil.ReadFile(conf.TopicDetailsFile)
		if err != nil {
			outData.TopicError = "Missing Topic Details File!"
		}

		err = json.Unmarshal(fTopic, &topics)
		if err != nil {
			outData.TopicError = "Failed to parse Topic Details File!"
		}

		// find topic detail that match the topic id given in the url
		for _, topic := range topics {
			if topic.TopicId == outData.TopicId {
				outData.TopicTitle = topic.Title
				outData.TopicCriteria = topic.Criteria
				break
			}
		}

		if outData.TopicTitle == "" {
			outData.TopicError = "Topic not found!"
		}
	}



	// obtain topic from the topic detail json file
	//outData.TopicTitle = "My wife has mild but worsening symptoms that our doctors can't diagnose"
	//outData.TopicCriteria = "Documents should discuss multisystem diseases that are difficult to diagnose. The document should discuss symptoms of a condition, and these symptoms should include one of: paresthesias, dizziness, balance impairment, shortness of breath, palpitations or fatigue"

	// pass ouput data to render the html page
	conf.templates["index"].Execute(w, outData)
	return 200, nil
}



