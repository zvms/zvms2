(import [time perf_counter])

(setv start (perf_counter))

(print (- (perf_counter) start))