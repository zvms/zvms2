(import zvms [create-app])

(when (= __name__ "__main__")
  (let [app (create-app)]
    (app.run
     :port 11452
     :host "0.0.0.0")))