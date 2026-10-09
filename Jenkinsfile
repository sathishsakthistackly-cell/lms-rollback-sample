pipeline {
    agent any
    options { timestamps(); disableConcurrentBuilds() }
    environment {
        IMAGE_NAME = 'lms-rollback-sample'
        CONTAINER_NAME = 'lms-rollback-sample'
        HOST_PORT = '8080'
        HEALTH_URL = 'http://127.0.0.1:8080/health'
    }
    stages {
        stage('Checkout') { steps { checkout scm } }
        stage('Build') {
            steps { sh 'docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} .' }
        }
        stage('Deploy and health check') {
            steps {
                sh 'PREVIOUS_IMAGE=$(cat .previous-image); sh scripts/deploy-rollback.sh ${CONTAINER_NAME} ${HEALTH_URL} "$PREVIOUS_IMAGE"'
                sh 'docker rm -f ${CONTAINER_NAME} >/dev/null 2>&1 || true'
                sh 'docker run -d --name ${CONTAINER_NAME} --restart unless-stopped -e APP_VERSION=${BUILD_NUMBER} -e ENVIRONMENT=jenkins -p ${HOST_PORT}:5000 ${IMAGE_NAME}:${BUILD_NUMBER}'
                sh 'PREVIOUS_IMAGE=$(cat .previous-image); scripts/deploy-rollback.sh ${CONTAINER_NAME} ${HEALTH_URL} "$PREVIOUS_IMAGE"'
            }
        }
    }
    post {
        success { echo 'Deployment completed and health check passed.' }
        failure { echo 'Deployment failed; inspect logs and rollback output.' }
        always { sh 'docker image prune -f || true' }
    }
}
