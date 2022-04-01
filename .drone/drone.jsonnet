local publishDocker() = {
    name: "docker-publish",
    kind: "pipeline",
    type: "docker",
    trigger: {branch: ["main"]},
    volumes: [{name: "docker", host: {path: "/var/run/docker.sock"}}],
    steps: [
        {
            name: "publish-image",
            image: "plugins/docker",
            volumes: [{name: "docker", path: "/var/run/docker.sock"}],
            settings: {
                username: "api",
                password: {from_secret: "proget_api_key"},
                repo: "proget.hunterwittenborn.com/docker/hunter/matrix-faq",
                registry: "proget.hunterwittenborn.com",
                dockerfile: "docker/Dockerfile",
				tags: "latest",
                no_cache: "true"
            }
        }
    ]
};

[
    publishDocker()
]
 
