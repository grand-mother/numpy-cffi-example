LIB= libgrand.abi3.so

lib: grand/$(LIB)

grand/$(LIB): ALWAYS
	python3 setup.py build --build-lib .

.PHONY: clean ALWAYS

ALWAYS:

clean:
	rm -rf grand/$(LIB) grand/__pycache__
