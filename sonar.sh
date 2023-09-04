# static check
mkdir -p .reports
mkdir -p .logs
pylint --rcfile config/.pylintrc ai_grpc.py >.reports/pylint-report.txt
flake8 --config=config/.flake8 ai_grpc.py >.reports/flake8-report.txt
# unittest
pytest -v -s --cov=. --cov-report xml:.reports/coverage.xml --junitxml=.reports/nosetests.xml

# sonar 9.9.1
/home/xavier/Codes/sonar-scanner-5.0.1.3006-linux/bin/sonar-scanner -X \
  -Dsonar.verbose=true \
  -Dsonar.projectKey=AI-service-grpc \
  -Dsonar.sources=. \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.login=sqp_5a9a2565094c1d25fc1a066548656f488dcb056c \
  &>.logs/sonar-scanner.log

# sonar 10.0.1
# /home/xavier/Codes/sonar-scanner-5.0.1.3006-linux/bin/sonar-scanner -X \
#   -Dsonar.verbose=true \
#   -Dsonar.projectKey=AI-service-grpc \
#   -Dsonar.sources=. \
#   -Dsonar.host.url=http://localhost:9000 \
#   -Dsonar.token=sqp_5a9a2565094c1d25fc1a066548656f488dcb056c \
#   &>.logs/sonar-scanner.log

# clean up
rm -rf .coverage
rm -rf .pytest_cache
rm -rf .reports
rm -rf .logs
rm -rf .scannerwork