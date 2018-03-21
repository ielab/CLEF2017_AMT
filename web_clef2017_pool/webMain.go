package main

import (
	"net/http"
	"log"
	"html/template"
	"path/filepath"
	"strings"
	"time"
)


func add(x, y int) int {
	return x + y
}


func loadTemplates() (map[string]*template.Template, error) {
	baseTemplate := template.New("base")
	baseTemplate, err := baseTemplate.ParseFiles("./template/base_template/base.html")
	if err != nil {
		return nil, err
	}

	tempFiles, err := filepath.Glob( "./template/*.html")
	if err != nil {
		return nil, err
	}

	layoutFiles, err := filepath.Glob( "/template/base_template/*.html")
	if err != nil {
		return nil, err
	}

	m := make(map[string]*template.Template)
	for _, f := range tempFiles {
		name := filepath.Base(f)
		name = strings.Replace(name, ".html", "", -1)
		t, err := baseTemplate.Clone()
		if err != nil {
			return nil, err
		}
		files := append(layoutFiles, f)
		funcs := template.FuncMap{"add": add}
		tmpl, err := t.Funcs(funcs).ParseFiles(files...)
		if err != nil {
			return nil, err
		}
		if err != nil {
			return nil, err
		}
		m[name] = tmpl
	}
	return m, err
}

func YourHandler(w http.ResponseWriter, r *http.Request) {
	w.Write([]byte("Gorilla!\n"))
}

func main() {
	println(
		`***** CLEF 2017 Pool (c) Jimmy, 2018 *****`)

	// load global variable config
	config, err := loadConfig()
	if err != nil {
		log.Panic(err)
	} else {
		println(`Config loaded.` )
	}

	// load template (html templates)
	templates, err := loadTemplates()
	if err != nil {
		log.Panic(err)
	}
	log.Println("templates loaded.")

	config.templates = templates

	r := loadRouter(config)
	srv := &http.Server{
		Handler: r,
		Addr: config.Domain + ":" + config.Port,
		WriteTimeout: 15 * time.Second,
		ReadTimeout:  15 * time.Second,
	}
	log.Println("server started at " + config.Domain + ":" + config.Port)
	log.Fatal(srv.ListenAndServe())
}