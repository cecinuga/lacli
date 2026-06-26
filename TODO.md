file: lacli -> improooove a lot the error handling
file: lacli/load -> add benchmarks mode: create a global state in lacli.benchmark.timer and handle all the login in there, every bench point must only set the relative variable, when the program stop, print the aggregated times
file: lacli/load -> add benchmarks timers: add timer between step of load pipeline, run integration test, and after check the aggregated times for each function, ottimize the slowest!!!
file: lacli/load -> if n_thread is 1, disable multithreading and load the file sequentially
