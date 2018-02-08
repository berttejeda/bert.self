---
post_title: 'Docker - Multi-Stage Builds'
layout: post
published: true
---
# What is meant by a multi-stage build in Docker?

Found this via https://chrisguitarguy.com/2017/12/16/multi-stage-docker-php/: 

_To put it simply, a multi-stage build is a Dockerfile with two or more FROM stanzas._

And my 0.02:

Think of each stanza as a stage (hence multi-stage), wherein actions taken in each produces an intermediary docker build that ultimately leads to the final docker image

# Test Case

Consider the following:

* Given:
A simple hello-world application (hello.go)
The code simply prints to standard output the sentence: _Hello, world. I am running Go!_
* You want to dockerize the program

# Singular approach

Your `Dockerfile`

	```
	FROM golang:1.9

	WORKDIR /go/src/github.com/berttejeda/hello-world

	COPY hello.go .

	RUN go get -d -v

	RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o app .

	CMD ["/go/src/github.com/berttejeda/hello-world/app"]
	```

Upon building the docker image with `docker build -t berttejeda/hello-world .`
And querying your docker daemon for the image result, you will note that the image size is quite large:
`docker images --format "{{.Repository}}\t{{.Size}}" --filter=reference=berttejeda/hello-world*`

berttejeda/hello-world       737MB

That's correct, over 700MB to simply output a HELLO WORLD string to your terminal!

# Multiple Docker Files

To save on image size, you could split up the build into two Dockerfile definitions, one file compiling hello.go locally, the other to copy the executable to a stripped down docker image, e.g. alpine. 

As with:

Dockerfile.00:

	```
	FROM golang:1.9

	WORKDIR /go/src/github.com/berttejeda/hello-world

	COPY hello.go .

	RUN go get -d -v

	RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o app .

	CMD ["/go/src/github.com/berttejeda/hello-world/app"]
	```

And invoking the build: `docker build -t berttejeda/hello-world-00 -f Dockerfile.00 .`

`Dockerfile.01`:

	```
	FROM alpine:latest  
	RUN apk --no-cache add ca-certificates

	COPY app .

	CMD ["/app"]	
	```		

And invoking the build:	`docker build -t berttejeda/hello-world-01 -f Dockerfile.01 .`

Reviewing the resulting image:

`docker images --format "{{.Repository}}\t{{.Size}}" --filter=reference=berttejeda/hello-world*`

Yields:

	```
	berttejeda/hello-world-01       6.57MB
	berttejeda/hello-world-00       737MB
	```

OK, looks much better. We can definitely work with that file size :)

# Multi-stage build approach 

An even better approach? Combine the above into one step!

Enter multi-stage builds,

As exemplified:

`Dockerfile`:

	```
	FROM golang:1.9 as builder

	WORKDIR /go/src/github.com/berttejeda/hello-world

	COPY hello.go .

	RUN go get -d -v

	RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o app .


	FROM alpine:latest  
	RUN apk --no-cache add ca-certificates

	WORKDIR /root/
	COPY --from=builder /go/src/github.com/berttejeda/hello-world/app .
	CMD ["./app"]	
	```			

And invoking the build: `docker build -t berttejeda/hello-world .`

Reviewing the resulting image:

`docker images --format "{{.Repository}}\t{{.Size}}" --filter=reference=berttejeda/hello-world*`

Yields:

	```
	berttejeda/hello-world  6.57MB
	berttejeda/hello-world-01       6.57MB
	berttejeda/hello-world-00       737MB
	```

I like it. Next time, there won't be a need for intermediate images.

# References

	Multi-Stage Docker build for Go
		https://github.com/alextanhongpin/go-docker-multi-stage-build	