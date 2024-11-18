pipeline {
    agent any

    environment {
        SERVER_IP = credentials('SERVER_IP') 
        SSH_USER = credentials('SSH_USER')           
        SSH_PASSWORD = credentials('SSH_PASSWORD')   
        KAFKA_PORT = credentials('KAFKA_PORT')
        LOCAL_PORT = credentials('LOCAL_PORT')
        PYTHONPATH = "${WORKSPACE}"
        PROJECT_NAME = "group-project-f24-ml-avengers-15"

    }

    stages {
        stage('Build') {
            steps {
                sh '''
                # Create a virtual environment and activate it
                python3 -m venv venv
                . venv/bin/activate
                pip install -r requirements.txt
                deactivate
                '''
            }
        }

        stage('Run Unit Tests and generate test report') {
            steps {
                sh '''
                . venv/bin/activate
                python -m pytest test/ --junitxml=report.xml
                deactivate
                '''
            }
        }

        stage('Run Offline Evaluation') {
            steps {
                echo 'Running Offline Evaluation'
                sh '''
                . venv/bin/activate
                cd evaluation
                python offline.py 
                deactivate
                '''
            }
        }

        stage('Run Online Evaluation') {
            steps {
                echo 'Running Online Evaluation'
                sh '''
                . venv/bin/activate
                python evaluation/online_evaluation.py
                deactivate
                '''
            }
        }

        stage('Run Data Quality') {
            steps {
                echo 'Running Data Quality'
                sh '''
                . venv/bin/activate
                python evaluation/data_qualitycheck.py
                deactivate
                '''
            }
        }

        stage('Run Data Drift') {
            steps {
                echo 'Running Data Drift'
                sh '''
                . venv/bin/activate
                python evaluation/data_drift.py
                deactivate
                '''
            }
        }
        
        stage('Deploy Using Docker Compose') {
            steps {
                script {
                    echo 'Deploying Using Docker Compose'
                    sh '''
                    docker-compose -p ${PROJECT_NAME} down || true
                    docker-compose -p ${PROJECT_NAME} up -d --build
                    '''
                }
            }
        }
    }

    post {
        success {
            junit 'report.xml' // Publish test results
        }
    }
}
