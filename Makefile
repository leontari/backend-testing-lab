.PHONY: up
up:
	docker compose up -d

.PHONY: down
down:
	docker compose down

.PHONY: logs
logs:
	docker compose logs -f

.PHONY: test
test:
	pytest -v

.PHONY: proto
proto:
	python -m grpc_tools.protoc -I./shared/proto --python_out=./shared/proto --grpc_python_out=./shared/proto ./shared/proto/payment.proto

.PHONY: lint
lint:
	ruff check .

.PHONY: format
format:
	ruff check . --fix
