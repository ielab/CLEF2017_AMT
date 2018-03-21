package main

import (
	"io/ioutil"
	"encoding/json"
	"regexp"
	"html/template"
)
const CONFIG_PATH = "./config.json"

type Config struct {
	PoolFileLocation string `json:"pool_file_location"`
	TopicDetailsFile string `json:"topic_details_file"`
	Domain string `json:domain`
	Port string `json:"port"`
	StaticFileLocation string `json:"static_file_location"`
	StaticFileDirectory string `json:"static_file_directory"`
	Salt string `json:"salt"`

	templates map[string]*template.Template

	reSymptom *regexp.Regexp
}

func loadConfig() (*Config, error) {
	var c Config

	f, err := ioutil.ReadFile(CONFIG_PATH)
	if err != nil {
		return nil, err
	}

	err = json.Unmarshal(f, &c)
	if err != nil {
		return nil, err
	}

	//Define regex to extract symptoms from query string: all phrases between quotes
	c.reSymptom, _ = regexp.Compile(`"(.*?)"`)

	return &c, nil
}
