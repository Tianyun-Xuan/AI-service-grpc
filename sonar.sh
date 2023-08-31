# static check
mkdir -p .reports
mkdir -p .logs
pylint --rcfile config/.pylintrc ai_grpc.py >.reports/pylint-report.txt
flake8 --config=config/.flake8 ai_grpc.py >.reports/flake8-report.txt
# unittest
pytest -v -s --cov=. --cov-report xml:.reports/coverage.xml --junitxml=.reports/nosetests.xml

# sonar
/home/xavier/Codes/sonar-scanner-5.0.1.3006-linux/bin/sonar-scanner -X \
  -Dsonar.verbose=true \
  -Dsonar.projectKey=AI-service-grpc \
  -Dsonar.sources=. \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.token=sqp_d6efb8d7618b22fb06d28ae2fda12f691219cdc6 \
  &>.logs/sonar-scanner.log

# clean up
rm -rf .coverage
rm -rf .pytest_cache
rm -rf .reports
rm -rf .logs
rm -rf .scannerwork