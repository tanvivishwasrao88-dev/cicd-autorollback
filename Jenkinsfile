pipeline {
    agent any

    environment {
       IMAGE_NAME = "myapp"
        CONTAINER_NAME = "myapp-live"
        SLACK_WEBHOOK = "SLACK_URL_HERE"
    }

    stages {

        stage('Clone Code') {
            steps {
                echo "Code already checked out by Jenkins"
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker image..."
                    sh "docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} ."
                    sh "docker tag ${IMAGE_NAME}:${BUILD_NUMBER} ${IMAGE_NAME}:latest"
                }
            }
        }

        stage('Health Check on Test Container') {
            steps {
                script {
                    echo "Starting test container..."
                    sh "docker run -d --name test-${BUILD_NUMBER} -p 5001:5000 ${IMAGE_NAME}:${BUILD_NUMBER}"
                    sh "sleep 5"

                    def status = sh(
                        script: "curl -s -o /dev/null -w '%{http_code}' http://localhost:5001/health",
                        returnStdout: true
                    ).trim()

                    echo "Health check status: ${status}"

                    sh "docker stop test-${BUILD_NUMBER} && docker rm test-${BUILD_NUMBER}"

                    if (status != "200") {
                        error("Health check FAILED! Got status: ${status}")
                    }

                    echo "Health check PASSED!"
                }
            }
        }

        stage('Deploy Live') {
            steps {
                script {
                    echo "Deploying to production..."
                    sh """
                        docker stop ${CONTAINER_NAME} || true
                        docker rm ${CONTAINER_NAME} || true
                        docker run -d --name ${CONTAINER_NAME} -p 5000:5000 ${IMAGE_NAME}:${BUILD_NUMBER}
                    """
                    echo "App is LIVE at port 5000!"
                }
            }
        }
    }

    post {
        success {
            sh """
                curl -X POST -H 'Content-type: application/json' \
                --data '{"text":"✅ SUCCESS! Build #${BUILD_NUMBER} deployed! App is live!"}' \
                ${SLACK_WEBHOOK}
            """
        }

        failure {
            script {
                echo "FAILED! Rolling back..."
                sh """
                    docker stop ${CONTAINER_NAME} || true
                    docker rm ${CONTAINER_NAME} || true
                    docker run -d --name ${CONTAINER_NAME} -p 5000:5000 ${IMAGE_NAME}:latest || true
                """
                sh """
                    curl -X POST -H 'Content-type: application/json' \
                    --data '{"text":"❌ FAILED! Build #${BUILD_NUMBER} rolled back to last working version!"}' \
                    ${SLACK_WEBHOOK}
                """
            }
        }
    }
}
