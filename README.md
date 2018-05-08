# Clombda

A Docker image that compiles a Leiningen project into an AWS Lambda deployment package using GraalVM and native-image.

## Usage

### Example Lein Project
```
➜ lein new minimal hello-clombda
➜ cd hello-clombda
➜ lein change :main set hello-clombda.core
➜ cat > src/hello_clombda/core.clj <<EOCLJ
(ns hello-clombda.core
  (:gen-class))

(defn -main []
  (println "{\"hello\": \"clombda!\"}"))
EOCLJ
```

### Compile and Package
```
➜ docker run --rm "-v$(pwd):/clj" "-v${HOME}/.m2:/root/.m2" spieden/clombda:latest
Compiling hello-clombda.core
Created /clj/target/clombda/uberjar/hello-clombda-0.1.0-SNAPSHOT.jar
Created /clj/target/clombda/uberjar/hello-clombda-0.1.0-SNAPSHOT-standalone.jar
Build on Server(pid: 54, port: 26681)*
   classlist:   5,984.78 ms
       (cap):   1,351.64 ms
       setup:   3,351.83 ms
  (typeflow):  14,569.62 ms
   (objects):   4,141.76 ms
  (features):     100.01 ms
    analysis:  19,090.45 ms
    universe:     522.60 ms
     (parse):   5,324.75 ms
    (inline):   2,593.70 ms
   (compile):  23,167.65 ms
     compile:  31,712.70 ms
       image:   1,680.40 ms
       write:     655.86 ms
     [total]:  63,117.43 ms
  adding: clj-native (deflated 69%)
  adding: lambda_function.py (deflated 55%)
built target/clombda/package.zip
```

### Deploy to Lambda and Test

```
➜ aws lambda create-function --function-name hello-clombda --runtime python2.7 --handler lambda_function.lambda_handler --zip-file fileb://target/clombda/package.zip --role arn:aws:iam::XXXXXXXXXXXX:role/service-role/testrole # <-- you must create role
...
➜ aws lambda invoke --function-name hello-clombda --log-type Tail - | jq -r .LogResult | base64 -D
START RequestId: 8e567605-52fb-11e8-ab75-d5a9cad8bc6f Version: $LATEST
STDOUT
{"hello": "clombda!"}

------
STDERR

------
return: 0
END RequestId: 8e567605-52fb-11e8-ab75-d5a9cad8bc6f
REPORT RequestId: 8e567605-52fb-11e8-ab75-d5a9cad8bc6f  Duration: 148.14 ms     Billed Duration: 200 ms         Memory Size: 128 MB  Max Memory Used: 20 MB
```

Full disclosure: The cold start duration above is a best of four. 🤔

## Thanks

.. to [Michiel Borkent](https://github.com/borkdude/cljtree-graalvm) and [Jan Stępień](https://www.innoq.com/en/blog/native-clojure-and-graalvm/) for pointing the way.

