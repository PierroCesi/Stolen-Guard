DOCKER=docker
IMAGE=stolen-guard
TAG=$(IMAGE)

build:
	@$(DOCKER) build --tag $(TAG) .

build-no-cache:
	@$(DOCKER) build --no-cache --tag $(TAG) .

run:
	@$(DOCKER) run --detach --name $(IMAGE) $(TAG)

bash:
	@$(DOCKER) exec -it $(IMAGE) /bin/bash

clean:
	@$(DOCKER) stop $(IMAGE)
	@$(DOCKER) rm -f $(IMAGE)

logs:
	@$(DOCKER) logs -f $(IMAGE)