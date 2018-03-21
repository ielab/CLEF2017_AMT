package main

import (
	"net/http"
	"github.com/gorilla/mux"
)

func loadRouter(conf *Config) *mux.Router {
	r := mux.NewRouter()

	gets := r.Methods("GET").Subrouter()
	//posts := r.Methods("POST").Subrouter()

	gets.Handle("/", handler{conf, handlerIndex})

	gets.PathPrefix(conf.StaticFileLocation).Handler(
		http.StripPrefix(conf.StaticFileLocation,
			http.FileServer(http.Dir(conf.StaticFileDirectory))))

	return r
}
