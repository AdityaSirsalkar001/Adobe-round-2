# Adobe Hackathon Round 1A – PDF Outline Extractor

## Build
```bash
docker build --platform linux/amd64 -t pdf-outline-extractor:latest .
```

## Run
```bash
docker run --rm ^
-v "%cd%/input:/app/input" ^
-v "%cd%/output:/app/output" ^
--network none ^
pdf-outline-extractor:latest
```
