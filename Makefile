.PHONY: test serve

test:
	py.test

serve:
	gunicorn -b 0.0.0.0:8000 koalas.app:app
