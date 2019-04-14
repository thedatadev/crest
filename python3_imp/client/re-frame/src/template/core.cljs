(ns template.core
  (:require [reagent.core :as reagent]
            [re-frame.core :refer [dispatch-sync]]
            [devtools.core :as devtools]

            [template.db] ; NOTE :refer :all triggers an exception since it's not allowed in ClojureScript
            [template.events]
            [template.views :refer [app]]
            [template.subs]))

(devtools/install!)

(reagent/render [app] (js/document.querySelector "#app"))