pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Build & Unit Test') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest
                '''
            }
        }

        stage('SAST - Bandit') {
            steps {
                sh '''
                    . venv/bin/activate
                    mkdir -p reports
                    bandit -r . -f html -o reports/bandit-report.html || true
                '''
            }
        }

        stage('SCA - pip-audit') {
            steps {
                sh '''
                    . venv/bin/activate
                    pip-audit -r requirements.txt || true
                '''
            }
        }

        stage('Archive Reports') {
            steps {
                archiveArtifacts artifacts: 'reports/*', allowEmptyArchive: true
            }
        }
    }
}