(ns template.events
    (:require 
            [re-frame.core :refer [reg-event-fx reg-event-db]]
            [ajax.core :as ajax]
            [day8.re-frame.http-fx]))