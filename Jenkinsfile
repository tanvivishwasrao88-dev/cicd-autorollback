pipeline {
    agent any
    environment {
        IMAGE_NAME = "myapp"
        CONTAINER_NAME = "myapp-live"
    }
    stages {
        stage('Build') {
            steps {
                sh "docker build -t myapp:${BUILD_NUMBER} ."
                sh "docker tag myapp:${BUILD_NUMBER} myapp:latest"
            }
        }
        stage('Health Check') {
            steps {
                script {
                    sh "docker run -d --name test-${BUILD_NUMBER} -p 5001:5000 myapp:${BUILD_NUMBER}"
                    sh "sleep 5"
                    def status = sh(script: "curl -s -o /dev/null -w '%{http_code}' http://localhost:5001/health", returnStdout: true).trim()
                    sh "docker stop test-${BUILD_NUMBER} && docker rm test-${BUILD_NUMBER}"
                    if (status != "200") { error("FAILED") }
                    echo "PASSED!"
                }
            }
        }
        stage('Deploy') {
            steps {
                sh "docker stop myapp-live || true"
                sh "docker rm myapp-live || true"
                sh "docker run -d --name myapp-live -p 5000:5000 myapp:${BUILD_NUMBER}"
            }
        }
    }
    post {
        success { echo "DEPLOYED SUCCESSFULLY!" }
        failure {
            sh "docker stop myapp-live || true"
            sh "docker rm myapp-live || true"
            sh "docker run -d --name myapp-live -p 5000:5000 myapp:latest || true"
            echo "ROLLED BACK!"
        }
    }
}
