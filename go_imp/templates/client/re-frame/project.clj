(defproject example-project "0.1.0-SNAPSHOT"
  :dependencies [[org.clojure/clojure       "1.10.0"]
                [org.clojure/clojurescript  "1.10.520"]
                [reagent                    "0.8.1"]
                [re-frame                   "0.10.6"]
                [cljs-ajax                  "0.8.0"]
                [day8.re-frame/http-fx      "0.1.6"]
                [day8.re-frame/tracing      "0.5.1"]]
  :profiles
    {:dev
      {:dependencies [[com.bhauman/figwheel-main "0.2.0"]
                      [com.bhauman/rebel-readline-cljs "0.1.4"]
                      [binaryage/devtools "0.9.10"]
                      [day8.re-frame/re-frame-10x "0.3.7-react16"]]
       :resource-paths ["target"]
       :clean-targets ^{:protect false} ["target"]}}
  :aliases {"fig" ["trampoline" "run" "-m" "figwheel.main"]})