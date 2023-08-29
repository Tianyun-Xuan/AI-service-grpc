# static check
mkdir -p .reports
pylint --rcfile .config/.pylintrc ai_grpc.py >.reports/pylint-report.txt
flake8 --config=.config/.flake8 ai_grpc.py >.reports/flake8-report.txt\

# unittest
pytest -v -s --junitxml=.reports/coverage.xml

# sonar
/home/xavier/Codes/sonar-scanner-5.0.1.3006-linux/bin/sonar-scanner -X \
  -Dsonar.verbose=true \
  -Dsonar.projectKey=AI-service-grpc \
  -Dsonar.sources=. \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.token=sqp_d6efb8d7618b22fb06d28ae2fda12f691219cdc6 \
  &>sonar-scanner.log
