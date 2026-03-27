# Phishing.army OpenCTI Connector

## docker-compose.yml setup network
```
services:
  connector-malshare:
    image: lopmconnector:latest
    networks:
      - opencti_default

networks:
  opencti_default:
    external: true
```

## setup connector
```sh
git clone https://github.com/LOPMaD/LOPM-OpenCTI-Con
cd LOPM-OpenCTI-Con
docker build -t lopmconnector:latest .
docker stack deploy -c docker-compose.yml opencti
```